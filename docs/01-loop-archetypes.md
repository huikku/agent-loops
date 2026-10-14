# The 5 Operational Loop Archetypes

In loop engineering, an autonomous agent system is categorized by its execution pattern, trigger mechanism, and termination criteria. 

This document details the mechanics, operational tradeoffs, failure vectors, and production patterns for each of the five archetypes.

---

## Taxonomy Matrix

| Archetype | Trigger Mechanism | Termination Criteria | Typical Frequency | Human Involvement | Primary Risk |
|---|---|---|---|---|---|
| **1. Message Loop** | Human user prompt | Agent response output | Ad-hoc (interactive) | 50% (conversational peer) | Human latency bottleneck |
| **2. Heartbeat Loop** | Periodic timer / pulse | Single cycle completion | Seconds to minutes | 0% (unattended) | Alert fatigue / noisy false alarms |
| **3. Schedule / Cron Loop** | Temporal clock boundary | Batch completion | Daily / Weekly | Reviewer / Consumer | Silent degradation on data drift |
| **4. Event Hook Loop** | External event (git, webhook) | Test / check pass/fail | Event-driven | Approver (on PR/commit) | CI pipeline queue blockage |
| **5. Goal Loop (`/goal`)** | High-level directive | Verified contract condition | Iterative cycles until done | Specifier & final reviewer | Infinite token burn / runaway loops |

---

## 1. The Message Loop (Interactive Human-in-the-Loop)

```
[Human Operator] ──(Prompt)──► [Agent Reasoning] ──(Response)──► [Human Operator]
```

### Overview
The Message Loop is the original conversational paradigm. The human and the agent take turns. The human provides intent, inspects partial outputs, identifies errors, and manually prompts the model to correct them.

### When to Use
- Exploratory design and initial idea discovery.
- Ambiguous architectural refactors where trade-offs must be evaluated collaboratively.
- High-stakes creative direction where real-time feedback shapes the output.

### Limitations
- The human operator is the single point of serialization and latency.
- It cannot scale beyond the human's active working hours.
- Repetitive, mechanical tasks (e.g., verifying 50 files) become cognitively exhausting.

---

## 2. The Heartbeat Loop (Metronome Liveness Pulse)

```
[Timer Tick (e.g. 30s)] ──► [Deterministic Health Probe] ──► [Liveness Check OK?]
                                                                    │
                                                        ┌───────────┴───────────┐
                                                        ▼                       ▼
                                                   [Exit Silent]          [Escalate Alert]
```

### Overview
A Heartbeat Loop functions like a biological pulse or hardware watchdog. It fires on a deterministic, high-frequency interval to answer simple, high-stakes binary questions:
- *"Is the customer-facing API endpoint responding with 200 OK?"*
- *"Has a P0 customer escalation arrived in Slack or ZenDesk?"*
- *"Is the model serving cluster throttling or running out of VRAM?"*

### Architecture Best Practices
- **Never invoke an LLM on every heartbeat tick:** The probe itself should be 100% deterministic (Python script, HTTP HEAD request, Redis query).
- **Invoke the reasoning agent only on state transition:** If a probe detects a failure or an anomaly, spawn the agent to triage the incident, summarize logs, and draft an incident briefing.

---

## 3. The Schedule / Cron Loop (Cadence Engine)

```
[Cron Trigger (06:00 UTC)] ──► [Layer 1: Data Ingestion] ──► [Layer 2: Agent Triage] ──► [Layer 3: Human Digest]
```

### Overview
The Schedule Loop operates on a calendar schedule. It handles recurring operational cadences:
- **Daily 06:00 Research Digest:** Ingests papers, RSS feeds, and GitHub releases; filters against personal taste; publishes a static briefing.
- **Weekly Dropped Commitments Audit:** Scans team communication channels every Friday afternoon to identify unfulfilled promises.
- **Monthly Infrastructure Cost Optimization:** Pulls AWS/GCP billing data, correlates with usage patterns, and produces optimization recommendations.

### State Requirements
A scheduled loop requires persistent disk tracking:
1. **Deduplication Set (`seen_ids.json`):** Ensures items processed on Monday are not re-analyzed on Tuesday.
2. **Audit Ledger (`decisions.log`):** Records why candidate items were included or excluded.

---

## 4. The Event Hook Loop (Triggered Reactive Execution)

```
[Git Commit / PR Webhook] ──► [Hook Dispatcher] ──► [Specialized Agent Checker] ──► [Post Status / Block Merge]
```

### Overview
Hook loops trigger reactively upon an upstream event. In modern software engineering, they run inside CI/CD pipelines, git pre-push hooks, or webhook listeners.

### High-Impact Patterns
1. **The Design System Duplication Detector:**
   - Every time a pull request modifies UI code, the agent inspects new React/Vue components.
   - It cross-references the official design system repository.
   - If an engineer created a bespoke `<CustomButton>` or `<DropdownPicker>`, the agent posts a PR review comment linking to the standard component and showing the exact refactor diff.
2. **The Documentation Sync Hook:**
   - When API routes change, the hook generates a pull request updating the OpenAPI spec and client SDKs.
3. **The Lint & Type Eradication Loop:**
   - On commit, runs compiler diagnostics. If errors exist, the agent loops locally until all linter and type-checker warnings reach zero.

---

## 5. The Goal Loop (`/goal`) (Contract-Driven Autonomous Loop)

```
[Goal Directive]
       │
       ▼
┌──────────────┐◄───────────────────────────────┐
│ Generator    │                                │
│ Agent Iter.  │                                │ Iteration < Ceiling
└──────┬───────┘                                │
       ▼                                        │
┌──────────────┐     Verification Fails?        │
│ Decoupled    ├────────────────────────────────┘
│ Grader Agent │
└──────┬───────┘
       │ Verification Passes!
       ▼
[Termination: Deploy & Report]
```

### Overview
A Goal Loop runs recursively until an explicit, testable definition of completion is satisfied. It is the core mechanism enabling multi-step autonomous tasks (such as whole-codebase migrations, large-scale dataset reconciliation, or multi-chapter technical editing).

### The Four Non-Negotiable Contract Requirements

#### 1. Binary, Testable Objective
The objective cannot rely on subjective heuristics.
- **Valid Objective:** `"Run until pytest exits with code 0 and all 42 tests pass."`
- **Valid Objective:** `"Iterate across all 30 markdown articles; ensure every file contains at least 2 verified internal links to existing pages in the sitemap."`
- **Invalid Objective:** `"Make the documentation read more professionally."`

#### 2. Decoupled Grader ("No Grading Your Own Paper")
An LLM that generated a piece of code or text will suffer from self-confirmation bias. A production goal loop must use an independent verification mechanism:
- A deterministic test suite or AST parser, OR
- A separate evaluator agent prompted exclusively with a critical grading rubric.

#### 3. Hard Stop Circuit Breakers
To prevent runaway loops that consume millions of tokens when encountering an impossible objective, every goal loop must enforce:
- **Maximum iteration ceiling:** (e.g., `MAX_ITERATIONS = 10`)
- **Wall-clock timeout:** (e.g., `TIMEOUT_SECONDS = 7200`)
- **Stagnation detection:** If two consecutive cycles produce identical error outputs, abort immediately.

#### 4. Structured Audit Trail
Every iteration must append its diff, error log, and corrective plan to disk (`goal_run.log`) to provide complete post-mortem observability.
