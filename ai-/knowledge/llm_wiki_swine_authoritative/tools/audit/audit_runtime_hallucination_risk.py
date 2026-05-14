import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

"""runtime 幻觉风险审计脚本。

由 run_swine_wiki_maintenance_checks.py 在更新后验收阶段调用。
它根据 runtime manifest 检查高风险表述、护栏引用和证据锚点，输出风险审计报告。
"""

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues"

MANIFEST = EXPORTS / "runtime_core_manifest.json"
SUMMARY_JSON = ISSUES / "runtime_hallucination_risk_audit_2026-05-09.json"
SUMMARY_MD = ISSUES / "runtime_hallucination_risk_audit_2026-05-09.md"

TZ = timezone(timedelta(hours=8))

HIGH_RISK_PATTERNS = {
    "dose_or_course": [
        r"剂量", r"用量", r"疗程", r"dose", r"course", r"mg/kg", r"mL/kg",
        r"毫克/千克", r"毫升/千克", r"单位/千克",
    ],
    "withdrawal_or_mrl": [
        r"休药期", r"弃奶期", r"MRL", r"残留", r"withdrawal", r"residue",
    ],
    "regulatory_or_emergency": [
        r"扑杀", r"封锁", r"调运", r"报告", r"一类动物疫病", r"二类动物疫病",
        r"检疫", r"无害化", r"movement", r"slaughter",
    ],
}

GUARDRAIL_IDS = {
    "dose_or_course": ["RC-DRUG-001", "RC-WITHDRAWAL-MRL-001"],
    "withdrawal_or_mrl": ["RC-WITHDRAWAL-MRL-001", "RC-DRUG-001"],
    "regulatory_or_emergency": ["RC-DISEASE-REGULATORY-001", "RC-ASF-001", "RC-VES-001"],
}

SYNTHESIS_POLICY_ANCHORS = [
    "RC-SYNTHESIS-SCOPE-001",
    "RC-REGULATORY-CURRENT-001",
    "RC-EVAL-RUBRIC-001",
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def load_manifest():
    if not MANIFEST.exists():
        return []
    return json.loads(MANIFEST.read_text(encoding="utf-8")).get("entries", [])


def risk_hits(text):
    hits = {}
    for category, patterns in HIGH_RISK_PATTERNS.items():
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, text, flags=re.IGNORECASE))
        if count:
            hits[category] = count
    return hits


def has_guardrail(text, category):
    return any(card_id in text for card_id in GUARDRAIL_IDS.get(category, []))


def is_synthesis_policy(entry, text):
    if entry.get("entity_type") != "synthesis":
        return False
    if entry.get("runtime_tier") in {"runtime_core_policy", "runtime_core_context"}:
        return True
    return any(anchor in text for anchor in SYNTHESIS_POLICY_ANCHORS)


def has_synthesis_guardrails(text):
    return all(anchor in text for anchor in SYNTHESIS_POLICY_ANCHORS)


def has_partial_gap_routing(text):
    return "RC-PARTIAL-GAP-ROUTING-001" in text


