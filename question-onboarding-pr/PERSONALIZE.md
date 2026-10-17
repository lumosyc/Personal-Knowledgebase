# PERSONALIZE —— clone 后要改的地方

clone 下来后，按这份清单把所有占位符换成你自己的内容就能用了。占位符统一是中括号形式（如 `[你的名字]`），方便全局搜索。改完后跑一下最底下的「自检」确认没漏。

> 提示：大部分内容性文件（`wiki/`、`courses/`、`socrates/progress.md` 等）**不需要手填** —— 它们由 Claude Code 在你使用时自动维护，初始是空 stub。你只需要改下面这几处「画像 / 身份」类文件。

---

## 问答式初始化（可选）

不想逐个编辑文件时，可以在仓库根目录启动所用的 AI 工具，并发送：

> 请通过提问帮我完成个性化初始化，一次问一个问题，先复用我已经提供的信息；不确定的内容先跳过，写入前给我确认。

AI 按下面的字段清单完成初始化，无需安装额外插件或 skill：

1. 先检查 `CLAUDE.md`、`AGENTS.md` 和 `socrates/learner_profile.md` 的现有信息，只询问会影响学习目标或教学方式的缺口，不覆盖用户未要求更改的已填内容。
2. 每次只问一个问题，按需了解称呼或化名、学习背景、目标与研究方向、语言和学习偏好；研究问题尚不清楚时，可以给出候选供用户选择，不把建议当成已确认信息。
3. 允许回答“不确定”“跳过”或“先开始学习”。暂缓字段保留占位符，后续再补；不编造个人信息，也不把自述熟悉度当成已验证的掌握程度。
4. 汇总答案并列出拟修改的文件和字段，按现有写入规则取得确认后，只填写下方清单中的对应内容：同步 `CLAUDE.md` / `AGENTS.md` 的身份、研究方向和核心问题，填写 `socrates/learner_profile.md`，并同步 `socrates/system.md` 中的学生称呼。若用户已明确授权自动填写，无需重复确认。
5. 保留核心问题的已有编号和引用；初始化后简要说明已填写与待补充的项目，再进入用户选择的学习任务。以后可通过对话修改相关字段，无需重做整套问答。

手动填写仍然可用。初始化不修改 `raw/`、教学规则、模板或已有学习记录；下方的署名、版权和其他选填项不在自动填写范围内。

---

## 1. 必填

| 文件 | 占位符 / 字段 | 填什么 |
|---|---|---|
| `CLAUDE.md` + `AGENTS.md` | 标题 `[你的名字]` | 你的名字 / 化名（两份要一致，内容本就相同）|
| `CLAUDE.md` + `AGENTS.md` | §1 Identity `[在这里填你的研究方向 ...]` | 一两句话描述你的研究 / 学习领域 |
| `CLAUDE.md` + `AGENTS.md` | §7 Core Research Questions 表 | 换成你自己的 driving questions（Q1、Q2…）。这些编号会被各 wiki 页 frontmatter 的 `questions:` 引用。表下有注释掉的格式示例可参考 |
| `socrates/learner_profile.md` | `[你的学习背景]` / `[你的学习目标]` / `[你的语言偏好]` / `[你的学习偏好]` | 你的背景、目标、语言偏好、学习风格。填得越具体，苏格拉底模式越贴合你 |
| `socrates/system.md` | `学生（[你的名字]）`（Feynman Mode 一节）| 你的名字 / 化名 |

## 2. 选填

| 文件 | 占位符 / 字段 | 填什么 |
|---|---|---|
| `LICENSE` + `README.md` | 署名 `Erber` | 如果这是你 fork 的，把 `Erber` 换成你自己的名字 / handle；版权年份按需更新 |
| `README.md` | `[你的知乎文章链接]` | 你介绍这个系统的文章 / 博客链接（没有就删掉那一行）|
| `socrates/course_mode.md` | 触发条件里的课程举例 | 可换成你正在上的课，纯举例，不影响功能 |
| `meta/architecture.md` / `meta/usage_guide.md` / `meta/workflows/maintenance.md` | "你（系统拥有者）" | 已是通用称呼，一般无需改；想个性化可替换 |

## 3. 不用动（Claude Code 自动维护，初始留空）

- `wiki/`（papers / concepts / questions / connections / claims / reading_missions / concept_debt）—— ingest 时自动生成
- `wiki/index.md`、`wiki/log.md`、`courses/index.md`、`courses/log.md` —— 自动更新
- `socrates/progress.md`、`socrates/revision_notes.md`、`socrates/session_archive.md` —— 会话时自动更新
- `meta/changelog.md`、`meta/migration_log.md`、`meta/phase_plan.md` —— 维护操作时自动更新
- `templates/` —— 页面模板，除非你想改默认格式，否则保持原样
- `examples/` —— 只是格式参考，可看可删

## 4. 放你自己的材料

把论文 / 课程材料放进 `raw/`（见 [raw/README.md](raw/README.md)）。`raw/` 和你之后生成的 `wiki/` 笔记都已被 `.gitignore` 忽略，不会误传到公开仓库。

---

## 自检

改完后在仓库根目录跑：

```bash
# 应该没有任何输出（占位符全部填完、没有残留示例署名）
grep -rn "\[你的\|\[在这里填" . --include=*.md | grep -v PERSONALIZE.md

# 确认 LICENSE/README 的署名已换成你（如果你 fork 了）
grep -rn "Erber" . --include=*.md LICENSE
```
