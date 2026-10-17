# 原版功能复核报告

复核版本：1.0.1。日期：2026-10-14（Asia/Shanghai）。原版来源为用户指定的 Personal-Knowledgebase-main 文件夹。

## 结论与证明范围

**就功能规格和学习路径而言，原版各模块已保留，没有发现功能删除。** 原版是让 Claude Code 执行的一组 Markdown 指令、模板与文件工作流；GPT 版仍由模型执行这些工作流，只将入口改为 Codex 技能，并用问答生成用户配置。

“无损”如果指页面类型、知识流动、教学步骤、证据状态、日志归属和续学机制，本次对照支持完整迁移。如果指模型输出、每轮追问、解题正确率和教学效果 100% 相同，本次不能证明，也不作该承诺。

这份报告区分四类证据：逐文件内容对照、自动源文件与模板覆盖检查、真实文件保存测试、隔离插件安装测试。尚未做 GPT / Claude 同材料完整教学对照，也没有连接用户实际 Obsidian 库进行端到端测试。

## 功能逐项核对

| 原版功能 | 本版对应 | 复核结果 |
|---|---|---|
| raw → 结构化 → 命题化 → 内化 | 保留 raw、wiki、claims/questions/connections、socrates/courses | 路径完整 |
| Research / Course / Socrates / Maintenance | AGENTS.md、入口技能、原详细工作流 | 四模式完整 |
| 原 13 个自然语言别名 | command_aliases.md 原表逐行保留 | 13/13 |
| Parking Ingest | 轻量 reading mission，不深读、不创建成批 concept | 完整 |
| Paper Learning | reading mission、paper spine、最多三阻塞概念、黑箱与可忽略内容、深入对话 | 完整 |
| Full Paper Ingest | 全文、paper、concept、claim、question、connection、索引与日志 | 完整 |
| Reading mission | 五种 role、L0–L4、Main Question、Must Understand ≤3、停止标准、读后成果 | 原模板正文完整 |
| Concept debt | parked / interface-level / needs deep study、最小接口、升级触发 | 原模板正文完整 |
| Idea Capture / Novelty Sweep | hypothesis 与下一步、关键词和近邻检索、有证据才谈创新 | 完整 |
| Claim ledger | 七种状态、支持证据、反证、假设、失效条件、实验和论文适用性 | 原模板正文完整 |
| Open questions / connections | 原问题状态、next trigger/action、非显然连接 | 完整；新增独立 connection 模板 |
| Research Query / Research Lint | 相关页综合、洞见保存、日志、孤立页、旧命题、Q 覆盖与 debt | 完整 |
| Course Ingest | 课程图、主题页、掌握记录、题库、实际错误、课程日志 | 原详细 course 工作流正文完全一致 |
| Course Ingest + Teach | 先入库，再主题图、诊断、提示阶梯与学习循环 | 完整 |
| Catch-up / Homework Prep | 即时目标、前置树、必需/有用/可跳过、薄弱项与类似题 | 完整 |
| 整目录防过载 | 先文件名与地图，再选子主题，单材料深读 | 完整 |
| 六步课程学习循环 | 最小概念 → 例题 → 独立练习 → 纠错 → 错题日志 → near-transfer | 完整 |
| 课程 L0–L5 / 提示 0–4 | 原等级与证据规则；新增“未评估”初始状态 | 完整且不混用尺度 |
| Research Socrates 七步 | 全局定位、问题、命题、假设、反例、用户 Q、全局重整合 | 完整 |
| 自适应颗粒度与思考时间 | 熟悉快进、不熟细问、why 回到直觉、单问后等回答、处理旁支再回主线 | 完整 |
| Feynman / Examiner | 用户讲、零基础同学追问；先题后回答再评分 | 完整 |
| 七类错误与纠错 | 错误类型、root cause、正确原则、重做题、复习日期 | 原模板正文完整 |
| 周复盘 | 原 weekly_review 模板、3–5 道跨主题题、下周优先级 | 保留并新增明确命令入口 |
| 会话保存、续接、归档 | progress、漏洞、下次起点、revision_notes、约 200 行归档 | 完整 |
| Markdown、frontmatter、wikilink、数学 | 原格式与命名、跨领域 domain、公式与条件 | 保留，预览按宿主适配 |
| 日志路由 | wiki / courses / socrates / meta 各负其责 | 完整 |
| Maintenance / shadow migration | 先诊断、按授权修复、复制验证、changelog 与 migration_log | 完整 |

