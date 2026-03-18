# ============================================================
# reviewer.py — Scores CP1 draft against the 6-field rubric
# ============================================================
# PURPOSE:
#   The reviewer is what makes this an AUTONOMOUS agent instead of
#   a chatbot. It scores the CP1 draft against the actual 6-field
#   form requirements and decides pass or retry.
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


def evaluate(idea, results, client, model):
    """Score the CP1 draft against the 6-field rubric."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────
    prompt = f"""You are a quality reviewer for a CP1 submission drafting agent at StudAI Foundry.

The CP1 form has exactly 6 fields. Review the draft below and check each field.

ORIGINAL IDEA: {idea}

CP1 DRAFT:
{results.get("submission_writer", "No draft generated")}

CHECK EACH OF THESE 6 FIELDS:

1. Problem Statement (min 50 chars): Is it specific? Does it describe a real pain point, not a generic statement? Would a judge understand exactly what problem is being solved?

2. Target Users (min 10 chars): Is the user segment specific (not "everyone" or "students")? Are demographics/context included?

3. Autonomy Loop Plan (min 50 chars): Does it map all 5 steps (THINK, PLAN, EXECUTE, REVIEW, UPDATE) to THIS specific product? Is it clear why this is autonomous and not a chatbot?

4. Tools & APIs: Are they listed comma-separated? Are they realistic for a student team? Do they include an LLM provider?

5. Evaluation Logic (min 20 chars): Does it explain HOW the agent measures success? Are there specific metrics or criteria?

6. Expected Output (min 20 chars): Does it describe a concrete deliverable the user receives? Can you picture exactly what the output looks like?

SCORING:
  9-10: All 6 fields present, specific, meets min lengths, autonomy clearly mapped, copy-paste ready
  7-8:  All fields present, mostly specific, minor gaps in one or two fields
  5-6:  Some fields generic or too short, autonomy explanation vague
  1-4:  Missing fields, too short to meet minimums, or generic filler

Return ONLY valid JSON — no markdown, no explanation, no extra text.
Use this exact format:
{{"score": 8, "passed": true, "what_is_good": "which fields are strong", "feedback": "which specific fields need improvement and how"}}"""

    # ── CALL THE LLM ─────────────────────────────────────────────
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=250,
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
    review["passed"] = review.get("score", 0) >= PASS_THRESHOLD

    return review
