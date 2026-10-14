# Commitment Triage Criteria & Policy

This policy document governs how the autonomous agent classifies communication items into commitments.

---

## 1. Definition of a True Commitment
A commitment exists when the operator explicitly agreed to perform work, deliver an asset, provide feedback, or unblock another person.

### High-Signal Indicators
- Temporal pledges: *"I will send this by [Day/Time]"*, *"Give me until tomorrow morning"*, *"I'll follow up on this later this week"*.
- Unblocking dependencies: *"Let me review the PR before you merge"*, *"I'll verify the GPU memory benchmarks today"*.
- Document/Asset promises: *"I will share the pitch deck"*, *"I'll attach the ComfyUI workflow JSON"*.

### False Positives (Discard / Ignore)
- Pleasantries: *"Great meeting everyone"*, *"Let's definitely catch up soon"*, *"Thanks for the update"*.
- Open invitations without deadlines: *"Feel free to reach out anytime"*, *"Let me know if you need anything"*.
- General informational commentary: *"The 128GB Thor dev kit runs unified memory very efficiently"*.

---

## 2. Priority Classifications

- **P0 - OVERDUE:** The promised delivery date was in the past and no subsequent fulfillment or update was found.
- **P1 - IMMINENT (Due <= 48 Hours):** A deadline is rapidly approaching within two business days.
- **P2 - LONG HORIZON:** General commitments with open or multi-week timelines.

---

## 3. Autonomous Output Requirements
For every P0 item identified, the agent must:
1. State the recipient name and original promise date.
2. Quote the exact commitment sentence.
3. Draft a courteous, concise reconciliation email that:
   - Acknowledges the delay without excessive defensive excuses.
   - States current status or attaches the requested deliverable.
   - Proposes a clear next step.
