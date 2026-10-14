# Example 04: Anti-Silent-Failure & Rollback Harness

This example implements defensive engineering against silent AI agent failures:
1. **Pre-flight Integrity Check (`preflight.py`):** Ensures inputs and historical ledgers are intact before launching expensive reasoning loops.
2. **Atomic Rollback Guard (`rollback_guard.py`):** Reverts workspace state if an iteration fails or aborts.
3. **Outbound Notification Hook (`alert_webhook.py`):** Pings communication channels loudly on any unhandled failure.

---

## Defensive Engineering in Action

```bash
# 1. Run Pre-flight Check
python3 preflight.py --min-expected 3

# 2. Test Atomic Rollback
python3 rollback_guard.py --simulate-failure

# 3. Test Alert Dispatch
python3 alert_webhook.py --severity P1 --message "Candidate ingestion returned 0 items; possible API payload schema change."
```

