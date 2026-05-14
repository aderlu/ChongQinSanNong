from __future__ import annotations

"""审计一份“绑定式 CRUD 决策文件”是否允许进入执行阶段。

本脚本是固定更新入口 `run_guarded_wiki_update.py` 的第二道门禁：

1. 第一关 `audit_governance_compliance.py` 负责检查治理体系是否完整；
2. 本脚本负责检查“这一次具体更新”是否被当前治理规则正确授权；
3. 通过后，固定入口才会真正执行 planned command 对应的更新脚本。

它检查的核心不是 Markdown 格式是否漂亮，而是以下安全语义：

- 决策文件是否存在于固定审计目录 `issues/crud_decisions/`；
- 决策文件是否包含“改什么、为什么改、旧数据怎么处理、风险是什么”；
- 生成决策时读取的治理文档 hash 是否仍然等于当前治理文档；
- 决策里写的 `Planned command` 是否和本次实际传入的更新命令完全一致；
- 高风险内容是否具备 A0/A1/规则卡等足够门槛；
- 删除、替换、降级、归档等操作是否写清安全说明。

因此，本脚本让 CRUD 决策文件从“人工说明”变成可机器验证的执行凭证。
"""

import argparse
import hashlib
import json
import re
import shlex
from datetime import datetime, timedelta, timezone
from pathlib import Path


WIKI_ROOT = Path(__file__).resolve().parents[2]
DECISION_DIR = WIKI_ROOT / "issues" / "crud_decisions"
TZ = timezone(timedelta(hours=8))

# 这些治理文档是决策生成前必须读取的规则来源。
# create_crud_decision.py 会把它们的 sha256 写入决策文件；
# 本脚本再重新计算 hash，确认“决策依据的规则版本”没有变。
GOVERNANCE_DOCS = {
    "WIKI_UPDATE_MANDATORY_SHORT_CARD.md": WIKI_ROOT / "WIKI_UPDATE_MANDATORY_SHORT_CARD.md",
    "WIKI_UPDATE_SCENARIO_SHORT_CARD.md": WIKI_ROOT / "WIKI_UPDATE_SCENARIO_SHORT_CARD.md",
    "WIKI_MAINTENANCE_GUIDE.md": WIKI_ROOT / "WIKI_MAINTENANCE_GUIDE.md",
    "WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md": WIKI_ROOT / "WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md",
}

# 决策文件必须具备的字段。
# 字段名统一转成小写后检查，所以模板中的大小写不会影响审计。
REQUIRED_KEYS = {
    "decision generated at",
    "governance documents read",
    "governance document hashes json",
    "crud template hash",
    "planned command",
    "target object type",
    "target object id/path",
    "intended action",
    "why this action is needed",
    "input source type",
    "old data exists",
    "old data handling",
    "authority level",
    "risk class",
    "source/fact anchor available",
    "runtime impact",
    "gold dataset impact",
    "deletion or replacement safety check",
    "final decision",
}

# 允许的 CRUD/维护动作集合。
# 任何新的动作类型都应先进入治理规则和模板，再加到这里。
ALLOWED_ACTIONS = {
    "create",
    "read",
    "update",
    "replace",
    "delete",
    "archive",
    "downgrade",
    "exclude",
    "rebuild",
    "migrate",
}

# 高风险类型需要更强的 authority gate。
# 例如 high_regulatory 不能只凭 SRC/A2/普通网页直接放行。
HIGH_RISK_CLASSES = {"drug_boundary", "high_regulatory", "withdrawal_mrl_residue", "food_safety"}
HIGH_RISK_AUTHORITIES = {"A0", "A1", "RC-RULE", "not applicable"}

# 替换和删除必须配套说明旧数据如何保留、降级、归档或排除。
# 这是为了避免医学/监管知识库里出现静默覆盖或静默删除。
REPLACE_OLD_HANDLING = {"supersede", "downgrade", "archive", "migrate", "exclude"}
DELETE_OLD_HANDLING = {"archive", "exclude", "delete", "migrate"}
NON_EMPTY_PLACEHOLDERS = {"", "todo", "tbd", "unknown"}


