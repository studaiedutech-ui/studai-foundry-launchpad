# ============================================================
# submission_writer.py — Tool 3: Generate Evaluation Logic + Expected Output
#                        and compile all 6 CP1 fields
# ============================================================
# PURPOSE:
#   This tool synthesises the outputs from Tool 1 and Tool 2 and
#   generates the remaining two CP1 form fields:
#     Field 5: Evaluation Logic (textarea, min 20 chars)
#     Field 6: Expected Output (textarea, min 20 chars)
#
#   It then compiles ALL 6 fields into a formatted, copy-paste-ready
#   CP1 submission draft. Each field is clearly labelled so students
#   can paste directly into the StudAI Foundry submission form.
#
# WHY THIS IS ALWAYS THE LAST TOOL (synthesis pattern):
#   The submission writer needs ALL previous outputs to produce the
#   final two fields and compile the complete draft. Evaluation logic
#   can't be written without knowing the autonomy loop plan. Expected
#   output can't be defined without knowing the problem and solution.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Change submission_writer.py to output a CP2 demo script
#    instead of a CP1 draft. Include sections for: Demo Flow,
#    Talking Points, Live Demo Checklist, and Backup Plan."
# ============================================================


def run(idea, problem_analysis, solution_architecture, client, model):
    """Generate Evaluation Logic, Expected Output, and compile all 6 CP1 fields."""

    # ── BUILD THE PROMPT ─────────────────────────────────────────
    prompt = f"""You are helping a student team complete their CP1 (Checkpoint 1) submission for StudAI Foundry — India's national autonomous AI hackathon.

Previous tools have already generated Fields 1-4. Now generate Fields 5-6 and compile ALL fields into the final submission.

PROJECT IDEA: {idea}

FIELDS 1-2 (from problem_definer):
{problem_analysis}

FIELDS 3-4 (from solution_architect):
{solution_architecture}

YOUR TASK — Generate Fields 5-6 and compile the complete submission:

Write the output using these EXACT headers. Each field must be clearly separated so students can copy-paste into the form.

---

## CP1 SUBMISSION — COPY-PASTE READY

### FIELD 1 — Problem Statement
(Extract and clean up the problem statement from the analysis above. Must be at least 50 characters. 3-5 clear sentences answering: "What problem does your AI agent solve?")

### FIELD 2 — Target Users
(Extract and clean up the target users from the analysis above. Must be at least 10 characters. One specific sentence answering: "Who will use this?")

### FIELD 3 — Autonomy Loop Plan
(Extract and clean up the autonomy loop plan from the analysis above. Must be at least 50 characters. Describes how the AI agent operates autonomously through THINK → PLAN → EXECUTE → REVIEW → UPDATE.)

### FIELD 4 — Tools & APIs
(Extract the tools list from the analysis above. Comma-separated. Example format: "Groq API, Streamlit, Python, python-dotenv")

### FIELD 5 — Evaluation Logic
(NEW — generate this now. How will you measure if the agent's output is successful? What metrics or criteria does the REVIEW step check? Be specific to THIS product. Must be at least 20 characters. 2-3 sentences. Example: "The agent scores its output on 3 criteria: accuracy of syllabus coverage (>80%), difficulty progression alignment, and time feasibility for the student's schedule. A combined score of 7/10 or higher passes quality review.")

### FIELD 6 — Expected Output
(NEW — generate this now. What does a successful output from this agent look like? Describe the concrete deliverable the user receives. Must be at least 20 characters. 2-3 sentences. Example: "A personalised 7-day study plan with daily 15-minute micro-lessons, 3 practice questions per topic, and priority ranking of weak areas — delivered as a formatted message via WhatsApp.")

---

IMPORTANT RULES:
- Each field must meet its minimum character length
- Fields must be directly copy-pasteable into the StudAI Foundry submission form
- Be specific to THIS project — no generic statements
- Every sentence must carry weight — judges read 100+ submissions
- Keep the total under 500 words"""

    # ── CALL THE LLM ─────────────────────────────────────────────
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=800,
    )

    return response.choices[0].message.content
