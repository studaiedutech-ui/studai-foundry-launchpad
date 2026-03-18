# CLAUDE.md — Project Brain for AI Coding Tools

## 1. What This Project Does

This is **StudAI LaunchPad** — the hands-on workshop product for **StudAI Foundry**, India's national autonomous AI systems hackathon. The workshop (March 19, 2026) is where engineering students at SRMIST learn the difference between a chatbot and an autonomous AI agent by cloning this repo, running it live, and then using "vibe coding" (directing GitHub Copilot or Claude Code) to build their own autonomous agent for the Foundry hackathon.

The product itself is a **CP1 Submission Drafter** — an autonomous AI agent (not a chatbot). The user enters their hackathon project idea. The agent autonomously defines the problem, architects the solution (with tech stack, autonomy angle, and 10-day build plan), drafts a formatted CP1 submission, reviews the draft against Foundry's actual CP1 criteria, and self-corrects if it's not submission-ready. It runs a 5-step loop up to 3 times until the draft passes a quality threshold of 7/10. Students walk out of the workshop with a usable CP1 draft they can refine and submit.

## 2. The 5-Step Autonomy Loop

```
┌─────────────────────────────────────────────────────┐
│           THE AUTONOMOUS AGENT LOOP                 │
│                                                     │
│   THINK → PLAN → EXECUTE → REVIEW → UPDATE          │
│     ↑                                   │           │
│     └───────────── (if score < 7) ──────┘           │
│                                                     │
│   Max 3 loops. Passes when review score >= 7/10.    │
└─────────────────────────────────────────────────────┘
```

- **THINK**: Parse the goal and incorporate feedback from any previous failed attempt — context awareness
- **PLAN**: Ask the LLM to generate a JSON step-by-step execution plan — the agent decides its own workflow
- **EXECUTE**: Run each tool in the plan (define → architect → write) — tool use with information chaining
- **REVIEW**: Score the output 1-10 against CP1 criteria — **self-evaluation, the core of autonomy**
- **UPDATE**: If review failed, carry specific feedback into the next loop iteration — self-correction

**Why is the REVIEW step what makes this autonomous?** A chatbot returns whatever the LLM generates. An autonomous agent *judges its own work* against a quality standard and decides whether to accept it or try again with specific improvements. This self-evaluation loop is what separates "I called an API" from "I built an autonomous system."

## 3. File Map — Every File and Its Purpose

```
studai-foundry-launchpad/
│
├── CLAUDE.md                    ← This file — project brain for AI tools
├── README.md                    ← Student setup guide (3 steps)
├── requirements.txt             ← groq, streamlit, python-dotenv
├── .env.example                 ← API key template
├── .gitignore                   ← Exclude .env and __pycache__
│
├── main.py                      ← Streamlit UI — display only, no agent logic
│
└── agent/
    ├── __init__.py               ← Package marker
    ├── loop.py                   ← THE CORE — the 5-step autonomy loop
    ├── planner.py                ← LLM call → JSON plan
    ├── executor.py               ← Routes plan steps → tool functions (with retry)
    ├── reviewer.py               ← Scores output against CP1 rubric → pass/fail
    │
    └── tools/
        ├── __init__.py           ← Package marker
        ├── problem_definer.py    ← Tool 1: extract problem, users, urgency
        ├── solution_architect.py ← Tool 2: design solution, tech stack, build plan
        └── submission_writer.py  ← Tool 3: formatted CP1 submission draft
```

**main.py** is UI only. It renders the Streamlit dashboard with step cards, a live activity log, loop counter, and educational content about autonomy. Do NOT put agent logic, LLM calls, or tool functions here.

**agent/loop.py** is the core autonomy loop. It orchestrates THINK → PLAN → EXECUTE → REVIEW → UPDATE. It imports planner, executor, and reviewer — nothing else. Do NOT modify its structure. This is the universal agent architecture.

