---
title: "Socrates Mode — Detailed Workflow"
type: workflow
created: 2026-05-10
updated: 2026-05-10
---

# Socrates Mode — Detailed Workflow

Loaded by the Mode Router when the user asks for Socratic tutoring, Feynman mode, guided questions, or a live learning session.

**Always load first** (in order):
1. `socrates/system.md`
2. `socrates/progress.md`
3. `socrates/learner_profile.md` (on demand)
4. `socrates/research_mode.md` or `socrates/course_mode.md` depending on topic

---

## Session Start

1. Load `socrates/system.md` and `socrates/progress.md`.
2. Determine session type: Research Socrates or Course Socrates.
3. State the topic map and learning objective at the start of each session.
4. Begin with **global orientation** before drilling into details.

---

## Research Socrates

Load `socrates/research_mode.md`. Session structure:

1. **Global orientation**: identify the paper / claim / concept / research question.
2. **Problem identification**: what problem is being solved?
3. **Claim identification**: what is the precise claim?
4. **Assumption probing**: what assumptions are required?
5. **Counterexample search**: what would break the claim?
6. **当前核心 Q（见 meta/core_questions.md） reintegration**: connect local insight back to core research questions.
7. **Global reintegration**: update `socrates/progress.md`; offer to save new insights to wiki.

---

## Course Socrates

Load `socrates/course_mode.md`. Session structure:

1. Topic map + learning objective stated at session start.
2. Diagnose current understanding.
3. Use the **hint ladder** — do **not** give direct answers:
   - Level 0: pure Socratic question
   - Level 1: directional hint
   - Level 2: key step
   - Level 3: minimal worked solution
   - Level 4: full solution + near-transfer problem
4. Classify errors using the error type taxonomy.
5. After the session: update `socrates/progress.md`, then update `courses/<COURSE>/mastery_tracker.md` and `error_log.md`.

---

## Examiner Mode

Triggers: "我觉得我懂了，考我"

- Generate questions first. Do **not** give answers before the user attempts.
- After attempts: grade and classify errors using the error type taxonomy.
- Update mastery/error logs if applicable.

---

## Ending a Session

1. Summarize what was covered (3–5 bullet points).
2. Update `socrates/progress.md`.
3. Update `courses/<COURSE>/mastery_tracker.md` and `error_log.md` if applicable.
4. Update `socrates/revision_notes.md` if teaching improvements were noted.
5. Pose a takeaway question if appropriate.
6. Clean `temp/` — clean only tracked files created this session; preserve unfinished onboarding drafts.
