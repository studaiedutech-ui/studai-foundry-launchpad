# ============================================================
# executor.py — Routes plan steps to tool functions
# ============================================================
# PURPOSE:
#   The executor takes the JSON plan from planner.py and runs each
#   step by calling the correct tool function. It is the "hands"
#   of the agent — it does the actual work.
#
# INFORMATION FLOW:
#   Each tool gets different inputs because information chains
#   through the pipeline:
#     - market_research: only needs the idea (it's the first tool)
#     - feasibility: needs the idea AND market research results
#       (so it can ground its scores in real market context)
#     - brief_writer: needs EVERYTHING (idea + research + scores)
#       because it synthesises all previous outputs into the final brief
#
# RESILIENCE:
#   Each tool call is wrapped in retry logic with exponential backoff.
#   This handles transient network errors and occasional API hiccups
#   without crashing the entire agent loop.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Add a new elif branch in executor.py for a tool called
#    competitor_finder. Import it from agent.tools.competitor_finder
#    and pass it the idea and market_research results."
# ============================================================

import time

from agent.tools import market_research, feasibility, brief_writer

# ── RETRY CONFIGURATION ─────────────────────────────────────────
# Why 2 retries: enough to survive a transient API blip, but not so
# many that a genuine error wastes the student's time waiting
MAX_RETRIES = 2
RETRY_DELAY = 2  # seconds — doubles on each retry (exponential backoff)


def _run_with_retry(fn, tool_name, on_log):
    """Run a tool function with retry logic for transient API errors."""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 2):  # +2 because range is exclusive and attempt 1 is the first try
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
        # Why each tool gets different inputs: later tools need the
        # outputs of earlier tools. This is how the agent builds up
        # a complete analysis step by step.
        if tool == "market_research":
            results["market_research"] = _run_with_retry(
                lambda: market_research.run(idea, client, model),
                tool, on_log,
            )

        elif tool == "feasibility":
            # Why we capture the value: Python closures bind by reference,
            # so we snapshot market_research result for the lambda
            mr = results.get("market_research", "")
            results["feasibility"] = _run_with_retry(
                lambda: feasibility.run(idea, mr, client, model),
                tool, on_log,
            )

        elif tool == "brief_writer":
            mr = results.get("market_research", "")
            fs = results.get("feasibility", "")
            results["brief_writer"] = _run_with_retry(
                lambda: brief_writer.run(idea, mr, fs, client, model),
                tool, on_log,
            )

        else:
            on_log(f"Unknown tool: {tool} — skipping")
            continue

        on_log(f"Tool {tool} complete ✓")

    return results