**agent/planner.py** creates a JSON action plan from the goal and feedback. It knows what tools are available (AVAILABLE_TOOLS list). To add a new tool to the agent, add it here first.

**agent/executor.py** routes each plan step to the correct tool function. Each tool gets different inputs because later tools need earlier outputs (information chaining). Includes retry logic with exponential backoff for API resilience.

**agent/reviewer.py** scores the output against StudAI Foundry's CP1 criteria and decides pass or retry. PASS_THRESHOLD = 7. This is the file that makes the system autonomous — it judges the agent's own work. Without this, you just have a pipeline.

**agent/tools/problem_definer.py** — Tool 1. Extracts target users, pain point, urgency, and current alternatives. Only needs the idea as input (first in the chain).

**agent/tools/solution_architect.py** — Tool 2. Designs the solution with autonomy angle, tech stack, agent tools, and 10-day build plan. Takes idea + problem analysis — this is information chaining.

**agent/tools/submission_writer.py** — Tool 3. Synthesises everything into a formatted CP1 submission draft. Always runs last because it needs all previous outputs.

## 4. The One Rule

**THE LOOP NEVER CHANGES. THE TOOLS DO.**

`agent/loop.py` stays the same no matter what domain the agent is for. To change what the agent does — from CP1 drafting to customer support to invoice processing — you only change the files in `agent/tools/`, update `AVAILABLE_TOOLS` in `planner.py`, update the routing in `executor.py`, and adjust the review criteria in `reviewer.py`.

This constraint is intentional. It teaches students that ALL autonomous agents — regardless of domain — follow the exact same 5-step loop: understand the goal, plan the work, execute tools, evaluate quality, self-correct. The domain-specific work lives in the tools. The autonomy architecture is universal.

When students vibe-code their Foundry project, they tell the AI: *"Keep loop.py exactly the same, change the tools to do X."* This is the skill they are learning.

## 5. How to Change the Domain

Step-by-step process:
1. **Rewrite tool files** in `agent/tools/` for your new domain
2. **Update `AVAILABLE_TOOLS`** in `planner.py` with new tool names and descriptions
3. **Update `elif` branches** in `executor.py` to route to your new tools
4. **Update review criteria** in `reviewer.py` to match your new output format
5. **Do NOT touch `loop.py`** — the autonomy loop is domain-independent

| Current Tool | Customer Support Agent | Invoice Processor | Sales Lead Qualifier |
|---|---|---|---|
| `problem_definer` | `ticket_classifier` | `invoice_parser` | `lead_scorer` |
| `solution_architect` | `response_generator` | `line_item_validator` | `company_researcher` |
| `submission_writer` | `resolution_summary` | `approval_report` | `outreach_draft` |

## 6. Copy-Paste Prompts for GitHub Copilot / Claude Code

### Prompt 1: Change the domain
```
Change this from a CP1 submission drafter to a customer support agent. Keep loop.py
exactly the same. Replace the 3 tools:
- problem_definer.py → ticket_classifier.py (classify the support ticket by urgency and category)
- solution_architect.py → response_generator.py (draft a response using the classification)
- submission_writer.py → resolution_summary.py (write a summary of the resolution)
Update AVAILABLE_TOOLS in planner.py, the elif branches in executor.py, and the
review criteria in reviewer.py. Do not change loop.py or main.py structure.
```

### Prompt 2: Add a new tool
```
Add a new tool called market_validator to the agent. Create a new file
agent/tools/market_validator.py with a run(idea, problem_analysis, client, model)
function that asks the LLM to validate market size claims and identify 3 real
competitors. Add it to AVAILABLE_TOOLS in planner.py. Add an elif branch in
executor.py that routes to it. Make it run as step 2 (after problem_definer,
before solution_architect). Do not change loop.py.
```

### Prompt 3: Make the reviewer stricter
```
In agent/reviewer.py, change PASS_THRESHOLD from 7 to 9. Update the scoring
criteria in the prompt to require: specific product description (not vague),
autonomy explanation with all 5 steps mapped to the product, realistic 10-day
build plan with daily milestones, and compelling "why this will win" section.
Do not change any other file.
```

