import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
SYNTHESIS = WIKI / "synthesis"
ISSUES = ROOT / "issues"

REPORT_JSON = ISSUES / "phase8_synthesis_regulatory_guardrails_2026-05-09.json"
REPORT_MD = ISSUES / "phase8_synthesis_regulatory_guardrails_2026-05-09.md"

TZ = timezone(timedelta(hours=8))

TARGETS = [
    "swine_regulatory_blocking_rules_china.md",
    "swine_drug_and_withdrawal_boundary.md",
    "swine_case_generation_context.md",
    "swine_answer_evaluation_rubric.md",
]


def now():
    return datetime.now(TZ).isoformat(timespec="seconds")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def guardrail_section(page_name):
    if page_name == "swine_answer_evaluation_rubric.md":
        role = "evaluation rubric and quality-control page"
    elif page_name == "swine_case_generation_context.md":
        role = "case-generation context and scenario-boundary page"
    elif page_name == "swine_drug_and_withdrawal_boundary.md":
        role = "drug, withdrawal-period, MRL, residue, and prescription-boundary policy page"
    else:
        role = "regulatory blocking and source-routing policy page"
    return f"""## Synthesis/regulatory runtime guardrails / Phase 8

- Runtime role: {role}; this page routes, blocks, or evaluates generation and must not be treated as a primary biomedical fact source.
- `RC-SYNTHESIS-SCOPE-001`: Synthesis pages may combine rules and retrieval policy, but must not create new disease, drug, dose, withdrawal, MRL, residue, or regulatory facts.
- `RC-REGULATORY-CURRENT-001`: Reporting, quarantine, culling, movement control, inspection, banned-drug, withdrawal-period, MRL, residue, edible-product, and jurisdiction-specific compliance conclusions require current official/regulatory sources.
- `RC-EVAL-RUBRIC-001`: Evaluation rubrics and blocking rules are for scoring, routing, refusal, or source escalation; they are not standalone factual evidence.
- `RC-DRUG-001`: Drug, dose, route, course, compatibility, contraindication, or prescription content must be resolved through drug pages, source expansion, and label/regulatory verification.
- `RC-WITHDRAWAL-MRL-001`: Withdrawal period, MRL, residue, and food-safety claims require current label/regulatory verification.

"""


def insert_after_title(text, section):
    marker = "## Synthesis/regulatory runtime guardrails / Phase 8"
    if marker in text:
        return text, False
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            new_lines = lines[: i + 1] + ["", section.rstrip(), ""] + lines[i + 1 :]
            return "\n".join(new_lines) + "\n", True
    return section + text, True


def process_page(name):
    path = SYNTHESIS / name
    if not path.exists():
        return {
            "page": rel(path),
            "changed": False,
            "reason": "missing",
        }
    original = path.read_text(encoding="utf-8", errors="replace")
    before = {
        "bytes": len(original.encode("utf-8")),
        "has_rc_synthesis": "RC-SYNTHESIS-SCOPE-001" in original,
        "has_rc_regulatory_current": "RC-REGULATORY-CURRENT-001" in original,
        "has_rc_eval": "RC-EVAL-RUBRIC-001" in original,
        "has_rc_drug": "RC-DRUG-001" in original,
        "has_rc_withdrawal": "RC-WITHDRAWAL-MRL-001" in original,
    }
    updated, changed = insert_after_title(original, guardrail_section(name))
    if changed:
        path.write_text(updated, encoding="utf-8")
    after = {
        "bytes": len(updated.encode("utf-8")),
        "has_rc_synthesis": "RC-SYNTHESIS-SCOPE-001" in updated,
        "has_rc_regulatory_current": "RC-REGULATORY-CURRENT-001" in updated,
        "has_rc_eval": "RC-EVAL-RUBRIC-001" in updated,
        "has_rc_drug": "RC-DRUG-001" in updated,
        "has_rc_withdrawal": "RC-WITHDRAWAL-MRL-001" in updated,
    }
    return {
        "page": rel(path),
        "changed": changed,
        "reason": "synthesis_regulatory_guardrails_added" if changed else "already_present",
        "before": before,
        "after": after,
    }


def write_reports(records):
    generated = now()
    changed = [record for record in records if record.get("changed")]
    missing_after = [
        record for record in records
        if not record.get("after", {}).get("has_rc_synthesis")
        or not record.get("after", {}).get("has_rc_regulatory_current")
        or not record.get("after", {}).get("has_rc_eval")
    ]
    payload = {
        "generated_at": generated,
        "purpose": "Phase 8 application of synthesis/regulatory runtime guardrails.",
        "targets": TARGETS,
        "records": records,
        "summary": {
            "pages_checked": len(records),
            "pages_changed": len(changed),
            "missing_core_synthesis_anchors_after": len(missing_after),
        },
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Phase 8 Synthesis/Regulatory Guardrails / 2026-05-09",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
        f"- Pages checked: {len(records)}",
        f"- Pages changed: {len(changed)}",
        f"- Missing core synthesis anchors after change: {len(missing_after)}",
        "",
        "## Changed Pages",
        "",
    ]
    if not changed:
        lines.append("- None")
    for record in changed:
        lines.append(
            f"- `{record['page']}`: bytes={record['before']['bytes']}->{record['after']['bytes']}"
        )
    lines.extend([
        "",
        "## Runtime Handling",
        "",
        "- These pages are policy, routing, blocking, case-generation, or evaluation pages.",
        "- They must not be treated as standalone disease, drug, dose, withdrawal, MRL, residue, or regulatory fact sources.",
        "- Current official/regulatory verification remains required for jurisdiction-specific compliance.",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    records = [process_page(name) for name in TARGETS]
    write_reports(records)
    print(json.dumps({
        "pages_checked": len(records),
        "pages_changed": sum(1 for record in records if record.get("changed")),
        "missing_core_synthesis_anchors_after": sum(
            1 for record in records
            if not record.get("after", {}).get("has_rc_synthesis")
            or not record.get("after", {}).get("has_rc_regulatory_current")
            or not record.get("after", {}).get("has_rc_eval")
        ),
        "report_json": rel(REPORT_JSON),
        "report_md": rel(REPORT_MD),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
