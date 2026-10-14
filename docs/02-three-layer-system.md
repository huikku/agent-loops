# The 3-Layer System: Three Jobs, Three Owners

The central architectural pattern in loop engineering is the **3-Layer System**. 

By cleanly dividing responsibilities across deterministic scripts, cognitive agent reasoning, and human taste policy, teams build loops that run unattended for months without drifting into hallucination or burning unnecessary tokens.

---

## Architectural Schema

```
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: DETERMINISTIC SCRIPTS                                         │
│ Role: Mechanical plumbing, candidate collection, filesystem I/O        │
│ Owner: Software Engineer / CI Engine                                   │
│ Technology: Python, Bash, Node.js, cURL, jq, Git                       │
│ Determinism: 100% | Token Cost: $0.00                                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Ingested Candidates & Normalized JSON
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: AGENT REASONING                                               │
│ Role: Context evaluation, triage, semantic synthesis, draft generation │
│ Owner: Autonomous AI Agent                                            │
│ Technology: Claude, GPT, Local Quantized LLMs, Custom Fine-tunes       │
│ Determinism: Probabilistic | Token Cost: Variable                     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Evaluated Against Policy
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: HUMAN JUDGMENT & POLICY                                       │
│ Role: Taste ownership, ethical boundaries, prioritization, authority   │
│ Owner: Human Operator (Strict, Immutable Ownership)                   │
│ Technology: Plain-English Markdown files (taste.md, rules.md)          │
│ Determinism: N/A (Human Intent) | Token Cost: N/A                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Deterministic Scripts (The Mechanical Plumbing)

### The Anti-Pattern
A frequent mistake in beginner AI architectures is asking the language model to:
- Connect to 15 different RSS feeds or web endpoints.
- Parse XML, regex-match timestamps, and handle HTTP retry backoffs.
- Iterate over directory trees and check file existence.

This is expensive, fragile, and slow. LLMs are notoriously poor at deterministic state keeping across large batches of raw data.

### The Correct Practice
Layer 1 is written in standard, deterministic code (Python, Bash, or Go). It acts as the land-grab harvester:
1. **Network & Ingestion:** Pulls raw data from APIs, Slack webhooks, Git logs, or RSS feeds.
2. **Deduplication Filter:** Compares candidate IDs against a local `seen_ids.json` ledger.
3. **Payload Sanitization:** Normalizes raw HTML or messy JSON into clean, consistent Markdown or lightweight JSON objects.
4. **Handoff Packaging:** Assembles only novel, relevant candidates into a structured context bundle ready for Layer 2.

**Rule of Thumb:** If a task can be expressed with a standard library function or a boolean conditional, it belongs in Layer 1.

---

## Layer 2: Agent Reasoning (The Cognitive Worker)

### Responsibilities
Layer 2 is where semantic reasoning is irreplaceable. The agent receives the filtered candidate bundle from Layer 1 and the policy files from Layer 3:
1. **Semantic Reading & Extraction:** Reads full-text articles or email threads, looking for commitments, key technical breakthroughs, or architectural regressions.
2. **Scoring & Triage:** Rates candidates on a multi-point rubric based on the criteria in `taste.md`.
3. **Drafting & Synthesis:** Produces high-density briefings, drafts response emails, or generates pull request code diffs.
4. **Decision Explanation:** For every item evaluated, outputs a structured rationale explaining why it passed or failed the threshold.

---

## Layer 3: Human Judgment & Policy (The Taste Owner)

### The Concept of Plain-English Policies
Traditional software encodes business rules in code. AI agent loops encode editorial tone, taste, and operational limits in plain-English Markdown files:
- `policy/taste.md`: What constitutes high-signal writing, preferred sources, and blacklist topics.
- `policy/constraints.md`: Formatting standards, tone guidelines, maximum allowable actions per run.
- `policy/commitments_rubric.md`: What qualifies as a high-priority commitment vs. casual banter.

### Example `taste.md`
```markdown
# Editorial Taste & Quality Guidelines

## High-Signal Criteria (Prioritize for inclusion)
- Grounded empirical benchmarks with reproducible source code or weights.
- Technical post-mortems detailing silent failure modes and architectural lessons.
- Novel hardware sizing methodologies (memory bandwidth, hybrid attention ratios).
- Independent engineering devlogs over corporate PR announcements.

## Hard Disqualification Criteria (Skip immediately)
- Superficial "Top 10 AI Tools" listicles or affiliate roundups.
- Speculative investment/venture capital market commentary.
- Vague marketing claims lacking code, architecture diagrams, or empirical proof.
- Content that has already appeared in the corpus within the past 30 days.
```

---

## The Authority Asymmetry Principle

One of the most vital security and reliability guarantees in loop engineering is the **Authority Asymmetry Principle**:

```
┌──────────────────────────┐             ┌──────────────────────────┐
│     AUTONOMOUS AGENT     │             │      HUMAN OPERATOR      │
├──────────────────────────┤             ├──────────────────────────┤
│ Can READ policy files    │             │ Can READ policy files    │
│ Can PROPOSE policy diffs │             │ Can WRITE policy files   │
│ CANNOT MODIFY policy     │             │ Holds EXCLUSIVE authority│
└──────────────────────────┘             └──────────────────────────┘
```

1. **Read-Only Access for the Agent:** The agent reads `taste.md` to guide its decisions during each cycle.
2. **Proposal Protocol:** The agent can observe longitudinal trends and append suggestions to an isolated staging file (`proposals.md`):
   ```markdown
   ### Agent Suggestion (Run 2026-10-14)
   - Feed `arxiv.org/list/cs.AI/recent` has yielded 0 accepted articles across the last 14 runs.
   - Propose: Retire feed or narrow keywords to `cs.LG`.
   ```
3. **Human Ratchet:** The human operator reads `proposals.md`, accepts or rejects suggestions, and commits changes to `taste.md`.

This prevents **policy drift**, where an unconstrained agent gradually lowers its own quality standards over time to minimize friction.

