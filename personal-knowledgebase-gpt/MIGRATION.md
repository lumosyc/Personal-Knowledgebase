# 功能与学习路径迁移对应表

| 原版能力 | GPT / Codex 版位置与行为 |
|---|---|
| raw 不可变源材料 | 原目录职责保留；bootstrap 只创建新模板原料目录，既有源材料只读 |
| 四层知识流 | raw → paper/concept → claim/question/connection → socrates/course 完整保留 |
| 四模式路由 | AGENTS.md + knowledgebase-coach → 原版 meta/workflows 按需加载 |
| 13 个自然语言别名 | command_aliases.md 完整保留，并覆盖 Feynman 与周复盘 |
| Parking Ingest | 轻量任务、可选 debt，不深读、不建成批概念页 |
| Paper Learning | mission → spine → 最多三阻塞概念 → 黑箱 → 深入互动 |
| Full Paper Ingest | 全文、摘要、概念、命题、问题、连接、索引与日志 |
| Reading Missions | 五种 role、阅读 L0–L4、核心问题、停止条件与读后成果 |
| Concept debt | parked / interface-level / needs deep study，触发深读与升级 |
| Idea Capture / Novelty Sweep | hypothesis 与下一步；检索维度、近邻工作、证据状态；不无证声称创新 |
| Claim ledger | 七种状态、支持与反证、假设、失效条件、实验和论文可用性 |
| 开放问题 | 原版全部 question 状态和 next trigger / next action |
| Research Query / Lint | 本地相关页综合、洞见保存、孤立页/证据/覆盖/debt 检查 |
| Course Ingest | 地图、主题、题库、掌握、真实错题与课程日志 |
| Course Ingest + Teach | 先入库，后 topic map / 诊断 / hint ladder / 学习循环 |
| Catch-up / Homework Prep | 即时目标、前置树、must/useful/skip、诊断和分级提示 |
| 整目录防过载 | 先文件名与地图，选择一个子主题，再读单文件 |
| Course learning loop | 最小概念 → 例题 → 独立练习 → 纠错 → error log → near-transfer |
| 课程掌握 L0–L5 | 原等级与证据原则保留，新增未评估，不把自述或 ingest 当能力 |
| Research Socrates 七步 | 定位 → 问题 → 命题 → 假设 → 反例 → 用户 Q → 全局重整合 |
| Course Hint Ladder 0–4 | 一次卡住提升一级，独立继续后归零；第 3 级局部解、第 4 级全解+迁移 |
| Socratic adaptive granularity | 熟悉快速推进，不熟细问，主动 why 回到直觉；一次一问、等回答 |
| Feynman / Examiner | 学生解释、同学追问；先题后答再评分，不抢答 |
| 错误分类 | 原七类错误、root cause、正确原则、重做与复习日期 |
| 会话收尾与续学 | 进度、知识漏洞、下一起点、教学改进、约 200 行归档、临时清理 |
| 模板与数学格式 | 原 13 个模板全部保留，补齐 frontmatter；新增 connection 模板；宿主预览适配 |
| Markdown / Obsidian wikilink | YAML、命名、跨领域概念、链接与索引全部保留 |
| Maintenance / shadow migration | 只读 lint 报告、授权修复、复制验证、changelog 与 migration log |
| 日志路由 | wiki / courses / socrates / meta 保留独立职责 |
| 手改 PERSONALIZE 与双入口 | 替换为对话初始化，JSON 单源 + 自动摘要，无须手改身份与系统文件 |
| 固定研究作者身份与 Q1–Q6 | 去除默认个人背景；动态稳定 Qn，无研究目标时允许为空 |

## 为迁移修正的历史不一致

源材料中部分文档还引用 mastery.md、error-log.md、wiki/claims.md 和旧 Phase 4 迁移计划。本版统一为 mastery_tracker.md、error_log.md、wiki/claims/index.md；保留研究与教学工作流本身。

原 course_mode 一处把最小解与完整解混写。采用其明确 Hint Ladder 定义：第 3 级只给卡住的一步，第 4 级才完整解加 near-transfer。

原使用指南含模板作者的六个具体研究问题；替换为用户问答生成的 core_questions，不把模板内容当作本用户资料。强数学/CS 假设改为按画像适配，完整形式化内容仍保留。

原“每次写文件询问”规则依其显式执行例外执行：用户已请求开始、入库或更新则必要保存不重复确认。未经授权的维护修复、删除和迁移仍按相应授权边界处理。

原 MIT License 完整保留，不把作者版权替换为使用者姓名。原项目未就地编辑。source-manifest.json 记录所有读入源文件哈希及模板覆盖便于核对。
