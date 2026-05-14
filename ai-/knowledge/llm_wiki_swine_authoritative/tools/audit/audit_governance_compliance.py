from __future__ import annotations

"""治理合规检查脚本。

本脚本在两个位置被调用：
1. 更新前 PREFLIGHT 阶段，确认治理文档、入口和工具链存在；
2. 更新后 CHECKS 阶段，再次确认维护结果仍满足治理约束。

它检查的是“制度是否还完整”，而不是检查某一次具体 CRUD 决策。
具体决策文件由 `audit_crud_decision.py` 审计。
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


WIKI_ROOT = Path(__file__).resolve().parents[2]
AI_ROOT = WIKI_ROOT.parents[1]
WORKSPACE_ROOT = WIKI_ROOT.parents[2]
CHANGE_RECORDS = WORKSPACE_ROOT / "knowledge_change_records"
TZ = timezone(timedelta(hours=8))

# 必需治理文档。
# 如果这些文档缺失，或不再包含强制控制点，Wiki 更新应当停止。
REQUIRED_DOCS = [
    WIKI_ROOT / "WIKI_UPDATE_MANDATORY_SHORT_CARD.md",
    WIKI_ROOT / "WIKI_UPDATE_SCENARIO_SHORT_CARD.md",
    WIKI_ROOT / "WIKI_MAINTENANCE_GUIDE.md",
    WIKI_ROOT / "WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md",
]

# 入口文档。
# 维护者可能从 README、index、schema、checklist 或 AGENTS 进入 Wiki，
# 因此这些入口都必须能把人引回强制治理规则和固定更新入口。
ENTRYPOINTS = [
    WIKI_ROOT / "README.md",
    WIKI_ROOT / "index.md",
    WIKI_ROOT / ".wiki-schema.md",
    WIKI_ROOT / "SOURCE_BATCH_INTAKE_CHECKLIST.md",
    WIKI_ROOT / "CHANGE_RECORD_TEMPLATE.md",
    AI_ROOT / "AGENTS.md",
]

# 必需治理工具。
# 这些脚本让治理链路可以被机器执行，而不仅是文档约束。
REQUIRED_TOOLS = [
    WIKI_ROOT / "tools" / "audit_governance_compliance.py",
    WIKI_ROOT / "tools" / "audit_graph_change_diff.py",
    WIKI_ROOT / "tools" / "run_swine_wiki_maintenance_checks.py",
    WIKI_ROOT / "tools" / "run_guarded_wiki_update.py",
]

# 最新变更记录的必需信息。
# 变更记录不能只写“改了哪些文件”，还必须说明 CRUD 类型、
# 旧数据处理、高风险影响，以及 runtime/gold dataset 的影响。
CHANGE_RECORD_REQUIRED_PATTERNS = {
    "governance_compliance": ["Governance Compliance", "治理合规", "是否遵守"],
    "maintenance_guide": ["WIKI_MAINTENANCE_GUIDE.md"],
    "crud_governance": ["WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md"],
    "mandatory_short_card": ["WIKI_UPDATE_MANDATORY_SHORT_CARD.md", "短执行卡"],
    "scenario_short_card": ["WIKI_UPDATE_SCENARIO_SHORT_CARD.md", "场景化短执行卡"],
    "guarded_entrypoint": ["run_guarded_wiki_update.py", "固定入口"],
    "crud_type": ["CRUD", "增删改查", "新增、查询、修改、删除", "新增、修改、删除"],
    "old_data": ["Old data", "旧数据"],
    "high_risk": ["High-risk", "高风险"],
    "runtime_manifest": ["Runtime manifest", "runtime manifest"],
    "gold_dataset": ["Gold dataset", "gold dataset", "黄金数据集"],
}

MOJIBAKE_PATTERNS = ["\ufffd", "\u951f"]


def read_text(path: Path) -> str:
    """按 UTF-8 读取文本文件。"""
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    """把绝对路径转换为相对工作区路径，便于报告阅读。"""
    try:
        return path.relative_to(WORKSPACE_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def contains_any(text: str, patterns: list[str]) -> bool:
    """检查文本中是否包含任一指定模式。"""
    lowered = text.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def latest_change_record() -> Path | None:
    """查找 knowledge_change_records 下最新的变更记录。"""
    if not CHANGE_RECORDS.exists():
        return None
    records = [
        path
        for path in CHANGE_RECORDS.glob("*.md")
        if path.name.lower() != "readme.md"
    ]
    if not records:
        return None
    return sorted(records, key=lambda p: p.name)[-1]


def collect_issues() -> list[dict[str, str]]:
    """收集治理文档、入口、工具、变更记录和乱码信号中的问题。

    返回空列表表示治理体系仍可用。任何 issue 都会让固定入口在 preflight
    阶段停止，避免在规则不完整或留痕缺失时继续写库。
    """
    issues: list[dict[str, str]] = []

    # 1. 检查治理文档是否存在，并且仍然保留强制控制信号。
    for doc in REQUIRED_DOCS:
        if not doc.exists():
            issues.append({"path": rel(doc), "issue": "missing_required_governance_doc"})
            continue
        text = read_text(doc)
        for label, patterns in {
            "mandatory": ["强制", "mandatory"],
            "change_records": ["knowledge_change_records"],
        }.items():
            if not contains_any(text, patterns):
                    issues.append({"path": rel(doc), "issue": f"missing_pattern:{label}"})

    # 2. 检查入口文档是否一致引用治理规则和固定更新入口。
    # 这些文档是维护者最可能先打开的位置；如果入口没有指回治理规则，
    # 人工维护很容易绕过固定流程。
    for entry in ENTRYPOINTS:
        if not entry.exists():
            issues.append({"path": rel(entry), "issue": "missing_entrypoint"})
            continue
        text = read_text(entry)
        for doc_name in [
            "WIKI_UPDATE_MANDATORY_SHORT_CARD.md",
            "WIKI_UPDATE_SCENARIO_SHORT_CARD.md",
            "WIKI_MAINTENANCE_GUIDE.md",
            "WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md",
        ]:
            if doc_name not in text:
                issues.append({"path": rel(entry), "issue": f"entrypoint_missing_governance_doc:{doc_name}"})
        if "run_guarded_wiki_update.py" not in text and entry.name in {"AGENTS.md", "README.md", "WIKI_MAINTENANCE_GUIDE.md", "WIKI_DATA_SOURCE_CRUD_GOVERNANCE.md"}:
            issues.append({"path": rel(entry), "issue": "entrypoint_missing_guarded_update_entrypoint"})

    # 3. 检查治理工具是否存在。
    # 文档规则必须有可执行工具配合，否则只能靠人工记忆。
    for tool in REQUIRED_TOOLS:
        if not tool.exists():
            issues.append({"path": rel(tool), "issue": "missing_required_governance_tool"})

    # 4. 检查最新变更记录是否具备完整审计信息。
    # 最新记录代表最近一次维护动作的治理留痕。
    record = latest_change_record()
    if record is None:
        issues.append({"path": rel(CHANGE_RECORDS), "issue": "missing_change_records"})
    else:
        text = read_text(record)
        for label, patterns in CHANGE_RECORD_REQUIRED_PATTERNS.items():
            if not contains_any(text, patterns):
                issues.append({"path": rel(record), "issue": f"latest_change_record_missing_pattern:{label}"})

    # 5. 检查常见乱码信号。
    # 治理文档和变更记录大量包含中文，若出现乱码，应尽早阻断。
    for path in [*REQUIRED_DOCS, *ENTRYPOINTS, *( [record] if (record := latest_change_record()) else [] )]:
        if path.exists():
            text = read_text(path)
            for pattern in MOJIBAKE_PATTERNS:
                if pattern in text:
                    issues.append({"path": rel(path), "issue": "mojibake_signal"})
                    break

    return issues


def main() -> int:
    """输出治理合规检查 JSON，并用退出码表示是否通过。"""
    issues = collect_issues()
    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "wiki_root": rel(WIKI_ROOT),
        "change_records_dir": rel(CHANGE_RECORDS),
        "latest_change_record": rel(latest_change_record()) if latest_change_record() else "",
        "passed": not issues,
        "issues": issues,
        "required_governance_docs": [rel(path) for path in REQUIRED_DOCS],
        "required_governance_tools": [rel(path) for path in REQUIRED_TOOLS],
        "entrypoints_checked": [rel(path) for path in ENTRYPOINTS],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
