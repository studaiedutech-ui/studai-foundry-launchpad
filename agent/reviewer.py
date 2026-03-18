# ============================================================
# reviewer.py — Scores output and decides pass or retry
# ============================================================
# PURPOSE:
#   The reviewer is what makes this an AUTONOMOUS agent instead of
#   a chatbot. A chatbot returns whatever the LLM generates. An
#   autonomous agent JUDGES its own output, scores it, and decides
#   whether it's good enough — or whether to try again with
#   specific feedback about what to improve.
#
# WHY THIS MATTERS:
#   Without a reviewer, the agent is just a pipeline. With a
#   reviewer, the agent has a quality gate — it can self-correct.
#   This is the core concept students learn in the workshop:
#   autonomy = planning + execution + SELF-EVALUATION.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Make the reviewer stricter — require score 9 to pass instead
#    of 7. Update the scoring criteria to emphasise specificity
#    and actionable recommendations."
# ============================================================

import json

# ── PASS THRESHOLD ───────────────────────────────────────────────
# Why this is a named constant: students can change this one number
# to make the agent stricter (higher) or more lenient (lower).
# Score 7+ = pass. Below 7 = the agent retries with feedback.
PASS_THRESHOLD = 7


def evaluate(idea, results, client, model):
    """Score the agent's output and decide whether to pass or retry."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────────
    prompt = f"""You are a quality reviewer for a startup validation agent.

Review the output below and score it on a scale of 1-10.

ORIGINAL IDEA: {idea}

GENERATED BRIEF:
{results.get("brief_writer", "No brief generated")}

FEASIBILITY SCORES:
{results.get("feasibility", "No feasibility scores generated")}

SCORING CRITERIA:
  9-10: Specific, actionable, includes concrete market data, clear verdict with reasoning
  7-8:  Good coverage of all sections, minor gaps in specificity
  5-6:  Generic analysis that could apply to almost any startup
  1-4:  Missing sections, too short, or factually unsupported claims

Return ONLY valid JSON — no markdown, no explanation, no extra text.
Use this exact format:
{{"score": 8, "passed": true, "what_is_good": "brief summary of strengths", "feedback": "specific improvements needed"}}"""

    # ── CALL THE LLM ─────────────────────────────────────────────────
    # Why temperature 0.2: review scoring must be consistent and
    # analytical — we don't want creative interpretation of quality
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200,
    )

    raw = response.choices[0].message.content

    # ── PARSE THE JSON ───────────────────────────────────────────────
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()

    review = json.loads(raw)

    # ── ENFORCE THRESHOLD ────────────────────────────────────────────
    # Why we override the LLM's "passed" field: the LLM might say
    # passed=true for a score of 6. We enforce our own threshold
    # so the agent's quality gate is deterministic, not probabilistic.
    review["passed"] = review.get("score", 0) >= PASS_THRESHOLD

    return review
