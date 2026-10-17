---
title: "Command Aliases — Dispatch Table"
type: workflow
created: 2026-05-10
updated: 2026-05-12
---

# Command Aliases — Dispatch Table

Match on intent, not exact phrasing. If the command may modify files, first state planned reads/writes and follow the authorization rules in AGENTS.md.

---

## Intent-Matching Rules

- "后面再看" / "暂时不想看懂" → **Parking Ingest**, not Full Paper Ingest.
- "学习" / "带我读" / "看懂" → **Paper Learning** (Reading Mission + Paper Spine first), then ask whether to enter Socrates Mode.
- "教我" / "带我学" → **Course or Socrates teaching flow**, not just ingest.
- "逃课" / "补课" → **Catch-up Session**; start with diagnostic test and prerequisite tree.
- "考我" → **Examiner Mode**; do not give answers before the user attempts.
- Never modify `raw/`.

---

## Dispatch Table

### Research

| # | Trigger Phrases | Workflow File | Section |
|---|---|---|---|
| ① | "ingest 这篇论文，我后面再看" · "先放进系统，后面再读" · "暂时不想看懂" | `meta/workflows/research.md` | Parking Ingest |
| ② | "我想学习这篇论文" · "带我读这篇论文" · "帮我看懂这篇论文" · "learn this paper" | `meta/workflows/research.md` | Paper Learning |
| ③ | "帮我正式 ingest 这篇论文" | `meta/workflows/research.md` | Full Paper Ingest |
| ④ | "帮我判断这个 idea 有没有人做过" | `meta/workflows/research.md` | Novelty Sweep |
| ⑤ | "把这个 idea 放进系统" | `meta/workflows/research.md` | Idea Capture |

### Course

| # | Trigger Phrases | Workflow File | Section |
|---|---|---|---|
| ⑥ | "帮我 ingest 这节课" | `meta/workflows/course.md` | Course Ingest |
| ⑦ | "ingest 这节课然后教我" · "ingest this lecture and teach me" · "整理这节课然后带我学" | `meta/workflows/course.md` | Course Ingest + Teach |
| ⑧ | "我逃课了，帮我补这节" | `meta/workflows/course.md` | Catch-up Session |
| ⑨ | "帮我准备这次作业" | `meta/workflows/course.md` | Homework Preparation |

### Socrates

| # | Trigger Phrases | Workflow File | Section |
|---|---|---|---|
| ⑩ | "用 Socrates 模式问我" | `meta/workflows/socrates.md` | Socrates Session |
| ⑪ | "我觉得我懂了，考我" | `meta/workflows/socrates.md` | Examiner Mode |

### Maintenance

| # | Trigger Phrases | Workflow File | Section |
|---|---|---|---|
| ⑫ | "帮我整理系统" | `meta/workflows/maintenance.md` | Light Lint |
| ⑬ | "帮我记录这次修改" | `meta/workflows/maintenance.md` | Change Log Update |


## GPT 版补充入口

| Trigger | Workflow | Behavior |
|---|---|---|
| 用 Feynman 模式检验这个概念 | socrates/system.md → Feynman Mode | 学生讲解、零基础同学追问，结束更新进度并回到原模式 |
| 本周复盘 / 帮我复盘这门课 | course.md + templates/course/weekly_review.md | 读取该周实际进度、mastery、error_log 与题库，区分能做/不能做、主要错误、待复习、下周优先级，再出 3–5 道跨主题题，等作答后记录；不编造本周表现 |
| 修改画像 / 换目标 / 初始化知识库 | 入口技能 → onboarding.md | 关键问题澄清、增量保存、稳定 Q 编号与历史保留 |
| 继续上次学习 | socrates/progress.md + 当前画像 + 对应课程/研究记录 | 恢复停止点、知识漏洞与下次起点，不重做完整问卷 |
