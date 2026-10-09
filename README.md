# AptiLens — Aptitude & Data Interpretation Studio

A desktop application (Python + CustomTkinter) that lets students solve,
analyze and practice the logical-reasoning and data-interpretation problems
commonly found in competitive/entrance exams (CAT, GATE, banking, GRE/GMAT,
UPSC/MPSC-style aptitude sections) — with an optional AI Study Assistant
layered on top of fully algorithmic, independently verified core logic.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Objectives](#objectives)
3. [Features](#features)
4. [AI Integration](#ai-integration)
5. [Technology Stack](#technology-stack)
6. [Architecture](#architecture)
7. [Installation](#installation)
8. [API Key Setup](#api-key-setup)
9. [How to Run](#how-to-run)
10. [How to Test](#how-to-test)
11. [Folder Structure](#folder-structure)
12. [Troubleshooting](#troubleshooting)
13. [Future Scope](#future-scope)

---

## Problem Statement

Design and develop an interactive Competitive Aptitude and Data
Interpretation Analysis System that provides students with a unified
platform to solve, analyze, and practice logical reasoning and data
interpretation problems commonly encountered in competitive and entrance
examinations — implementing algorithmic solutions for clock and calendar
problems, pattern recognition, and multiple forms of data interpretation
(tables, bar graphs, pie charts, line graphs, scatter diagrams, histograms,
caselets, missing-data problems), with interactive solving, graphical
visualization, step-by-step analysis, AI-assisted explanations and result
evaluation.

## Objectives

- Provide **verified, algorithmic** solutions for every supported problem
  type — never a black-box or AI-guessed answer.
- Visualize data (bar/pie/line/scatter/histogram) and interpret it with
  real statistics (max/min/trend/correlation/frequency).
- Offer a **Practice Mode** with timed MCQ/numerical questions and instant
  scoring, plus a **Performance Analysis** dashboard.
- Layer an **AI Study Assistant** on top that explains, hints, and
  generates similar questions — without ever being allowed to override a
  verified numeric result.
- Keep the application **fully functional offline** / without any AI key.

## Features

| # | Module | What it does |
|---|--------|---------------|
| 0 | **Concepts Library** (new) | 25 topics covering every Clock & Calendar concept — key ideas, formulas, worked examples, exam tips, search, and deep links to the solvers |
| 1 | Clock Problems | Angle between hands, reflex angle, time-for-angle |
| 2 | Calendar Problems | Day of week (Zeller's Congruence), leap year, date difference (Julian Day Number), date shifting |
| 3 | Pattern Recognition | Detects AP, GP, Fibonacci-like, square/cube, quadratic (2nd-difference), alternating patterns |
| 4 | Tabular Data Interpretation | Sum, average, max/min, % of total, ratio, difference, % change on a real Pandas dataset |
| 5 | Graph Analysis | Bar / Pie / Line / Scatter / Histogram — generated with Matplotlib and analyzed with NumPy |
| 6 | Caselet Data Interpretation | 5 caselets, 25 questions, solved by a generic table-driven solver |
| 7 | Missing Data Interpretation | Recovers missing table cells via total/average/ratio/growth relationships |
| 8 | AI Study Assistant | Explain a solution, give a hint, explain a formula, generate a similar question, simplify an explanation, explain why an answer is correct |
| 9 | Practice Mode | Topic/difficulty-filtered timed quiz with instant scoring and an in-quiz "Ask AI for Hint" |
| 10 | Performance Analysis | Accuracy/attempted-by-topic charts aggregated across every saved practice session |
| 11 | User Guide / About | In-app help and project info |

The whole UI uses a professional **dark theme** (`assets/theme/aptilens_dark.json` + the palette in `src/config/settings.py`), including dark-styled Matplotlib charts.

Every module page follows the same navigation pattern:

```
Dashboard → Module → Inputs → Calculate → Result → [Explain with AI] → Back to Dashboard
```

## AI Integration

**Core Logic Layer** and **AI Assistant Layer** are strictly separated:

```
Clock Problem → Python clock algorithm → Correct numerical answer
                                              │
                                              ▼
                              AI receives problem + calculation
                                              │
                                              ▼
                        AI explains the solution in simple language
```

- The AI is **never** asked to compute an answer — only to explain,
  hint, or simplify an answer the Core Logic Layer already verified.
- If the AI ever disagrees with the supplied calculation, its system
  prompt instructs it to say so explicitly rather than silently produce a
  different number.
- If no `OPENAI_API_KEY` is configured (or the network/API call fails for
  any reason), the app shows:

  > "AI Assistant is currently unavailable. Core solving features are
  > still fully functional."

  and every other feature keeps working normally. See
  `src/ai/ai_client.py` and `src/ai/ai_service.py`.

## Technology Stack

- **Python 3.11+**
- **GUI:** CustomTkinter
- **Data:** Pandas, NumPy
- **Visualization:** Matplotlib (embedded via `FigureCanvasTkAgg`)
- **AI:** OpenAI-compatible chat-completions API (`openai` SDK)
- **Environment:** python-dotenv
- **Testing:** pytest

No web framework (Flask/Django/etc.) is used anywhere — this is a desktop
application built on a single Tkinter/CustomTkinter root window.

## Architecture

```
                    USER
                      │
                      ▼
              MAIN DASHBOARD
                      │
              NAVIGATION LAYER (single CTk root + stacked Frames)
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
 LOGICAL MODULES   DATA MODULES   AI ASSISTANT
  Clock              Tabular DI     Explanation
  Calendar           Graphs         Hints
  Patterns           Caselets       Formula Help
  Missing Data                      Similar Questions
       │              │              │
       └──────────────┼──────────────┘
                       ▼
              CORE LOGIC ENGINE  (pure Python / Pandas / NumPy)
                       │
                       ▼
                   RESULTS
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Practice Mode       Performance Analysis
```

Every module has a matching pair of files: `*_logic.py` (pure, testable,
zero GUI/AI dependency) and `*_ui.py` (CustomTkinter page that calls the
logic module and, optionally, `src/ai/ai_service.py`).

## Installation

```bash
# 1. Clone / unzip the project, then enter its folder
cd AptiLens

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

> **Linux users:** CustomTkinter needs the system `tkinter` package, which
> is not installed by pip. Install it with your package manager first,
> e.g. `sudo apt install python3-tk` on Debian/Ubuntu.

## API Key Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and set your key:
   ```
   OPENAI_API_KEY=sk-...your-real-key...
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_BASE_URL=https://api.openai.com/v1
   ```
3. **Never commit `.env`** — it is already listed in `.gitignore`.
4. If you skip this step entirely, the application still runs perfectly;
   only the "Explain with AI" buttons will show the unavailable message.

## How to Run

```bash
python main.py
```

This opens the AptiLens dashboard in a single window. Click any feature
card to open that module; every module page has a **← Back to Dashboard**
button and (where relevant) a **Reset** button.

## How to Test

```bash
pytest tests/ -v
```

- All core algorithm tests (`test_clock.py`, `test_calendar.py`,
  `test_patterns.py`, `test_tabular.py`, `test_graphs.py`,
  `test_caselet.py`, `test_missing_data.py`) run with **zero** network
  access and **zero** GUI — they call the logic modules directly.
- `test_ai_service.py` mocks the AI client entirely, so it also needs
  **no real API key** and **no internet connection**, while still
  verifying the offline-fallback behaviour and every AI operation.

## Folder Structure

```
AptiLens/
├── main.py                    Entry point
├── requirements.txt
├── README.md / USER_MANUAL.md / PROJECT_REPORT.md
├── .env.example                Template for your API key (never commit .env)
├── assets/theme/               aptilens_dark.json (dark colour theme)
├── data/                       sample_questions.json, tabular_data.csv,
│                                graph_data.csv, caselet_data.json
├── src/
│   ├── app.py                  App bootstrap
│   ├── config/settings.py      Paths, theme, AI settings loader
│   ├── ui/                     main_window, dashboard, navigation, styles,
│   │                           widgets, ai_panel, ai_assistant_page, about_page
│   ├── modules/
│   │   ├── concepts/                (concepts_data.py + concepts_ui.py)
│   │   ├── clock/  calendar/  patterns/  tabular/  graphs/
│   │   └── caselet/  missing_data/       (each: *_logic.py + *_ui.py)
│   ├── practice/                question_engine.py, scoring.py, practice_ui.py
│   ├── analytics/               performance.py, performance_ui.py
│   ├── ai/                      ai_client.py, ai_prompts.py, ai_service.py
│   └── utils/                   validators.py, helpers.py, chart_utils.py
└── tests/                       9 pytest files, 140+ tests
```

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `ModuleNotFoundError: No module named 'tkinter'` | Install your OS's Tk package (`python3-tk` on Debian/Ubuntu, bundled by default on Windows/macOS python.org installers). |
| "AI Assistant is currently unavailable" | No `.env` / no `OPENAI_API_KEY`, an invalid key, or no internet — every other feature still works. |
| Blank/garbled chart | Make sure `matplotlib` installed correctly; try `pip install --upgrade matplotlib`. |
| `FileNotFoundError: ... data file not found` | Run `main.py` from the project root so relative paths under `data/` resolve correctly. |
| CSV/JSON edits break a module | The loaders validate structure and raise a friendly `ValueError`/`FileNotFoundError` shown directly in the GUI rather than crashing. |

## Future Scope

- Persist per-user profiles/login so multiple students can track separate
  histories.
- Add more question banks and auto-generate fresh numeric variants of
  clock/pattern/DI questions for unlimited practice.
- Export a PDF performance report per practice session.
- Add speech-to-text/text-to-speech for accessibility.
- Support additional AI providers beyond OpenAI-compatible endpoints.

---

*Academic project — see `PROJECT_REPORT.md` for the full case-study write-up
and `USER_MANUAL.md` for a page-by-page usage guide.*