def audit_entry(entry):
    relpath = entry.get("path", "")
    path = ROOT / relpath
    if not path.exists():
        return {
            "page_id": entry.get("page_id", ""),
            "path": relpath,
            "risk_score": 100,
            "findings": ["manifest_path_missing"],
        }

    text = read_text(path)
    findings = []
    score = 0
    size = path.stat().st_size

    replacement_chars = text.count("\ufffd")
    if replacement_chars:
        findings.append(f"encoding_replacement_chars:{replacement_chars}")
        score += min(25, replacement_chars // 20 + 5)

    if size > 50_000:
        findings.append(f"oversized_page_bytes:{size}")
        score += 15
    elif size > 20_000:
        findings.append(f"large_page_bytes:{size}")
        score += 8

    synthesis_policy = is_synthesis_policy(entry, text)
    synthesis_guarded = synthesis_policy and has_synthesis_guardrails(text)

    partial_gap_routed = has_partial_gap_routing(text)

    if (
        entry.get("runtime_tier") == "runtime_core_partial"
        and entry.get("source_status") != "source_anchored"
        and not synthesis_guarded
        and not partial_gap_routed
    ):
        findings.append("partial_without_source_anchor_or_gap_routing")
        score += 10

    if entry.get("source_status") in {"source_missing", "source_conflicted", "source_damaged", "source_level_mismatch"}:
        findings.append(f"source_status:{entry.get('source_status')}")
        score += 15

    if entry.get("fact_validity") and entry.get("fact_validity") != "valid":
        findings.append(f"fact_validity:{entry.get('fact_validity')}")
        score += 15

    candidate_count = text.count("candidate_fact")
    if candidate_count:
        findings.append(f"candidate_fact_mentions:{candidate_count}")
        score += min(20, candidate_count)

    hits = risk_hits(text)
    for category, count in hits.items():
        if synthesis_guarded:
            continue
        if not has_guardrail(text, category):
            findings.append(f"{category}_terms_without_expected_guardrail:{count}")
            score += min(15, 3 + count // 25)

    if synthesis_policy and not synthesis_guarded:
        findings.append("synthesis_policy_without_phase8_guardrails")
        score += 8

    if entry.get("entity_type") == "drug" and "RC-DRUG-001" not in text:
        findings.append("drug_page_without_RC_DRUG_001_text_anchor")
        score += 5

    if entry.get("entity_type") == "drug" and "RC-WITHDRAWAL-MRL-001" not in text and hits.get("withdrawal_or_mrl"):
        findings.append("drug_with_withdrawal_terms_without_RC_WITHDRAWAL_MRL_001")
        score += 10

    if entry.get("risk_class") in {"high_regulatory", "withdrawal_mrl_residue", "food_safety"} and entry.get("authority_level") not in {"A0", "RC", "RULE"}:
        if entry.get("task_use_status") == "train_ready":
            findings.append("high_risk_train_ready_without_A0_or_rule_authority")
            score += 20

    return {
        "page_id": entry.get("page_id", ""),
        "path": relpath,
        "entity_type": entry.get("entity_type", ""),
        "runtime_tier": entry.get("runtime_tier", ""),
        "synthesis_policy": synthesis_policy,
        "partial_gap_routed": partial_gap_routed,
        "bytes": size,
        "risk_score": min(score, 100),
        "risk_hits": hits,
        "findings": findings,
    }


def severity(score):
    if score >= 35:
        return "high"
    if score >= 15:
        return "medium"
    if score > 0:
        return "low"
    return "none"


def write_reports(results):
    by_severity = {"high": 0, "medium": 0, "low": 0, "none": 0}
    for item in results:
        by_severity[severity(item["risk_score"])] += 1

    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "entries_checked": len(results),
        "severity_counts": by_severity,
        "top_risks": sorted(results, key=lambda x: x["risk_score"], reverse=True)[:40],
        "all_results": results,
    }
    SUMMARY_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    top = payload["top_risks"][:25]
    lines = [
        "# Runtime Hallucination Risk Audit / 2026-05-09",
        "",
        f"Generated: {payload['generated_at']}",
        f"Manifest: `{payload['manifest']}`",
        f"Entries checked: {payload['entries_checked']}",
        "",
        "## Severity Counts",
        "",
    ]
    lines.extend(f"- {key}: {by_severity[key]}" for key in ["high", "medium", "low", "none"])
    lines.extend(["", "## Top Risk Pages", ""])
    for item in top:
        lines.append(
            f"- score={item['risk_score']} severity={severity(item['risk_score'])} "
            f"`{item['page_id']}` `{item['path']}` findings={'; '.join(item['findings']) or 'none'}"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- This audit is a risk triage, not a truth-quality judgment.",
        "- High or medium pages should be reviewed before they are used for unrestricted production retrieval.",
        "- Drug, withdrawal/MRL, and regulatory findings should be handled with rule-card gating and source expansion.",
        "",
    ])
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    """执行 runtime 风险审计并写入 JSON/Markdown 报告。"""
    entries = load_manifest()
    results = [audit_entry(entry) for entry in entries]
    write_reports(results)
    print(json.dumps({
        "entries_checked": len(results),
        "report_json": str(SUMMARY_JSON.relative_to(ROOT)),
        "report_md": str(SUMMARY_MD.relative_to(ROOT)),
        "high": sum(1 for x in results if severity(x["risk_score"]) == "high"),
        "medium": sum(1 for x in results if severity(x["risk_score"]) == "medium"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
