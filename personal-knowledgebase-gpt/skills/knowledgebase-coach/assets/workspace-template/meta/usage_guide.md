---
title: "Usage Guide"
type: meta
status: complete
created: 2026-05-09
updated: 2026-05-10
---

# 操作模式说明 — V2 完整版

> V2 迁移完成（Phase 1–8）。此文件描述四种操作模式的完整工作流程。
> 权威操作规范见 `AGENTS.md`；此文件是其精简参考版本。

---

## 模式识别（Mode Router）

| 触发信号 | 进入模式 |
|---|---|
| 论文 / 研究想法 / claim / 文献 / 概念 / 开放问题 | Research Mode |
| 课程主题 / 讲义 / 作业 / 考试 / 练习题 | Course Mode |
| Socratic 辅导 / Feynman 模式 / 引导提问 / 实时学习 | Socrates Mode |
| Lint / 迁移 / 架构更新 / 模板 / 日志修改 | Maintenance Mode |

---

## Research Mode（研究模式）

**进入时加载**：`wiki/index.md` → 相关 wiki 页面

### Paper Ingest 流程

1. 读取全文
2. 创建 **Reading Mission**（`templates/research/reading_mission.md`）：Role / Target Level / Must Understand ≤ 3 / Stopping Criterion
3. 确定 Role：`survey` / `ingredient` / `nearest prior work` / `baseline` / `theory foundation`
4. 确定 Target Level：L0–L4
5. 在 `wiki/papers/` 创建论文摘要页（`templates/research/paper.md`）
6. 处理各关键概念：
   - 已有概念页 → 更新，注明来源
   - 无概念页 → 从 `templates/research/concept.md` 创建
   - 边缘概念 → 记录至 `wiki/concept_debt/index.md`，不建页
7. 如果来源支持/削弱某 claim → 更新 `wiki/claims/index.md`
8. 新开放问题 → 创建 `wiki/questions/q-*.md`
9. 非显然跨概念连接 → 创建 `wiki/connections/conn-*.md`
10. 标注涉及的核心研究问题（**当前核心 Q（见 meta/core_questions.md）**）
11. 更新 `wiki/index.md`
12. 追加至 `wiki/log.md`：`## [YYYY-MM-DD] ingest | Source Title`
13. 更新 `wiki/reading_missions/index.md`：将任务移至"已完成"

### Research Query 流程

1. 读取 `wiki/index.md`，定位相关页面
2. 加载并阅读相关页面
3. 用 `[[wikilinks]]` 综合回答
4. 若产生新连接 → 提议保存为 claim / question / connection 页面

### Research Lint 检查项

1. 孤立页（无入链的 concept / paper 页）
2. 文本中提及但无独立页的概念 → 是否升级为 concept page
3. 被新来源削弱的旧 claim
4. 当前核心 Q（见 meta/core_questions.md） 覆盖密度分布——哪些问题缺乏文献支撑
5. Concept debt 状态：`parked` 已满足升级条件的项
6. Reading missions：已完成任务的 Key Takeaway 是否填写

---

## Course Mode（课程模式）

**进入时加载**：`courses/index.md` → `courses/<COURSE>/course_map.md` + `mastery_tracker.md`

### Course Ingest 流程

1. 读取课程材料（`raw/courses/<COURSE>/`）
2. 更新 `courses/<COURSE>/course_map.md`
3. 在 `courses/<COURSE>/topic_pages/` 创建/更新主题页（仅当主题值得独立页面时）
4. 更新 `courses/<COURSE>/mastery_tracker.md`
5. 有习题 → 追加至 `courses/<COURSE>/problem_bank.md`
6. 发现实际错误/漏洞 → 追加至 `courses/<COURSE>/error_log.md`（不预测性填写）
7. 追加至 `courses/log.md`：`## [YYYY-MM-DD] ingest | COURSE — Topic`

### 掌握度等级（L0–L5）

| Level | 含义 | 升级条件 |
|---|---|---|
| **L0** | 听说过 | — |
| **L1** | 能解释核心思想 | 能用自己的话表达 |
| **L2** | 能跟随例题 | 能复现教师解题步骤 |
| **L3** | 能独立解标准题 | 独立解出 ≥1 道新题 |
| **L4** | 能解 transfer / 考试题 | 独立解出 transfer 题 |
| **L5** | 能用于研究或项目 | 有具体应用证据 |

