# ============================================================
# executor.py — Routes plan steps to tool functions
# ============================================================
# PURPOSE:
#   The executor takes the JSON plan from planner.py and runs each
#   step by calling the correct tool function. It is the "hands"
#   of the agent — it does the actual work.
#
# INFORMATION FLOW (4-tool pipeline):
#   problem_definer    → only needs the idea (first in chain)
#   solution_architect → needs idea + problem analysis
#   idea_challenger    → needs idea + problem + solution (challenges both)
#   submission_writer  → needs EVERYTHING including challenger output
#
# RESILIENCE:
#   Each tool call is wrapped in retry logic with exponential backoff.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Add a new elif branch in executor.py for a tool called
#    market_validator. Import it from agent.tools.market_validator
#    and pass it the idea and problem_definer results."
# ============================================================

import time

from agent.tools import problem_definer, solution_architect, idea_challenger, submission_writer

# ── RETRY CONFIGURATION ─────────────────────────────────────────
MAX_RETRIES = 2
RETRY_DELAY = 2


def _run_with_retry(fn, tool_name, on_log):
    """Run a tool function with retry logic for transient API errors."""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt <= MAX_RETRIES:
                wait = RETRY_DELAY * (2 ** (attempt - 1))
                on_log(f"Tool {tool_name} error (attempt {attempt}): {e} — retrying in {wait}s...")
                time.sleep(wait)
            else:
                on_log(f"Tool {tool_name} failed after {attempt} attempts: {e}")
                raise last_error


def run_plan(plan, idea, client, model, on_log):
    """Execute each step in the plan by routing to the correct tool."""

    results = {}

    for step in plan:
        tool = step["tool"]
        on_log(f"Running tool: {tool} — {step['reason']}")

        # ── ROUTE TO THE CORRECT TOOL ────────────────────────────────
        if tool == "problem_definer":
            results["problem_definer"] = _run_with_retry(
                lambda: problem_definer.run(idea, client, model),
                tool, on_log,
            )

        elif tool == "solution_architect":
            pd = results.get("problem_definer", "")
            results["solution_architect"] = _run_with_retry(
                lambda: solution_architect.run(idea, pd, client, model),
                tool, on_log,
            )

        elif tool == "idea_challenger":
            pd = results.get("problem_definer", "")
            sa = results.get("solution_architect", "")
            results["idea_challenger"] = _run_with_retry(
                lambda: idea_challenger.run(idea, pd, sa, client, model),
                tool, on_log,
            )

        elif tool == "submission_writer":
            pd = results.get("problem_definer", "")
            sa = results.get("solution_architect", "")
            ic = results.get("idea_challenger", "")
            results["submission_writer"] = _run_with_retry(
                lambda: submission_writer.run(idea, pd, sa, ic, client, model),
                tool, on_log,
            )

        else:
            on_log(f"Unknown tool: {tool} — skipping")
            continue

        on_log(f"Tool {tool} complete ✓")

    return results
