# Example 01: Dropped Commitments & Loose-Ends Reconciler

This example demonstrates how to build an autonomous scheduled loop that scans communication channels (sent emails, Slack messages, meeting notes) over a sliding 14-day window, identifies unfulfilled commitments, and drafts actionable reconciliation briefs.

---

## Architecture

1. **Layer 1 (Deterministic Input Ingestion):**
   - Connects to mailboxes, Slack APIs, and note exports.
   - Extracts messages sent *by* the operator or where the operator was assigned action items.
   - Normalizes text into a standardized JSON array (`sample_inputs.json`).

2. **Layer 2 (Agent Reasoning & Classification):**
   - Evaluates each message against `taste_criteria.md`.
   - Separates real commitments (*"I'll have the PR up by Wednesday"*, *"Let me send you that benchmark deck"*) from passive status updates or pleasantries.
   - Flags urgency: `P0 (Overdue)`, `P1 (Due within 48h)`, or `P2 (Long horizon)`.
   - Generates pre-drafted reconciliation emails ready for operator review.

3. **Layer 3 (Human Judgment & Sign-off):**
   - The operator inspects the generated report.
   - Reviews and clicks send on approved draft responses.
   - No email is ever sent autonomously without human judgment.

---

## Running the Example

```bash
python3 scan_commitments.py --input sample_inputs.json --criteria taste_criteria.md
```

This will output:
- A Markdown summary of reconciled vs. dropped commitments.
- Drafted replies for any P0 overdue items.
- Append audit entries to `audit_triage.log`.

