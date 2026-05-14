from __future__ import annotations

"""LLM Wiki 候选事实的分层自动复核。

本模块不让 LLM 或程序直接把高风险候选写入正式 facts。它做的是可执行的
分层复核：

1. 程序硬校验：source/raw/external_url/evidence_excerpt 是否齐全、是否可追溯。
2. 规则风险分层：诊断、监管、兽药、休药期等高风险主题必须人工确认。
3. 自动标记：低风险来源记录可进入 AUTO_READY_SOURCE，高风险进入 HUMAN_REQUIRED。

这样第六阶段不再停留在“人工复核”口径，而是变成可自动执行、可审计、
可追问的复核报告。
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

from .authority import is_authoritative_url

REVIEW_REPORT_PATH = "exports/knowledge_facts.review_report.json"
HIGH_RISK_ROLES = {
    "diagnosis_standard",
    "drug_rule",
    "regulation",
    "clinical_reference",
}
HIGH_RISK_TERMS = (
    "诊断",
    "确诊",
    "实验室",
    "兽药",
    "禁用",
    "休药期",
    "监管",
    "公告",
    "标准",
    "diagnosis",
    "diagnostic",
    "drug",
    "withdrawal",
    "regulation",
    "standard",
)


@dataclass(frozen=True)
class CandidateReviewReport:
    """候选事实分层复核报告。"""

    wiki_dir: str
    candidates_path: str
    reviewed_path: str
    report_path: str
    total_count: int
    auto_ready_count: int
    human_required_count: int
    needs_fetch_count: int
    needs_metadata_count: int
    rejected_count: int
    decision_counts: dict[str, int]
    rejected_fact_ids: tuple[str, ...]
    human_required_fact_ids: tuple[str, ...]


def review_candidate_facts(wiki_dir: str | Path) -> CandidateReviewReport:
    """对 ``knowledge_facts.candidates.json`` 执行分层自动复核。

    复核结果会写回候选事实文件，并额外生成
    ``exports/knowledge_facts.review_report.json``。该函数不会修改
    ``exports/knowledge_facts.json``，因此不会越过正式事实复核边界。
    """

    root = Path(wiki_dir)
    candidates_path = root / "exports" / "knowledge_facts.candidates.json"
    candidates = _load_candidates(candidates_path)

    reviewed: list[dict[str, Any]] = []
    decision_counts: dict[str, int] = {}
    rejected_fact_ids: list[str] = []
    human_required_fact_ids: list[str] = []

    for candidate in candidates:
        item = dict(candidate)
        decision, tier, reasons = _review_one(root, item)
        item["review_tier"] = tier
        item["review_decision"] = decision
        item["review_reasons"] = reasons
        item["formal_promotion_allowed"] = decision == "AUTO_READY_SOURCE"
        item["formal_fact_write_allowed"] = False
        reviewed.append(item)
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
        fact_id = str(item.get("fact_id") or "")
        if decision == "REJECTED":
            rejected_fact_ids.append(fact_id)
        if decision == "HUMAN_REQUIRED":
            human_required_fact_ids.append(fact_id)

    candidates_path.write_text(json.dumps(reviewed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path = root / REVIEW_REPORT_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report = CandidateReviewReport(
        wiki_dir=str(root),
        candidates_path=str(candidates_path),
        reviewed_path=str(candidates_path),
        report_path=str(report_path),
        total_count=len(reviewed),
        auto_ready_count=decision_counts.get("AUTO_READY_SOURCE", 0),
        human_required_count=decision_counts.get("HUMAN_REQUIRED", 0),
        needs_fetch_count=decision_counts.get("LEGACY_NEEDS_FETCH", 0),
        needs_metadata_count=decision_counts.get("LEGACY_NEEDS_METADATA", 0),
        rejected_count=decision_counts.get("REJECTED", 0),
        decision_counts=decision_counts,
        rejected_fact_ids=tuple(rejected_fact_ids),
        human_required_fact_ids=tuple(human_required_fact_ids),
    )
    report_path.write_text(json.dumps(_asdict(report), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _append_log(
        root,
        (
            f"{_today_iso()} candidate-review"
            f" | total={report.total_count}"
            f" | decisions={json.dumps(report.decision_counts, ensure_ascii=False, sort_keys=True)}"
            f" | reason=layered_program_review"
            f" | evidence={report_path.relative_to(root).as_posix()}"
        ),
    )
    return report


def _review_one(root: Path, candidate: Mapping[str, Any]) -> tuple[str, str, list[str]]:
    """复核单条候选事实，返回 decision、tier 和原因列表。"""

    reasons: list[str] = []
    source_page = str(candidate.get("source_page") or "").strip()
    source_path = root / source_page if source_page else Path()
    if not source_page or not source_path.is_file():
        reasons.append("source_page_missing")

    external_url = str(candidate.get("external_url") or _external_url_from_source(source_path)).strip()
    if external_url:
        if not external_url.startswith(("http://", "https://")):
            reasons.append("external_url_invalid")
        elif not is_authoritative_url(external_url):
            reasons.append("external_url_not_allowlisted")
    else:
        if source_path.is_file():
            return "LEGACY_NEEDS_METADATA", "legacy_enrichment_layer", ["external_url_missing"]
        reasons.append("external_url_missing")

    raw_path = _raw_path_from_source(root, source_path)
    if not raw_path:
        reasons.append("raw_path_missing")
    elif not raw_path.is_file():
        reasons.append("raw_file_missing")

    source_type = _source_type_from_source(source_path)
    excerpt = str(candidate.get("evidence_excerpt") or _excerpt_from_source(source_path)).strip()
    if raw_path and source_type in {"url", "html", "pdf"} and not excerpt:
        return "LEGACY_NEEDS_FETCH", "legacy_enrichment_layer", ["evidence_excerpt_missing"]

    if reasons:
        return "REJECTED", "program_hard_gate", reasons

    role = str(candidate.get("evidence_role") or "").strip().lower()
    subject = str(candidate.get("subject") or "").strip().lower()
    high_risk = role in HIGH_RISK_ROLES or any(term in subject or term in excerpt.lower() for term in HIGH_RISK_TERMS)
    if high_risk:
        return "HUMAN_REQUIRED", "risk_layer", ["high_risk_domain_requires_human_confirmation"]

    host = urlparse(external_url).hostname or ""
    return "AUTO_READY_SOURCE", "program_and_rule_layer", [f"allowlisted_source_ready:{host}"]


def _load_candidates(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, list):
        return []
    return [dict(item) for item in payload if isinstance(item, Mapping)]


def _external_url_from_source(source_path: Path) -> str:
    text = _read_text(source_path)
    for line in text.splitlines():
        if line.startswith("external_url:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def _raw_path_from_source(root: Path, source_path: Path) -> Path | None:
    text = _read_text(source_path)
    for line in text.splitlines():
        if line.startswith("source_path:"):
            rel = line.split(":", 1)[1].strip().strip('"').strip("'")
            return root / rel
    return None


def _excerpt_from_source(source_path: Path) -> str:
    text = _read_text(source_path)
    marker = "## Excerpt"
    if marker not in text:
        return ""
    return text.split(marker, 1)[1].split("## ", 1)[0].strip()


def _source_type_from_source(source_path: Path) -> str:
    text = _read_text(source_path)
    for line in text.splitlines():
        if line.startswith("source_type:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'").lower()
    return ""


def _read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _asdict(report: CandidateReviewReport) -> dict[str, Any]:
    return {
        "wiki_dir": report.wiki_dir,
        "candidates_path": report.candidates_path,
        "reviewed_path": report.reviewed_path,
        "report_path": report.report_path,
        "total_count": report.total_count,
        "auto_ready_count": report.auto_ready_count,
        "human_required_count": report.human_required_count,
        "needs_fetch_count": report.needs_fetch_count,
        "needs_metadata_count": report.needs_metadata_count,
        "rejected_count": report.rejected_count,
        "decision_counts": report.decision_counts,
        "rejected_fact_ids": list(report.rejected_fact_ids),
        "human_required_fact_ids": list(report.human_required_fact_ids),
    }


def _today_iso() -> str:
    """返回本地日期字符串，供复核日志使用。"""

    from datetime import date

    return date.today().isoformat()


def _append_log(root: Path, line: str) -> None:
    """追加候选复核审计日志。"""

    log_path = root / "log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n{line}\n")


__all__ = ["CandidateReviewReport", "REVIEW_REPORT_PATH", "review_candidate_facts"]
