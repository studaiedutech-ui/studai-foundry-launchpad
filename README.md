# 🚀 StudAI LaunchPad — CP1 Submission Drafter

> **The official workshop product for [StudAI Foundry](https://studai.one) — India's national autonomous AI systems hackathon**
>
> Organised by **StudAI One × SRMIST × Startup Singam** | Prize pool: **INR 1,00,000+**

```
  ╔═══════════════════════════════════════════════════════════════════╗
  ║                                                                   ║
  ║      ███████╗████████╗██╗   ██╗██████╗  █████╗ ██╗               ║
  ║      ██╔════╝╚══██╔══╝██║   ██║██╔══██╗██╔══██╗██║               ║
  ║      ███████╗   ██║   ██║   ██║██║  ██║███████║██║               ║
  ║      ╚════██║   ██║   ██║   ██║██║  ██║██╔══██║██║               ║
  ║      ███████║   ██║   ╚██████╔╝██████╔╝██║  ██║██║               ║
  ║      ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝               ║
  ║                                                                   ║
  ║              L A U N C H P A D                                    ║
  ║       CP1 Submission Drafter — Autonomous AI Agent                ║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝
```

---

## 📋 Table of Contents

- [What Is This?](#-what-is-this)
- [Chatbot vs Autonomous Agent](#-chatbot-vs-autonomous-agent)
- [How the Autonomous Loop Works](#-how-the-autonomous-loop-works)
- [Project Architecture](#-project-architecture)
- [Installation Guide](#-installation-guide)
- [Running the App](#-running-the-app)
- [What You Will See](#-what-you-will-see)
- [Troubleshooting](#-troubleshooting)
- [How to Extend for Your Foundry Project](#-how-to-extend-for-your-foundry-project)
- [Tech Stack](#-tech-stack)
- [Hackathon Timeline](#-hackathon-timeline)
- [Deployment](#-deployment)

---

## 🧠 What Is This?

This is an **autonomous AI agent** that drafts your **CP1 (Checkpoint 1) submission** for the StudAI Foundry hackathon. You give it one input — your project idea. The agent does the rest:

1. **Defines** the core problem, target users, urgency, and current alternatives
2. **Architects** the solution with autonomy angle, tech stack, and 10-day build plan
3. **Writes** a formatted CP1 submission draft matching Foundry's criteria
4. **Reviews** its own draft against the CP1 rubric (scores it 1-10)
5. **Self-corrects** if the draft isn't submission-ready — and tries again

The final output is a downloadable **CP1 submission draft** you can refine with your team and submit before the March 23 deadline.

> **This was built for the StudAI LaunchPad workshop** — the official kickoff of StudAI Foundry, India's national autonomous AI hackathon. Students clone this repo, run it, watch the autonomous loop draft their CP1 live, then use AI coding tools (GitHub Copilot / Claude Code) to modify it for their own hackathon project.

---

## 🤖 Chatbot vs Autonomous Agent

This is the core concept taught in the workshop. Understanding this difference is **the entire point**.

```
  ╔══════════════════════════════════════════════════════════════════╗
  ║                         CHATBOT                                  ║
  ║                                                                  ║
  ║    User Input ──→ LLM Call ──→ Output ──→ Done.                  ║
  ║                                                                  ║
  ║    • One shot — whatever the LLM returns, you get                ║
  ║    • No quality check                                            ║
  ║    • No self-correction                                          ║
  ║    • The user must judge if the output is good                   ║
  ╚══════════════════════════════════════════════════════════════════╝

  ╔══════════════════════════════════════════════════════════════════╗
  ║                    AUTONOMOUS AGENT                              ║
  ║                                                                  ║
  ║    User gives a GOAL                                             ║
  ║      │                                                           ║
  ║      ▼                                                           ║
  ║    ┌──────────────────────────────────────────────┐              ║
  ║    │  THINK ──→ PLAN ──→ EXECUTE ──→ REVIEW       │              ║
  ║    │    ▲                              │           │              ║
  ║    │    │         ┌────────────────────┘           │              ║
  ║    │    │         ▼                                │              ║
  ║    │    │    Score < 7?                            │              ║
  ║    │    │     YES → UPDATE (carry feedback) ───┐   │              ║
  ║    │    │      NO → DELIVER result             │   │              ║
  ║    │    │                                      │   │              ║
  ║    │    └──────────────────────────────────────┘   │              ║
  ║    └──────────────────────────────────────────────┘              ║
  ║                                                                  ║
  ║    • Agent decides what to do (PLAN)                             ║
  ║    • Agent runs tools in sequence (EXECUTE)                      ║
  ║    • Agent judges its own output (REVIEW)   ← THIS IS KEY       ║
  ║    • Agent improves on retry (UPDATE)                            ║
  ║    • Up to 3 loops — no human in the loop                        ║
  ╚══════════════════════════════════════════════════════════════════╝
```

**The REVIEW step is what makes it autonomous.** A chatbot accepts any output. An autonomous agent evaluates its own work, decides if it's good enough, and self-corrects if it's not.

---

## 🔄 How the Autonomous Loop Works

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                  THE 5-STEP AUTONOMY LOOP                       │
  │                                                                 │
  │   ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌─────────┐      │
  │   │  THINK  │──→│  PLAN   │──→│ EXECUTE  │──→│ REVIEW  │      │
  │   │         │   │         │   │          │   │         │      │
  │   │ Parse   │   │ Create  │   │ Run 3    │   │ Score   │      │
  │   │ goal +  │   │ JSON    │   │ tools in │   │ output  │      │
  │   │ feedback│   │ action  │   │ sequence │   │ 1-10    │      │
  │   └─────────┘   │ plan    │   └──────────┘   └────┬────┘      │
  │       ▲         └─────────┘                       │            │
  │       │                                           ▼            │
  │       │                                    ┌────────────┐      │
  │       │                                    │ Score >= 7? │      │
  │       │                                    └──────┬─────┘      │
  │       │                                    YES│   │NO          │
  │       │                                       │   ▼            │
  │       │                                       │ ┌────────┐    │
  │       │                                       │ │ UPDATE │    │
  │       │                                       │ │ Carry  │    │
  │       │                                       │ │feedback│    │
  │       │                                       │ └───┬────┘    │
  │       │                                       │     │          │
  │       └───────────────────────────────────────┼─────┘          │
  │                                               │                │
  │                                               ▼                │
  │                                        ┌────────────┐          │
  │                                        │  DELIVER   │          │
  │                                        │  Results   │          │
  │                                        └────────────┘          │
  └─────────────────────────────────────────────────────────────────┘
                        Max 3 loops
```

### What each step does:

| Step | What Happens | Why It Matters |
|------|-------------|---------------|
| **THINK** | Parses the startup idea + any feedback from previous loops | The agent builds context before acting — just like re-reading a brief before starting work |
| **PLAN** | LLM generates a JSON action plan: `[{step, tool, reason}]` | The agent decides **what** to do — you don't tell it step by step. That's self-direction. |
| **EXECUTE** | Runs 3 tools in sequence: problem definer → solution architect → submission writer | Each tool's output feeds into the next one. This is **information chaining**. |
| **REVIEW** | Scores the output 1-10 against quality criteria | **This is autonomy.** The agent judges its own work. A chatbot skips this entirely. |
| **UPDATE** | Carries specific feedback into the next loop | Not blind retry — **directed self-correction** with concrete improvements. |

---

## 🏗️ Project Architecture

### File Structure

```
  studai-foundry-launchpad/
  │
  ├── 📄 CLAUDE.md              ← Project brain for AI coding tools (Copilot/Claude)
  ├── 📄 README.md              ← You are here
  ├── 📄 requirements.txt       ← 3 dependencies: groq, streamlit, python-dotenv
  ├── 📄 .env.example           ← API key template (copy to .env)
  ├── 📄 .gitignore             ← Excludes .env, __pycache__, secrets
  │
  ├── 🖥️ main.py               ← Streamlit UI — display only, no agent logic
  │
  └── 🤖 agent/                 ← THE AUTONOMOUS AGENT
      ├── __init__.py
      ├── 🔄 loop.py            ← THE CORE — the 5-step autonomy loop
      ├── 📋 planner.py         ← LLM → JSON action plan
      ├── ⚡ executor.py         ← Routes plan steps → tool functions
      ├── ✅ reviewer.py         ← Scores output, decides pass/retry
      │
      └── 🔧 tools/             ← DOMAIN-SPECIFIC TOOLS (these change)
          ├── __init__.py
          ├── problem_definer.py   ← Tool 1: users, pain point, urgency
          ├── solution_architect.py← Tool 2: solution, tech stack, build plan
          └── submission_writer.py ← Tool 3: formatted CP1 draft
```

### How Data Flows Through the System

```
  ┌──────────────┐
  │   User       │
  │   enters     │
  │   hackathon  │
  │   idea       │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐         ┌──────────────────────────────────┐
  │   main.py    │────────→│         agent/loop.py            │
  │   (UI only)  │         │    The 5-step autonomy loop      │
  │              │◀────────│    Returns final results dict    │
  └──────────────┘         └───────────────┬──────────────────┘
                                           │
                           ┌───────────────┼───────────────┐
                           ▼               ▼               ▼
                    ┌────────────┐  ┌────────────┐  ┌────────────┐
                    │ planner.py │  │executor.py │  │reviewer.py │
                    │            │  │            │  │            │
                    │ LLM → JSON │  │ Plan → Run │  │ Score 1-10 │
                    │ action plan│  │ each tool  │  │ Pass/Fail  │
                    └────────────┘  └──────┬─────┘  └────────────┘
                                           │
                           ┌───────────────┼───────────────┐
                           ▼               ▼               ▼
                    ┌────────────┐  ┌────────────┐  ┌────────────┐
                    │  Tool 1    │  │  Tool 2    │  │  Tool 3    │
                    │  problem_  │  │ solution_  │  │ submission │
                    │  definer   │──→│ architect  │──→│ _writer    │
                    │            │  │            │  │            │
                    │ Target     │  │ Solution   │  │ Formatted  │
                    │ users,     │  │ design,    │  │ CP1 draft  │
                    │ pain point │  │ tech stack │  │ ready to   │
                    │ urgency    │  │ build plan │  │ submit     │
                    └────────────┘  └────────────┘  └────────────┘
                                                          │
                                                          ▼
                                                   ┌────────────┐
                                                   │  User gets │
                                                   │  CP1 draft │
                                                   │  + download│
                                                   └────────────┘
```

### Information Chaining Between Tools

```
  Tool 1: problem_definer
    Input:  idea
    Output: target users, pain point, urgency, current alternatives
              │
              ▼
  Tool 2: solution_architect
    Input:  idea + problem_definer output
    Output: solution design, autonomy angle, tech stack, 10-day build plan
              │
              ▼
  Tool 3: submission_writer
    Input:  idea + problem_definer output + solution_architect output
    Output: Formatted CP1 submission draft
```

> **Why this order matters:** Each tool builds on the previous one's output. The solution architecture is more grounded when it's based on a clear problem definition. The CP1 draft is stronger when it can reference both the problem analysis AND the solution design. This is called **information chaining** — and it's how production AI agents work.

---

## 💻 Installation Guide

### Prerequisites

| Requirement | Details |
|-------------|---------|
| **Python** | Version 3.10 or higher |
| **pip** | Comes with Python |
| **Groq API Key** | Free — no credit card needed |
| **Internet** | Required for LLM API calls |
| **Browser** | Any modern browser (Chrome, Firefox, Edge, Safari) |

### Step 1: Get Your Free Groq API Key

1. Go to **[console.groq.com](https://console.groq.com)**
2. Sign up with Google or email (takes 30 seconds)
3. Click **API Keys** in the left sidebar
4. Click **Create API Key**
5. Copy the key — it looks like: `gsk_xxxxxxxxxxxxxxxxxxxx`
6. Save it somewhere — you'll paste it in Step 3

> **Why Groq?** It's free (14,400 requests/day), fast (300+ tokens/sec), and uses Llama 3.3 70B — a powerful open-source model. Students see results instantly, which is critical for workshop demos.

### Step 2: Clone and Install

#### On Windows (Command Prompt or PowerShell)

```bash
git clone https://github.com/studai-one/studai-foundry-launchpad.git
cd studai-foundry-launchpad
pip install -r requirements.txt
copy .env.example .env
```

#### On macOS / Linux (Terminal)

```bash
git clone https://github.com/studai-one/studai-foundry-launchpad.git
cd studai-foundry-launchpad
pip install -r requirements.txt
cp .env.example .env
```

> **What gets installed:** Only 3 packages — `groq` (LLM client), `streamlit` (web UI), `python-dotenv` (reads .env files). No heavy frameworks.

### Step 3: Add Your API Key

Open the `.env` file in any text editor and replace the placeholder:

```
# Before:
GROQ_API_KEY=your_groq_api_key_here

# After:
GROQ_API_KEY=gsk_your_actual_key_here
```

> **Alternatively**, you can paste the key directly in the app's sidebar — no `.env` file needed.

### Step 4: Verify Installation

```bash
python -c "from agent import loop; print('All imports OK')"
```

If you see `All imports OK`, you're ready to run.

---

## ▶️ Running the App

```bash
streamlit run main.py
```

The app opens automatically in your browser at **http://localhost:8501**.

```
  ┌─────────────────────────────────────────────────────────┐
  │  Browser: http://localhost:8501                         │
  │                                                         │
  │  ┌───────────────────────────────────────────────────┐  │
  │  │          StudAI LaunchPad                         │  │
  │  │   Startup Idea Validator — Autonomous Agent       │  │
  │  │                                                   │  │
  │  │  ┌─────────────────────────────────────────────┐  │  │
  │  │  │  Enter your startup idea...                 │  │  │
  │  │  └─────────────────────────────────────────────┘  │  │
  │  │                                                   │  │
  │  │  [🚀 Draft My CP1]            [💡 Try Example]   │  │
  │  │                                                   │  │
  │  │  ┌───────┬───────┬────────┬───────┬───────┐       │  │
  │  │  │ THINK │ PLAN  │EXECUTE │REVIEW │UPDATE │       │  │
  │  │  │  ○    │  ○    │   ○    │  ○    │  ○    │       │  │
  │  │  └───────┴───────┴────────┴───────┴───────┘       │  │
  │  │                                                   │  │
  │  │  ┌─────────────────────────────────────────────┐  │  │
  │  │  │  Activity Log                               │  │  │
  │  │  │  [HH:MM:SS] ═══ Loop 1 of 3 ═══            │  │  │
  │  │  │  [HH:MM:SS] Parsing goal: AI tutor app...   │  │  │
  │  │  │  [HH:MM:SS] Plan created with 3 steps       │  │  │
  │  │  │  [HH:MM:SS] Running tool: problem_definer     │  │  │
  │  │  │  ...                                        │  │  │
  │  │  └─────────────────────────────────────────────┘  │  │
  │  └───────────────────────────────────────────────────┘  │
  └─────────────────────────────────────────────────────────┘
```

### How to Use:

1. **Paste your Groq API key** in the sidebar (or set it in `.env`)
2. **Type a startup idea** in the text box — be specific! (or click **💡 Try Example**)
3. **Click 🚀 Draft My CP1** — watch the 5 step cards light up in real time
4. **Read the final brief** — it appears below with a verdict
5. **Download** the brief as a markdown file using the download button

---

## 👀 What You Will See

When you click **Draft My CP1**, the agent works autonomously:

### Step Cards Light Up in Real Time

```
  Loop 1:
  ┌───────┐  ┌───────┐  ┌────────┐  ┌───────┐  ┌───────┐
  │ THINK │  │ PLAN  │  │EXECUTE │  │REVIEW │  │UPDATE │
  │  ✔    │→ │  ✔    │→ │   ✔    │→ │  ✔    │→ │  ⚙    │
  │ done  │  │ done  │  │  done  │  │ done  │  │active │
  └───────┘  └───────┘  └────────┘  └───────┘  └───────┘
                                     Score: 5/10
                                     FAILED — retrying...

  Loop 2:
  ┌───────┐  ┌───────┐  ┌────────┐  ┌───────┐  ┌───────┐
  │ THINK │  │ PLAN  │  │EXECUTE │  │REVIEW │  │UPDATE │
  │  ✔    │→ │  ✔    │→ │   ✔    │→ │  ✔    │→ │  ↩    │
  │ done  │  │ done  │  │  done  │  │ done  │  │skipped│
  └───────┘  └───────┘  └────────┘  └───────┘  └───────┘
                                     Score: 8/10
                                     PASSED ✓ — delivering!
```

### Final Output

A structured **CP1 Submission Draft** with:

- **Project Title** — compelling, specific title
- **Problem Statement** — who, what, why now
- **Proposed Solution** — what the product does, how users interact
- **How Autonomy Works** — the 5-step loop mapped to THIS product
- **Target Users** — specific segment with demographics
- **Tech Stack** — LLM, UI, libraries, APIs
- **Agent Tools** — the tools the agent will use
- **10-Day Build Plan** — day-by-day milestones
- **Why This Will Win** — the unfair advantage

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **`ModuleNotFoundError: No module named 'groq'`** | Run `pip install -r requirements.txt` again |
| **`ModuleNotFoundError: No module named 'agent'`** | Make sure you're in the `studai-foundry-launchpad/` directory when running |
| **"API key missing" error in the app** | Paste your Groq key in the sidebar, or check your `.env` file |
| **"Rate limited" error** | Wait 60 seconds and try again. Free tier has per-minute limits. |
| **"Model error"** | Switch to a different model in the sidebar dropdown |
| **App doesn't open in browser** | Go to `http://localhost:8501` manually |
| **`streamlit: command not found`** | Try `python -m streamlit run main.py` instead |
| **Python version error** | Make sure you're using Python 3.10+: `python --version` |
| **Port 8501 already in use** | Run `streamlit run main.py --server.port 8502` |
| **Stuck on "Agent is working..."** | Check your internet connection — Groq API needs internet |

---

## 🛠️ How to Extend for Your Foundry Project

This repo is your **foundation**. The product you submit to StudAI Foundry is whatever you build on top of it.

### The One Rule

```
  ╔═══════════════════════════════════════════════════════╗
  ║                                                       ║
  ║       THE LOOP NEVER CHANGES. THE TOOLS DO.           ║
  ║                                                       ║
  ║   loop.py  → KEEP IT          (same for every agent)  ║
  ║   tools/   → CHANGE THESE     (your domain goes here) ║
  ║                                                       ║
  ╚═══════════════════════════════════════════════════════╝
```

### How to Vibe Code Your Own Agent

1. Open the project in **VS Code** with **GitHub Copilot** (or use **Claude Code**)
2. Read `CLAUDE.md` — it explains every file and has **6 ready-to-paste prompts**
3. Paste this into Copilot Chat:

```
I want to build [your idea]. Keep loop.py exactly the same.
Change the tools in agent/tools/ so this agent does [your domain]
instead of startup validation. Update planner.py's AVAILABLE_TOOLS
list and executor.py's routing to match the new tools.
```

### What to Change for Different Domains

```
  ┌─────────────────┬──────────────────────┬─────────────────────────┐
  │  Current Tool         │  Customer Support    │  Invoice Processor      │
  ├─────────────────────┼──────────────────────┼─────────────────────────┤
  │ problem_definer      │ ticket_classifier    │ document_parser         │
  │ solution_architect   │ knowledge_search     │ line_item_extractor     │
  │ submission_writer    │ response_drafter     │ approval_report         │
  ├─────────────────┼──────────────────────┼─────────────────────────┤
  │  Files to change: tools/, planner.py (AVAILABLE_TOOLS),          │
  │  executor.py (elif branches), reviewer.py (scoring criteria)     │
  │                                                                   │
  │  Files to KEEP:  loop.py, main.py                                │
  └───────────────────────────────────────────────────────────────────┘
```

### Example Prompts for Copilot / Claude Code

See `CLAUDE.md` for 6 detailed ready-to-paste prompts, including:
- Change domain (e.g., customer support, sales qualifier)
- Add a new tool
- Make the reviewer stricter
- Change the output format for CP1 submission
- Update branding
- Add a second agent

---

## ⚙️ Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| **LLM Provider** | [Groq API](https://console.groq.com) | Free tier (14,400 req/day), 300+ tokens/sec, no credit card |
| **LLM Model** | Llama 3.3 70B Versatile | Fast, capable, free — perfect for live demos |
| **UI Framework** | [Streamlit](https://streamlit.io) | Zero frontend knowledge needed, live updates native |
| **Language** | Python 3.10+ | Students already know the basics |
| **Dependencies** | `groq`, `streamlit`, `python-dotenv` | **3 packages only** — no bloat |

```
  No database.
  No authentication.
  No external services beyond Groq.
  No framework dependencies (no LangChain, no CrewAI).
  Pure Python agent — students can read every line.
```

---

## 📅 Hackathon Timeline — StudAI Foundry

```
  March 19  ──── 🎓 StudAI LaunchPad Workshop
                    Clone this repo, run the demo, start building
                    │
  March 21  ──── 🔨 Build week starts
                    Use Copilot/Claude Code to vibe-code your agent
                    │
  March 23  ──── 📋 CP1 Deadline (11:59 PM IST)
                    Submit: idea + architecture + initial prototype
                    │
  March 25  ──── 🎥 CP2 — Working Demo
                    Show your agent running live
                    │
  March 26  ──── 🏁 Final Submission
                    Complete product + demo video
                    │
  March 30  ──── 🏆 Grand Finale at SRMIST
                    INR 1,00,000+ prize pool
                    Live demos + judging
```

---

## 🚀 Deployment (Optional)

### Option A: Streamlit Cloud (Free — 3 Steps)

```
  1. Push repo to GitHub (must be public)
            │
            ▼
  2. Go to share.streamlit.io
     Connect your GitHub repo
            │
            ▼
  3. Set GROQ_API_KEY in Secrets
     Click Deploy
            │
            ▼
     Live URL in 2 minutes ✓
     Use this URL for your CP2 demo video
```

### Option B: Run Locally for Demos

```bash
streamlit run main.py
```

Share your screen during the demo. No deployment needed for CP1/CP2.

---

## 🤝 Credits

| | |
|---|---|
| **Built for** | [StudAI Foundry](https://studai.one) — National Autonomous AI Hackathon |
| **Workshop** | StudAI LaunchPad — March 19, 2026 |
| **Organised by** | StudAI One × SRMIST × Startup Singam |
| **Prize Pool** | INR 1,00,000+ |
| **Target Audience** | Engineering students building autonomous AI agents |

---

> **Remember: This repo is not the product. This repo is the foundation. The product is whatever YOU build on top of it in 10 days.**
