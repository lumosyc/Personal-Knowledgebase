# 画像字段与事实源

唯一可编辑事实源：工作区 `meta/learner_profile.json`。`socrates/learner_profile.md` 和 `meta/core_questions.md` 是自动生成摘要；对话更新应写增量 JSON 并调用保存脚本，不手动分散改三份。

顶层：`schema_version: 1`、`updated`（脚本生成）、`identity`、`goals`、`preferences`、`onboarding`、`provenance`、`deferred_fields`、`driving_questions`、`courses`。

| 字段 | 内容 |
|---|---|
| identity.display_name / background / domain | 称呼（可空）、背景、研究或学习方向；未知填 null |
| identity.strengths / gaps | 自述基础、待补强方向，字符串列表 |
| goals.mode | research / course / mixed，待定可 null |
| goals.description / success_criteria | 目标文字 / 可验证成果字符串列表 |
| goals.deadline / time_budget | 用户给的期限、可用时间；未知为 null |
| preferences.language / explanation_order / formula_depth / pace / feedback | 语言、讲解顺序、形式化深度、节奏、反馈偏好 |
| preferences.avoid / analogy_domains | 不喜欢的教学方式、熟悉类比领域；字符串列表 |
| onboarding.state / next_question | new / collecting / provisional / ready；下次待问内容，结束为 null |
| provenance | 路径 → `{kind, quote, date}`；kind 为 user-stated / observed / proposed |
| deferred_fields | 跳过或不确定的字段路径字符串列表；不是错误 |
| driving_questions | `{id: "Q1", text, key_concepts: [], status: "confirmed"}`；也可 provisional / retired |
| courses | `{slug: "linear-algebra", name: "线性代数", target_level: "L3"}` |

研究问题和课程列表按 id / slug 增量合并，未提到的条目保留；其他列表代表该字段新值。新问题用 max(Q 编号)+1，不能用已有编号表达不同的问题；改写同一问题保留 ID。停用标 retired，不删除历史引用。更换学习目标保留历史进度与旧课程，不清空知识库。

例如，用户说“我是医学工程本科生，想学懂信号处理，先中文讲”，本轮增量可以是：

```json
{
  "identity": {"background": "医学工程本科生", "domain": "信号处理"},
  "goals": {"mode": "course", "description": "学懂信号处理"},
  "preferences": {"language": "中文为主"},
  "onboarding": {"state": "collecting", "next_question": "目前最卡哪个主题？"},
  "provenance": {
    "identity.background": {"kind": "user-stated", "quote": "我是医学工程本科生", "date": "用户当地日期"},
    "preferences.language": {"kind": "user-stated", "quote": "先中文讲", "date": "用户当地日期"}
  }
}
```

这是格式示例，不是本用户画像。保存时填实际当地日期，不复制示例背景。
