# PROJECT REPORT

## 1. Title

**AptiLens: Aptitude & Data Interpretation Studio**

## 2. Abstract

Competitive and entrance examinations (CAT, GATE, banking exams, GRE/GMAT,
UPSC/MPSC-style aptitude sections) consistently test a narrow but
high-value set of skills: clock and calendar arithmetic, number-pattern
recognition, and data interpretation across tables, charts and caselets.
Students preparing for these exams typically rely on scattered PDFs,
static answer keys, or generic calculators that show a final number
without a verifiable method. AptiLens addresses this gap with a single
desktop application that (a) solves each problem type with a transparent,
independently-verified algorithm; (b) visualizes and statistically
analyzes data interpretation charts; (c) offers a timed Practice Mode with
instant scoring; (d) tracks performance over time; and (e) layers an
optional AI Study Assistant on top that explains — but never overrides —
the verified numeric answer. The system is built entirely as a Python
desktop application using CustomTkinter, Pandas, NumPy and Matplotlib, and
remains fully functional even without any AI API key configured.

## 3. Problem Identification

Existing aptitude-preparation resources fall into two broad, unsatisfying
categories: (1) static content (PDFs, books, pre-recorded videos) that
cannot respond to a student's specific numbers, and (2) generic online
calculators that compute an answer but rarely show *why* it is correct or
let a student practice under timed, scored conditions. Neither category
combines verified algorithmic solving, data visualization, spaced/timed
practice, and personalized explanation in one coherent workflow.

## 4. Problem Statement

Design and develop an interactive Competitive Aptitude and Data
Interpretation Analysis System that provides students with a unified
platform to solve, analyze, and practice logical reasoning and data
interpretation problems commonly encountered in competitive and entrance
examinations — implementing algorithmic solutions for clock and calendar
problems, pattern recognition, and multiple forms of data interpretation
(tables, bar graphs, pie charts, line graphs, scatter diagrams, histograms,
caselets, and missing-data problems) — with interactive problem solving,
automatic calculations, graphical visualization, step-by-step analysis,
AI-assisted explanations, and result evaluation to improve students'
accuracy, speed and analytical reasoning skills.

## 5. Objectives

1. Implement verifiably-correct algorithms for every supported problem
   type (clock, calendar, patterns, tabular/graph/caselet/missing-data DI).
2. Provide a professional, consistent, navigable desktop GUI.
3. Visualize DI charts and back every interpretation with real computed
   statistics rather than eyeballed guesses.
4. Provide a timed Practice Mode with instant, explainable scoring.
5. Track and visualize performance over time (accuracy/speed by topic).
6. Layer an AI Study Assistant that explains/hints/simplifies without ever
   being permitted to override a verified numeric result.
7. Keep the application fully usable offline / without any AI credentials.

## 6. Target Audience

Students preparing for competitive/entrance examinations at the
undergraduate/postgraduate level (engineering entrance, MBA entrance,
banking and government recruitment exams, GRE/GMAT), as well as
instructors who want a demonstrable, transparent tool for classroom use.

## 7. Existing System

