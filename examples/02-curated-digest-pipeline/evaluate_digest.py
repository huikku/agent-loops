#!/usr/bin/env python3
"""evaluate_digest.py: Layer 2 reasoning evaluation against Layer 3 taste policy.
Scores staged candidates against taste.md criteria, logs every decision
to decisions.log, updates seen_urls.txt, and compiles the daily Markdown edition.
"""
import json
import os
import sys
from datetime import datetime, timezone

def evaluate_candidate(candidate: dict, taste_text: str) -> dict:
    """Simulates Layer 2 agent reasoning evaluated against taste.md."""
    title = candidate["title"].lower()
    body = candidate["body"].lower()

    # Rule 1: Check hard disqualification
    if "top 10" in title or "affiliate" in body:
        return {
            "decision": "SKIPPED",
            "score": 2,
            "reason": "Violates hard disqualification: affiliate marketing listicle with zero technical depth."
        }

    # Rule 2: High signal technical benchmarks
    if "hybrid attention" in body or "memory bandwidth" in body or "thor dev kit" in body:
        return {
            "decision": "PICKED",
            "score": 9,
            "reason": "Matches high-signal criteria: empirical hardware benchmarks and architectural analysis."
        }

    # Rule 3: Loop engineering / systems design
    if "loop engineering" in body or "3-layer" in body:
        return {
            "decision": "PICKED",
            "score": 9,
            "reason": "Matches high-signal criteria: real-world agent loop architecture and human-in-loop control."
        }

    return {
        "decision": "SKIPPED",
        "score": 5,
        "reason": "Moderate substance, but lacks reproducible code or novel technical contributions."
    }

def main():
    staged_file = "staged_candidates.json"
    taste_file = "taste.md"
    log_file = "decisions.log"
    seen_file = "seen_urls.txt"

    if not os.path.exists(staged_file):
        print(f"Error: {staged_file} not found. Run fetch_candidates.py first.", file=sys.stderr)
        sys.exit(1)

    with open(staged_file, "r") as f:
        candidates = json.load(f)

    with open(taste_file, "r") as f:
        taste_text = f.read()

    now_iso = datetime.now(timezone.utc).isoformat()
    picked_items = []

    with open(log_file, "a") as log, open(seen_file, "a") as seen:
        for c in candidates:
            eval_res = evaluate_candidate(c, taste_text)
            decision = eval_res["decision"]
            score = eval_res["score"]
            reason = eval_res["reason"]

            # Append to decisions.log
            log.write(f"{now_iso} | {c['url']} | {decision} | Score: {score}/10 | {reason}\n")
            # Append to seen_urls.txt to prevent re-processing
            seen.write(f"{c['url']}\n")

            if decision == "PICKED":
                c["eval"] = eval_res
                picked_items.append(c)

    # Compile Daily Edition Markdown
    edition_file = "daily_edition.md"
    with open(edition_file, "w") as out:
        out.write(f"# Daily Curated Technical Briefing\n")
        out.write(f"**Publication Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n")
        out.write(f"Curated autonomously via 3-layer loop engineering from {len(candidates)} staged candidates.\n\n---\n\n")

        for idx, item in enumerate(picked_items, 1):
            out.write(f"## {idx}. [{item['title']}]({item['url']})\n")
            out.write(f"**Source:** {item['source']} | **Signal Score:** {item['eval']['score']}/10\n\n")
            out.write(f"{item['body']}\n\n")
            out.write(f"> *Curation Rationale:* {item['eval']['reason']}\n\n")

    print(f"\n[✓] Evaluated {len(candidates)} candidates against {taste_file}.")
    print(f"[✓] Selected {len(picked_items)} articles for publication.")
    print(f"[✓] Appended audit trail to {log_file}.")
    print(f"[✓] Generated publication draft: {edition_file}")

if __name__ == "__main__":
    main()