各项对应的详细文件位置见 [迁移对应表](migration_reference.md)。上表“完整”表示功能指令与数据结构存在且已对照，不表示每项都已通过真实学习会话测试。

## 有意的适配，不隐藏为“逐字相同”

1. **运行入口**：原 CLAUDE.md / AGENTS.md 双副本改为 AGENTS.md + Codex 技能；功能详细文档与模板继续按需读取。
2. **初始化**：手填身份、背景、目标与学习风格改为渐进问答。JSON 是画像事实源，自动生成 Markdown 摘要和研究问题；允许未知、跳过、续问。
3. **研究问题**：模板作者的固定 Q1–Q6 及示例方向改为用户自己的稳定 Qn；纯课程模式可为空。已有 Q 引用不重编号。
4. **教学背景**：固定“强数学/CS 背景”改为按用户画像选择解释深度；完整数学条件与形式化内容不删减。
5. **写入授权**：用户已经请求开始、入库或更新时，必要本地保存不重复确认；未授权的删除、迁移和修复仍按授权边界处理。
6. **旧路径与协议冲突**：统一 mastery_tracker.md、error_log.md、wiki/claims/index.md；课程第 3 级仅局部解、第 4 级全解加迁移题；复杂公式预览依宿主能力。
7. **临时清理**：限制为本次登记文件，保留未完成画像草稿，防止清掉其他会话资料；临时文件管理本身保留。
8. **Obsidian 链接**：将遗留 redirect 中的 `../socrates/` 改为 vault 根相对的 `socrates/`；学习记录的权威目录不变。实际应用内呈现仍需用户库验证。

## 实际复核证据

- 核对原版 **57 个文件**的 SHA256，与此前源清单一致；没有改动原版目录。
- 原 **13 个模板**的全部正文经必要名称/路径替换后逐一相等，原 frontmatter 字段没有丢失；新增字段仅补足通用元数据。
- 核对 **8 个核心工作流与教学文件**；原章节全部存在，对差异逐段检查。其中详细 `meta/workflows/course.md` 与原版内容完全一致。
- 原 **13 个别名分发表条目**逐行存在；新增费曼、周复盘、画像更新和续学入口。
- 插件内模板与提供的工作区协议同步；画像与已有原料没有在本次文档修改中重置。
- **10 项真实文件行为测试**通过，见验证记录。模型知识页编辑仍由 Codex 文件工具完成，并非所有写操作都由画像脚本包办。
- 最终 **1.0.1** 版本在隔离 Codex 配置中安装、启用及技能文件识别成功；未改变当前账户的插件安装配置。

自动覆盖检查的明细保存在发行包 `audit-results.json`。它是源文件与结构覆盖证据，不是教学效果评分。

## 尚未证明的能力边界

实际 GPT / Claude 教学一致性；用户的扫描 PDF / OCR；联网文献搜索完整性；长时间多会话教学；用户现有 Obsidian 仓库及第三方插件；进程意外终止后的全自动跨文件恢复，均未完成真实端到端验证。README 已说明这些边界，没有将它们写成已验证能力。

本次提供的是本地 Codex 技能插件及同文件夹 Obsidian 使用方式。没有添加 Obsidian 内聊天面板、实时监听或后台自动整理，也没有未经授权操作现有 Obsidian 笔记库。
