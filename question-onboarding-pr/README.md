# Personal Knowledgebase —— 个人研究 + 学习知识系统

一个由 [Claude Code](https://claude.com/claude-code) 驱动的个人知识系统：把你读的论文、上的课、冒出来的研究想法，**一层层从「原料」沉淀成「成品」**，并用苏格拉底 / 费曼式对话帮你真正学懂、内化。你只管喂材料和提问，Claude Code 按既定结构把它整理进 wiki、追踪你的研究命题、在你薄弱的地方追问你。

灵感来自 **Andrej Karpathy 的 LLM Wiki**「用 LLM 维护个人 wiki」的思路，以及**吴乐旻的苏格拉底学习法**（以提问驱动理解，而非灌输答案）。

> 这是一个**模板**：clone 下来，按 [PERSONALIZE.md](PERSONALIZE.md) 填好你自己的信息，就能在自己的领域里用。

---

## 它解决什么

- 读了很多论文，但读完就忘、串不起来 → 自动沉淀成 concept / paper / claim 页，互相 wikilink。
- 有研究想法但不知道有没有人做过、值不值得做 → idea 进系统，追踪成 question / claim，标注证据状态。
- 上课 / 自学，想知道自己哪里没真懂 → 苏格拉底 / 费曼模式追问你，记录错题与掌握度。

## 目录结构：raw 原料 → wiki 成品

两层核心：**`raw/` 放你喂进来的原料，`wiki/` 放系统整理出的成品**。

| 目录 | 作用 |
|---|---|
| `raw/` | 不可变原料：论文 PDF、网页剪藏、课程材料。系统**只读不改**。默认 `.gitignore`，不进公开仓库。|
| `wiki/` | 研究成品：concepts（概念）、papers（论文摘要）、questions（开放问题）、connections（跨概念连接）、claims（命题追踪）。|
| `courses/` | 课程学习：掌握度、错题日志、习题库、主题页。|
| `socrates/` | 苏格拉底 / 费曼教学系统：学习者画像、会话进度、教学改进。|
| `templates/` | 各类页面的模板。|
| `meta/` | 系统说明、工作流、变更日志。|
| `temp/` | 会话临时文件，用完即清。|

## 四层知识流动

材料进入系统后，会经过四层加工，逐层升华：

1. **摄取（raw/）** —— 把论文 / 剪藏 / 课程材料放进 `raw/`。
2. **结构化（wiki/papers + wiki/concepts）** —— 拆成论文摘要页和概念页，建立 wikilink。
3. **命题化（wiki/claims + questions + connections）** —— 提炼出可追踪的研究命题、开放问题、跨概念连接，并标注证据状态。
4. **内化（socrates/ + courses/）** —— 用苏格拉底 / 费曼对话讲解、追问，用错题与掌握度表巩固，把「看过」变成「学会」。

每种页面长什么样，见 [examples/](examples/)（格式示例）。

---

## Quickstart

1. **Clone**
   ```bash
   git clone https://github.com/Erber102/Personal-Knowledgebase.git
   cd Personal-Knowledgebase
   ```
2. **个性化** —— 按 [PERSONALIZE.md](PERSONALIZE.md) 把占位符（名字、研究方向、driving questions、学习画像）填好。 也可以在启动后说：“请通过提问帮我完成个性化初始化，一次问一个问题，先复用我已经提供的信息；写入前给我确认。”详见 [问答式初始化](PERSONALIZE.md#问答式初始化可选)。
3. **启动 Claude Code** —— 在 `Personal-Knowledgebase/` 目录下运行 `claude`。系统提示词（`CLAUDE.md` / `AGENTS.md`）会自动加载。
4. **放原料** —— 把论文 / 课程材料丢进 `raw/`（见 [raw/README.md](raw/README.md)）。

### 怎么 ingest（自然语言触发，见 CLAUDE.md §5）

| 你说 | 系统做什么 |
|---|---|
| 「正式 ingest 这篇论文」 | 完整读一篇论文，生成 paper 页 + 相关 concept 页 + claims |
| 「我想学习这篇论文」 / 「带我读」 | 带读模式，边读边讲 |
| 「ingest 这篇论文，我后面再看」 | 先轻量入库（停车场），之后再细读 |
| 「把这个 idea 放进系统」 | 把一个研究想法登记成 question / claim |
| 「帮我 ingest 这节课」 | 把一节课材料整理进 `courses/` |

### 怎么用苏格拉底法

| 你说 | 系统做什么 |
|---|---|
| 「用 Socrates 模式问我」 | 以提问驱动，带你一步步想清楚某个主题 |
| 「考我」 | 出题检验掌握度，记录错题 |
| 「用 Feynman 模式检验[某概念]」 | 你来讲、它扮演零基础同学追问，暴露你没真懂的地方 |

---

## 需要填入的内容

所有 clone 后要改的文件和字段，集中列在 **[PERSONALIZE.md](PERSONALIZE.md)**，照着填即可，不用自己翻文件找。

## 致谢 / 延伸

- Andrej Karpathy —— LLM Wiki（用 LLM 维护个人 wiki 的思路）
- 吴乐旻 —— 苏格拉底学习法
- 这个系统的介绍文章：[如何用AI学会所有东西：基于Obsidian+Claude Code的个人知识库构建](https://zhuanlan.zhihu.com/p/2033334385555010512)

## License

[MIT](LICENSE)