Most existing tools are either (a) single-purpose calculators (e.g. "clock
angle calculator" web widgets) with no practice or tracking features, or
(b) large, generic quiz platforms that treat aptitude questions as plain
multiple-choice trivia with no algorithmic transparency, DI-chart
generation, or genuine step-by-step derivation. AI chatbots, used alone,
can explain a problem but are also prone to silently computing an
incorrect final answer with no independent verification.

## 8. Proposed System

AptiLens separates concerns into a **Core Logic Layer** (deterministic,
independently testable Python algorithms) and an **AI Assistant Layer**
(purely explanatory, always given the already-verified result). A single
CustomTkinter window hosts a dashboard and one page per module, all
sharing common navigation, styling and result-display conventions. Every
module supports "Explain with AI" once — and only once — a verified result
exists.

## 9. Scope

**In scope:** clock, calendar, pattern, tabular DI, graph DI (5 chart
types), caselet DI, missing-data DI, an AI Study Assistant, Practice Mode,
Performance Analysis, and supporting documentation/tests.

**Out of scope (see Future Scope):** multi-user accounts/login, cloud
sync, mobile apps, non-English localisation, and adaptive
difficulty-selection algorithms.

## 10. Functional Requirements

- FR1: The system shall compute the angle between clock hands for any
  valid hour/minute and normalize it to the smaller angle.
- FR2: The system shall compute day-of-week, leap-year status, and the
  number of days between two dates using explicit algorithms.
- FR3: The system shall detect the governing rule of a numeric sequence
  and predict its next term, or clearly report "not recognized."
- FR4: The system shall load a real dataset and compute sum, average,
  min/max, ratio, difference, and percentage change on demand.
- FR5: The system shall generate Bar/Pie/Line/Scatter/Histogram charts and
  compute verified statistics for each.
- FR6: The system shall present caselets with tabular data and solve
  arbitrary declared operations against that data.
- FR7: The system shall recover missing table values from
  total/average/ratio/growth relationships.
- FR8: The system shall provide an AI explanation for any verified result,
  and shall degrade gracefully (with a clear message) if AI is
  unavailable.
- FR9: The system shall run a configurable timed practice quiz and report
  aggregate + per-topic scoring.
- FR10: The system shall persist practice results locally and display
  aggregated performance analytics.

## 11. Non-Functional Requirements

- **Usability:** consistent navigation (`Back to Dashboard` / `Reset` on
  every page), clear error banners instead of crashes.
- **Reliability:** the application must never crash due to invalid input,
  a missing/corrupt data file, or an AI/network failure.
- **Performance:** all core calculations return in well under 100ms;
  AI calls run on a background thread so the GUI never freezes.
- **Security:** no API key is ever hardcoded, logged, or committed;
  `.env` is git-ignored; only `.env.example` (with placeholders) is
  version-controlled.
- **Maintainability:** strict `*_logic.py` / `*_ui.py` separation per
  module, PEP 8 style, type hints, docstrings, no circular imports.
- **Testability:** every core algorithm and the AI fallback path is unit
  tested without requiring a GUI, network access, or a real API key.

## 12. System Architecture

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
              CORE LOGIC ENGINE
                       │
                       ▼
                   RESULTS
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Practice Mode       Performance Analysis
```

A single `ctk.CTk()` root window is created once in `main_window.py`.
Every "page" is a `CTkFrame` registered with a `NavigationController`,
which raises the requested frame via `tkraise()`. No module ever creates
its own root window, keeping navigation centralized and predictable.

## 13. Module Architecture

Each functional module is a self-contained package with exactly two
files: `<name>_logic.py` (pure functions/dataclasses, zero GUI or AI
imports) and `<name>_ui.py` (a `CTkFrame` subclass that wires the logic
module's outputs into `ResultCard`/`AIPanel` widgets). This 1:1 mapping is
what makes every algorithm independently unit-testable and lets the GUI
layer be modified without touching solving logic (and vice versa).

### Concepts Library (v2.0)

A theory module that complements the solvers. `src/modules/concepts/concepts_data.py` holds
25 data-driven topics (12 Clock, 13 Calendar), each with key ideas, formulas, worked examples
and an exam tip; `concepts_ui.py` renders them with a searchable sidebar and responsive text.
Every numeric claim in the examples is re-computed in `tests/test_concepts.py` against the
verified logic layer (and against Python's `datetime` for calendar results), so the written
theory cannot drift from the algorithms.

### Dark UI (v2.0)

The interface uses a single dark palette (`src/config/settings.py`) plus a CustomTkinter theme
file (`assets/theme/aptilens_dark.json`); Matplotlib charts are styled to match.

## 14. AI Architecture

```
src/ai/
├── ai_client.py    Talks to the OpenAI-compatible API only.
│                   Raises AIUnavailableError for: no key, network
│                   failure, timeout, empty/invalid response.
├── ai_prompts.py   Builds the system prompt + one prompt-template
│                   function per AI operation. Every template embeds
│                   an ALREADY-VERIFIED result; the AI is asked only
│                   to explain/hint/simplify it.
└── ai_service.py   High-level operations (explain_solution,
                    generate_hint, explain_formula, analyze_graph,
                    generate_similar_question, simplify_explanation,
                    explain_why_correct). Catches AIUnavailableError
                    and always returns {"available": bool, "text": str},
                    so the UI layer never needs its own error handling
                    for AI failures.
```

The UI's `AIPanel` widget calls `ai_service` on a background `threading.Thread`
and marshals the result back to the main thread via `widget.after(0, ...)`,
so a slow/failed network call never freezes the GUI.

## 15. Algorithms

- **Clock angle:** `Angle = |30H - 5.5M|`, folded to `min(angle, 360-angle)`.
- **Leap year:** divisible by 4 and (not divisible by 100, or divisible by 400).
- **Day of week:** Zeller's Congruence —
  `h = (q + floor(13(m+1)/5) + K + floor(K/4) + floor(J/4) - 2J) mod 7`.
- **Date difference:** Julian Day Number (Fliegel & Van Flandern) subtraction.
- **Pattern detection:** ordered checks for arithmetic, geometric,
  Fibonacci-like, perfect square/cube, constant second-difference
  (quadratic), and alternating (two interleaved) sequences.
- **Tabular/Caselet operations:** Pandas-vectorised sum/mean/idxmax/idxmin,
  simplified ratios via `math.gcd`, percentage and percentage-change
  formulas.
- **Graph statistics:** NumPy `argmax`/`argmin`/`diff`/`corrcoef`/`polyfit`/
  `histogram` for bar/line/scatter/histogram analysis; direct proportion
  math for pie charts.
- **Missing-data solving:** iterative constraint propagation over
  `Value[i] = Value[i-1] x (1 + Growth%/100)` until every solvable cell is
  filled or no further progress can be made.

## 16. Flowcharts

**Per-module interaction flow (identical across all 7 solving modules):**

```
Dashboard -> Module Page -> Enter Inputs -> [Calculate]
   -> Validate Input --(invalid)--> Show Error Banner (stay on page)
        |(valid)
        v
 Run Core Logic Algorithm
        v
 Render Formula + Calculation + Verified Answer
        v
 [Explain with AI] (optional) --> AI Service (background thread)
        |                              |
        |                    (no key / failure)   (success)
        |                              v                v
        |                     "AI unavailable" msg   Explanation text
        v
 [<- Back to Dashboard]
```

**Practice Mode flow:**

```
Setup (topics, difficulty, count) -> [Start Practice]
   -> Question -> [Ask AI for Hint]? -> [Submit] -> Feedback + Explanation
        |                                              |
        +---------------- [Next Question] <-------------+
                              | (last question)
                              v
                    Session Summary -> Save Session
                              |
              +---------------+---------------+
              v                                v
     Performance Analysis                Practice Again
```

## 17. Data Flow

```
data/*.json, *.csv  --->  *_logic.py (Pandas/NumPy)  --->  verified result dict
                                                              |
                              +--------------------------------+
                              v                                v
                     *_ui.py renders ResultCard        ai_service.py (only if
                                                        "Explain with AI" clicked)
                                                              |
                                                              v
                                                     AIPanel renders explanation
```

Practice Mode additionally writes session summaries to
`data/sessions.json`, which `analytics/performance.py` re-reads and
aggregates for the Performance Analysis charts.

## 18. Technology Stack

Python 3.11+, CustomTkinter, Pandas, NumPy, Matplotlib, Pillow,
python-dotenv, the `openai` SDK (for any OpenAI-compatible endpoint), and
pytest for testing. See `requirements.txt` for pinned minimum versions.

## 19. Implementation

The implementation strictly follows the module architecture in Section 13:
every solving feature was written first as a pure `*_logic.py` function
set, unit-tested in isolation, and only then wired into a `*_ui.py`
CustomTkinter page. The AI layer (Section 14) was implemented as an
injectable `AIService(client=...)` specifically so it could be unit tested
with a mock client — no real network access or API key is required to
validate its fallback behaviour. All 12 pages share one
`NavigationController` instance created once in `main_window.py`, and all
matplotlib figures are embedded via a single shared helper
(`utils/chart_utils.py`) to keep chart styling and lifecycle management
(figure creation/closing) consistent.

## 20. Testing

`tests/` contains 8 files and 84 automated pytest tests:

| File | Focus |
|---|---|
| `test_clock.py` | Angle formula correctness across many hour/minute combinations, boundary/invalid input |
| `test_calendar.py` | Day-of-week and date-difference cross-checked against Python's own `datetime` module for many dates |
| `test_patterns.py` | Every detection strategy (AP, GP, Fibonacci, square, cube, quadratic, alternating, unrecognized) |
| `test_tabular.py` | Every operation (sum/average/min/max/percent-of-total/ratio/difference/percent-change) plus error paths |
| `test_graphs.py` | Bar/pie/line/scatter/histogram statistics, including perfect +/-1 correlation edge cases |
| `test_caselet.py` | All 5 caselets x all questions solve without error; specific numeric assertions on caselet 1 |
| `test_missing_data.py` | Total/average/ratio solvers plus the exact worked example from the spec and a multi-step growth-chain case |
| `test_ai_service.py` | AIClient's "not configured" state, and every `AIService` operation via a mocked client — **no real API key or internet required** |

All 84 tests pass (`pytest tests/ -v`). In addition, the GUI itself was
smoke-tested headlessly (via Xvfb) by instantiating every page and
exercising every Calculate/Generate/Analyze/Solve/Submit code path
end-to-end, confirming the application runs without runtime errors.

## 21. Results

- 7 core algorithmic modules, each independently verified against known
  correct values (cross-checked with Python's `datetime` for calendar
  math, and hand-computed for clock/pattern/DI examples).
- 5 chart types generated and statistically analyzed with real NumPy
  computations (not simulated/hardcoded numbers).
- 5 caselets / 25 DI questions solved by one generic, data-driven solver.
- A working timed Practice Mode producing per-session and aggregated
  cross-session performance analytics.
- An AI layer that degrades gracefully to a clear, non-technical message
  when no API key is configured, with zero impact on any other feature.

## 22. Advantages

- **Transparency:** every answer comes with the exact formula and
  substituted calculation, not just a final number.
- **Separation of concerns:** the AI can never silently produce a wrong
  final answer, because it is never asked to compute one.
- **Offline-first:** 100% of the solving/practice/analytics functionality
  works with zero internet access or AI credentials.
- **Extensibility:** adding a new question type means adding a new
  `*_logic.py`/`*_ui.py` pair; the navigation, styling and AI-panel
  patterns are already reusable.

## 23. Limitations

- Practice Mode's question bank is a curated JSON file rather than an
  infinite generator (though Clock/Pattern/Calendar problems could be
  parameterized indefinitely using their own `*_logic.py` functions in a
  future iteration).
- No multi-user accounts — Performance Analysis reflects one local
  `data/sessions.json` file per installation.
- The AI Study Assistant depends on a third-party API and its associated
  cost/rate limits when a key is configured.

## 24. AI Integration (Summary)

See Section 14 (AI Architecture) for the full design. In one sentence:
**the core mathematical solution is generated entirely by AptiLens's own
algorithms; the AI is integrated purely as an explanatory layer** that
explains the verified result, offers hints, and generates similar practice
questions — never as a replacement for the underlying logic.

## 25. Future Scope

- Per-user login and cloud-synced performance history.
- Dynamically generated (rather than fixed-bank) practice questions for
  every topic, using each module's own `*_logic.py` as a question
  generator.
- Exportable PDF performance reports per session.
- Support for additional AI providers/local LLMs beyond OpenAI-compatible
  endpoints.
- Accessibility improvements (text-to-speech explanations, adjustable
  font scaling).

## 26. Conclusion

AptiLens demonstrates that a rigorous, exam-relevant desktop tool can
combine fully verifiable algorithmic problem-solving with a genuinely
useful AI explanatory layer — without ever letting the AI compromise
correctness. Its strict Core Logic / AI Assistant separation, comprehensive
automated test suite (84 passing tests with no network dependency), and
consistent single-window navigation make it both a practical study aid and
a demonstrable software-engineering case study.

## 27. References

- Zeller, C. (1887). *Zeller's Congruence* — standard algorithm for
  calculating the day of the week for any Julian or Gregorian calendar
  date.
- Fliegel, H. F., & Van Flandern, T. C. (1968). *A Machine Algorithm for
  Processing Calendar Dates*. Communications of the ACM.
- CustomTkinter documentation — https://customtkinter.tomschimansky.com/
- Pandas documentation — https://pandas.pydata.org/docs/
- NumPy documentation — https://numpy.org/doc/
- Matplotlib documentation — https://matplotlib.org/stable/
- OpenAI API reference — https://platform.openai.com/docs/

## 28. Appendix: Project Team

- **Team Members:** [Add your name(s) here]
- **College:** [Add your college name]
- **Department:** [Add your department]
- **Academic Year:** [Add academic year]
