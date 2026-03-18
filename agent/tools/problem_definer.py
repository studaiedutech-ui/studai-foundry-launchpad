# ============================================================
# problem_definer.py — Tool 1: Extract and define the problem
# ============================================================
# PURPOSE:
#   This tool takes a raw startup/project idea and extracts a
#   structured problem definition: who has the problem, what
#   exactly the problem is, how urgent it is, and what people
#   currently do without a solution.
#
# WHY THIS IS A SEPARATE FILE (single responsibility):
#   Each tool does ONE job. problem_definer doesn't propose
#   solutions — it only clarifies the problem. This forces the
#   agent to understand the problem BEFORE jumping to solutions,
#   which is how good product thinking works.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Change problem_definer.py to extract problems specific to
#    [your domain]. For example, for a healthcare agent, extract
#    patient pain points, clinical workflow gaps, and regulatory
#    constraints instead of generic startup problems."
# ============================================================


def run(idea, client, model):
    """Extract a structured problem definition from a raw idea."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────
    prompt = f"""You are a product strategist helping a student team define their problem clearly for a hackathon submission.

Given this project idea, extract a structured problem definition.

PROJECT IDEA: {idea}

Respond with these exact sections:

**Target Users:**
Who exactly has this problem? Be specific — not "students" but "2nd-3rd year engineering students in tier-2 Indian colleges who struggle with X."

**The Problem:**
What is the specific pain point in 2-3 sentences? Don't describe the solution — describe the PAIN. What are users frustrated by? What takes too long? What fails?

**Urgency & Frequency:**
How often do users face this problem? Is it daily, weekly, seasonal? Why does it need to be solved NOW — what has changed recently (AI availability, policy changes, market shifts)?

**Current Alternatives:**
What do users do TODAY without this solution? Manual process? Existing apps that fall short? Asking friends? Nothing? Be specific.

**Problem Severity (1-10):**
Rate how painful this problem is with one sentence justification.

Be specific to India where relevant. Under 250 words. No generic filler."""

    # ── CALL THE LLM ─────────────────────────────────────────────
    # Why temperature 0.4: we want specific, grounded analysis —
    # not creative fiction about the problem
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=400,
    )

    return response.choices[0].message.content
