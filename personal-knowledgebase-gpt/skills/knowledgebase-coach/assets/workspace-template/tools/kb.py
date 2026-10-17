"""Local knowledgebase bootstrap and conversational-profile persistence. Stdlib only."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid
from datetime import datetime, timedelta, timezone

VERSION = "1.0.0"

def now():
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")

def dumps(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def safe(root, relative, allow_raw=False):
    root = Path(root).resolve()
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts or not rel.parts:
        raise ValueError("Only contained relative paths are allowed")
    target = (root / rel).resolve()
    if not target.is_relative_to(root):
        raise ValueError("Path escapes the selected knowledgebase")
    if rel.parts[0].lower() == "raw" and not allow_raw:
        raise ValueError("raw/ is immutable")
    cursor = root
    for part in rel.parts:
        cursor = cursor / part
        if cursor.is_symlink() or (hasattr(cursor, "is_junction") and cursor.is_junction()):
            raise ValueError("Linked paths cannot be written")
    return target

def owned(root):
    marker = safe(root, ".pkb.json")
    if not marker.exists() or read_json(marker).get("format") != "personal-knowledgebase-gpt":
        raise ValueError("Choose a GPT knowledgebase workspace, not the plugin cache or original Claude folder")

def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        staging.write_bytes(data)
        os.replace(staging, path)
    finally:
        if staging.exists():
            staging.unlink()

def transaction(root, writes):
    """Back up before replacing, roll back on a caught error; leave recovery record on crash."""
    root = Path(root).resolve()
    targets = {rel: safe(root, rel) for rel in writes}
    lock = safe(root, ".pkb.lock")
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(dumps({"started": now(), "pid": os.getpid()}))
    backup_rel = "meta/backups/" + datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:8]
    backup = safe(root, backup_rel)
    originals = {}
    manifest = {"state": "prepared", "started": now(), "files": []}
    try:
        backup.mkdir(parents=True)
        for rel, target in targets.items():
            old = target.read_bytes() if target.exists() else None
            originals[rel] = old
            if old is not None:
                atomic_write(safe(root, backup_rel + "/" + rel), old)
            manifest["files"].append({"path": rel, "existed": old is not None,
                "before_sha256": hashlib.sha256(old).hexdigest() if old is not None else None,
                "after_sha256": hashlib.sha256(writes[rel]).hexdigest()})
        atomic_write(backup / "transaction.json", dumps(manifest).encode("utf-8"))
        for rel, target in targets.items():
            atomic_write(target, writes[rel])
        manifest["state"] = "committed"
        atomic_write(backup / "transaction.json", dumps(manifest).encode("utf-8"))
    except Exception:
        for rel, old in originals.items():
            if old is None:
                if targets[rel].exists():
                    targets[rel].unlink()
            else:
                atomic_write(targets[rel], old)
        manifest["state"] = "rolled-back"
        if backup.exists():
            atomic_write(backup / "transaction.json", dumps(manifest).encode("utf-8"))
        raise
    finally:
        lock.unlink(missing_ok=True)
    return backup_rel

def initialize(root, template):
    root, template = Path(root).resolve(), Path(template).resolve()
    if not template.is_dir() or not (template / ".pkb.json").is_file():
        raise ValueError("Workspace template is missing")
    if root == template or root.is_relative_to(template):
        raise ValueError("Keep learner state outside the plugin template/cache")
    if root.exists() and any(root.iterdir()):
        owned(root)
        return {"status": "already-initialized", "root": str(root)}
    # Resolve every destination before creating anything; copy only shipped seed files.
    files = [p for p in template.rglob("*") if p.is_file()]
    for source in files:
        if source.is_symlink():
            raise ValueError("Template contains a symbolic link")
        safe(root, source.relative_to(template), allow_raw=True)
    root.mkdir(parents=True, exist_ok=True)
    made = []
    try:
        for source in files:
            target = safe(root, source.relative_to(template), allow_raw=True)
            atomic_write(target, source.read_bytes())
            made.append(target)
    except Exception:
        for target in made:
            target.unlink(missing_ok=True)
        raise
    return {"status": "initialized", "root": str(root), "next": "Begin conversational onboarding"}

def merge(old, patch):
    result = copy.deepcopy(old)
    for key, value in patch.items():
        if key in ("driving_questions", "courses"):
            identity = "id" if key == "driving_questions" else "slug"
            if not isinstance(value, list):
                raise ValueError(key + " must be a list")
            items = {item[identity]: copy.deepcopy(item) for item in result.get(key, [])}
            seen = set()
            for item in value:
                if not isinstance(item, dict) or identity not in item:
                    raise ValueError(key + " entries require " + identity)
                item_id = item[identity]
                if not isinstance(item_id, str) or item_id in seen:
                    raise ValueError("Duplicate or invalid stable identifier")
                seen.add(item_id)
                items[item_id] = merge(items.get(item_id, {}), item)
            result[key] = list(items.values())
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result

def validate(profile):
    if profile.get("schema_version") != 1:
        raise ValueError("Unsupported profile schema")
    for section in ("identity", "goals", "preferences", "onboarding", "provenance"):
        if not isinstance(profile.get(section), dict):
            raise ValueError("Invalid section: " + section)
    if profile["onboarding"].get("state") not in ("new", "collecting", "provisional", "ready"):
        raise ValueError("Invalid onboarding state")
    if profile["goals"].get("mode") not in (None, "research", "course", "mixed"):
        raise ValueError("Invalid learning mode")
    for key in ("background", "domain", "display_name"):
        if not isinstance(profile["identity"].get(key), (str, type(None))):
            raise ValueError("Identity fields must be text or null")
    for section, key in (("identity", "strengths"), ("identity", "gaps"),
                         ("goals", "success_criteria"), ("preferences", "avoid"),
                         ("preferences", "analogy_domains")):
        if not isinstance(profile[section].get(key), list) or not all(isinstance(x, str) for x in profile[section][key]):
            raise ValueError(section + "." + key + " must be a text list")
    for key in ("description", "deadline", "time_budget"):
        if not isinstance(profile["goals"].get(key), (str, type(None))):
            raise ValueError("Goal fields must be text or null")
    for key in ("language", "explanation_order", "formula_depth", "pace", "feedback"):
        if not isinstance(profile["preferences"].get(key), (str, type(None))):
            raise ValueError("Preference fields must be text or null")
    if not isinstance(profile.get("deferred_fields"), list) or not all(isinstance(x, str) for x in profile["deferred_fields"]):
        raise ValueError("deferred_fields must be a text list")
    for field, evidence in profile["provenance"].items():
        if not isinstance(evidence, dict) or evidence.get("kind") not in ("user-stated", "observed", "proposed"):
            raise ValueError("Provenance requires kind: user-stated, observed, or proposed")
    for q in profile.get("driving_questions", []):
        if not re.fullmatch(r"Q[1-9][0-9]*", q.get("id", "")) or not isinstance(q.get("text"), str):
            raise ValueError("Research questions require stable Qn IDs and text")
        if q.get("status") not in ("confirmed", "provisional", "retired"):
            raise ValueError("Invalid research question status")
        if not isinstance(q.get("key_concepts"), list) or not all(isinstance(x, str) for x in q["key_concepts"]):
            raise ValueError("key_concepts must be a text list")
    for course in profile.get("courses", []):
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", course.get("slug", "")):
            raise ValueError("Course slug must be lowercase kebab-case")
        if not isinstance(course.get("name"), str) or course.get("target_level") not in tuple("L" + str(x) for x in range(6)):
            raise ValueError("Course requires name and target_level L0-L5")
    if profile["onboarding"]["state"] == "ready" and (not profile["goals"].get("description") or not profile["goals"].get("mode")):
        raise ValueError("Ready requires a goal and learning mode; use provisional when undecided")

def text_value(value):
    if value is None or value == "" or value == []:
        return "尚未确定"
    if isinstance(value, list):
        return "；".join(map(str, value))
    return str(value)

def cell(value):
    return text_value(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")

def render_profile(p):
    rows = ["# 学习者画像", "", "> 由对话自动生成；事实源为 meta/learner_profile.json。", "", "## Background"]
    for key, label in (("display_name", "称呼"), ("background", "背景"), ("domain", "方向"), ("strengths", "已有基础"), ("gaps", "自述薄弱点")):
        rows.append(f"- {label}：{text_value(p['identity'].get(key))}")
    rows.extend(["", "## Learning Goals"])
    for key, label in (("mode", "学习模式"), ("description", "目标"), ("success_criteria", "可验证成果"), ("deadline", "期限"), ("time_budget", "时间预算")):
        rows.append(f"- {label}：{text_value(p['goals'].get(key))}")
    rows.extend(["", "## Preferred Language", "- " + text_value(p["preferences"].get("language")), "", "## Learning Style"])
    for key, label in (("explanation_order", "讲解顺序"), ("formula_depth", "公式深度"), ("pace", "节奏"), ("feedback", "反馈方式"), ("avoid", "希望避免"), ("analogy_domains", "熟悉的类比领域")):
        rows.append(f"- {label}：{text_value(p['preferences'].get(key))}")
    rows.extend(["", "## Onboarding", "- 状态：" + p["onboarding"]["state"], "- 下次补充：" + text_value(p["onboarding"].get("next_question")),
                 "- 暂缓字段：" + text_value(p.get("deferred_fields")), "", "## 画像依据", "用户自述、教学观察和暂定建议分开保存；不把自述熟悉度当作掌握证据。", ""])
    rows.extend(["| 字段 | 依据类型 | 原话或表现 | 日期 |", "|---|---|---|---|"])
    for field, source in p["provenance"].items():
        rows.append(f"| {cell(field)} | {cell(source['kind'])} | {cell(source.get('quote'))} | {cell(source.get('date'))} |")
    return "\n".join(rows) + "\n"

def render_questions(p):
    lines = ["# 核心研究问题", "", "编号稳定：新增使用新编号；停用标记 retired，历史页面引用不重编号。", "", "| ID | Question | Key concepts | Status |", "|---|---|---|---|"]
    for q in p["driving_questions"]:
        lines.append(f"| {q['id']} | {cell(q['text'])} | {cell(q['key_concepts'])} | {q['status']} |")
    if not p["driving_questions"]:
        lines.extend(["", "目前未设定研究问题。纯课程学习可保持为空；研究时通过对话补充。"])
    return "\n".join(lines) + "\n"

def update_profile(root, patch_file):
    root = Path(root).resolve()
    owned(root)
    old = read_json(safe(root, "meta/learner_profile.json"))
    patch = read_json(Path(patch_file))
    if not isinstance(patch, dict):
        raise ValueError("Profile patch must be an object")
    permitted = {"identity", "goals", "preferences", "onboarding", "provenance", "driving_questions", "courses", "deferred_fields"}
    if set(patch) - permitted:
        raise ValueError("Patch contains unsupported fields")
    new = merge(old, patch)
    new["updated"] = now()
    validate(new)
    writes = {"meta/learner_profile.json": dumps(new), "socrates/learner_profile.md": render_profile(new),
              "meta/core_questions.md": render_questions(new)}
    course_index = safe(root, "courses/index.md").read_text(encoding="utf-8")
    for course in new["courses"]:
        slug, name = course["slug"], course["name"]
        for template, filename in (("course_map", "course_map"), ("mastery_tracker", "mastery_tracker")):
            rel = f"courses/{slug}/{filename}.md"
            if not safe(root, rel).exists():
                content = safe(root, f"templates/course/{template}.md").read_text(encoding="utf-8")
                content = content.replace('title: ""', "title: " + json.dumps(name, ensure_ascii=False)).replace('course: ""', "course: " + json.dumps(slug))
                content = content.replace("YYYY-MM-DD", now()[:10]).replace("[COURSE]", name)
                # No mastery level may be inferred from onboarding or reading alone.
                if template == "mastery_tracker":
                    content = content.replace("| | L3 | L0 | | | | |", f"| 待诊断 | {course['target_level']} | 未评估 | 尚无作答证据 | 待诊断 | 首次诊断 | 待安排 |")
                writes[rel] = content
        for filename, title in (("error_log", "错题与知识漏洞"), ("problem_bank", "习题库")):
            rel = f"courses/{slug}/{filename}.md"
            if not safe(root, rel).exists():
                writes[rel] = f"# {name} — {title}\n\n尚无记录。只有实际作答后才填入表现。\n"
        rel = f"courses/{slug}/topic_pages/.gitkeep"
        if not safe(root, rel).exists():
            writes[rel] = ""
        link = f"[[courses/{slug}/course_map]]"
        if link not in course_index:
            course_index += f"\n- {cell(name)}：{link}；[[courses/{slug}/mastery_tracker]]\n"
    if course_index != safe(root, "courses/index.md").read_text(encoding="utf-8"):
        writes["courses/index.md"] = course_index
    log_path = safe(root, "meta/profile_log.md")
    log = log_path.read_text(encoding="utf-8") if log_path.exists() else "# 画像变更记录\n"
    writes["meta/profile_log.md"] = log + f"\n## {now()}\n- 更新字段：{', '.join(patch)}\n- 初始化状态：{old['onboarding']['state']} → {new['onboarding']['state']}\n"
    backup = transaction(root, {rel: data.encode("utf-8") for rel, data in writes.items()})
    return {"status": "saved", "state": new["onboarding"]["state"], "files": list(writes), "backup": backup}

def lint(root):
    root = Path(root).resolve()
    owned(root)
    profile = read_json(safe(root, "meta/learner_profile.json"))
    validate(profile)
    pages = []
    for directory in ("wiki", "courses", "socrates"):
        for page in (root / directory).rglob("*.md"):
            if page.is_symlink() or not page.resolve().is_relative_to(root):
                raise ValueError("Linked pages are not linted")
            pages.append(page)
    by_stem = {}
    by_path = {}
    for page in pages:
        by_stem.setdefault(page.stem, []).append(page)
        by_path[page.relative_to(root).with_suffix("").as_posix()] = page
    inbound = {page: 0 for page in pages}
    issues = []
    core_ids = {q["id"] for q in profile["driving_questions"]}
    for page in pages:
        content = page.read_text(encoding="utf-8-sig")
        for link in re.findall(r"\[\[([^\]]+)\]\]", content):
            key = link.split("|", 1)[0].split("#", 1)[0].removesuffix(".md")
            if not key or key.startswith("raw/") or key.endswith("/"):
                continue
            if key.startswith(("./", "../")):
                relative_target = (page.parent / (key + ".md")).resolve()
                matches = [relative_target] if relative_target in inbound else []
            else:
                matches = [by_path[key]] if key in by_path else by_stem.get(key, [])
            if not matches:
                issues.append({"type": "broken-link", "file": str(page.relative_to(root)), "target": key})
            elif len(matches) > 1:
                issues.append({"type": "ambiguous-link", "file": str(page.relative_to(root)), "target": key})
            elif matches[0] != page:
                inbound[matches[0]] += 1
        match = re.search(r"^questions:\s*\[([^\]]*)\]", content, re.MULTILINE)
        if match:
            for qid in re.findall(r"\bQ\d+\b", match.group(1)):
                if qid not in core_ids:
                    issues.append({"type": "unknown-question", "file": str(page.relative_to(root)), "target": qid})
    for page, count in inbound.items():
        if page.parent.name in ("papers", "concepts") and count == 0:
            issues.append({"type": "orphan", "file": str(page.relative_to(root))})
    # Semantic checks remain a model task: evidence contradictions, debt promotion, log routing.
    return {"status": "checked", "profile_state": profile["onboarding"]["state"], "pages": len(pages), "issues": issues,
            "semantic_checks_remaining": ["claim evidence", "concept debt promotion", "question coverage", "log routing", "index completeness"]}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--root", required=True)
    init.add_argument("--template", required=True)
    profile = sub.add_parser("profile")
    profile.add_argument("--root", required=True)
    profile.add_argument("--patch", required=True)
    for command in ("status", "lint"):
        item = sub.add_parser(command)
        item.add_argument("--root", required=True)
    args = parser.parse_args(argv)
    if args.command == "init":
        result = initialize(args.root, args.template)
    elif args.command == "profile":
        result = update_profile(args.root, args.patch)
    elif args.command == "lint":
        result = lint(args.root)
    else:
        owned(Path(args.root).resolve())
        p = read_json(safe(args.root, "meta/learner_profile.json"))
        validate(p)
        result = {"root": str(Path(args.root).resolve()), "state": p["onboarding"]["state"], "next_question": p["onboarding"].get("next_question"), "updated": p["updated"]}
    print(dumps(result), end="")

if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(dumps({"status": "error", "message": str(exc)}), file=sys.stderr, end="")
        sys.exit(1)
