# ============================================================
# solution_architect.py — Tool 2: Design the solution & build plan
# ============================================================
# PURPOSE:
#   This tool takes the idea AND the problem analysis from Tool 1,
#   then designs a concrete solution: what to build, what tech stack
#   to use, how autonomy/AI fits in, and a realistic 10-day build
#   plan for the Foundry hackathon.
#
# WHY THIS TAKES problem_analysis AS INPUT (information chaining):
#   The solution must directly address the problem defined in Tool 1.
#   If we skipped Tool 1 and went straight to solution design, the
#   LLM might propose a solution for a DIFFERENT problem than what
#   the user described. Information chaining keeps the pipeline
#   grounded — each tool builds on the previous one's output.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Update solution_architect.py to design solutions for [your
#    domain]. Change the tech stack recommendations and build plan
#    timeline to match your hackathon's requirements."
# ============================================================


def run(idea, problem_analysis, client, model):
    """Design a solution architecture and 10-day build plan."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────
    prompt = f"""You are a technical architect helping a student team design their hackathon project for StudAI Foundry — a national autonomous AI systems hackathon.

The team has defined their problem. Now design their solution.

PROJECT IDEA: {idea}

PROBLEM ANALYSIS:
{problem_analysis}

Respond with these exact sections:

**Proposed Solution:**
What exactly will this product do? Describe it in 3-4 sentences. Be concrete — not "an AI-powered platform" but "a WhatsApp bot that receives a photo of a prescription and returns a simplified explanation in Hindi/English within 30 seconds."

**The Autonomy Angle:**
How does the 5-step autonomous agent loop (THINK → PLAN → EXECUTE → REVIEW → UPDATE) apply to this product? What does the agent THINK about? What tools does it PLAN to use? What does it EXECUTE? How does it REVIEW its own output? Be specific — this is what makes it an autonomous agent, not a chatbot.

**Recommended Tech Stack:**
List the specific technologies. Keep it realistic for a student team with 10 days:
- LLM Provider: (Groq / OpenAI / etc.)
- UI: (Streamlit / Gradio / WhatsApp API / etc.)
- Key Libraries: (list 3-5 max)
- External APIs: (if any — keep it to free tiers)

**Agent Tools Design:**
List 3-4 tools the agent would use (like the tools/ folder in the starter repo). For each:
- Tool name (snake_case)
- What it does in one sentence
- What input it needs

**10-Day Build Plan:**
Day 1-2: [what to build]
Day 3-4: [what to build]
Day 5-6: [what to build]
Day 7-8: [what to build]
Day 9-10: [what to build — polish, demo video, final submission]

Be realistic. Students have classes. Assume 3-4 hours/day of building. Under 400 words."""

    # ── CALL THE LLM ─────────────────────────────────────────────
    # Why temperature 0.3: technical architecture needs to be precise
    # and realistic — we don't want hallucinated tech stacks
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600,
    )

    return response.choices[0].message.content
