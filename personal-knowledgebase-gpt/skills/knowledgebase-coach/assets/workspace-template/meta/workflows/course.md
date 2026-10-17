---
title: "Course Mode — Detailed Workflow"
type: workflow
created: 2026-05-10
updated: 2026-05-10
---

# Course Mode — Detailed Workflow

Loaded by the Mode Router when the user asks about a course topic, lecture, homework, exam, or wants to practice problems.

**Always load first**: `courses/index.md` → `courses/<COURSE>/course_map.md` and `mastery_tracker.md`.

---

## Anti-Context-Overload Rule

If the user asks to teach an entire `raw/courses/<COURSE>/<SECTION>/` directory:

1. Do **not** deep-read all PDFs at once.
2. Inspect filenames and existing `course_map.md` / `mastery_tracker.md`.
3. Build a topic map from filenames and existing records.
4. Ask which subtopic to start with.
5. Then deep-read one file / subtopic at a time.

---

## Course Ingest

When told to ingest course material from `raw/courses/<COURSE>/`:

1. Read the course source material.
2. Update `courses/<COURSE>/course_map.md` with any new units, dependencies, or high-risk topics.
3. Create or update topic pages in `courses/<COURSE>/topic_pages/` only when the topic warrants a dedicated page.
4. Update `courses/<COURSE>/mastery_tracker.md` based on what was covered.
5. If practice problems are present, add entries to `courses/<COURSE>/problem_bank.md`.
6. Add error log entries to `courses/<COURSE>/error_log.md` only when actual mistakes or gaps are observed — not speculatively.
7. Append entry to `courses/log.md`: `## [YYYY-MM-DD] ingest | COURSE — Topic`.

---

## Course Learning Loop

For each topic being studied, follow this sequence:

```
minimum concept → worked example → independent problem → correction → error log → near-transfer problem
```

Mastery levels:

| Level | Meaning |
|---|---|
| **L0** | Heard of it |
| **L1** | Can explain the core idea |
| **L2** | Can follow a worked example |
| **L3** | Can solve standard problems independently |
| **L4** | Can solve transfer / exam-level problems |
| **L5** | Can apply to research or project |

Rules:
- Course learning is not summary-first. Evidence of mastery is problem-solving, not reading notes.
- For graded homework or exams, use the hint ladder (see `socrates/course_mode.md`) rather than giving direct answers.
- When a topic has research relevance, link to the corresponding `wiki/concepts/` page.

---

## Course Ingest + Teach

Triggers: "ingest 这节课然后教我" · "ingest this lecture and teach me" · "整理这节课然后带我学"

- Complete Course Ingest first.
- Then enter Socrates Course Mode: global orientation → topic map → diagnostic question → hint ladder.
- Follow learning loop: minimum concept → worked example → independent problem → correction → error log → near-transfer problem.
- Update `mastery_tracker.md` and `error_log.md` only after actual interaction, not speculatively.

---

## Catch-up Session

Triggers: "我逃课了，帮我补这节"

- First identify the immediate goal: homework / quiz / exam / follow next lecture.
- Build a prerequisite tree. Separate must-know / useful / can-skip.
- Start with diagnostic questions — do **not** begin with a full lecture summary.

---

## Homework Preparation

Triggers: "帮我准备这次作业"

- Identify relevant topics and prerequisites.
- Check `mastery_tracker.md` and `error_log.md`.
- Use hint ladder. Do not directly solve graded homework — prefer similar practice problems unless user explicitly requests a non-graded explanation.