def sha256_file(path: Path) -> str:
    """计算文件 hash，用来验证治理文档是否还是决策生成时的版本。"""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def latest_decision() -> Path | None:
    """返回最近修改的决策文件。

    仅用于人工/兼容检查。固定更新入口应显式传入 `--decision`，
    避免误用“最新文件”授权错误更新。
    """
    if not DECISION_DIR.exists():
        return None
    decisions = [path for path in DECISION_DIR.glob("*.md") if path.is_file()]
    if not decisions:
        return None
    return sorted(decisions, key=lambda path: path.stat().st_mtime)[-1]


def parse_decision(text: str) -> dict[str, str]:
    """从 Markdown 列表项中抽取 `字段: 值`。

    决策文件是给人审计的 Markdown，但门禁需要机器可读字段。
    这里采用保守解析：只读取形如 `- Key: value` 的单行字段。
    """
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*-\s*([^:]+):\s*(.*)\s*$", line)
        if not match:
            continue
        fields[match.group(1).strip().lower()] = match.group(2).strip()
    return fields


def is_blank(value: str) -> bool:
    """判断必填字段是否仍是空值或占位符。"""
    return value.strip().lower() in NON_EMPTY_PLACEHOLDERS


def command_string(parts: list[str]) -> str:
    """把命令列表渲染成与 create_crud_decision.py 一致的审计字符串。"""
    return " ".join(shlex.quote(part) for part in parts)


def normalized_command(value: str) -> str:
    """标准化决策文件中的 planned command，降低 shell 引号差异造成的误报。"""
    try:
        return command_string(shlex.split(value))
    except ValueError:
        return value.strip()


def resolve_decision(path_text: str | None) -> Path | None:
    """解析决策文件路径。

    支持绝对路径、从当前工作目录解析的相对路径，以及以 `issues/`
    开头的 Wiki 内部路径。
    """
    if not path_text:
        return latest_decision()
    path = Path(path_text)
    if not path.is_absolute():
        path = (WIKI_ROOT / path).resolve() if path_text.startswith("issues/") else path.resolve()
    return path


