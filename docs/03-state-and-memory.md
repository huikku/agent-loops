# State & Memory Architecture in Loop Engineering

A core difference between interactive chatbots and autonomous loops is how memory is maintained. 

In interactive chat sessions, developers rely on conversational context windows. In production loops, in-memory context is considered ephemeral and untrusted.

---

## The Ephemeral Axiom: Zero In-Memory Retention

> **Every automated loop execution spawns a fresh agent instance with zero memory of previous runs.**

When designing a production loop (whether running on cron, GitHub Actions, or local daemon):
- Do not assume conversational session history will survive computer reboots, network interruptions, or process restarts.
- Do not let in-memory state accumulate indefinitely (context windows fill up and degrade reasoning quality).
- **System state exists strictly in what is committed to disk or git.**

---

## The Three Core State Artifacts

A robust loop relies on three standardized persistent files on disk:

```
state/
├── seen_ids.json       # 1. Deduplication Ledger (High-speed hash / ID lookup)
├── decisions.log       # 2. Append-Only Audit Trail (Full historical rationale)
└── proposals.md        # 3. Agent Improvement Queue (Staged for human review)
```

### 1. Deduplication Ledger (`seen_ids.json`)
The deduplication ledger prevents duplicate processing, token waste, and repetitive outputs.

#### Schema
```json
{
  "version": 1,
  "last_updated": "2026-10-14T06:00:15Z",
  "records": {
    "https://example.com/article-101": {
      "first_seen": "2026-10-12T06:00:10Z",
      "processed_run": "run_2026-10-12_06",
      "decision": "PICKED"
    },
    "https://example.com/article-102": {
      "first_seen": "2026-10-14T06:00:05Z",
      "processed_run": "run_2026-10-14_06",
      "decision": "SKIPPED"
    }
  }
}
```

#### Ingestion Rule
Before handing candidates to Layer 2 (Agent Reasoning), Layer 1 (Deterministic Scripts) filters against `seen_ids.json`. If an item's key exists in `records`, it is stripped from the context payload with zero LLM overhead.

---

### 2. Append-Only Audit Trail (`decisions.log`)
When a loop makes editorial or operational judgments unattended, the operator must be able to inspect **why** every decision was made.

The audit trail is structured as a single-line delimited format (or JSON Lines):

```text
2026-10-14T06:00:12Z | run_20261014_06 | item_9912 | PICKED  | Score: 9/10 | High-signal analysis of hybrid attention layer ratios
2026-10-14T06:00:14Z | run_20261014_06 | item_9913 | SKIPPED | Score: 3/10 | Lacks technical substance; purely promotional marketing copy
2026-10-14T06:00:18Z | run_20261014_06 | item_9914 | SKIPPED | Score: 2/10 | Duplicate topic covered in run_20261011_06
```

#### Benefits
- **Debugging Policy Drift:** If the loop starts picking unwanted content, the operator inspects `decisions.log` to determine which rule in `taste.md` was misinterpreted.
- **Explainability:** Enables complete post-mortem auditability for compliance or quality assurance.

---

### 3. Agent Proposal Queue (`proposals.md`)
Because the agent cannot edit policy files directly (under the Authority Asymmetry Principle), it records longitudinal observations in `proposals.md`.

#### Format
```markdown
# Agent Evolution Proposals

## Staged for Human Review: Run 2026-10-14T06:00:00Z
- **Feed Performance:** Source `https://news.ycombinator.com/rss` yielded 4 out of 5 picks today. Propose increasing candidate fetch limit from 25 to 50.
- **Pattern Flag:** Author `Jane Doe` has been picked 6 times this week with consistent 9/10 scores. Propose adding Jane Doe to `priority_authors` in `taste.md`.
- **Negative Pattern:** Keyword `Web3 gaming` has been skipped in 100% of candidate instances. Propose adding to `hard_blacklist` in `taste.md`.
```

---

## Atomic Disk Writes: Preventing Corrupted State

When scripts write state to disk, a process crash or power interruption can corrupt JSON files. Always use atomic write patterns:

```python
import json
import os
import tempfile

def atomic_save_json(filepath: str, data: dict):
    """Write JSON data to a temporary file and atomically rename it."""
    dir_name = os.path.dirname(filepath)
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, suffix=".tmp") as f:
        json.dump(data, f, indent=2)
        temp_name = f.name
    os.replace(temp_name, filepath)
```

By using `os.replace()` (an atomic operation on POSIX filesystems), `seen_ids.json` is never left in a partially written or corrupted state.
