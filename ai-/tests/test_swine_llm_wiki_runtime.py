from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIKI_ROOT = PROJECT_ROOT / "knowledge" / "llm_wiki_swine_authoritative"
EXPORTS = WIKI_ROOT / "exports"
ISSUES = WIKI_ROOT / "issues"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_swine_runtime_manifest_is_allowlist_and_has_status_contract() -> None:
    manifest = json.loads((EXPORTS / "runtime_core_manifest.json").read_text(encoding="utf-8"))
    entries = manifest["entries"]
    assert entries
    contract = manifest["status_contract"]
    forbidden = {"evidence_status", "legacy_evidence_status", "task_use_status", "gold_dataset_role", "source_status", "fact_validity"}
    assert {"source_trust", "evidence_coverage", "usage_scope"}.issubset(set(contract["primary_fields"]))
    assert not set(contract.get("legacy_fields", [])).intersection(forbidden)
    assert forbidden.isdisjoint(set(contract["primary_fields"]))
    required = {"source_trust", "evidence_coverage", "usage_scope", "authority_level", "risk_class"}
    for entry in entries:
        assert required.issubset(entry)
        assert forbidden.isdisjoint(entry)
        assert entry["source_trust"] in {"authoritative", "needs_source_check"}
        assert entry["evidence_coverage"]
        assert entry["usage_scope"]
        assert entry["path_exists"] is True
        assert not entry["path"].startswith(("raw/", "issues/"))
        assert "treatment_matrix" not in entry["path"]
        assert "prescription_matrix" not in entry["path"]
        assert "graph-data.json" not in entry["path"]


def test_swine_denylist_excludes_non_runtime_material() -> None:
    denylist = json.loads((EXPORTS / "runtime_exclude_patterns.json").read_text(encoding="utf-8"))
    patterns = set(denylist["exclude_patterns"])
    for expected in ["raw/**", "issues/**", "wiki/graph-data.json", "wiki/evidence_expansions/**"]:
        assert expected in patterns
    assert any("treatment_matrix" in pattern for pattern in patterns)
    assert any("prescription_matrix" in pattern for pattern in patterns)


def test_gold_dataset_readiness_controls_generation_and_evaluation() -> None:
    rows = _read_csv(EXPORTS / "gold_dataset_readiness_index.csv")
    assert rows
    assert not [row for row in rows if row["missing_critical_fields"]]
    for row in rows:
        usage_scope = set((row.get("usage_scope") or "").replace(";", ",").split(","))
        if "retrieval" in usage_scope and "gold_candidate" not in usage_scope:
            assert row["positive_generation_allowed"] == "false"
        if row["risk_class"] in {"high_regulatory", "withdrawal_mrl_residue", "food_safety"} and row["authority_level"] != "A0":
            assert row["positive_generation_allowed"] == "false"
        if row["positive_generation_allowed"] == "true":
            assert row["source_ids"] or row["entity_type"] in {"rule_card", "synthesis", "comparison", "syndrome"}
            assert row["rule_card_ids"]


def test_drug_high_risk_claims_require_a0_or_label_level_source() -> None:
    rows = _read_csv(EXPORTS / "drug_gold_role_index.csv")
    assert rows
    assert not [row for row in rows if row["authority_level"] != "A0" and row["positive_generation_allowed"] == "true"]
    negative_traps = [row for row in rows if "negative_trap" in row.get("usage_scope", "")]
    assert negative_traps
    for row in negative_traps:
        assert row["positive_generation_allowed"] == "false"
        assert "RC-DRUG-001" in row["requires_rule_cards"]


def test_partial_pages_route_to_gap_handling() -> None:
    rows = _read_csv(EXPORTS / "gold_dataset_readiness_index.csv")
    partials = [
        row for row in rows
        if row.get("evidence_coverage") in {"partial", "minimal"} or "gap_routing" in row.get("usage_scope", "")
    ]
    assert partials
    for row in partials:
        assert row.get("evidence_coverage") in {"partial", "minimal"} or "gap_routing" in row.get("usage_scope", "")
        assert "standalone_prescription" in row["blocked_question_types"] or row["positive_generation_allowed"] == "false"


