---
title: "Research Mode — Detailed Workflow"
type: workflow
created: 2026-05-10
updated: 2026-05-10
---

# Research Mode — Detailed Workflow

Loaded by the Mode Router when the user asks about a paper, research idea, claim, literature, concept, or open question.

**Always load first**: `wiki/index.md` → relevant wiki pages as needed.

---

## Paper Ingest

When told to ingest a research source from `raw/`:

1. Read the full source.
2. For nontrivial papers, create a **reading mission** first (`templates/research/reading_mission.md`): identify role, target level, and main question before writing the summary.
3. Decide the paper's role: `survey` / `ingredient` / `nearest prior work` / `baseline` / `theory foundation`.
4. Decide target reading level: L0 / L1 / L2 / L3 / L4.
5. Create or update the paper summary page in `wiki/papers/` using `templates/research/paper.md`.
6. For each key concept:
   - If concept page exists → update it, note the source.
   - If concept page doesn't exist → create it from `templates/research/concept.md`.
   - If the concept is peripheral → record it as concept debt; do not create a full page now.
7. If the source supports, weakens, or motivates a specific research claim, record it in `wiki/claims/index.md`.
8. Create or update question pages (`wiki/questions/`) when new open problems arise.
9. Create connection pages (`wiki/connections/`) when the source reveals non-obvious links between existing concepts.
10. Tag which core research questions (**当前核心 Q（见 meta/core_questions.md）**) the source speaks to.
11. Update `wiki/index.md`.
12. Append entry to `wiki/log.md`: `## [YYYY-MM-DD] ingest | Source Title`.

---

## Research Query

When asked a research question:

1. Read `wiki/index.md` to identify relevant pages.
2. Load and read those pages.
3. Synthesize an answer using `[[wikilinks]]` to source pages.
4. If a genuinely new connection or insight emerges, offer to save it as a question, connection, or claim page.
5. If a new connection or insight was saved, append a query log entry to `wiki/log.md` (format below).

### Research Query Log Entry Format

```
## [YYYY-MM-DD] query | <Topic or Question Title>

**Question**: <the question asked, in one sentence>

**Conclusion**: <the answer or synthesis reached; if inconclusive, state what is still open>

**Sources / pages touched**: <wikilinks to pages read>

**New connection**: <if a connection/claim/question page was created, link it here; otherwise "none">

**Next action**: <follow-up reading, experiment, or claim status change; otherwise "none">
```

Only log if the session produced a conclusion or a saved artifact (new page, updated claim). Skip trivial lookups.

---

## Research Lint

When asked to lint the research wiki:

1. Check for orphan pages (no inbound wikilinks).
2. Check for concepts mentioned in text that lack their own page.
3. Check for stale or contradicted claims (newer sources may weaken older ones).
4. Check for thin coverage across **当前核心 Q（见 meta/core_questions.md）** — note which questions are underrepresented.
5. Check concept debt: flag accumulated concept debt that now warrants a full page.
6. Suggest specific papers or topics to investigate for identified gaps.
7. Report in a structured format with actionable fixes.

---

## Parking Ingest

Triggers: "ingest 这篇论文，我后面再看" · "ingest this paper for later" · "先放进系统，后面再读" · "暂时不想看懂"

- Do **not** deep-read. Do not create a long paper summary.
- Create or update a lightweight reading mission in `wiki/reading_missions/index.md` (role, target level, why it may matter, stopping criterion).
- Add concept debt only if obvious.
- Optionally add a short entry to `wiki/log.md`.
- Do **not** create concept pages. Do **not** modify `raw/`.
- Before writing: report planned updates; execute when already authorized by the user task, otherwise ask once.

---

## Paper Learning (Learning Ingest)

Triggers: "我想学习这篇论文" · "带我读这篇论文" · "帮我看懂这篇论文" · "learn this paper"

- Create a reading mission first (role, target level).
- Extract paper spine: problem / bottleneck / core idea / mechanism / main claim / evidence / limitation.
- Identify at most 3 blocking concepts. Explicitly state what can be treated as a black box.
- Ask whether to enter Socrates Mode for deep understanding.
- Do **not** start with a long full summary.

---

## Full Paper Ingest

Triggers: "帮我正式 ingest 这篇论文"

Follow the full Paper Ingest workflow above. Sequence:
reading mission → `wiki/papers/` page → update concept pages → update claims/questions/connections → update `wiki/index.md` and `wiki/log.md`.

Use `templates/research/`.

---

## Idea Capture

Triggers: "把这个 idea 放进系统"

- Create/update a claim or question entry (`wiki/claims/index.md` or `wiki/questions/`).
- Mark status as `hypothesis` unless supported by existing sources.
- Add a next action.
- Do **not** overdevelop into a full paper plan unless asked.

---

## Novelty Sweep

Triggers: "帮我判断这个 idea 有没有人做过"

- Decompose idea into search dimensions.
- Identify nearest prior work categories and possible keywords / alternative framings.
- Do **not** claim novelty without evidence.
- Create reading missions if relevant papers emerge.
- Report intended writes; follow the authorization rules in AGENTS.md.
