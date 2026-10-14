#!/usr/bin/env python3
"""run_goal_loop.py: The loop controller for Example 03 Goal Loop.
Coordinates iterative generator passes, runs decoupled grader.py,
detects stagnation, and enforces hard stop ceilings.
"""
import json
import os
import subprocess
import sys
import time

def run_grader() -> int:
    """Executes the decoupled verification script."""
    res = subprocess.run([sys.executable, "grader.py"], capture_output=True, text=True)
    print(res.stdout.strip())
    if res.stderr:
        print(res.stderr.strip(), file=sys.stderr)
    return res.returncode

def apply_simulated_agent_fixes(cycle: int, targets: list):
    """Simulates iterative agent fixes applied over successive passes."""
    print(f"\n--- [AGENT CYCLE {cycle}] Applying corrective edits to targets ---")
    
    if cycle == 1:
        # Pass 1: Fix post_1 by adding H1 and a second link
        p1 = "posts/post_1.md"
        with open(p1, "w") as f:
            f.write("# Post One: Architecture Overview\n\nThis is post one.\nSee [Link One](https://example.com/one) and [Link Two](https://example.com/two).\n")
        print(f"  [FIXED] {p1}: Added H1 and missing link.")

    elif cycle == 2:
        # Pass 2: Fix post_2 by adding a second link
        p2 = "posts/post_2.md"
        with open(p2, "w") as f:
            f.write("# Post Two: Memory Laws\n\nThis post now has [One Link](https://example.com/single) and [Second Link](https://example.com/double).\n")
        print(f"  [FIXED] {p2}: Added second internal link.")

    elif cycle == 3:
        # Pass 3: Fix post_3 by adding H1 and 2 links
        p3 = "posts/post_3.md"
        with open(p3, "w") as f:
            f.write("# Post Three: State Ledgers\n\nFull state documentation.\nReferences: [Doc Link](https://example.com/doc) and [Repo Link](https://example.com/repo).\n")
        print(f"  [FIXED] {p3}: Added H1 heading and 2 internal links.")

def main():
    contract_file = "contract.json"
    with open(contract_file, "r") as f:
        contract = json.load(f)

    max_iter = contract.get("max_iterations", 5)
    targets = contract.get("targets", [])

    print(f"=== LAUNCHING GOAL LOOP: {contract['contract_id']} ===")
    print(f"Objective: {contract['description']}")
    print(f"Ceiling: Max {max_iter} iterations\n")

    # Cycle 0: Initial verification
    print("[CYCLE 0] Running initial baseline evaluation...")
    code = run_grader()
    if code == 0:
        print("\n[SUCCESS] Contract already satisfied at baseline! Zero edits needed.")
        sys.exit(0)

    # Iterative Goal Loop
    for cycle in range(1, max_iter + 1):
        apply_simulated_agent_fixes(cycle, targets)
        time.sleep(0.5)

        print(f"[CYCLE {cycle}] Invoking decoupled grader...")
        code = run_grader()

        if code == 0:
            print(f"\n🎉 [GOAL REACHED] Objective verified and passed on Cycle {cycle}!")
            print("[✓] Terminating loop cleanly. Ready for deployment/commit.")
            sys.exit(0)
        else:
            print(f"[RETRY] Grader reported remaining unmet requirements. Continuing to next pass...")

    print(f"\n🚨 [CIRCUIT BREAKER] Hard stop ceiling reached ({max_iter} iterations).")
    print("[!] Halting to prevent infinite token consumption. Operator intervention required.")
    sys.exit(1)

if __name__ == "__main__":
    main()

