from __future__ import annotations

"""为一次猪病 Wiki 更新创建“绑定式 CRUD 决策文件”。

本脚本是受控更新流程里的第一个可执行步骤。它故意独立于
`run_guarded_wiki_update.py`，因为固定更新入口在执行 preflight 之前，
必须先拿到一份已经生成好的 CRUD 决策文件。

本脚本提供的保证：

1. 生成决策文件之前，先读取强制治理文档。这样可以把“维护者应该先读规则”
   变成机器可审计的动作。
2. 记录这些治理文档以及 `CRUD_DECISION_TEMPLATE.md` 的 SHA-256 hash。
   如果决策生成后治理规则发生变化，后续 `audit_crud_decision.py` 可以据此
   拒绝这份过期决策。
3. 记录本次计划执行的更新命令。后续 `run_guarded_wiki_update.py` 会把真实
   命令传给 `audit_crud_decision.py`；如果真实命令和 planned command 不一致，
   流程会在执行前被阻断。
4. 把 Markdown 决策文件写入 `issues/crud_decisions/`。这是猪病 Wiki 治理工具
   约定的固定审计目录。

本脚本不会修改 Wiki 知识内容。它只创建一个“执行前决策证据”，用于授权后续
通过固定入口执行的受控更新。
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

# 生成决策前必须读取的治理规则。
# 这些文件的 hash 会写入决策文件，供 audit_crud_decision.py 在执行前复核。
GOVERNANCE_DOCS = [
    WIKI_ROOT / "WIKI_UPDATE_MANDATORY_SHORT_CARD.md",
    WIKI_ROOT / "WIKI_UPDATE_SCENARIO_SHORT_CARD.md",
    WIKI_ROOT / "WIKI_MAINTENANCE_GUIDE.md",
    WIKI_ROOT / "WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md",
]

# 决策模板本身也参与 hash 绑定。
# 如果模板字段或要求发生变化，旧决策需要重新生成，而不是沿用旧格式。
TEMPLATE = WIKI_ROOT / "CRUD_DECISION_TEMPLATE.md"


def sha256_file(path: Path) -> str:
    """返回文件 hash，用于把决策绑定到具体版本的治理规则。"""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command_string(parts: list[str]) -> str:
    """把命令列表渲染成审计脚本使用的 shell-quoted 字符串。"""
    return " ".join(shlex.quote(part) for part in parts)


def slugify(value: str) -> str:
    """把人工填写的主题转换成稳定、可作为文件名后缀的 slug。"""
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower()).strip("-")
    return slug[:80] or "crud-decision"


def parse_args() -> argparse.Namespace:
    """解析所有决策字段，以及 `--` 后面的 planned command。

    大多数字段都直接对应 `CRUD_DECISION_TEMPLATE.md`。末尾的
    `planned_command` 特意用 remainder 参数原样接收，这样决策文件才能绑定到
    后续传给 `run_guarded_wiki_update.py` 的那条精确命令。
    """
    parser = argparse.ArgumentParser(
        description="Create a bound CRUD decision file after reading required swine Wiki governance documents."
    )
    parser.add_argument("--topic", required=True, help="Short topic used in the decision filename.")
    parser.add_argument("--target-object-type", required=True)
    parser.add_argument("--target-object-id-path", required=True)
    parser.add_argument("--intended-action", required=True)
    parser.add_argument("--why", required=True, help="Why this action is needed.")
    parser.add_argument("--input-source-type", required=True)
    parser.add_argument("--new-evidence-source", default="not applicable")
    parser.add_argument("--old-data-exists", required=True, choices=["yes", "no", "unknown"])
    parser.add_argument("--old-data-handling", required=True)
    parser.add_argument("--authority-level", required=True)
    parser.add_argument("--risk-class", required=True)
    parser.add_argument("--source-fact-anchor-available", required=True, choices=["yes", "no", "not applicable"])
    parser.add_argument("--runtime-impact", required=True)
    parser.add_argument("--gold-dataset-impact", required=True)
    parser.add_argument(
        "--safety-check",
        default="no referenced object will be silently deleted",
        help="Required deletion/replacement safety statement.",
    )
    parser.add_argument("--final-decision", default="allowed", choices=["allowed", "blocked", "manual_review"])
    parser.add_argument("--replacement-reason", default="not applicable")
    parser.add_argument("--deletion-reason", default="not applicable")
    parser.add_argument("--downgrade-archive-exclude-reason", default="not applicable")
    parser.add_argument("--conflict-handling", default="not applicable")
    parser.add_argument("--required-follow-up-checks", default="run guarded update and full maintenance checks")
    parser.add_argument(
        "planned_command",
        nargs=argparse.REMAINDER,
        help="Command planned for run_guarded_wiki_update.py after '--'.",
    )
    args = parser.parse_args()
    if args.planned_command and args.planned_command[0] == "--":
        args.planned_command = args.planned_command[1:]
    if not args.planned_command:
        parser.error("planned command is required after --")
    return args


def main() -> int:
    """读取治理上下文，写入决策文件，并输出 JSON 证据。"""
    args = parse_args()
    # 先确认治理文档和模板都存在。缺失任何一项，都不能生成授权凭证。
    missing = [path.as_posix() for path in [*GOVERNANCE_DOCS, TEMPLATE] if not path.exists()]
    if missing:
        print(json.dumps({"passed": False, "missing": missing}, ensure_ascii=False, indent=2))
        return 1

    docs = []
    for path in GOVERNANCE_DOCS:
        # 读取全文不是为了把内容写入决策，而是为了形成“已读取”和“版本 hash”
        # 两个可审计证据。
        text = path.read_text(encoding="utf-8")
        docs.append(
            {
                "path": path.relative_to(WIKI_ROOT).as_posix(),
                "sha256": sha256_file(path),
                "bytes": len(text.encode("utf-8")),
            }
        )

    now = datetime.now(TZ)
    decision_path = DECISION_DIR / f"{now:%Y-%m-%d-%H%M}-{slugify(args.topic)}.md"
    # planned command 必须与后续 run_guarded_wiki_update.py 里 `--` 后的真实命令一致。
    # 它是决策和执行之间的绑定点。
    planned = command_string(args.planned_command)
    docs_json = json.dumps(docs, ensure_ascii=False, sort_keys=True)

    text = f"""# CRUD Decision: {args.topic}