### Prompt 4: Change output to CP2 demo script
```
Change submission_writer.py to output a CP2 demo script instead of a CP1 draft.
Replace the markdown sections with: Demo Flow (step by step what to show),
Talking Points (what to say at each step), Live Demo Checklist (what must work),
Backup Plan (what to do if the demo breaks), and Key Metrics to Highlight.
Keep the run() function signature the same. Do not change loop.py.
```

### Prompt 5: Rebrand the UI
```
Change the UI title and branding in main.py from "StudAI LaunchPad" to
"[Your Product Name]". Update the header, page title, sidebar text, and
placeholder example to match your product. Keep the step card rendering,
log box, loop counter, and callback structure exactly the same. Do not change
any agent/ files.
```

### Prompt 6: Add a devil's advocate agent
```
Add a second review pass in reviewer.py that acts as a "devil's advocate" —
after the initial scoring, run a second LLM call that specifically challenges
the submission's assumptions and looks for weaknesses. Include the devil's
advocate feedback in the review output so the agent can address it in the next
loop. Keep the evaluate() function signature the same. Do not change loop.py.
```

## 7. What NOT to Change

- **`loop.py` structure** — The 5-step loop (THINK → PLAN → EXECUTE → REVIEW → UPDATE) must remain intact. This is the universal autonomous agent pattern.
- **Callback pattern** — `on_step(step, status)` and `on_log(message)` must keep their signatures. The UI depends on these exact callbacks.
- **Function signatures** — All tool files must keep `run(...) -> str`. The planner must keep `create_plan(idea, feedback, client, model) -> list`. The executor must keep `run_plan(plan, idea, client, model, on_log) -> dict`.

## 8. Running the Project

```bash
pip install -r requirements.txt
cp .env.example .env       # paste your Groq API key
streamlit run main.py
```

## 9. StudAI Foundry Hackathon Connection

This repo is the **foundation** for StudAI Foundry — the national autonomous AI hackathon organised by [StudAI One](https://studai.one) in partnership with SRMIST and Startup Singam.

Students clone this repo in the LaunchPad workshop, understand the autonomy loop, then vibe-code it into their own product using the tools and prompts above. After 10 days of building, they submit a startup-ready autonomous AI product to the hackathon.

Each Foundry track can be built by swapping the tools in this repo:

| Foundry Track | Tool 1 | Tool 2 | Tool 3 |
|---|---|---|---|
| HealthTech | `symptom_analyser` | `risk_scorer` | `care_plan_writer` |
| EdTech | `learning_gap_finder` | `curriculum_matcher` | `study_plan_writer` |
| FinTech | `expense_categoriser` | `budget_scorer` | `savings_plan_writer` |
| AgriTech | `crop_analyser` | `yield_predictor` | `farm_plan_writer` |
| LegalTech | `clause_extractor` | `risk_flagger` | `summary_writer` |
| Social Impact | `need_identifier` | `impact_scorer` | `proposal_writer` |

**The loop stays the same. The tools change. That's the lesson.**

## 10. Advanced: Adding Real Internet Access (MCP)

The current tools use the LLM's training knowledge only — no live internet access. For students who want to level up during build week:

**Day 2-5: Add Tavily web search**
```
Add a new tool called web_researcher.py that uses the Tavily API (free tier)
to search the internet for real market data and competitor info. Install tavily-python.
Pass the search results into problem_definer so it uses real data instead of
LLM knowledge. Add TAVILY_API_KEY to .env.example.
```

**Day 5-10: Add MCP (Model Context Protocol)**
MCP is Anthropic's protocol that lets AI agents connect to external services (web search, databases, Google Sheets, browser automation) through a standard interface. Think of it like USB for AI agents. Students who add MCP-based tools will stand out at the finale.

**The loop stays the same. The tools get more powerful.**
