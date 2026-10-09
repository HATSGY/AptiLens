"""GUI page for Practice Mode: setup -> timed questions -> summary."""

from __future__ import annotations

import threading

import customtkinter as ctk

from src.ai.ai_service import default_ai_service
from src.analytics.performance import save_session
from src.config.settings import SAMPLE_QUESTIONS_FILE, SESSIONS_FILE
from src.practice.question_engine import available_topics, build_practice_set, check_answer, load_question_bank
from src.practice.scoring import Attempt, PracticeSession
from src.ui.styles import COLORS, font, heading_font
from src.ui.widgets import ErrorBanner, PageHeader, SectionLabel
from src.utils.helpers import Stopwatch

DIFFICULTIES = ["Any", "Easy", "Medium", "Hard"]


class PracticePage(ctk.CTkFrame):
    def __init__(self, parent, controller_show):
        super().__init__(parent, fg_color=COLORS["background"])
        self.controller_show = controller_show
        self.bank: list[dict] = []
        self.topic_vars: dict[str, ctk.BooleanVar] = {}
        self.current_set: list[dict] = []
        self.current_index = 0
        self.session = PracticeSession()
        self.stopwatch = Stopwatch()
        self._timer_job = None
        self._submitted = False

        self.outer = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        self.outer.pack(fill="both", expand=True, padx=24, pady=20)

        PageHeader(self.outer, "📝 Practice Mode", on_back=lambda: controller_show("dashboard"),
                   on_reset=self._go_to_setup).pack(fill="x", pady=(0, 16))

        self.load_error = ErrorBanner(self.outer)
        self.load_error.pack(fill="x")

        self.setup_frame = ctk.CTkFrame(self.outer, fg_color="transparent")
        self.question_frame = ctk.CTkFrame(self.outer, fg_color="transparent")
        self.summary_frame = ctk.CTkFrame(self.outer, fg_color="transparent")

        self._build_setup_frame()
        self._load_bank()
        self._go_to_setup()

    # ---- Data loading ---------------------------------------------------
    def _load_bank(self) -> None:
        try:
            self.bank = load_question_bank(SAMPLE_QUESTIONS_FILE)
        except (FileNotFoundError, ValueError) as exc:
            self.load_error.show(str(exc))
            return
        topics = available_topics(self.bank)
        for topic in topics:
            var = ctk.BooleanVar(value=True)
            self.topic_vars[topic] = var
            ctk.CTkCheckBox(self.topics_box, text=topic, variable=var,
                             fg_color=COLORS["primary"]).pack(anchor="w", padx=4, pady=3)

    # ---- Setup screen -----------------------------------------------------
    def _build_setup_frame(self) -> None:
        card = ctk.CTkFrame(self.setup_frame, corner_radius=12, fg_color=COLORS["card"],
                             border_width=1, border_color=COLORS["border"])
        card.pack(fill="x")

        SectionLabel(card, "1. Choose topics").pack(anchor="w", padx=16, pady=(16, 6))
        self.topics_box = ctk.CTkFrame(card, fg_color="transparent")
        self.topics_box.pack(anchor="w", padx=16, pady=(0, 10))

        SectionLabel(card, "2. Choose difficulty").pack(anchor="w", padx=16, pady=(6, 6))
        self.difficulty_menu = ctk.CTkOptionMenu(card, values=DIFFICULTIES, width=160)
        self.difficulty_menu.pack(anchor="w", padx=16, pady=(0, 10))

        SectionLabel(card, "3. Number of questions").pack(anchor="w", padx=16, pady=(6, 6))
        self.count_entry = ctk.CTkEntry(card, width=100, placeholder_text="e.g. 5")
        self.count_entry.insert(0, "5")
        self.count_entry.pack(anchor="w", padx=16, pady=(0, 14))

        self.setup_error = ErrorBanner(card)
        self.setup_error.pack(fill="x", padx=16)

        ctk.CTkButton(card, text="Start Practice", command=self._on_start,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=38
                      ).pack(anchor="w", padx=16, pady=(6, 18))

    def _on_start(self) -> None:
        self.setup_error.clear()
        selected_topics = [t for t, v in self.topic_vars.items() if v.get()]
        try:
            count = int(self.count_entry.get().strip())
            if count <= 0:
                raise ValueError
        except ValueError:
            self.setup_error.show("Enter a valid positive number of questions.")
            return
        try:
            self.current_set = build_practice_set(
                self.bank, selected_topics or None, self.difficulty_menu.get(), count)
        except ValueError as exc:
            self.setup_error.show(str(exc))
            return

        self.session = PracticeSession()
        self.current_index = 0
        self._go_to_question()

    # ---- Question screen ----------------------------------------------
    def _clear_question_frame(self) -> None:
        for w in self.question_frame.winfo_children():
            w.destroy()

    def _go_to_question(self) -> None:
        self._clear_question_frame()
        self._submitted = False
        q = self.current_set[self.current_index]

        card = ctk.CTkFrame(self.question_frame, corner_radius=12, fg_color=COLORS["card"],
                             border_width=1, border_color=COLORS["border"])
        card.pack(fill="x")

        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(16, 4))
        ctk.CTkLabel(top_row, text=f"Question {self.current_index + 1} of {len(self.current_set)}",
                     font=font(13, "bold"), text_color=COLORS["text"]).pack(side="left")
        ctk.CTkLabel(top_row, text=f"  {q['topic']} • {q['difficulty']}", font=font(12),
                     text_color=COLORS["text_muted"]).pack(side="left")
        self.timer_label = ctk.CTkLabel(top_row, text="⏱ 0s", font=font(12, "bold"),
                                         text_color=COLORS["primary"])
        self.timer_label.pack(side="right")

        ctk.CTkLabel(card, text=q["question"], font=font(16, "bold"), wraplength=820,
                     justify="left", text_color=COLORS["text"]).pack(anchor="w", padx=16, pady=(6, 12))

        self.answer_var = ctk.StringVar(value="")
        self.answer_entry = None
        if q.get("type") == "MCQ" and q.get("options"):
            for opt in q["options"]:
                ctk.CTkRadioButton(card, text=opt, variable=self.answer_var, value=opt,
                                   fg_color=COLORS["primary"]).pack(anchor="w", padx=20, pady=4)
        else:
            self.answer_entry = ctk.CTkEntry(card, width=200, placeholder_text="Your numeric answer")
            self.answer_entry.pack(anchor="w", padx=20, pady=6)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(10, 6))
        self.submit_btn = ctk.CTkButton(btn_row, text="Submit", command=self._on_submit,
                                         fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"])
        self.submit_btn.pack(side="left")
        self.hint_btn = ctk.CTkButton(btn_row, text="🤖 Ask AI for Hint", command=self._on_hint,
                                       fg_color=COLORS["surface_alt"], hover_color=COLORS["surface_hover"])
        self.hint_btn.pack(side="left", padx=10)

        self.hint_box = ctk.CTkTextbox(card, height=70, corner_radius=8, fg_color=COLORS["input_bg"],
                                        wrap="word", font=font(12))
        self.hint_box.configure(state="disabled")

        self.feedback_label = ctk.CTkLabel(card, text="", font=font(14, "bold"), justify="left",
                                            wraplength=820)
        self.feedback_label.pack(anchor="w", padx=16, pady=(8, 4))
        self.explanation_label = ctk.CTkLabel(card, text="", font=font(13), justify="left",
                                               wraplength=820, text_color=COLORS["text_muted"])
        self.explanation_label.pack(anchor="w", padx=16, pady=(0, 6))

        self.next_btn = ctk.CTkButton(card, text="Next Question →", command=self._on_next,
                                       fg_color=COLORS["success"], hover_color=COLORS["success_hover"])

        self.stopwatch.start()
        self._tick()
        self.question_frame.pack(fill="x")

    def _tick(self) -> None:
        if self._submitted:
            return
        self.timer_label.configure(text=f"⏱ {int(self.stopwatch.elapsed())}s")
        self._timer_job = self.after(1000, self._tick)

    def _on_hint(self) -> None:
        q = self.current_set[self.current_index]
        self.hint_box.pack(fill="x", padx=16, pady=(0, 10))
        self.hint_btn.configure(state="disabled")
        self.hint_box.configure(state="normal")
        self.hint_box.delete("1.0", "end")
        self.hint_box.insert("1.0", "🤖 Thinking of a hint...")
        self.hint_box.configure(state="disabled")

        def worker() -> None:
            result = default_ai_service.generate_hint(q["topic"], q["question"], q["difficulty"])

            def finish() -> None:
                self.hint_btn.configure(state="normal")
                self.hint_box.configure(state="normal")
                self.hint_box.delete("1.0", "end")
                prefix = "💡 " if result["available"] else "ℹ️  "
                self.hint_box.insert("1.0", prefix + result["text"])
                self.hint_box.configure(state="disabled")

            self.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    def _on_submit(self) -> None:
        if self._submitted:
            return
        q = self.current_set[self.current_index]
        user_answer = self.answer_var.get() if self.answer_entry is None else self.answer_entry.get()
        if not user_answer.strip():
            self.feedback_label.configure(text="Please provide an answer before submitting.",
                                           text_color=COLORS["warning"])
            return

        self._submitted = True
        time_taken = self.stopwatch.elapsed()
        correct = check_answer(q, user_answer)

        self.session.record(Attempt(
            question_id=q["id"], topic=q["topic"], difficulty=q["difficulty"],
            correct=correct, time_taken=time_taken, user_answer=user_answer,
            correct_answer=str(q["answer"]),
        ))

        if correct:
            self.feedback_label.configure(text=f"✅ Correct!  (Time taken: {time_taken}s)",
                                           text_color=COLORS["success"])
        else:
            self.feedback_label.configure(
                text=f"❌ Incorrect. Correct answer: {q['answer']}  (Time taken: {time_taken}s)",
                text_color=COLORS["danger"])
        self.explanation_label.configure(text=f"Explanation: {q.get('explanation', 'N/A')}")

        is_last = self.current_index == len(self.current_set) - 1
        self.next_btn.configure(text="Finish & See Results" if is_last else "Next Question →")
        self.next_btn.pack(anchor="w", padx=16, pady=(6, 16))
        self.submit_btn.configure(state="disabled")

    def _on_next(self) -> None:
        if self.current_index < len(self.current_set) - 1:
            self.current_index += 1
            self._go_to_question()
        else:
            self._finish_session()

    # ---- Summary screen -------------------------------------------------
    def _finish_session(self) -> None:
        self.question_frame.pack_forget()
        for w in self.summary_frame.winfo_children():
            w.destroy()

        summary = self.session.summary()
        try:
            save_session(SESSIONS_FILE, summary)
        except Exception:
            pass  # session persistence must never crash the practice flow

        card = ctk.CTkFrame(self.summary_frame, corner_radius=12, fg_color=COLORS["card"],
                             border_width=1, border_color=COLORS["border"])
        card.pack(fill="x")
        ctk.CTkLabel(card, text="🏁 Practice Session Complete", font=heading_font(20),
                     text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(20, 12))

        stats = [
            ("Total Questions", summary["total_questions"]),
            ("Correct", summary["correct"]),
            ("Incorrect", summary["incorrect"]),
            ("Accuracy", f"{summary['accuracy_percent']}%"),
            ("Total Time", f"{summary['total_time']}s"),
            ("Average Time / Question", f"{summary['average_time']}s"),
        ]
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=(0, 16))
        for i, (label, value) in enumerate(stats):
            row, col = divmod(i, 3)
            box = ctk.CTkFrame(grid, corner_radius=10, fg_color=COLORS["info_bg"])
            box.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            grid.grid_columnconfigure(col, weight=1)
            ctk.CTkLabel(box, text=str(value), font=font(20, "bold"),
                         text_color=COLORS["primary"]).pack(pady=(12, 0))
            ctk.CTkLabel(box, text=label, font=font(12), text_color=COLORS["text_muted"]).pack(pady=(0, 12))

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(anchor="w", padx=20, pady=(0, 20))
        ctk.CTkButton(btn_row, text="View Performance Analysis",
                      command=lambda: self.controller_show("performance"),
                      fg_color=COLORS["success"], hover_color=COLORS["success_hover"]).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="Practice Again", command=self._go_to_setup,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]).pack(side="left")

        self.summary_frame.pack(fill="x")

    # ---- Screen switching -------------------------------------------------
    def _go_to_setup(self) -> None:
        self.question_frame.pack_forget()
        self.summary_frame.pack_forget()
        self.setup_error.clear()
        self.setup_frame.pack(fill="x")

    def on_show(self, **_kwargs) -> None:
        pass
