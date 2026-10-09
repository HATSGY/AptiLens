# AptiLens — User Manual

This manual walks through every screen of the application. For installation
and setup, see `README.md`.

---

## Contents

- [Dashboard](#dashboard)
- [Concepts Library](#concepts-library)
- [1. Clock Problems](#1-clock-problems)
- [2. Calendar Problems](#2-calendar-problems)
- [3. Pattern Recognition](#3-pattern-recognition)
- [4. Tabular Data Interpretation](#4-tabular-data-interpretation)
- [5. Graph Analysis](#5-graph-analysis)
- [6. Caselet Data Interpretation](#6-caselet-data-interpretation)
- [7. Missing Data Interpretation](#7-missing-data-interpretation)
- [8. AI Study Assistant](#8-ai-study-assistant)
- [9. Practice Mode](#9-practice-mode)
- [10. Performance Analysis](#10-performance-analysis)
- [AI API Configuration](#ai-api-configuration)

---

## Dashboard

The first screen you see. It shows the AptiLens header and four sections
(Learn, Aptitude Solvers, Data Interpretation, Practice & Insights) of feature
cards. Click anywhere on a card to open that module. Every module has a **← Dashboard** button in its
top-left corner that returns you here instantly — no data from other
modules is lost, since each page keeps its own state.

## Concepts Library

Open it from the **Clock Concepts** / **Calendar Concepts** cards on the dashboard,
or from the **📘 Concepts** button on the Clock and Calendar pages.

1. Choose **Clock** (12 topics) or **Calendar** (13 topics) at the top of the sidebar.
2. Click a topic, or type in **Search concepts** to find one across both categories.
3. Each topic shows **Key ideas**, **Formulas**, **Worked examples** (with a highlighted
   answer), an **Exam tip**, and sometimes a reference table.
4. Use **Previous / Next** to walk through the topics, or **Try it in the … solver →**
   to practise the same concept on your own numbers.

Clock topics: hand speeds, angle between hands, time for a given angle, overlapping
hands, opposite hands & right angles, minute-space shortcut, frequency counts, mirror &
water image, fast/slow clocks, striking clocks, time arithmetic, cheat sheet.

Calendar topics: odd days, leap years, odd days in years/centuries, day-of-week (odd-days
method), Zeller's Congruence, Doomsday rule, weekday after N days, days between dates,
counting a weekday, repeating calendars, identical-month groups, Gregorian cycle, cheat sheet.

## 1. Clock Problems

1. Enter an **Hour** (1–12) and a **Minute** (0–59).
2. Click **Calculate**.
3. The Result panel shows the formula `|30H - 5.5M|`, the substituted
   values, and the final smaller angle (plus the reflex angle in the
   working steps).
4. Click **🤖 Explain with AI** for a plain-language, step-by-step
   explanation of that exact verified result.
5. **Reset** clears the inputs and result.

Sample competitive-exam questions are listed below the form for reference.

## 2. Calendar Problems

Four tabs, each independent:

- **Day of Week** — enter a date; get the weekday via Zeller's Congruence.
- **Leap Year** — enter a year; get a Yes/No with the divisibility rule
  used.
- **Date Difference** — enter Date A and Date B; get the number of days
  between them (via Julian Day Number subtraction).
- **Add / Subtract Days** — enter a date and an offset (e.g. `45` or
  `-10`); get the resulting date.

Each tab has its own Calculate button and shares one Result panel + AI
Explain button at the bottom of the page.

## 3. Pattern Recognition

1. Type a sequence of numbers separated by commas or spaces (at least 3
   numbers), e.g. `2, 4, 8, 16`.
2. Click **Analyze Pattern**.
3. The app detects the underlying rule (arithmetic, geometric,
   Fibonacci-like, perfect square/cube, quadratic/second-difference, or
   alternating) and predicts the next term with full reasoning.
4. If no standard rule matches, the app says so honestly instead of
   guessing.

## 4. Tabular Data Interpretation

- The built-in dataset (Quarterly Regional Sales) loads automatically into
  the table at the top.
- Choose an **Operation** (Sum, Average, Maximum, Minimum, Percentage of
  Total, Ratio, Difference, % Increase/Decrease).
- Choose the **Column**, and — for row-based operations — **Row A**
  (and **Row B**, which appears automatically when needed).
- Click **Calculate** to see the formula, calculation and verified answer.

## 5. Graph Analysis

1. Pick a **Graph Type**: Bar, Pie, Line, Scatter, or Histogram.
2. Click **Generate Graph** to draw it (Bar/Pie/Line use the monthly
   revenue dataset; Scatter compares Marketing Spend vs Revenue; Histogram
   uses a 40-student test-score dataset).
3. Click **Analyze Graph** to compute real statistics for that exact chart
   (highest/lowest, % change, trend, correlation coefficient, frequency
   distribution, etc.).
4. Click **🤖 Explain with AI** — the AI only ever receives the numbers
   already computed in step 3, so its explanation matches the chart.

## 6. Caselet Data Interpretation

1. Choose a **Caselet** from the dropdown (5 available: Sales, Banking,
   Exam Scores, Manufacturing, Household Budget).
2. Read the paragraph and the data table.
3. Choose a **Question** and click **Solve** to see the formula,
   calculation and answer.
4. Use **Explain with AI** for a plain-language walkthrough.

## 7. Missing Data Interpretation

1. Choose a sample problem (a Year/Value/Growth% table with some cells
   shown as `?`).
2. Click **Solve Missing Values**. The app fills in every recoverable cell
   step by step (e.g. `Value(2023) = Value(2022) × (1 + growth/100)`) and
   shows exactly which formula was used at each step.
3. Use **Explain with AI** to have the steps explained simply.

## 8. AI Study Assistant

A dedicated page with six tabs for interacting with the AI directly (not
tied to any specific module result):

| Tab | Purpose |
|---|---|
| Explain a Solution | Paste any problem/formula/verified result and get a step-by-step explanation |
| Give a Hint | Get a nudge toward the method *without* the final answer |
| Explain a Formula | Ask what a named formula means and when to use it |
| Similar Question | Generate a new practice question in the same style/difficulty |
| Simplify | Paste a confusing explanation to get a simpler rewrite |
| Why Correct | Understand why a given verified answer is correct (and the common mistake it avoids) |

A status banner at the top tells you immediately whether the AI Assistant
is configured or currently unavailable.

## 9. Practice Mode

1. **Setup:** tick the topics you want (all are ticked by default), choose
   a difficulty (or "Any"), and set the number of questions.
2. Click **Start Practice**.
3. For each question: select an option (MCQ) or type a number (Numerical),
   optionally click **🤖 Ask AI for Hint**, then **Submit**.
4. You'll immediately see Correct/Incorrect, the correct answer, an
   explanation, and the time you took, then **Next Question**.
5. After the last question you get a full summary: Total Questions,
   Correct, Incorrect, Accuracy %, Total Time, Average Time — and buttons
   to jump straight to **Performance Analysis** or **Practice Again**.

Every completed session is saved locally so Performance Analysis always
reflects your full history.

## 10. Performance Analysis

Shows, aggregated across every practice session you've ever completed:

- Sessions Completed, Total Questions, Overall Accuracy, Average Time per
  Question.
- Two charts: **Accuracy by Topic** and **Questions Attempted by Topic**.

If you haven't completed a practice session yet, this page tells you so
and points you back to Practice Mode.

## AI API Configuration

1. Copy `.env.example` to `.env` in the project root.
2. Set `OPENAI_API_KEY=<your key>` (and optionally `OPENAI_MODEL` /
   `OPENAI_BASE_URL` if you use a different OpenAI-compatible provider).
3. Restart the application.
4. **Never** share or commit your real `.env` file — it's already excluded
   via `.gitignore`.

Without a configured key, every "Explain with AI" button and the AI Study
Assistant page will clearly say the AI Assistant is unavailable — every
other part of AptiLens (all calculations, graphs, practice, scoring,
performance analytics) works exactly the same either way.
