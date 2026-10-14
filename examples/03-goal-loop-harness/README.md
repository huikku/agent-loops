# Example 03: Autonomous Goal Loop Harness (`/goal`)

This example demonstrates how to implement an iterative, contract-driven **Goal Loop** with an independent grader and hard-stop circuit breakers.

---

## The Goal Loop Protocol

1. **The Contract (`contract.json`):**
   Defines the exact criteria required for completion. In this example, 3 mock markdown documents must each satisfy two requirements:
   - Must contain a valid `# ` top-level heading.
   - Must contain at least two verified internal markdown links `[link](url)`.

2. **The Generator Agent:**
   Iterates through the target files, inspecting discrepancies and applying edits.

3. **The Decoupled Grader (`grader.py`):**
   An independent verification script that validates the generated files without LLM bias. It tests:
   - Does every file exist?
   - Does every file contain an H1 heading?
   - Does every file contain >= 2 valid markdown links?
   Returns exit code `0` ONLY when 100% of the contract is satisfied.

4. **The Loop Controller (`run_goal_loop.py`):**
   - Coordinates iterations.
   - Halts and celebrates when `grader.py` returns `0`.
   - Trips a hard stop if `MAX_ITERATIONS` is reached without passing.

---

## Running the Goal Loop

```bash
python3 run_goal_loop.py
```

