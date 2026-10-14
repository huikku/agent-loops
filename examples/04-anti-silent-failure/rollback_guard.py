#!/usr/bin/env python3
"""rollback_guard.py: Law II - Atomic Rollback.
Simulates taking a workspace snapshot before an agent batch, detecting failures,
and cleanly reverting workspace state to prevent partial/half-broken deployments.
"""
import argparse
import os
import shutil
import sys

SNAPSHOT_DIR = ".workspace_snapshot"
DATA_FILE = "workspace_data.txt"

def snapshot():
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    if os.path.exists(DATA_FILE):
        shutil.copy2(DATA_FILE, os.path.join(SNAPSHOT_DIR, DATA_FILE))
    print(f"[SNAPSHOT] Created clean workspace checkpoint for {DATA_FILE}.")

def rollback():
    snap_file = os.path.join(SNAPSHOT_DIR, DATA_FILE)
    if os.path.exists(snap_file):
        shutil.copy2(snap_file, DATA_FILE)
        print(f"[ROLLBACK] Restored {DATA_FILE} to last known good checkpoint.")
    elif os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        print(f"[ROLLBACK] Removed corrupted {DATA_FILE}.")
    if os.path.exists(SNAPSHOT_DIR):
        shutil.rmtree(SNAPSHOT_DIR)

def cleanup():
    if os.path.exists(SNAPSHOT_DIR):
        shutil.rmtree(SNAPSHOT_DIR)
    print("[CLEANUP] Batch verified; discarded temporary snapshot.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate-failure", action="store_true", help="Simulate a mid-batch agent failure.")
    args = parser.parse_args()

    # Create baseline file
    with open(DATA_FILE, "w") as f:
        f.write("BASELINE STATE: 100% HEALTHY\n")

    print("=== EXECUTING ATOMIC ROLLBACK GUARD ===")
    snapshot()

    # Agent starts modifying files
    print("[AGENT] Modifying workspace files (Item 1 of 10)...")
    with open(DATA_FILE, "a") as f:
        f.write("CORRUPTED PARTIAL WRITE (ITEM 4 FAILED)\n")

    if args.simulate_failure:
        print("\n🚨 [ERROR] Agent encountered unhandled exception on item 4!")
        print("Enforcing Law II: Never deploy or retain half-broken state.")
        rollback()
        with open(DATA_FILE, "r") as f:
            print(f"[VERIFY CURRENT FILE] Contents:\n{f.read().strip()}")
        sys.exit(1)
    else:
        print("\n[✓] All 10 items processed and verified.")
        cleanup()
        sys.exit(0)

if __name__ == "__main__":
    main()