This decision was generated by `tools/create_crud_decision.py` after reading the required governance documents.

## Governance Context

- Decision generated at: {now.isoformat(timespec="seconds")}
- Governance documents read: {", ".join(doc["path"] for doc in docs)}
- Governance document hashes JSON: {docs_json}
- CRUD template hash: {sha256_file(TEMPLATE)}
- Planned command: {planned}

## CRUD Decision

- Target object type: {args.target_object_type}
- Target object id/path: {args.target_object_id_path}
- Intended action: {args.intended_action}
- Why this action is needed: {args.why}
- Input source type: {args.input_source_type}
- New evidence/source: {args.new_evidence_source}
- Old data exists: {args.old_data_exists}
- Old data handling: {args.old_data_handling}
- Authority level: {args.authority_level}
- Risk class: {args.risk_class}
- Source/fact anchor available: {args.source_fact_anchor_available}
- Runtime impact: {args.runtime_impact}
- Gold dataset impact: {args.gold_dataset_impact}
- Deletion or replacement safety check: {args.safety_check}
- Final decision: {args.final_decision}

## Reasoning Notes

- Replacement reason, if action is replace: {args.replacement_reason}
- Deletion reason, if action is delete: {args.deletion_reason}
- Downgrade/archive/exclude reason, if applicable: {args.downgrade_archive_exclude_reason}
- Conflict handling, if new and old data disagree: {args.conflict_handling}
- Required follow-up checks: {args.required_follow_up_checks}
"""
    DECISION_DIR.mkdir(parents=True, exist_ok=True)
    decision_path.write_text(text, encoding="utf-8")
    payload = {
        "passed": True,
        "decision_file": decision_path.as_posix(),
        "planned_command": planned,
        "governance_documents": docs,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
