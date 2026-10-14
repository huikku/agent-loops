#!/usr/bin/env python3
"""scan_commitments.py: Layer 1/2 harness for the dropped commitments reconciler.
Demonstrates deterministic candidate ingestion, criteria-based evaluation,
draft email generation, and structured audit trail logging.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

def parse_args():
    parser = argparse.ArgumentParser(description="Scan communications for dropped commitments.")
    parser.add_argument("--input", default="sample_inputs.json", help="Path to input messages JSON.")
    parser.add_argument("--criteria", default="taste_criteria.md", help="Path to plain-English policy criteria.")
    parser.add_argument("--audit-log", default="audit_triage.log", help="Path to append audit log.")
    return parser.parse_args()

def evaluate_message(msg: dict, today: datetime) -> dict:
    """Simulates Layer 2 semantic evaluation against policy criteria."""
    text = msg["text"].lower()
    
    # 1. Check for pleasantries / non-commitments
    if "great demo" in text or "grab coffee" in text or "great sync" in text and "will review" not in text:
        return {
            "id": msg["id"],
            "is_commitment": False,
            "reason": "Social pleasantry or informational comment with no actionable deliverable."
        }
    
    # 2. Extract commitment and priority
    msg_dt = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
    days_old = (today - msg_dt).days

    if "by end of day tuesday" in text or days_old >= 7:
        priority = "P0 - OVERDUE"
        due_status = f"Past due by ~{days_old} days"
        draft = (
            f"Subject: Re: ComfyUI workflow follow-up\n\n"
            f"Hi {msg['recipient'].split()[0]},\n\n"
            f"I promised to send this over earlier and let it slip past my radar. "
            f"Here is the updated ComfyUI multi-GPU LoRA workflow JSON attached. "
            f"Let me know if you run into any dependency issues during testing.\n\n"
            f"Best,\nJohn"
        )
    elif "by thursday" in text or days_old >= 3:
        priority = "P0 - OVERDUE"
        due_status = "Missed Thursday deadline"
        draft = (
            f"Subject: Re: PR #44 review status\n\n"
            f"Hi {msg['recipient'].split()[0]},\n\n"
            f"Apologies for the delay on PR #44. I am reviewing the tracking hub changes now "
            f"and will leave comments by 2:00 PM so you can proceed with the release.\n\n"
            f"Best,\nJohn"
        )
    else:
        priority = "P1 - IMMINENT"
        due_status = "Due this Friday"
        draft = None

    return {
        "id": msg["id"],
        "is_commitment": True,
        "recipient": msg["recipient"],
        "channel": msg["channel"],
        "original_text": msg["text"],
        "priority": priority,
        "due_status": due_status,
        "draft_reply": draft,
        "reason": "Explicit promise of deliverable with temporal deadline."
    }

def main():
    args = parse_args()
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.", file=sys.stderr)
        sys.exit(1)

    today = datetime(2026, 10, 14, tzinfo=timezone.utc)
    with open(args.input, "r") as f:
        messages = json.load(f)

    results = []
    with open(args.audit_log, "a") as log:
        for msg in messages:
            res = evaluate_message(msg, today)
            results.append(res)
            # Log decision ledger
            status_tag = "COMMITMENT" if res["is_commitment"] else "DISCARDED"
            p_tag = res.get("priority", "N/A")
            log.write(f"{today.isoformat()} | {msg['id']} | {status_tag} | {p_tag} | {res['reason']}\n")

    # Generate Markdown Report
    print("# Dropped Commitments & Loose-Ends Triage Report")
    print(f"**Audit Timestamp:** {today.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"**Messages Scanned:** {len(messages)}\n")

    overdue = [r for r in results if r.get("priority") == "P0 - OVERDUE"]
    imminent = [r for r in results if r.get("priority") == "P1 - IMMINENT"]

    print(f"## 🚨 Overdue Items Requiring Immediate Reconciliation ({len(overdue)})")
    for o in overdue:
        print(f"### [{o['priority']}] To: {o['recipient']} ({o['channel'].upper()})")
        print(f"> \"{o['original_text']}\"")
        print(f"- **Status:** {o['due_status']}")
        if o['draft_reply']:
            print("```text")
            print(o['draft_reply'])
            print("```\n")

    print(f"## ⏳ Upcoming / Imminent Deadlines ({len(imminent)})")
    for i in imminent:
        print(f"- **{i['recipient']}**: {i['original_text']} ({i['due_status']})")

    print(f"\n[✓] Audit decisions appended to {args.audit_log}")

if __name__ == "__main__":
    main()
