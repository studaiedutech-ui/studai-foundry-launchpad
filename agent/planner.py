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
#    market_validator with a description. Then add the routing
#    in executor.py."
# ============================================================

import json

# ── AVAILABLE TOOLS ──────────────────────────────────────────────
# This list tells the LLM what tools exist. When you add a new tool
# file in agent/tools/, you MUST also add it here — otherwise the
# planner won't know it exists and will never include it in a plan.
AVAILABLE_TOOLS = [
    {
        "name": "problem_definer",
        "description": "Generate CP1 Field 1 (Problem Statement) and Field 2 (Target Users) from the raw idea",
    },
    {
        "name": "solution_architect",
        "description": "Generate CP1 Field 3 (Autonomy Loop Plan) and Field 4 (Tools & APIs) using the problem analysis",
    },
    {
        "name": "idea_challenger",
        "description": "Devil's advocate — challenge the idea, find blind spots, anticipate judge questions, suggest improvements",
    },
    {
        "name": "submission_writer",
        "description": "Generate CP1 Field 5 (Evaluation Logic) and Field 6 (Expected Output), compile all 6 fields using insights from the challenger",
    },
]


def create_plan(idea, feedback, client, model):
    """Ask the LLM to generate a JSON execution plan for the given idea."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────
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

GOAL: Generate a complete CP1 submission for StudAI Foundry hackathon. The CP1 form has 6 fields: Problem Statement, Target Users, Autonomy Loop Plan, Tools & APIs, Evaluation Logic, and Expected Output.

PROJECT IDEA: {idea}
{feedback_section}
AVAILABLE TOOLS:
{tools_description}

Create an execution plan with exactly 4 steps, one per tool.
Order: problem_definer → solution_architect → idea_challenger → submission_writer
The submission_writer MUST be last (it synthesises all previous outputs).
The idea_challenger MUST come before submission_writer (its critique improves the final draft).

Return ONLY valid JSON — no markdown, no explanation, no extra text.
Use this exact format:
[
  {{"step": 1, "tool": "problem_definer", "reason": "why this step"}},
  {{"step": 2, "tool": "solution_architect", "reason": "why this step"}},
  {{"step": 3, "tool": "idea_challenger", "reason": "why this step"}},
  {{"step": 4, "tool": "submission_writer", "reason": "why this step"}}
]"""

    # ── CALL THE LLM ─────────────────────────────────────────────
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )

    raw = response.choices[0].message.content

    # ── PARSE THE JSON ───────────────────────────────────────────
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()

    plan = json.loads(raw)
    return plan
