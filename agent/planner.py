# ============================================================
# planner.py — LLM call that returns a JSON action plan
# ============================================================
# PURPOSE:
#   The planner takes a startup idea (and optional feedback from a
#   previous failed loop) and asks the LLM to produce a step-by-step
#   execution plan as JSON. Each step names a tool to run and why.
#
# THE PLANNING PATTERN:
#   An autonomous agent doesn't just "do stuff" — it first PLANS
#   what to do. The plan is a list of tool calls in order. This is
#   what separates an agent from a chatbot: the agent decides its
#   own workflow before executing it.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Add a new tool called competitor_finder to the AVAILABLE_TOOLS
#    list in planner.py. Set its description to: 'Find and analyse
#    the top 3 competitors in this market.' Then update executor.py
#    to route this tool to a new file agent/tools/competitor_finder.py."
# ============================================================

import json

# ── AVAILABLE TOOLS ──────────────────────────────────────────────
# Why this list matters: the planner tells the LLM what tools exist.
# To add a new capability to the agent, add it here FIRST, then
# create the tool file, then add the routing in executor.py.
AVAILABLE_TOOLS = [
    {
        "name": "market_research",
        "description": "Research target customers, market size, and core problem",
    },
    {
        "name": "feasibility",
        "description": "Score the idea on technical, market, revenue, competition, and founder dimensions",
    },
    {
        "name": "brief_writer",
        "description": "Write the final structured validation brief with verdict and next steps",
    },
]


def create_plan(idea, feedback, client, model):
    """Ask the LLM to generate a JSON execution plan for the given idea."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────────
    # Why we include feedback: if the reviewer rejected the last attempt,
    # we pass its feedback here so the planner can adjust the strategy
    feedback_section = ""
    if feedback:
        feedback_section = f"""
FEEDBACK FROM PREVIOUS ATTEMPT (use this to improve the plan):
{feedback}
"""

    tools_description = "\n".join(
        [f'  - {t["name"]}: {t["description"]}' for t in AVAILABLE_TOOLS]
    )

    prompt = f"""You are a planning engine for an autonomous startup validation agent.

GOAL: Validate this startup idea thoroughly and produce a structured brief.

STARTUP IDEA: {idea}
{feedback_section}
AVAILABLE TOOLS:
{tools_description}

Create an execution plan with exactly 3 steps, one per tool.
The brief_writer tool MUST be the last step (it synthesises all previous outputs).

Return ONLY valid JSON — no markdown, no explanation, no extra text.
Use this exact format:
[
  {{"step": 1, "tool": "tool_name", "reason": "why this step is needed"}},
  {{"step": 2, "tool": "tool_name", "reason": "why this step is needed"}},
  {{"step": 3, "tool": "tool_name", "reason": "why this step is needed"}}
]"""

    # ── CALL THE LLM ─────────────────────────────────────────────────
    # Why temperature 0.2: planning needs to be deterministic — we want
    # the same logical structure every time, not creative variation
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )

    raw = response.choices[0].message.content

    # ── PARSE THE JSON ───────────────────────────────────────────────
    # Why we strip code fences: some LLMs wrap JSON in ```json ... ```
    # even when told not to — this handles that gracefully
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()

    plan = json.loads(raw)
    return plan
