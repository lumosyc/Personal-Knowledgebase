# [你的名字] AI Research & Learning System

> **Version**: V3 (slimmed 2026-05-10 — Phase 9)
> **Note**: Detailed workflows moved to `meta/workflows/`. Load them only when needed.

---

## 1. Identity

[你的名字]'s personal AI-assisted research and learning system. Research domain: [在这里填你的研究方向 —— 例如：表示学习 / 计算神经科学 / 你正在深耕的某个领域，一两句话描述]. 详见 `PERSONALIZE.md`。

### 问答式初始化（可选）

首次使用且身份或学习画像仍有占位符时，可提供问答初始化选项；用户也可以直接学习或手动填写。用户选择问答初始化或主动要求修改个人信息时，读取 `PERSONALIZE.md` 的“问答式初始化”一节：复用已有信息，一次只问一个问题，允许跳过，按现有写入规则确认后填写对应字段，并同步 `CLAUDE.md` / `AGENTS.md`。无需额外插件或 skill，不改动教学流程。

---

## 2. Hard Rules

- **Never modify `raw/`**. It is the immutable source of truth.
- Before modifying files, **report planned reads/writes and ask for confirmation** unless the user explicitly says to execute.
- Use the Mode Router (§4) to determine which workflow and files to load.
- Load detailed workflow files only when the mode is activated.
- Maintain strict boundaries: research content → `wiki/`, course content → `courses/`, tutoring → `socrates/`, system changes → `meta/`.
- Do not delete existing files unless explicitly instructed by you (the system owner).
- Prefer shadow migration over direct moves.

---

## 3. Directory Responsibilities

| Directory | Purpose |
|---|---|
| `raw/` | Immutable input material (papers, clips, course files). Never write here. |
| `wiki/` | Research knowledge base: concepts, papers, claims, questions, connections. |
| `courses/` | Course mastery tracking, error logs, problem banks, lecture spines. |
| `socrates/` | Tutoring session system, learner profile, session progress. |
| `templates/` | Reusable page templates for all page types. |
| `meta/` | Architecture docs, migration log, changelog, workflow files. |
| `temp/` | Session math rendering artifacts. Clean after each session. |

---

## 4. Mode Router

### Research Mode
**Trigger**: user asks about a paper, research idea, claim, literature, concept, or open question.

**Load**:
1. `meta/workflows/research.md`
2. `wiki/index.md`
3. Relevant wiki pages as needed.

### Course Mode
**Trigger**: user asks about a course topic, lecture, homework, exam, or wants to practice problems.

**Load**:
1. `meta/workflows/course.md`
2. `courses/index.md`
3. `courses/<COURSE>/course_map.md` and `mastery_tracker.md`

### Socrates Mode
**Trigger**: user asks for Socratic tutoring, Feynman mode, guided questions, or a live learning session.

**Load**:
1. `meta/workflows/socrates.md`
2. `socrates/system.md`
3. `socrates/progress.md`
4. `socrates/research_mode.md` or `socrates/course_mode.md` depending on topic

### Maintenance Mode
**Trigger**: user asks to lint, migrate, update architecture, create templates, or modify logs.

**Load**:
1. `meta/workflows/maintenance.md`
2. `meta/phase_plan.md` → `meta/migration_log.md` as needed

---

## 5. Minimal Command Aliases

Full alias descriptions: `meta/workflows/command_aliases.md`

| Trigger phrase | Alias | Mode |
|---|---|---|
| "ingest 这篇论文，我后面再看" | Parking Ingest | Research |
| "我想学习这篇论文" / "带我读" | Paper Learning | Research |
| "正式 ingest 这篇论文" | Full Paper Ingest | Research |
| "把这个 idea 放进系统" | Idea Capture | Research |
| "帮我判断这个 idea 有没有人做过" | Novelty Sweep | Research |
| "帮我 ingest 这节课" | Course Ingest | Course |
| "ingest 这节课然后教我" | Course Ingest + Socrates | Course + Socrates |
| "我逃课了，帮我补这节" | Catch-up | Course |
| "帮我准备这次作业" | Homework Prep | Course |
| "用 Socrates 模式问我" | Socrates Session | Socrates |
| "考我" | Examiner | Socrates |
| "帮我整理系统" | Light Lint | Maintenance |
| "帮我记录这次修改" | Change Log Update | Maintenance |

---

## 6. Logging Destinations

| Log file | What goes here |
|---|---|
| `wiki/log.md` | Research ingest / query / lint operations |
| `courses/log.md` | Course material ingest operations |
| `courses/<COURSE>/mastery_tracker.md` | Course mastery status per topic |
| `courses/<COURSE>/error_log.md` | Course mistakes, misconceptions, knowledge gaps |
| `socrates/progress.md` | Tutoring session history and current state |
| `socrates/revision_notes.md` | Teaching system improvements |
| `meta/changelog.md` | Architecture and system-level changes |
| `meta/migration_log.md` | Migration phase records |

**Routing rule**: course-sourced material → `courses/log.md`; research-sourced material → `wiki/log.md`.

---

## 7. Core Research Questions

> 把下面这张表换成你自己的 driving questions（详见 `PERSONALIZE.md`）。
> 这些编号会被各 wiki 页 frontmatter 的 `questions:` 字段引用，用来把每条笔记挂回你的核心问题。

| # | Question | Key concepts |
|---|---|---|
| **Q1** | [在这里填你的第一个 driving question] | [相关概念] |
| **Q2** | [在这里填你的第二个 driving question] | [相关概念] |
| **Q3** | [按需增减] | [相关概念] |

<!-- 格式示例（仅供参考，请替换成你自己的问题）：
| **Q1** | 一个"好"的表示由什么定义？ | 压缩 vs 结构、信息瓶颈 |
| **Q2** | 学习规则能否从能量最小化中涌现？ | 能量模型、Hopfield 网络、变分原理 |
-->


---

## 8. Page Conventions (Summary)

Full details: `meta/architecture.md`

- All pages use YAML frontmatter with `title`, `type`, `created`, `updated`, `sources`, `questions`, `tags`, `domain`.
- Use Obsidian wikilinks: `[[page-name]]`. Forward links must be explicit.
- Naming: `lowercase-with-hyphens.md` for concepts/topics; `AuthorYear-short-title.md` for papers.
- Write for a reader with strong math/CS background. Use proper notation. Preserve mathematical formulations.
- 中英文混用 is fine.

---

## 9. Templates

All templates in `templates/`. Do not embed template contents in CLAUDE.md.

| Template | Path |
|---|---|
| Paper summary | `templates/research/paper.md` |
| Concept page | `templates/research/concept.md` |
| Claim entry | `templates/research/claim.md` |
| Research question | `templates/research/question.md` |
| Reading mission | `templates/research/reading_mission.md` |
| Concept debt entry | `templates/research/concept_debt.md` |
| Course map | `templates/course/course_map.md` |
| Topic page | `templates/course/topic_page.md` |
| Mastery tracker | `templates/course/mastery_tracker.md` |
| Problem bank entry | `templates/course/problem_bank_entry.md` |
| Error log entry | `templates/course/error_log_entry.md` |
| Weekly review | `templates/course/weekly_review.md` |
| Change entry | `templates/meta/change_entry.md` |
