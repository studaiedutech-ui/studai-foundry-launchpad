# ============================================================
# planner.py — Creates a JSON execution plan from goal + feedback
# ============================================================
# PURPOSE:
#   The planner asks the LLM to create a step-by-step action plan
#   in JSON format. It tells the LLM what tools are available and
#   lets the LLM decide the order and reasoning for each step.
#
# THE PLANNING PATTERN:
#   An autonomous agent doesn't just "do stuff" — it first PLANS
#   what to do. The plan is a list of tool calls in order. This is
#   what separates an agent from a chatbot: the agent decides its
#   own workflow before executing it.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Add a new tool to AVAILABLE_TOOLS in planner.py called
#    competitor_analyzer with a description of what it does.
#    Then add the routing in executor.py."
# ============================================================

import json

# ── AVAILABLE TOOLS ──────────────────────────────────────────────
# This list tells the LLM what tools exist. When you add a new tool
# file in agent/tools/, you MUST also add it here — otherwise the
# planner won't know it exists and will never include it in a plan.
AVAILABLE_TOOLS = [
    {
        "name": "problem_definer",
        "description": "Extract and define the core problem: target users, pain point, urgency, current alternatives",
    },
    {
        "name": "solution_architect",
        "description": "Design the solution: proposed product, autonomy angle, tech stack, agent tools, and 10-day build plan",
    },
    {
        "name": "submission_writer",
        "description": "Write the final formatted CP1 submission draft with all required sections for the StudAI Foundry hackathon",
    },
]


def create_plan(idea, feedback, client, model):
    """Ask the LLM to generate a JSON execution plan for the given idea."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────
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

    prompt = f"""You are a planning engine for an autonomous CP1 submission drafting agent.

GOAL: Help a student team prepare their CP1 (Checkpoint 1) submission for StudAI Foundry hackathon based on this idea.

PROJECT IDEA: {idea}
{feedback_section}
AVAILABLE TOOLS:
{tools_description}

Create an execution plan with exactly 3 steps, one per tool.
The submission_writer tool MUST be the last step (it synthesises all previous outputs).

Return ONLY valid JSON — no markdown, no explanation, no extra text.
Use this exact format:
[
  {{"step": 1, "tool": "tool_name", "reason": "why this step is needed"}},
  {{"step": 2, "tool": "tool_name", "reason": "why this step is needed"}},
  {{"step": 3, "tool": "tool_name", "reason": "why this step is needed"}}
]"""

    # ── CALL THE LLM ─────────────────────────────────────────────
    # Why temperature 0.2: planning needs to be deterministic — we want
    # the same logical structure every time, not creative variation
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )

    raw = response.choices[0].message.content

    # ── PARSE THE JSON ───────────────────────────────────────────
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