**规则**：掌握度升级需要**解题证据**，不是阅读笔记。Socratic 会话中"掌握" ≠ 独立解题 L4。

### 课程学习循环

```
最小概念 → 例题 → 独立练习 → 纠错 → 写入 error_log → near-transfer 题
```

---

## Socrates Mode（辅导模式）

**进入时必须加载**（按序）：
1. `socrates/system.md` — 教学规则
2. `socrates/progress.md` — 上次停止位置

然后根据主题选择子模式：

### Research Socrates

加载 `socrates/research_mode.md`，执行 7 步协议：

1. **全局定位**：确认论文 / claim / 概念 / 研究问题
2. **问题识别**：它解决什么问题？
3. **claim 识别**：精确的断言是什么？
4. **假设探针**：需要哪些假设？
5. **反例搜索**：什么情况会打破 claim？
6. **当前核心 Q（见 meta/core_questions.md） 重整合**：局部洞见如何连接核心研究问题？
7. **全局重整合**：更新 `socrates/progress.md`；提议保存新洞见至 wiki

### Course Socrates

加载 `socrates/course_mode.md`，使用 **Hint Ladder**（不直接给答案）：

| Level | 行为 |
|---|---|
| 0 | 纯 Socratic 提问 |
| 1 | 方向性提示 |
| 2 | 关键步骤 |
| 3 | 最小完整解 |
| 4 | 完整解 + near-transfer 题 |

**防过载规则**：一次一个问题；不给出大段文字墙；明确说明哪些内容可以跳过；每 2–3 个主题后 check-in。

### 会话结束步骤

1. 总结覆盖内容（3–5 条）
2. 更新 `socrates/progress.md`
3. 如适用：更新 `courses/<COURSE>/mastery_tracker.md` + `error_log.md`
4. 如有教学改进：更新 `socrates/revision_notes.md`
5. 提出 takeaway 问题（可选）
6. 清理本次会话已登记临时文件，保留未完成初始化草稿

---

## Maintenance Mode（维护模式）

**进入时加载**：`meta/phase_plan.md` → `meta/migration_log.md`（按需）

### Lint 检查清单

| 检查项 | 方法 |
|---|---|
| 孤立研究页（无入链）| 搜索 `wiki/concepts/`、`wiki/papers/` 中无 `[[` 引用的文件 |
| stale wikilink | 搜索 `[[page-name]]` 是否有对应文件 |
| stale 路径引用 | grep `teacher/`、`raw/assets`、`questions (1-5)`、`wiki/system.md` |
| `temp/` 残留 | 检查 `temp/` 是否为空 |
| Concept debt 升级 | 检查 `wiki/concept_debt/index.md` 中 parked 项是否满足升级条件 |
| claims 状态 | 检查 `wiki/claims/index.md` 中 hypothesis 项是否有新证据 |
| `wiki/index.md` 完整性 | 每个 `wiki/concepts/*.md` 和 `wiki/papers/*.md` 是否在 index 中有条目 |

### 日志路由规则

| 操作类型 | 写入位置 |
|---|---|
| 研究 ingest / query / lint | `wiki/log.md` |
| 课程材料 ingest | `courses/log.md` |
| 课程掌握度更新 | `courses/<COURSE>/mastery_tracker.md` |
| 课程错误 / 漏洞 | `courses/<COURSE>/error_log.md` |
| 辅导会话日志 | `socrates/progress.md` |
| 教学改进建议 | `socrates/revision_notes.md` |
| 架构 / 系统变更 | `meta/changelog.md` |
| 迁移操作细节 | `meta/migration_log.md` |

### 维护约束

- `raw/` **绝不修改**
- 不删除文件，除非你（系统拥有者）明确授权
- 优先 shadow copy（先复制再删除），不直接移动
- 每次架构变更后更新 `meta/changelog.md`
- `wiki/index.md` 和 `courses/index.md` 在每次 ingest 后保持最新

---

## 核心研究问题

从 `meta/core_questions.md` 读取用户动态 Q 编号，不加载模板作者的示例方向。
