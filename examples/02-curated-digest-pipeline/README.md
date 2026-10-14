# Example 02: 3-Layer Automated Curated Newspaper Pipeline

This example implements the exact 3-layer architecture behind Jason Elgin's 6-day unattended morning newspaper and research digest.

---

## The System Architecture

```
[Cron Trigger 05:00]
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 1: fetch_candidates.py                           │
│ • Deterministic Python script (0 AI tokens)           │
│ • Pulls RSS feeds & API endpoints                      │
│ • Strips previously processed URLs via seen_urls.txt   │
│ • Writes fresh items to staged_candidates.json         │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 2 & 3: evaluate_digest.py                        │
│ • Reads staged_candidates.json                         │
│ • Loads human policy rules from taste.md               │
│ • Evaluates each candidate against criteria            │
│ • Appends decisions (PICKED/SKIPPED) to decisions.log  │
│ • Updates seen_urls.txt                                │
│ • Generates daily_edition.html / daily_edition.md      │
└────────────────────────────────────────────────────────┘
```

---

## Running the Pipeline

1. **Step 1: Ingest & Deduplicate Candidates (Layer 1)**
   ```bash
   python3 fetch_candidates.py
   ```
   *Pulls raw candidates, filters out items already in `seen_urls.txt`, and stages novel items.*

2. **Step 2: Evaluate Against Policy & Publish Digest (Layer 2 & 3)**
   ```bash
   python3 evaluate_digest.py
   ```
   *Scores candidates against `taste.md`, writes `daily_edition.md`, and logs rationale to `decisions.log`.*

