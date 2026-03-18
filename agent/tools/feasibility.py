# ============================================================
# feasibility.py — Tool 2: Score the idea on 5 dimensions
# ============================================================
# PURPOSE:
#   This tool scores a startup idea across 5 feasibility dimensions
#   (technical, market, revenue, competition, founder fit) and returns
#   a structured text block with scores and reasons.
#
# INFORMATION CHAINING:
#   feasibility takes market_research as input because it needs the
#   customer and market context discovered by Tool 1. This is how
#   autonomous agents chain information — each tool builds on the
#   output of previous tools, creating deeper analysis than any
#   single LLM call could produce.
#
# SINGLE RESPONSIBILITY:
#   This tool ONLY scores — it does not research or write briefs.
#   Each tool does ONE job so students can swap or extend tools
#   independently.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Change the 5 scoring dimensions in feasibility.py to evaluate
#    [your domain] instead of startups. For example, for a customer
#    support agent, score on: response accuracy, tone, resolution
#    speed, escalation need, customer satisfaction."
# ============================================================

def run(idea, market_research, client, model):
    """Score the startup idea on 5 feasibility dimensions using LLM analysis."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────────
    prompt = f"""You are a startup feasibility analyst.

Score this startup idea on 5 dimensions. Use the market research context to make your scores specific and grounded.

STARTUP IDEA: {idea}

MARKET RESEARCH CONTEXT:
{market_research}

Score each dimension from 1-10 with a one-sentence reason. Use this exact format:

[Score/10] Technical Feasibility: Can a small team build this with current AI/tech tools?
[Score/10] Market Demand: Is there real urgency and willingness to pay?
[Score/10] Revenue Potential: Can it make money within 12 months?
[Score/10] Competition Gap: Is there a real gap vs existing solutions?
[Score/10] Founder Fit: Can a student or early-stage team execute this?

End with:
OVERALL SCORE: X/10

Be honest and direct. A score of 7+ means genuinely strong. Do not inflate scores."""

    # ── CALL THE LLM ─────────────────────────────────────────────────
    # Why temperature 0.3: scoring needs consistency — we want the model
    # to be analytical, not creative, when assigning numbers
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=350,
    )

    return response.choices[0].message.content
