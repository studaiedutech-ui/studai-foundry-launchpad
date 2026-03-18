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
    layout="centered",
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
# Why this matters: students need to see the difference between a
# chatbot and an autonomous agent BEFORE they click Run.
with st.expander("🤖 What makes this AUTONOMOUS (not a chatbot)?", expanded=False):
    st.markdown("""
**A chatbot** takes your input → calls an LLM once → returns whatever it gets. One shot. Done. No quality check.

**An autonomous agent** takes your *goal* and then:

| Step | What the Agent Does | Why It Matters |
|------|-------------------|---------------|
| **THINK** | Parses the goal + any feedback from previous attempts | Context awareness — like re-reading a brief before starting |
| **PLAN** | Asks the LLM to create a JSON action plan | Self-directed — it decides *what* to do, not you |
| **EXECUTE** | Runs each tool in sequence (define → architect → write) | Tool use — each tool does one job, outputs chain together |
| **REVIEW** | Scores its own output 1-10 against CP1 criteria | **Self-evaluation — THIS is what makes it autonomous** |
| **UPDATE** | If score < 7, carries feedback into the next loop | Self-correction — it learns from its own mistakes |

The loop runs up to **3 times**. Each retry uses specific feedback to improve. This is the exact same architecture used in production AI agents — the domain changes, the loop doesn't.

> **The one rule: THE LOOP NEVER CHANGES. THE TOOLS DO.**
>
> To build a different agent (customer support, invoice processor, sales qualifier), you keep the loop and change only the tools.
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
    - `reviewer.py` — Scores output against CP1 rubric
    - `tools/` — The domain-specific work (THESE change)

    **The 3 tools in this agent:**
    1. `problem_definer` — Extracts the core problem
    2. `solution_architect` — Designs the solution + build plan
    3. `submission_writer` — Writes the CP1 draft

    **Why this is autonomous:**
    The **reviewer** scores the draft against actual CP1 criteria. If it's not good enough, it tells the agent *what* to improve — and the agent tries again.
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
# Why this exists: in a live workshop with 200+ students, many freeze
# on "what do I type." A one-click example removes that friction and
# lets everyone see the loop running within 10 seconds.
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

# Why we use session_state: Streamlit reruns the entire script on
# every interaction — session_state persists the example across reruns
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
    elif "PASSED" in message or ("passed" in message.lower() and "success" in message.lower()):
        return f'{time_span} <span class="log-pass">{message}</span>'
    elif "FAILED" in message or "failed" in message.lower():
        return f'{time_span} <span class="log-fail">{message}</span>'
    else:
        return f"{time_span} {message}"


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
        st.error("⚠️ **No idea entered.** Describe your hackathon idea above, or click **💡 Try Example** for a demo.")
        st.stop()

    # ── INITIALISE STATE ─────────────────────────────────────────
    client = Groq(api_key=api_key)
    statuses = {key: "pending" for key in STEP_KEYS}
    log_lines = []
    current_loop = [1]

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
                st.error(f"🧠 **Model error.** The selected model may be unavailable.\n\nTry a different model from the sidebar.\n\nDetails: `{error_msg}`")
            else:
                st.error(f"❌ **Agent error:** `{error_msg}`\n\nCheck your API key and internet connection.")
            st.stop()

    # ── DISPLAY RESULTS ──────────────────────────────────────────
    st.divider()

    st.markdown("## 📋 Your CP1 Submission Draft")

    if results.get("submission_writer"):
        st.markdown(results["submission_writer"])

        # ── DOWNLOAD BUTTON ──────────────────────────────────────
        st.download_button(
            label="📥 Download CP1 Draft as Markdown",
            data=results["submission_writer"],
            file_name="studai-foundry-cp1-draft.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.warning("No draft was generated. Check the activity log above for errors.")

    with st.expander("🔍 Raw tool outputs (for learning)"):
        st.markdown("**Why look at these?** Each tool produces one piece of the submission. "
                     "The submission_writer *synthesises* them all. Understanding this chain is "
                     "key to building your own autonomous agent.")
        st.markdown("---")
        st.markdown("### Tool 1: Problem Definition")
        st.markdown(results.get("problem_definer", "*Not generated*"))
        st.markdown("---")
        st.markdown("### Tool 2: Solution Architecture")
        st.markdown(results.get("solution_architect", "*Not generated*"))

    # ── POST-RUN EDUCATION ───────────────────────────────────────
    with st.expander("🎓 What just happened? (The autonomy explained)"):
        loops_used = current_loop[0]
        st.markdown(f"""
**The agent ran {loops_used} loop{'s' if loops_used > 1 else ''}** to draft your CP1 submission. Here's what happened at each step:

1. **THINK** — The agent parsed your idea as its goal. On retries, it also incorporated specific feedback from the reviewer about what to improve.

2. **PLAN** — The agent asked the LLM to create a JSON execution plan: *which tools to run and in what order*. The agent decided its own workflow — you didn't tell it what to do step by step.

3. **EXECUTE** — The agent ran 3 tools in sequence. Each tool's output became input for the next one (this is called *information chaining*):
   - **Problem Definer** → extracted target users, pain point, urgency, alternatives
   - **Solution Architect** → used that analysis to design the solution, tech stack, and build plan
   - **Submission Writer** → synthesised everything into a formatted CP1 draft

4. **REVIEW** — **This is the key step.** The agent scored its OWN draft against StudAI Foundry's CP1 criteria. If the score was below 7, it decided the draft wasn't submission-ready. A chatbot would have just returned it. An autonomous agent judges itself.

5. **UPDATE** — If the review failed, the agent extracted specific feedback ("autonomy section is too vague", "build plan is unrealistic") and carried it into the next loop to improve.

**This is the difference between a chatbot and an autonomous agent:**
A chatbot gives you one draft. An agent gives you its *best* draft — and keeps improving until it meets the quality bar.

**Next step:** Copy this draft, refine it with your team, and submit before the CP1 deadline!
        """)
