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
# CP1 RUBRIC:
#   The reviewer scores against StudAI Foundry's actual CP1
#   criteria — not generic quality. This ensures the submission
#   draft meets the hackathon's specific requirements.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Make the reviewer stricter — require score 9 to pass instead
#    of 7. Update the scoring criteria to match CP2 requirements
#    (working demo, user testing results, iteration evidence)."
# ============================================================

import json

# ── PASS THRESHOLD ───────────────────────────────────────────────
# Why this is a named constant: students can change this one number
# to make the agent stricter (higher) or more lenient (lower).
# Score 7+ = pass. Below 7 = the agent retries with feedback.
PASS_THRESHOLD = 7


def evaluate(idea, results, client, model):
    """Score the agent's CP1 draft and decide whether to pass or retry."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────
    prompt = f"""You are a quality reviewer for a CP1 submission drafting agent at StudAI Foundry — India's national autonomous AI hackathon.

Review the CP1 submission draft below and score it on a scale of 1-10.

ORIGINAL IDEA: {idea}

CP1 SUBMISSION DRAFT:
{results.get("submission_writer", "No submission draft generated")}

SOLUTION ARCHITECTURE:
{results.get("solution_architect", "No solution architecture generated")}

SCORING CRITERIA — based on what Foundry judges look for in CP1:
  9-10: Specific problem with evidence, concrete solution with autonomy angle clearly explained,
        realistic tech stack, actionable 10-day build plan, compelling "why this will win" section
  7-8:  All required sections present, mostly specific but some gaps in detail or autonomy explanation
  5-6:  Generic problem/solution that could apply to any project, weak autonomy angle, vague build plan
  1-4:  Missing required sections, no autonomy explanation, unrealistic scope, or too short

KEY THINGS TO CHECK:
  - Is the problem statement SPECIFIC (not "students struggle with learning")?
  - Does the autonomy section explain THINK/PLAN/EXECUTE/REVIEW/UPDATE for THIS product?
  - Is the build plan realistic for students with 3-4 hours/day?
  - Would a judge understand exactly what this product does after reading?

Return ONLY valid JSON — no markdown, no explanation, no extra text.
Use this exact format:
{{"score": 8, "passed": true, "what_is_good": "brief summary of strengths", "feedback": "specific improvements needed"}}"""

    # ── CALL THE LLM ─────────────────────────────────────────────
    # Why temperature 0.2: review scoring must be consistent and
    # analytical — we don't want creative interpretation of quality
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200,
    )

    raw = response.choices[0].message.content

    # ── PARSE THE JSON ───────────────────────────────────────────
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()

    review = json.loads(raw)

    # ── ENFORCE THRESHOLD ────────────────────────────────────────
    # Why we override the LLM's "passed" field: the LLM might say
    # passed=true for a score of 6. We enforce our own threshold
    # so the agent's quality gate is deterministic, not probabilistic.
    review["passed"] = review.get("score", 0) >= PASS_THRESHOLD

    return review
