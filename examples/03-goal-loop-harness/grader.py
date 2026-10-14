#!/usr/bin/env python3
"""grader.py: Independent, decoupled verifier for Example 03 Goal Loop.
Validates target files against contract.json requirements.
Exits with 0 ONLY if 100% of the contract passes; otherwise exits with 1.
An agent cannot grade its own paper.
"""
import json
import os
import re
import sys

def grade_file(filepath: str) -> list:
    errors = []
    if not os.path.exists(filepath):
        return [f"File {filepath} does not exist."]

    with open(filepath, "r") as f:
        content = f.read()

    # Rule 1: Check for H1 header
    if not re.search(r"^#\s+[^\n]+", content, re.MULTILINE):
        errors.append(f"{filepath}: Missing required top-level '# Title' heading.")

    # Rule 2: Check for at least 2 markdown links
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
    if len(links) < 2:
        errors.append(f"{filepath}: Has {len(links)} links; requires at least 2.")

    return errors

def main():
    contract_path = "contract.json"
    if not os.path.exists(contract_path):
        print(f"[FAIL] Contract {contract_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(contract_path, "r") as f:
        contract = json.load(f)

    all_errors = []
    for target in contract["targets"]:
        target_path = os.path.join(os.path.dirname(__file__), target)
        errs = grade_file(target_path)
        all_errors.extend(errs)

    if all_errors:
        print(f"[GRADER: FAIL] Found {len(all_errors)} unmet contract requirements:")
        for e in all_errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("[GRADER: PASS] All target files meet 100% of contract requirements!")
        sys.exit(0)

if __name__ == "__main__":
    main()

