# ============================================================
# main.py — Streamlit UI for StudAI LaunchPad
# ============================================================
# PURPOSE:
#   This file is the user interface ONLY. It renders the Streamlit
#   web app with step cards, a log box, and the final CP1 draft.
#   All agent logic lives in agent/loop.py — this file just handles
#   display and user input.
#
# UI-ONLY RULE:
#   Do not put agent logic, LLM calls, or tool functions in this
#   file. main.py calls agent.loop.run() and displays the results.
#   That's it.
#
# HOW TO CUSTOMISE (vibe coding prompt):
#   "Change the UI title and branding in main.py to [your product
#    name]. Update the sidebar architecture section to match your
#    new tools. Keep the step card rendering and log box the same."
# ============================================================

import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from agent import loop

# ── LOAD ENVIRONMENT ─────────────────────────────────────────────
load_dotenv()

# ── PAGE CONFIG ──────────────────────────────────────────────────
st.set_page_config(
    page_title="StudAI LaunchPad — CP1 Submission Drafter",
    page_icon="🚀",
    layout="wide",
)

# ── CUSTOM CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    /* Step cards */
    .step-card {
        border-radius: 10px;
        padding: 16px 8px;
        text-align: center;
        margin: 4px;
        font-size: 14px;
        min-height: 110px;
        transition: all 0.3s ease;
    }
    .step-pending {
        background-color: #f0f0f0;
        border: 2px solid #cccccc;
        color: #888888;
    }
    .step-active {
        background-color: #fff8e1;
        border: 2px solid #ffc107;
        color: #f57f17;
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.3); }
        50% { box-shadow: 0 0 12px 4px rgba(255, 193, 7, 0.3); }
    }
    .step-done {
        background-color: #e8f5e9;
        border: 2px solid #4caf50;
        color: #1b5e20;
    }
    .step-failed {
        background-color: #ffebee;
        border: 2px solid #f44336;
        color: #b71c1c;
    }
    .step-skipped {
        background-color: #f3e5f5;
        border: 2px solid #9c27b0;
        color: #4a148c;
    }

    /* Activity log */
    .log-box {
        background-color: #1E1E2E;
        color: #cdd6f4;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        padding: 12px;
        border-radius: 8px;
        max-height: 220px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .log-time { color: #6c7086; }
    .log-tool { color: #89b4fa; }
    .log-pass { color: #a6e3a1; }
    .log-fail { color: #f38ba8; }
    .log-loop { color: #cba6f7; font-weight: bold; }

    /* Branding */
    .brand-title {
        text-align: center;
        font-size: 2.4em;
        font-weight: 800;
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .brand-sub {
        text-align: center;
        font-size: 1.05em;
        color: #64748b;
        margin-top: 2px;
        margin-bottom: 4px;
    }
    .brand-badge {
        text-align: center;
        margin-bottom: 16px;
    }
    .brand-badge span {
        background-color: #7c3aed;
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.78em;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Loop counter */
    .loop-counter {
        text-align: center;
        background-color: #1E1E2E;
        color: #cba6f7;
        padding: 8px 16px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 14px;
        margin: 8px 0;
    }

    /* Score card */
    .score-card {
        text-align: center;
        padding: 20px;
        border-radius: 12px;
        font-weight: bold;
    }
    .score-pass {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        border: 2px solid #4caf50;
        color: #1b5e20;
    }
    .score-fail {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border: 2px solid #f44336;
        color: #b71c1c;
    }

    /* Field validation badge */
    .field-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }
    .badge-pass {
        background-color: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #a5d6a7;
    }
    .badge-needs-work {
        background-color: #fff8e1;
        color: #f57f17;
        border: 1px solid #ffe082;
    }
    .badge-fail {
        background-color: #ffebee;
        color: #c62828;
        border: 1px solid #ef9a9a;
    }

    /* Tool pipeline */
    .pipeline-card {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER & BRANDING ───────────────────────────────────────────
st.markdown('<div class="brand-title">StudAI LaunchPad</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="brand-sub">CP1 Submission Drafter — Autonomous AI Agent</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="brand-badge"><span>STUDAI FOUNDRY — NATIONAL AUTONOMOUS AI HACKATHON</span></div>',
    unsafe_allow_html=True,
)

# ── AUTONOMY EXPLAINER ──────────────────────────────────────────
with st.expander("🤖 What makes this AUTONOMOUS (not a chatbot)?", expanded=False):
    st.markdown("""
**A chatbot** takes your input → calls an LLM once → returns whatever it gets. One shot. Done. No quality check.

**An autonomous agent** takes your *goal* and then:

| Step | What the Agent Does | Why It Matters |
|------|-------------------|---------------|
| **THINK** | Parses the goal + any feedback from previous attempts | Context awareness — like re-reading a brief before starting |
| **PLAN** | Asks the LLM to create a JSON action plan | Self-directed — it decides *what* to do, not you |
| **EXECUTE** | Runs each tool in sequence (define → architect → challenge → write) | Tool use — each tool does one job, outputs chain together |
| **REVIEW** | Scores its own output 1-10 against CP1 criteria | **Self-evaluation — THIS is what makes it autonomous** |
| **UPDATE** | If score < 7, carries feedback into the next loop | Self-correction — it learns from its own mistakes |

The loop runs up to **3 times**. Each retry uses specific feedback to improve. This is the exact same architecture used in production AI agents — the domain changes, the loop doesn't.

**4-Tool Pipeline:**
1. **Problem Definer** → Extracts Problem Statement + Target Users
2. **Solution Architect** → Designs Autonomy Loop Plan + Tools & APIs
3. **Idea Challenger** → Devil's advocate: finds weaknesses, blind spots, hard judge questions
4. **Submission Writer** → ADDRESSES the challenger's critique + compiles all 6 fields

> **The one rule: THE LOOP NEVER CHANGES. THE TOOLS DO.**
    """)

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Get your free key at console.groq.com",
    )
    st.markdown("[🔑 Get your free Groq API key](https://console.groq.com)")

    st.divider()

    st.markdown("### 🏗️ How Autonomy Works Here")
    st.markdown("""
    **The 5-step loop** (`agent/loop.py`):
    ```
    THINK → PLAN → EXECUTE → REVIEW → UPDATE
      ↑                                  |
      └──────── (if score < 7) ──────────┘
    ```

    **What each file does:**
    - `loop.py` — Runs the 5-step cycle (NEVER changes)
    - `planner.py` — LLM → JSON action plan
    - `executor.py` — Routes plan → tool functions
    - `reviewer.py` — Scores output per-field against CP1
    - `tools/` — The domain-specific work (THESE change)

    **The 4 tools in this agent:**
    1. `problem_definer` — Extracts the core problem
    2. `solution_architect` — Designs the solution
    3. `idea_challenger` — Devil's advocate critique
    4. `submission_writer` — Compiles the final draft

    **Why this is autonomous:**
    The **reviewer** scores each field individually. If the overall score < 7, it tells the agent *which fields* to improve — and the agent tries again.
    """)

    st.divider()

    model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768"],
        help="llama-3.3-70b is recommended for best results",
    )

    st.divider()
    st.caption("Built for [StudAI Foundry](https://studai.one) — the national autonomous AI hackathon by StudAI One × SRMIST × Startup Singam")

# ── MAIN AREA — INPUT ────────────────────────────────────────────
idea = st.text_area(
    "Describe your Foundry hackathon idea",
    placeholder="Example: An AI agent that helps small restaurant owners in India manage their daily inventory by scanning purchase bills via WhatsApp, predicting demand for the next 3 days, and auto-generating purchase orders for suppliers.",
    height=130,
)

# ── PRE-FILLED EXAMPLE BUTTON ───────────────────────────────────
col_run, col_example = st.columns([3, 1])
with col_run:
    run_button = st.button("🚀 Draft My CP1 Submission", use_container_width=True, type="primary")
with col_example:
    if st.button("💡 Try Example", use_container_width=True):
        st.session_state["example_idea"] = (
            "An AI tutor agent for engineering students in India that creates "
            "personalised study plans based on their semester syllabus, past "
            "exam papers, and weak topics — delivered via WhatsApp with daily "
            "15-minute micro-lessons and practice questions. The agent autonomously "
            "adjusts difficulty based on quiz performance."
        )
        st.rerun()

if "example_idea" in st.session_state:
    idea = st.session_state.pop("example_idea")
    st.text_area(
        "Describe your Foundry hackathon idea",
        value=idea,
        height=130,
        key="idea_filled",
        label_visibility="collapsed",
    )

st.divider()

# ── STEP DISPLAY CONTAINERS ─────────────────────────────────────
step_container = st.container()
loop_label = st.empty()
log_header = st.empty()
log_container = st.empty()

# ── STEP ICONS AND LABELS ───────────────────────────────────────
STEP_ICONS = {
    "pending": "○",
    "active": "⚙",
    "done": "✔",
    "failed": "✖",
    "skipped": "↩",
}

STEP_LABELS = ["THINK", "PLAN", "EXECUTE", "REVIEW", "UPDATE"]
STEP_KEYS = ["think", "plan", "execute", "review", "update"]

STEP_DESCRIPTIONS = {
    "think": "Parse goal",
    "plan": "Create plan",
    "execute": "Run tools",
    "review": "Score draft",
    "update": "Self-correct",
}


def render_steps(statuses, container):
    """Render the 5 step cards with current statuses."""
    with container:
        container.empty()
        cols = st.columns(5)
        for i, col in enumerate(cols):
            key = STEP_KEYS[i]
            status = statuses.get(key, "pending")
            icon = STEP_ICONS.get(status, "○")
            label = STEP_LABELS[i]
            desc = STEP_DESCRIPTIONS.get(key, "")
            col.markdown(
                f"""<div class="step-card step-{status}">
                    <div style="font-size: 24px;">{icon}</div>
                    <div style="font-weight: bold; margin-top: 4px;">{label}</div>
                    <div style="font-size: 11px; margin-top: 2px; opacity: 0.8;">{desc}</div>
                    <div style="font-size: 12px; margin-top: 4px;">{status.upper()}</div>
                </div>""",
                unsafe_allow_html=True,
            )


def format_log(message):
    """Add timestamp and color-code log lines for readability."""
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    time_span = f'<span class="log-time">[{ts}]</span>'

    if message.startswith("═══"):
        return f'{time_span} <span class="log-loop">{message}</span>'
    elif "Running tool:" in message:
        return f'{time_span} <span class="log-tool">{message}</span>'
    elif "PASSED" in message or (
        "passed" in message.lower() and "success" in message.lower()
    ):
        return f'{time_span} <span class="log-pass">{message}</span>'
    elif "FAILED" in message or "failed" in message.lower():
        return f'{time_span} <span class="log-fail">{message}</span>'
    else:
        return f"{time_span} {message}"


# ── HELPER: PARSE FIELDS FROM SUBMISSION ─────────────────────────
def parse_fields(submission_text):
    """Parse the 6 CP1 fields from the submission writer output."""
    fields = {}
    current_field = None
    current_content = []

    for line in submission_text.split("\n"):
        # Check for field headers
        for field_num in range(1, 7):
            if f"FIELD {field_num}" in line.upper():
                if current_field is not None:
                    fields[current_field] = "\n".join(current_content).strip()
                current_field = field_num
                current_content = []
                break
        else:
            if current_field is not None:
                current_content.append(line)

    # Capture the last field
    if current_field is not None:
        fields[current_field] = "\n".join(current_content).strip()

    return fields


# ── HELPER: RENDER SCORE DASHBOARD ───────────────────────────────
def render_score_dashboard(review):
    """Render the per-field score dashboard."""
    overall = review.get("score", review.get("overall_score", 0))
    passed = review.get("passed", False)

    # Overall score card
    score_class = "score-pass" if passed else "score-fail"
    score_emoji = "✅" if passed else "🔄"
    st.markdown(
        f"""<div class="score-card {score_class}">
            <div style="font-size: 36px;">{score_emoji}</div>
            <div style="font-size: 28px; margin-top: 4px;">{overall}/10</div>
            <div style="font-size: 14px; margin-top: 4px;">{"PASSED — Ready to submit" if passed else "NEEDS IMPROVEMENT — Agent will retry"}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    # Per-field breakdown
    field_scores = review.get("fields", [])
    if field_scores:
        st.markdown("#### Per-Field Scores")
        for field in field_scores:
            field_name = field.get("name", f"Field {field.get('field', '?')}")
            field_score = field.get("score", 0)
            status = field.get("status", "needs_work")
            note = field.get("note", "")

            # Badge color
            if status == "pass":
                badge_class = "badge-pass"
                badge_icon = "✅"
            elif status == "needs_work":
                badge_class = "badge-needs-work"
                badge_icon = "⚠️"
            else:
                badge_class = "badge-fail"
                badge_icon = "❌"

            # Progress bar color
            bar_color = "#4caf50" if field_score >= 7 else "#ffc107" if field_score >= 5 else "#f44336"

            st.markdown(
                f"""<div style="margin: 6px 0; padding: 8px 12px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid {bar_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span><strong>{badge_icon} {field_name}</strong>
                            <span class="field-badge {badge_class}">{field_score}/10</span>
                        </span>
                        <span style="font-size: 12px; color: #666;">{note}</span>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )

    # Strengths and feedback
    if review.get("what_is_good"):
        st.success(f"**Strengths:** {review['what_is_good']}")
    if review.get("feedback") and not passed:
        st.warning(f"**Feedback for retry:** {review['feedback']}")


# ── FIELD NAMES FOR DISPLAY ──────────────────────────────────────
FIELD_NAMES = {
    1: "Problem Statement",
    2: "Target Users",
    3: "Autonomy Loop Plan",
    4: "Tools & APIs",
    5: "Evaluation Logic",
    6: "Expected Output",
}

FIELD_TYPES = {
    1: "textarea",
    2: "input",
    3: "textarea",
    4: "input (comma-separated)",
    5: "textarea",
    6: "textarea",
}

FIELD_MIN_CHARS = {
    1: 50,
    2: 10,
    3: 50,
    4: 1,
    5: 20,
    6: 20,
}


# ── RUN THE AGENT ────────────────────────────────────────────────
if run_button:
    # ── VALIDATION ───────────────────────────────────────────────
    if not api_key or "your_groq" in api_key:
        st.error(
            "⚠️ **Groq API key missing.** Paste your key in the sidebar.\n\n"
            "Get one free (no credit card) → [console.groq.com](https://console.groq.com)"
        )
        st.stop()

    if not idea.strip():
        st.error(
            "⚠️ **No idea entered.** Describe your hackathon idea above, or click **💡 Try Example** for a demo."
        )
        st.stop()

    # ── INITIALISE STATE ─────────────────────────────────────────
    client = Groq(api_key=api_key)
    statuses = {key: "pending" for key in STEP_KEYS}
    log_lines = []
    current_loop = [1]
    review_data = [None]

    render_steps(statuses, step_container)
    log_header.markdown("### 📋 Activity Log")

    # ── CALLBACKS ────────────────────────────────────────────────
    def on_step(step, status):
        """Update a step card status and re-render all cards."""
        statuses[step] = status
        render_steps(statuses, step_container)

    def on_log(message):
        """Append a timestamped log line and re-render the log box."""
        if message.startswith("═══ Loop"):
            try:
                loop_num = int(message.split("Loop ")[1].split(" ")[0])
                current_loop[0] = loop_num
                max_loops = int(message.split("of ")[1].split(" ")[0])
                loop_label.markdown(
                    f'<div class="loop-counter">AUTONOMOUS LOOP: {loop_num} of {max_loops}</div>',
                    unsafe_allow_html=True,
                )
            except (ValueError, IndexError):
                pass

        log_lines.append(format_log(message))
        visible = log_lines[-12:]
        log_html = "\n".join(visible)
        log_container.markdown(
            f'<div class="log-box">{log_html}</div>',
            unsafe_allow_html=True,
        )

    # ── RUN THE LOOP ─────────────────────────────────────────────
    with st.spinner("🤖 Agent is drafting your CP1 submission autonomously — watch the steps light up..."):
        try:
            results = loop.run(idea, client, model, on_step, on_log)
        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "auth" in error_msg.lower():
                st.error(
                    "🔑 **API key error.** Your Groq key may be invalid or expired.\n\n"
                    "Get a new one → [console.groq.com](https://console.groq.com)"
                )
            elif "rate_limit" in error_msg.lower() or "429" in error_msg:
                st.error(
                    "⏳ **Rate limited by Groq.** You've hit the free tier limit.\n\n"
                    "Wait 60 seconds and try again, or switch to a smaller model in the sidebar."
                )
            elif "model" in error_msg.lower():
                st.error(
                    f"🧠 **Model error.** The selected model may be unavailable.\n\n"
                    f"Try a different model from the sidebar.\n\nDetails: `{error_msg}`"
                )
            else:
                st.error(
                    f"❌ **Agent error:** `{error_msg}`\n\nCheck your API key and internet connection."
                )
            st.stop()

    # ── DISPLAY RESULTS ──────────────────────────────────────────
    st.divider()

    st.markdown("## 📋 Your CP1 Submission — Copy-Paste Ready")
    st.markdown(
        "Each field below maps to the StudAI Foundry CP1 form. "
        "Copy each field directly into the submission form."
    )

    if results.get("submission_writer"):
        submission = results["submission_writer"]
        parsed_fields = parse_fields(submission)

        # ── TABBED VIEW ──────────────────────────────────────────
        tab_fields, tab_full, tab_reasoning, tab_raw = st.tabs(
            ["📝 Per-Field View", "📄 Full Draft", "🧠 Agent Reasoning", "🔍 Raw Outputs"]
        )

        # ── TAB 1: PER-FIELD COPY BOXES ──────────────────────────
        with tab_fields:
            st.markdown("**Copy each field into the CP1 submission form:**")

            for field_num in range(1, 7):
                field_name = FIELD_NAMES[field_num]
                field_type = FIELD_TYPES[field_num]
                min_chars = FIELD_MIN_CHARS[field_num]
                content = parsed_fields.get(field_num, "")

                # Validation
                char_count = len(content)
                meets_min = char_count >= min_chars

                if meets_min:
                    badge_html = f'<span class="field-badge badge-pass">✅ {char_count} chars</span>'
                else:
                    badge_html = f'<span class="field-badge badge-fail">❌ {char_count}/{min_chars} chars</span>'

                st.markdown(
                    f"**Field {field_num}: {field_name}** ({field_type}) {badge_html}",
                    unsafe_allow_html=True,
                )

                if field_type == "input" or field_type == "input (comma-separated)":
                    st.text_input(
                        f"Field {field_num}",
                        value=content,
                        key=f"field_{field_num}",
                        label_visibility="collapsed",
                    )
                else:
                    st.text_area(
                        f"Field {field_num}",
                        value=content,
                        height=100 if field_num != 3 else 150,
                        key=f"field_{field_num}",
                        label_visibility="collapsed",
                    )

            st.divider()

            # ── CP1 FORM FIELD REFERENCE ─────────────────────────
            st.markdown("### 📝 CP1 Form Fields Reference")
            st.markdown("""
| # | Field | Type | Min Length |
|---|-------|------|-----------|
| 1 | Problem Statement | Textarea | 50 chars |
| 2 | Target Users | Input | 10 chars |
| 3 | Autonomy Loop Plan | Textarea | 50 chars |
| 4 | Tools & APIs | Input (comma-separated) | 1 char |
| 5 | Evaluation Logic | Textarea | 20 chars |
| 6 | Expected Output | Textarea | 20 chars |
            """)

        # ── TAB 2: FULL DRAFT ────────────────────────────────────
        with tab_full:
            st.markdown(submission)
            st.divider()
            st.download_button(
                label="📥 Download CP1 Draft as Markdown",
                data=submission,
                file_name="studai-foundry-cp1-draft.md",
                mime="text/markdown",
                use_container_width=True,
            )

        # ── TAB 3: AGENT REASONING ───────────────────────────────
        with tab_reasoning:
            st.markdown("### 🧠 How the Agent Thought Through Your Idea")

            # Tool pipeline visualization
            st.markdown("**4-Tool Pipeline:**")
            p_cols = st.columns(4)
            pipeline_tools = [
                ("1️⃣", "Problem\nDefiner", "Fields 1-2"),
                ("2️⃣", "Solution\nArchitect", "Fields 3-4"),
                ("3️⃣", "Idea\nChallenger", "Devil's\nAdvocate"),
                ("4️⃣", "Submission\nWriter", "All 6 Fields"),
            ]
            for i, col in enumerate(p_cols):
                icon, name, output = pipeline_tools[i]
                col.markdown(
                    f"""<div class="pipeline-card">
                        <div style="font-size: 24px;">{icon}</div>
                        <div style="font-weight: bold; margin-top: 4px;">{name}</div>
                        <div style="font-size: 11px; color: #666; margin-top: 4px;">{output}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

            st.markdown("---")

            # Devil's Advocate output — the key differentiator
            if results.get("idea_challenger"):
                st.markdown("### 😈 Devil's Advocate Critique")
                st.markdown(
                    "The idea challenger found weaknesses BEFORE judges could. "
                    "The submission writer used this critique to STRENGTHEN the final draft."
                )
                st.info(results["idea_challenger"])

            st.markdown("---")

            # Loops used
            loops_used = current_loop[0]
            st.markdown(
                f"**Autonomous loops used:** {loops_used} of 3"
            )
            if loops_used == 1:
                st.success("Draft passed quality review on the first attempt!")
            else:
                st.info(
                    f"The agent self-corrected {loops_used - 1} time(s) based on reviewer feedback."
                )

        # ── TAB 4: RAW TOOL OUTPUTS ──────────────────────────────
        with tab_raw:
            st.markdown(
                "**Why look at these?** Each tool generates specific CP1 fields. "
                "The submission_writer compiles them all into the final draft. "
                "Understanding this chain is key to building your own autonomous agent."
            )
            st.markdown("---")

            st.markdown("### Tool 1: Problem Definer (Fields 1-2)")
            st.markdown(results.get("problem_definer", "*Not generated*"))
            st.markdown("---")

            st.markdown("### Tool 2: Solution Architect (Fields 3-4)")
            st.markdown(results.get("solution_architect", "*Not generated*"))
            st.markdown("---")

            st.markdown("### Tool 3: Idea Challenger (Devil's Advocate)")
            st.markdown(results.get("idea_challenger", "*Not generated*"))
            st.markdown("---")

            st.markdown("### Tool 4: Submission Writer (All 6 Fields)")
            st.markdown(results.get("submission_writer", "*Not generated*"))

    else:
        st.warning("No draft was generated. Check the activity log above for errors.")

    # ── POST-RUN EDUCATION ───────────────────────────────────────
    with st.expander("🎓 What just happened? (The autonomy explained)"):
        loops_used = current_loop[0]
        st.markdown(f"""
**The agent ran {loops_used} loop{'s' if loops_used > 1 else ''}** to draft your CP1 submission. Here's what happened:

1. **THINK** — The agent parsed your idea as its goal. On retries, it incorporated reviewer feedback about which CP1 fields needed improvement.

2. **PLAN** — The agent created a JSON plan: run problem_definer → solution_architect → idea_challenger → submission_writer. It decided this order itself.

3. **EXECUTE** — The agent ran **4 tools** in sequence. Each builds on the previous:
   - **Problem Definer** → Field 1 (Problem Statement) + Field 2 (Target Users)
   - **Solution Architect** → Field 3 (Autonomy Loop Plan) + Field 4 (Tools & APIs)
   - **Idea Challenger** → Devil's advocate: found weaknesses, blind spots, judge questions
   - **Submission Writer** → ADDRESSED the critique + compiled all 6 fields

4. **REVIEW** — The agent scored **each field individually** against the CP1 rubric. It checked: presence, minimum lengths, specificity, autonomy mapping, and whether the challenger's critique was addressed.

5. **UPDATE** — If overall score < 7, the agent carried field-specific feedback into the next loop.

**Next step:** Go to the "Per-Field View" tab, copy each field, paste into the StudAI Foundry submission form, refine with your team, and submit!
        """)
