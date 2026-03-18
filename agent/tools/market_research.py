# ============================================================
# market_research.py — Tool 1: Research customers and market size
# ============================================================
# PURPOSE:
#   This tool calls the LLM to analyse a startup idea and produce
#   a focused market research summary: who the customers are, how
#   big the market is, what problem is being solved, and what
#   alternatives exist today.
#
# SINGLE RESPONSIBILITY:
#   Each tool in agent/tools/ does exactly ONE job. market_research
#   only researches the market — it does not score or write briefs.
#   This makes it easy to swap, extend, or replace without touching
#   any other file.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Change market_research.py to research [your domain] instead
#    of startup ideas. Keep the function signature run(idea,
#    client, model) -> str exactly the same."
# ============================================================

def run(idea, client, model):
    """Call the LLM to produce a market research summary for the given idea."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────────
    prompt = f"""You are a startup market research analyst.

Analyse this startup idea and provide a focused market research summary:

STARTUP IDEA: {idea}

Cover these 4 areas (be specific, not generic):
1. **Target Customer Segment** — Who exactly will pay for this? Be specific about demographics, geography, and behaviour.
2. **Market Size Estimate** — How big is this market? Focus on India where relevant. Use real numbers if possible.
3. **Core Problem** — What specific pain point does this solve? One sentence.
4. **Current Alternatives** — What do customers use today to solve this problem? Name real products or workarounds.

Keep it under 200 words. Be specific and actionable — avoid generic statements like "large addressable market" without numbers."""

    # ── CALL THE LLM ─────────────────────────────────────────────────
    # Why temperature 0.4: we want some creativity for market insights
    # but not so much that it hallucinates market data
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=300,
    )

    return response.choices[0].message.content
