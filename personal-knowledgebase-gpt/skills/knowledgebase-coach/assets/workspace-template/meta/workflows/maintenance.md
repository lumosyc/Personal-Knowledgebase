---
title: "Maintenance Mode — Detailed Workflow"
type: workflow
created: 2026-05-10
updated: 2026-05-10
---

# Maintenance Mode — Detailed Workflow

Loaded by the Mode Router when the user asks to lint, migrate, update architecture, create templates, or modify logs.

**Always load first**: `meta/phase_plan.md` → `meta/migration_log.md` as needed.

---

## Hard Rules

- **Never modify `raw/`**. It is the immutable source of truth.
- Do not delete existing files unless explicitly instructed by you (the system owner).
- Prefer **shadow migration** (copy first, verify, then remove legacy) over direct moves.
- Record all architecture changes in `meta/changelog.md`.
- Record migration details in `meta/migration_log.md`.
- Keep `wiki/index.md` and `courses/index.md` updated after every ingest.
- Do not mix course management records into research wiki files unless the concept has genuine research relevance.
- When in doubt about which log to update, prefer more specific (course log over wiki log; course error log over general progress).

---

## Light Lint

Triggers: "帮我整理系统"

Check and report the following — do **not** modify files until confirmed:

1. Stale references (wikilinks pointing to files that no longer exist or moved).
2. Misplaced files (files in wrong directories per architecture).
3. Log routing errors (course content in wiki log, research content in course log).
4. Broken wikilinks.
5. Concept debt entries that now warrant a full page.
6. Orphan pages (no inbound wikilinks).
7. Thin 当前核心 Q（见 meta/core_questions.md） coverage.

Report in a structured format with actionable fixes. Ask for confirmation before making any changes.

---

## Architecture Cleanup

When performing structural changes:

1. Use shadow migration: create the new file, verify, then remove the old one (only if authorized).
2. Update `meta/changelog.md` with a structured entry.
3. Update `meta/migration_log.md` with phase details.
4. Update any affected index files (`wiki/index.md`, `courses/index.md`).
5. Update redirect stubs if a file was moved.

---

## Changelog Rules

- Every architecture or system-level change must be recorded in `meta/changelog.md`.
- Format: date header + type + what changed + what was NOT changed + what comes next.
- Newest entries at the top.
- Content-level changes (paper ingests, concept updates) go to `wiki/log.md` or `courses/log.md`, not here.

---

## Change Log Update

Triggers: "帮我记录这次修改"

- Update `meta/changelog.md` and `meta/migration_log.md` as appropriate.
- Do not modify unrelated files.
- Use the `templates/meta/change_entry.md` format.
