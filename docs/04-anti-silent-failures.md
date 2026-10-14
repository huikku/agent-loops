# Anti-Entropy: Defending Against Silent Failures

Traditional software fails with visible errors: an unhandled exception throws a stack trace, crashes the process, and returns a non-zero exit code.

AI agent loops fail in insidious, quiet ways. This document covers the failure modes unique to loops and the defensive engineering harness required to neutralize them.

---

## Anatomy of a Silent Loop Failure

```
┌────────────────────────────────────────────────────────────────────────┐
│ THE SILENT LOOP ANOMALY                                                │
│ 1. Upstream API silently changes payload key ('articles' -> 'items').  │
│ 2. Layer 1 scraper fails to extract records; returns empty list [].    │
│ 3. Layer 2 agent receives empty list; reasons "No candidates today".   │
│ 4. Script writes clean state and exits with Return Code 0.             │
│ 5. Operator sees green status; pipeline appears healthy.               │
│ 6. Real outcome: 0 dropped commitments or news items caught for weeks. │
└────────────────────────────────────────────────────────────────────────┘
```

Other common silent failure modes include:
- **Hallucinated Early Exit:** The agent claims an objective is "fully reconciled" when it only completed 3 of 30 items.
- **Infinite Stagnation Loop:** The agent encounters a difficult edge case, attempts the same failing edit 50 times in a row, and burns \$50 worth of tokens overnight.
- **Corrupted State Drift:** A crash midway through writing state produces a truncated JSON file, breaking all future runs.

---

## The Three Defensive Laws

To guarantee unattended reliability, every production loop must enforce **The Three Defensive Laws**:

```
                       ┌─────────────────────────┐
                       │   THE 3 DEFENSIVE LAWS  │
                       └────────────┬────────────┘
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
   ┌───────────┐              ┌───────────┐              ┌───────────┐
   │   LAW I   │              │  LAW II   │              │  LAW III  │
   │ PRE-FLIGHT│              │  ATOMIC   │              │  BE LOUD  │
   │ INTEGRITY │              │ ROLLBACK  │              │ ON FAILURE│
   └───────────┘              └───────────┘              └───────────┘
```

---

### Law I: The Pre-Flight Integrity Check

Before launching the main reasoning cycle, the loop harness must run a pre-flight probe:

1. **Verify Prior Run State:** Check if the previous run's output file exists, is non-empty, and valid JSON/Markdown.
2. **Detect Ingestion Anomalies:** If a daily scraper that normally fetches 50–200 items suddenly yields `0` items, treat this as a failure state rather than a normal condition.
3. **Verify Git Working Tree:** Ensure the working directory is clean or at a known commit before modifying files.

```python
def preflight_check(candidates: list, min_expected: int = 5):
    """Ensure candidate ingestion meets historical floor thresholds."""
    if len(candidates) < min_expected:
        raise IngestionAnomalyError(
            f"Pre-flight failed: Ingestion returned only {len(candidates)} items "
            f"(historical threshold is >= {min_expected}). Halting to prevent empty run."
        )
```

---

### Law II: Atomic Rollback

Never commit or publish partial, half-broken state. 

If an agent is instructed to process 30 blog posts or reconcile 15 dropped commitments:
- If an unhandled exception or verification failure occurs on item 14, **the entire batch must be rolled back**.
- Do not leave the workspace in a half-modified state where some files have been edited and others have not.

#### Implementation with Git
```bash
#!/bin/bash
# Stash any untracked changes before running the loop
git stash save "loop-pre-run-snapshot"

# Run the autonomous loop
python3 run_goal_loop.py
LOOP_EXIT=$?

if [ $LOOP_EXIT -ne 0 ]; then
    echo "[!] Loop failed with exit code $LOOP_EXIT. Rolling back workspace..."
    git reset --hard HEAD
    git clean -fd
    # Alert operator
    python3 alert_webhook.py --status "FAILED" --code $LOOP_EXIT
    exit $LOOP_EXIT
else
    echo "[✓] Loop succeeded and verified. Committing state..."
    git add state/ output/
    git commit -m "Auto-commit: Successful loop run $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
fi
```

---

### Law III: Be Loud on Failure

A production loop must never fail in silence. 

Any error condition (pre-flight failure, verification failure, or circuit-breaker trip) must immediately dispatch an outbound alert across an out-of-band communication channel:
- **Slack / Discord Webhook:** Pings a dedicated `#agent-ops` channel.
- **Email Notification:** Dispatches a high-priority alert to the system owner.
- **Terminal Bell / OS Alert:** For local developer runs, plays an audible alert to break cognitive focus.

```python
import urllib.request
import json

def send_alert(webhook_url: str, message: str, severity: str = "P1"):
    payload = {
        "text": f"🚨 *[AGENT LOOP FAILURE - {severity}]* 🚨\n{message}"
    }
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req, timeout=10)
```

---

## Circuit Breakers & Stagnation Detection

In Goal Loops (`/goal`), agents can get stuck in self-reinforcing retry loops. Implement a **Stagnation Circuit Breaker**:

1. **Hash the State Diff:** After each iteration, calculate the SHA-256 hash of the modified files.
2. **Track Consecutive Repeated States:** If `hash(cycle_N) == hash(cycle_N-1)` or `error(cycle_N) == error(cycle_N-1)`, increment `stagnation_counter`.
3. **Trip the Breaker:** If `stagnation_counter >= 3`, terminate execution immediately and flag:
   ```text
   [ABORT] Stagnation Circuit Breaker Tripped:
   Agent produced identical outputs across 3 consecutive cycles without resolving errors.
   Aborting loop to protect token quota.
   ```