def collect_issues(
    path: Path | None,
    actual_command: list[str] | None = None,
    allow_legacy: bool = False,
) -> tuple[dict[str, str], list[dict[str, str]]]:
    """执行 CRUD 决策的全部语义检查，并返回字段与问题列表。"""
    if path is None:
        return {}, [{"issue": "missing_crud_decision_file", "path": DECISION_DIR.as_posix()}]
    if not path.exists():
        return {}, [{"issue": "crud_decision_file_not_found", "path": path.as_posix()}]

    fields = parse_decision(path.read_text(encoding="utf-8"))
    issues: list[dict[str, str]] = []

    # legacy 模式只用于旧文件人工排查。真实 guarded update 不应开启它，
    # 因为没有治理 hash 和 planned command 的旧决策不能提供完整授权。
    required = REQUIRED_KEYS if not allow_legacy else REQUIRED_KEYS - {
        "decision generated at",
        "governance documents read",
        "governance document hashes json",
        "crud template hash",
        "planned command",
    }
    for key in sorted(required - set(fields)):
        issues.append({"issue": f"missing_required_field:{key}", "path": path.as_posix()})
    for key in sorted(required & set(fields)):
        if is_blank(fields[key]):
            issues.append({"issue": f"blank_required_field:{key}", "path": path.as_posix()})

    # 抽出后续规则要使用的字段，并统一大小写。
    action = fields.get("intended action", "").strip().lower()
    old_handling = fields.get("old data handling", "").strip().lower()
    authority = fields.get("authority level", "").strip()
    risk = fields.get("risk class", "").strip().lower()
    runtime_impact = fields.get("runtime impact", "").strip().lower()
    gold_impact = fields.get("gold dataset impact", "").strip().lower()
    final_decision = fields.get("final decision", "").strip().lower()
    safety = fields.get("deletion or replacement safety check", "").strip().lower()
    anchor = fields.get("source/fact anchor available", "").strip().lower()

    # 基础 CRUD 语义检查：动作是否合法、最终决策是否允许执行。
    if action and action not in ALLOWED_ACTIONS:
        issues.append({"issue": f"invalid_intended_action:{action}", "path": path.as_posix()})
    if final_decision != "allowed":
        issues.append({"issue": f"final_decision_not_allowed:{final_decision or 'blank'}", "path": path.as_posix()})
    if action == "replace" and old_handling not in REPLACE_OLD_HANDLING:
        issues.append({"issue": f"replace_requires_old_data_handling:{old_handling or 'blank'}", "path": path.as_posix()})
    if action == "delete" and old_handling not in DELETE_OLD_HANDLING:
        issues.append({"issue": f"delete_requires_safe_old_data_handling:{old_handling or 'blank'}", "path": path.as_posix()})
    if action in {"replace", "delete"} and "no referenced object will be silently deleted" not in safety:
        issues.append({"issue": "replace_or_delete_requires_reference_safety_statement", "path": path.as_posix()})

    # 高风险门禁：诊断、监管、药物、残留/食品安全等内容不能用低等级来源放行。
    if risk in HIGH_RISK_CLASSES and authority not in HIGH_RISK_AUTHORITIES:
        issues.append({"issue": f"high_risk_requires_authoritative_gate:{risk}:{authority or 'blank'}", "path": path.as_posix()})

    # 写入类动作必须明确有 source/fact anchor，否则不能进入执行阶段。
    if action in {"create", "update", "replace"} and anchor == "no":
        issues.append({"issue": "write_action_requires_source_or_fact_anchor", "path": path.as_posix()})

    # 某些治理工具本身的维护不一定直接影响 runtime/gold。
    # 但普通 source/fact/runtime 更新必须说明 runtime 或 gold dataset 影响。
    governance_only = (
        fields.get("target object type", "").strip().lower() in {"other", "export", "graph"}
        and authority == "not applicable"
        and risk == "not applicable"
    )
    if action in {"create", "update", "replace", "delete", "archive", "downgrade", "exclude", "rebuild", "migrate"} and not governance_only:
        if runtime_impact == "none" and gold_impact == "none":
            issues.append({"issue": "write_action_requires_runtime_or_gold_impact_assessment", "path": path.as_posix()})

    if not allow_legacy:
        # 验证治理文档 hash：如果规则在决策生成后变了，旧决策不能继续执行。
        raw_hashes = fields.get("governance document hashes json", "")
        try:
            docs = json.loads(raw_hashes)
        except json.JSONDecodeError:
            docs = []
            issues.append({"issue": "invalid_governance_document_hashes_json", "path": path.as_posix()})
        by_path = {doc.get("path"): doc.get("sha256") for doc in docs if isinstance(doc, dict)}
        for doc_name, doc_path in GOVERNANCE_DOCS.items():
            expected = by_path.get(doc_name)
            if not expected:
                issues.append({"issue": f"governance_hash_missing:{doc_name}", "path": path.as_posix()})
            elif not doc_path.exists() or expected != sha256_file(doc_path):
                issues.append({"issue": f"governance_hash_mismatch:{doc_name}", "path": path.as_posix()})

        if actual_command is not None:
            # 命令绑定检查：决策批准的是 planned command，真实执行必须完全匹配。
            # 这可以防止“拿 A 决策去执行 B 脚本”。
            planned = normalized_command(fields.get("planned command", ""))
            actual = command_string(actual_command)
            if planned != actual:
                issues.append(
                    {
                        "issue": "planned_command_mismatch",
                        "path": path.as_posix(),
                        "planned": planned,
                        "actual": actual,
                    }
                )

    return fields, issues


def parse_args() -> argparse.Namespace:
    """解析决策路径和可选的实际更新命令。

    `command` 使用 REMAINDER 接收 `--` 后面的完整命令，避免 argparse
    把更新脚本自己的参数误认为审计脚本参数。
    """
    parser = argparse.ArgumentParser(description="Audit a bound swine Wiki CRUD decision file.")
    parser.add_argument("--decision", help="Decision file path. Defaults to latest for legacy/manual checks.")
    parser.add_argument("--allow-legacy", action="store_true", help="Allow old decision files without governance hashes.")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Optional actual update command after --.")
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    return args


def main() -> int:
    """运行审计并输出 JSON；退出码 0 表示本次决策可进入执行阶段。"""
    args = parse_args()
    decision = resolve_decision(args.decision)
    fields, issues = collect_issues(decision, args.command or None, args.allow_legacy)
    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "passed": not issues,
        "decision_file": decision.as_posix() if decision else "",
        "decision_fields": fields,
        "issues": issues,
        "required_directory": DECISION_DIR.as_posix(),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
