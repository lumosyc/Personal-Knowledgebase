---
title: "Architecture"
type: meta
status: living
---

# Research-Wiki — 架构说明

> 此文件描述系统的目录结构与各模块职责，与 AGENTS.md 和入口技能共同定义工作区。
> 系统级变更记录在 [[changelog]]。

---

## 顶层目录结构

```
research-wiki/
├── AGENTS.md                        ← 工作区操作规则
├── .agents/skills/                  ← 项目技能与问答初始化
│
├── raw/                             ← 不可变源文件。绝不修改。（默认被 .gitignore）
│   ├── papers/                      ← 论文 PDF
│   ├── clips/                       ← 网页文章 + 嵌入资产文件夹
│   └── courses/
│       └── <COURSE>/                ← 课程讲义 / 章节 PDF / 习题
│
├── wiki/                            ← 研究知识库（LLM 维护）
│   ├── index.md                     ← 研究 wiki 页面目录
│   ├── log.md                       ← 研究 ingest / query / lint 日志
│   ├── concepts/                    ← 研究概念页（每个关键概念一页）
│   ├── papers/                      ← 论文摘要页（每篇论文一页）
│   ├── questions/                   ← 开放研究问题
│   ├── connections/                 ← 跨概念连接页
│   ├── claims/index.md              ← Claim Ledger（活跃研究命题追踪）
│   ├── reading_missions/index.md    ← 阅读任务追踪
│   ├── concept_debt/index.md        ← 概念债务追踪
│   ├── system.md / learner_profile.md ← redirect stub → socrates/
│   └── progress.md / revision_notes.md← redirect stub → socrates/
│
├── courses/                         ← 课程学习系统（LLM 维护）
│   ├── index.md                     ← 课程目录
│   ├── log.md                       ← 课程材料 ingest 日志
│   └── <COURSE>/                    ← 每门课一个子目录
│       ├── course_map.md            ← 课程概念图 + 依赖顺序
│       ├── mastery_tracker.md       ← 各主题掌握程度追踪
│       ├── error_log.md             ← 知识漏洞与错误记录
│       ├── problem_bank.md          ← 习题库
│       └── topic_pages/             ← 主题详细页
│
├── socrates/                        ← Socratic 辅导系统（LLM 维护）
│   ├── system.md                    ← 教学规则与会话协议
│   ├── research_mode.md             ← Research Socrates 协议
│   ├── course_mode.md               ← Course Socrates Hint Ladder 协议
│   ├── learner_profile.md           ← 学习者背景与偏好
│   ├── progress.md                  ← 会话日志 + 当前学习状态
│   ├── revision_notes.md            ← 教材改进建议
│   └── session_archive.md           ← 历史会话归档
│
├── templates/                       ← 可复用页面模板
│   ├── research/                    ← paper / concept / claim / question / ...
│   ├── course/                      ← course_map / topic_page / mastery_tracker / ...
│   └── meta/                        ← change_entry
│
├── meta/                            ← 系统文档层
│   ├── architecture.md              ← 本文件
│   ├── migration_log.md             ← 迁移操作记录
│   ├── changelog.md                 ← 系统级变更日志
│   ├── usage_guide.md               ← 操作模式说明
│   └── phase_plan.md                ← 阶段 / 计划记录
│
└── temp/                            ← 本次临时文件，按清单清理
```

---

## 模块职责边界

### `raw/` — 不可变源文件
- 所有输入材料的唯一真实来源；LLM 只读，绝不写入。
- 子目录：`papers/`（论文 PDF）、`clips/`（网页剪辑）、`courses/<COURSE>/`（课程材料）。
- 默认被 `.gitignore`：这是你私有、可能受版权的输入，不进公开仓库。

### `wiki/` — 研究知识库
- **面向研究**：所有页面围绕你在 meta/core_questions.md 定义的核心研究问题组织。
- `concepts/`：有研究关联的概念页（包括 course-origin 但有研究关联的概念）。
- `claims/`、`reading_missions/`、`concept_debt/`：研究工作流追踪（directory-based）。
- 遗留 Socrates 文件（`system.md` 等）为 redirect stub；`socrates/` 为权威版本。
- `log.md`：仅记录研究操作；课程 ingest 记录在 `courses/log.md`。

### `courses/` — 课程学习系统
- 课程掌握度追踪、错误日志、习题库、主题页。
- 与 `wiki/` 的边界：有研究关联的概念留在 `wiki/concepts/`（frontmatter 加 `domain: [research, course]`）；纯教学内容归入各课程子目录。

### `socrates/` — Socratic 辅导系统
- `system.md`：教学规则与会话协议。
- `progress.md`：会话叙事日志；课程掌握度表格迁移至 `courses/<COURSE>/mastery_tracker.md`。
- `research_mode.md` / `course_mode.md`：两种教学模式协议。

### `templates/` — 可复用模板
- 所有模板以独立文件存在，不嵌入 AGENTS.md。使用场景见入口技能及各 workflow。

### `meta/` — 系统文档
- 架构说明（本文件）、迁移日志、变更日志、操作指南、阶段计划。
- 仅供你和 LLM 参考，不出现在研究索引中。

### `temp/` — 临时文件
- 会话内数学渲染和画像草稿；只清理本次已登记文件，保留未完成初始化草稿；不进入任何索引或 wikilink。
