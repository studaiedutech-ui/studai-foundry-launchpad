# ============================================================
# reviewer.py — Scores CP1 draft with FIELD-LEVEL breakdown
# ============================================================
# PURPOSE:
#   The reviewer is what makes this an AUTONOMOUS agent instead of
#   a chatbot. It scores the CP1 draft against the actual 6-field
#   form requirements and decides pass or retry.
#
#   UPGRADE: Now returns per-field scores so the UI can show
#   exactly which fields passed and which need improvement.
#
# CP1 FORM FIELDS IT CHECKS:
#   Field 1: Problem Statement   (min 50 chars, specific pain point)
#   Field 2: Target Users        (min 10 chars, specific segment)
#   Field 3: Autonomy Loop Plan  (min 50 chars, maps THINK/PLAN/EXECUTE/REVIEW/UPDATE)
#   Field 4: Tools & APIs        (comma-separated, realistic stack)
#   Field 5: Evaluation Logic    (min 20 chars, measurable criteria)
#   Field 6: Expected Output     (min 20 chars, concrete deliverable)
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Make the reviewer stricter — require score 9 to pass instead
#    of 7. Check that the Autonomy Loop Plan mentions all 5 steps
#    explicitly (THINK, PLAN, EXECUTE, REVIEW, UPDATE)."
# ============================================================

import json

# ── PASS THRESHOLD ───────────────────────────────────────────────
# Score 7+ = pass. Below 7 = the agent retries with feedback.
PASS_THRESHOLD = 7

# ── FIELD DEFINITIONS ────────────────────────────────────────────
FIELDS = [
    {"id": 1, "name": "Problem Statement", "min_chars": 50},
    {"id": 2, "name": "Target Users", "min_chars": 10},
    {"id": 3, "name": "Autonomy Loop Plan", "min_chars": 50},
    {"id": 4, "name": "Tools & APIs", "min_chars": 1},
    {"id": 5, "name": "Evaluation Logic", "min_chars": 20},
    {"id": 6, "name": "Expected Output", "min_chars": 20},
]


def evaluate(idea, results, client, model):
    """Score the CP1 draft with per-field breakdown."""

    draft = results.get("submission_writer", "No draft generated")
    challenger = results.get("idea_challenger", "No critique generated")

    # ── BUILD THE PROMPT ─────────────────────────────────────────
    prompt = f"""You are a quality reviewer for a CP1 submission drafting agent at StudAI Foundry.

The CP1 form has exactly 6 fields. Review the draft below and score EACH field individually.

ORIGINAL IDEA: {idea}

CP1 DRAFT:
{draft}

DEVIL'S ADVOCATE CRITIQUE (check if it was addressed):
{challenger}

SCORE EACH FIELD on a 1-10 scale:

Field 1 — Problem Statement (min 50 chars):
  Is it specific? Does it describe a real pain point? Would a judge understand exactly what problem is being solved?

Field 2 — Target Users (min 10 chars):
  Is the user segment specific (not "everyone")? Are demographics/context included?

Field 3 — Autonomy Loop Plan (min 50 chars):
  Does it map all 5 steps (THINK, PLAN, EXECUTE, REVIEW, UPDATE) to THIS product? Is it clear why this is autonomous?

Field 4 — Tools & APIs:
  Are they listed comma-separated? Realistic for a student team? Include an LLM provider?

Field 5 — Evaluation Logic (min 20 chars):
  Does it explain HOW the agent measures success? Specific metrics?

Field 6 — Expected Output (min 20 chars):
  Concrete deliverable? Can you picture what the user receives?

Also check: Did the draft ADDRESS the devil's advocate critique? Or did it ignore the weaknesses?

Return ONLY valid JSON — no markdown, no explanation, no extra text.
Use this exact format:
{{"overall_score": 8, "passed": true, "fields": [{{"field": 1, "name": "Problem Statement", "score": 8, "status": "pass", "note": "specific and clear"}}, {{"field": 2, "name": "Target Users", "score": 7, "status": "pass", "note": "good segment"}}, {{"field": 3, "name": "Autonomy Loop Plan", "score": 6, "status": "needs_work", "note": "missing REVIEW step"}}, {{"field": 4, "name": "Tools & APIs", "score": 9, "status": "pass", "note": "realistic stack"}}, {{"field": 5, "name": "Evaluation Logic", "score": 7, "status": "pass", "note": "measurable"}}, {{"field": 6, "name": "Expected Output", "score": 8, "status": "pass", "note": "concrete"}}], "critique_addressed": true, "what_is_good": "strengths summary", "feedback": "specific improvements needed"}}

RULES for field status:
- score >= 7 → "pass"
- score 5-6 → "needs_work"
- score < 5 → "fail"
overall_score = average of all 6 field scores (rounded to nearest integer)"""

    # ── CALL THE LLM ─────────────────────────────────────────────
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500,
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
    score = review.get("overall_score", review.get("score", 0))
    review["score"] = score
    review["passed"] = score >= PASS_THRESHOLD

    return review
