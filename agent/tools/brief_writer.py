# ============================================================
# brief_writer.py — Tool 3: Write the final validation brief
# ============================================================
# PURPOSE:
#   This tool synthesises all previous tool outputs into a single
#   structured markdown brief with a clear verdict. It is always
#   the LAST tool in the pipeline because it needs the outputs of
#   market_research and feasibility to produce a complete brief.
#
# SYNTHESIS PATTERN:
#   brief_writer is always last because it is the "synthesiser" —
#   it combines research + scores into a final deliverable. This
#   pattern applies to ANY autonomous agent: the last tool always
#   produces the user-facing output using everything gathered before.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Change brief_writer.py to output a StudAI Foundry CP1
#    submission draft instead of a validation brief. Include
#    sections for: Problem Statement, Proposed Solution, Target
#    Users, Tech Stack, and 10-Day Build Plan."
# ============================================================

def run(idea, market_research, feasibility, client, model):
    """Synthesise all tool outputs into a structured validation brief."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────────
    prompt = f"""You are a startup advisor writing a validation brief.

Using the research and scoring below, write a structured startup validation brief.

STARTUP IDEA: {idea}

MARKET RESEARCH:
{market_research}

FEASIBILITY SCORES:
{feasibility}

Write the brief using these EXACT sections and markdown headers:

## Startup Validation Brief

### The Idea
(One sentence summary)

### Target Customer
(Who exactly will use and pay for this)

### Problem Being Solved
(The specific pain point, not a generic statement)

### Market Opportunity
(Size, growth, timing — use specific numbers from the research)

### Feasibility Summary
(Summarise the 5 scores and what they mean together)

### Key Risks
(2-3 SPECIFIC risks — not generic ones like "competition exists")

### Recommended Next Steps
(3 concrete actions the founder should take THIS WEEK)

### Verdict
State one of: **STRONG IDEA** / **NEEDS REFINEMENT** / **PIVOT RECOMMENDED**
Follow with one sentence explaining why.

Keep it under 400 words. Be direct and honest — students need real feedback, not cheerleading."""

    # ── CALL THE LLM ─────────────────────────────────────────────────
    # Why temperature 0.4: briefs need some stylistic flexibility
    # but must stay grounded in the data from previous tools
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=600,
    )

    return response.choices[0].message.content