def test_exporter_hard_block_rules_cover_phase8_required_failures() -> None:
    payload = json.loads((EXPORTS / "exporter_hard_block_rules.json").read_text(encoding="utf-8"))
    required = {
        "unsupported_dose",
        "unsupported_withdrawal_mrl",
        "unsupported_regulatory_action",
        "single_test_causality_overclaim",
        "no_source_citation",
        "source_level_mismatch",
    }
    assert required.issubset(payload["rules"])
    for rule in required:
        assert payload["rules"][rule]["requires_any_rule_card"]
        assert payload["rules"][rule]["trigger_terms"]


def test_swine_runtime_encoding_and_retrieval_smoke_reports_pass() -> None:
    encoding = json.loads((ISSUES / "encoding_integrity_audit_2026-05-09.json").read_text(encoding="utf-8"))
    summary = encoding.get("summary", encoding)
    assert summary["runtime_damaged_count"] == 0
    smoke = json.loads((ISSUES / "runtime_retrieval_smoke_test_2026-05-09.json").read_text(encoding="utf-8"))
    assert smoke["passed"] is True
    for item in smoke["tests"]:
        assert item["hit_forbidden"] is False


def test_phase11_pilot_samples_have_source_fact_rule_provenance() -> None:
    report = json.loads((ISSUES / "gold_dataset_pilot_inspection_2026-05-09.json").read_text(encoding="utf-8"))
    assert report["acceptance"]["passed"] is True
    assert report["inspection"]["provenance_complete_rate"] == 1.0
    assert report["inspection"]["high_risk_overreach"] == []
    for relpath in report["outputs"].values():
        samples = _read_jsonl(WIKI_ROOT / relpath)
        for sample in samples:
            provenance = sample["provenance"]
            assert provenance["rule_card_ids"]
            assert provenance["source_ids"] or sample["entity_type"] in {"rule_card", "synthesis"}
            assert sample["question"]
            assert sample["answer"]


def test_swine_wiki_governance_compliance_preflight_passes() -> None:
    script = WIKI_ROOT / "tools" / "audit_governance_compliance.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["passed"] is True


def test_swine_wiki_guarded_update_entrypoint_exists_and_supports_bound_dry_run() -> None:
    create_script = WIKI_ROOT / "tools" / "create_crud_decision.py"
    planned = [sys.executable, "-c", "print('noop')"]
    create = subprocess.run(
        [
            sys.executable,
            str(create_script),
            "--topic",
            "pytest-bound-dry-run",
            "--target-object-type",
            "other",
            "--target-object-id-path",
            "pytest noop",
            "--intended-action",
            "rebuild",
            "--why",
            "Verify that guarded dry-run requires an explicit bound CRUD decision.",
            "--input-source-type",
            "not applicable",
            "--old-data-exists",
            "no",
            "--old-data-handling",
            "not applicable",
            "--authority-level",
            "not applicable",
            "--risk-class",
            "not applicable",
            "--source-fact-anchor-available",
            "not applicable",
            "--runtime-impact",
            "none",
            "--gold-dataset-impact",
            "none",
            "--",
            *planned,
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert create.returncode == 0, create.stdout + create.stderr
    decision = json.loads(create.stdout)["decision_file"]

    script = WIKI_ROOT / "tools" / "run_guarded_wiki_update.py"
    try:
        result = subprocess.run(
            [sys.executable, str(script), "--decision", decision, "--dry-run", "--", *planned],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        Path(decision).unlink(missing_ok=True)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["passed"] is True
    assert payload["dry_run"] is True
    assert "audit_governance_compliance.py" in payload["steps"][0]["command"]
    assert "audit_crud_decision.py" in payload["steps"][1]["command"]


def test_swine_wiki_update_scripts_require_guarded_context() -> None:
    script = WIKI_ROOT / "tools" / "apply_dis026_fmd_authority_web_refresh.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert "run_guarded_wiki_update.py" in result.stderr + result.stdout


def test_swine_wiki_graph_change_diff_artifacts_exist() -> None:
    required = [
        WIKI_ROOT / "tools" / "audit_graph_change_diff.py",
        WIKI_ROOT / "wiki" / "knowledge-graph.html",
        WIKI_ROOT / "wiki" / "graph-data.json",
    ]
    for path in required:
        assert path.exists(), str(path)
