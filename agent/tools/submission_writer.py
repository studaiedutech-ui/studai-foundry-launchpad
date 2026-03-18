# ============================================================
# submission_writer.py — Tool 3: Write the CP1 submission draft
# ============================================================
# PURPOSE:
#   This tool synthesises the problem analysis (Tool 1) and the
#   solution architecture (Tool 2) into a formatted CP1 checkpoint
#   submission draft for the StudAI Foundry hackathon.
#
# WHY THIS IS ALWAYS THE LAST TOOL (synthesis pattern):
#   The submission writer needs ALL previous outputs to produce a
#   complete draft. It's the "assembler" — it takes raw analysis
#   and architecture, and formats them into a submission-ready
#   document. In any autonomous agent, the last tool is always
#   the synthesiser that produces the final user-facing output.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Change submission_writer.py to output a CP2 demo script
#    instead of a CP1 draft. Include sections for: Demo Flow,
#    Talking Points, Live Demo Checklist, and Backup Plan."
# ============================================================


def run(idea, problem_analysis, solution_architecture, client, model):
    """Synthesise all tool outputs into a formatted CP1 submission draft."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────
    prompt = f"""You are helping a student team write their CP1 (Checkpoint 1) submission for StudAI Foundry — India's national autonomous AI systems hackathon.

Using the problem analysis and solution architecture below, write a complete CP1 submission draft.

PROJECT IDEA: {idea}

PROBLEM ANALYSIS:
{problem_analysis}

SOLUTION ARCHITECTURE:
{solution_architecture}

Write the submission using these EXACT sections and markdown headers:

## StudAI Foundry — CP1 Submission

### Team's Project Title
(Create a compelling, specific title — not generic)

### Problem Statement
(3-4 sentences: Who has the problem, what exactly the problem is, why it matters NOW. Must be specific, not generic.)

### Proposed Solution
(3-4 sentences: What the product does, how the user interacts with it, what the output looks like. Be concrete.)

### How Autonomy Works in This Product
(Explain the THINK → PLAN → EXECUTE → REVIEW → UPDATE cycle for THIS specific product. What does each step do? Why is this an autonomous agent and not a chatbot? This section is critical for the judges.)

### Target Users
(Specific user segment with demographics — not "everyone" or "students")

### Tech Stack
(Table or list: LLM provider, UI framework, key libraries, external APIs)

### Agent Tools
(List each tool the agent uses with a one-line description)

### 10-Day Build Plan
(Day-by-day or phase-by-phase plan. Must be realistic for students with 3-4 hours/day.)

### Why This Idea Will Win
(2-3 sentences: What makes this stand out from other submissions? What's the unfair advantage?)

Keep it under 500 words. Be direct, specific, and compelling. Judges read 100+ submissions — make it impossible to skim past.
No filler. No generic statements. Every sentence should carry weight."""

    # ── CALL THE LLM ─────────────────────────────────────────────
    # Why temperature 0.4: submissions need personality and punch
    # but must stay grounded in the actual analysis
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=800,
    )

    return response.choices[0].message.content
