from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIKI_ROOT = PROJECT_ROOT / "knowledge" / "llm_wiki_swine_authoritative"
EXPORTS = WIKI_ROOT / "exports"
PHASE12_SCRIPT = WIKI_ROOT / "tools" / "phase12_plan_samples_from_wiki.py"
PHASE13_SCRIPT = WIKI_ROOT / "tools" / "phase13_build_answer_skeletons.py"
PHASE14_SCRIPT = WIKI_ROOT / "tools" / "phase14_generate_two_stage_samples.py"
PHASE15_SCRIPT = WIKI_ROOT / "tools" / "phase15_fact_level_evaluate_samples.py"
PHASE16_SCRIPT = WIKI_ROOT / "tools" / "phase16_export_layered_training_sets.py"
PHASE18_SCRIPT = WIKI_ROOT / "tools" / "phase18_dual_judge_and_arbitrate.py"
PHASE12_REQUIRED_FIELDS = {
    "plan_id",
    "entity_id",
    "entity_type",
    "page_relpath",
    "task_type",
    "ability_layer",
    "source_trust",
    "evidence_coverage",
    "usage_scope",
    "authority_level",
    "risk_class",
    "expected_output_type",
    "positive_generation_allowed",
    "negative_trap_allowed",
    "evaluation_allowed",
    "required_rule_cards",
    "question_blueprint",
}


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _latest_jsonl(directory: Path, *name_parts: str) -> Path:
    matches = [
        path
        for path in directory.glob("*.jsonl")
        if all(part in path.name for part in name_parts)
    ]
    assert matches, f"no jsonl matching {name_parts!r} under {directory}"
    return max(matches, key=lambda path: path.stat().st_mtime)


def _run_phase12(*args: str) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(PHASE12_SCRIPT), *args],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def test_phase12_plans_are_runtime_allowlisted() -> None:
    summary = _run_phase12("--date", "pytest", "--limit", "60")
    assert summary["passed"] is True
    plans = _read_jsonl(WIKI_ROOT / summary["output"])
    manifest = json.loads((EXPORTS / "runtime_core_manifest.json").read_text(encoding="utf-8"))
    runtime_paths = {entry["path"] for entry in manifest["entries"]}
    assert plans
    for plan in plans:
        assert PHASE12_REQUIRED_FIELDS.issubset(plan)
        assert plan["page_relpath"] in runtime_paths
        assert not str(plan["page_relpath"]).startswith(("raw/", "issues/"))
        assert "graph-data.json" not in str(plan["page_relpath"])
        assert plan["ability_layer"]


def test_phase12_high_risk_plans_require_rule_cards() -> None:
    summary = _run_phase12("--date", "pytest", "--limit", "120")
    plans = _read_jsonl(WIKI_ROOT / summary["output"])
    high_risk = [
        plan
        for plan in plans
        if plan["risk_class"] in {"high_regulatory", "withdrawal_mrl_residue", "drug_boundary"}
    ]
    assert high_risk
    assert summary["acceptance"]["high_risk_plans_have_required_rule_cards"] is True
    for plan in high_risk:
        assert plan["required_rule_cards"]


def test_phase12_limited_or_source_check_pages_are_not_positive_generation() -> None:
    summary = _run_phase12("--date", "pytest", "--limit", "120")
    plans = _read_jsonl(WIKI_ROOT / summary["output"])
    limited = [
        plan
        for plan in plans
        if plan["evidence_coverage"] in {"partial", "minimal"} or plan["source_trust"] == "needs_source_check"
    ]
    assert limited
    assert summary["acceptance"]["limited_or_source_check_not_positive"] is True
    for plan in limited:
        assert plan["positive_generation_allowed"] is False


def test_phase12_ability_layer_contracts() -> None:
    summary = _run_phase12("--date", "pytest", "--limit", "180")
    plans = _read_jsonl(WIKI_ROOT / summary["output"])
    layers = {plan["ability_layer"] for plan in plans}
    assert {"L1_retrieval_grounded", "L2_diagnosis_support", "L3_differential_support", "L4_control_boundary"}.issubset(layers)
    for plan in plans:
        usage_scope = set(plan["usage_scope"])
        if plan["ability_layer"] == "L6_regulatory_guardrail":
            assert plan["risk_class"] == "high_regulatory" or "regulatory_boundary" in usage_scope
            assert plan["expected_output_type"] == "boundary_or_refusal"
        if plan["ability_layer"] == "L5_drug_boundary_negative":
            assert usage_scope.intersection({"drug_boundary", "negative_trap"})


def _phase13_fixture(tmp_path: Path) -> Path:
    wiki_root = tmp_path / "wiki"
    exports = wiki_root / "exports"
    _write_jsonl(
        exports / "planned_samples" / "wiki_sample_plan_20260513.jsonl",
        [
            {
                "plan_id": "PLAN-DIS-002-0001",
                "entity_id": "DIS-002",
                "entity_type": "disease",
                "page_relpath": "wiki/diseases/DIS-002-african-swine-fever-virus.md",
                "task_type": "retrieval_grounded",
                "ability_layer": "L1_retrieval_grounded",
                "source_trust": "authoritative",
                "evidence_coverage": "complete",
                "usage_scope": ["retrieval"],
                "risk_class": "normal_clinical",
                "expected_output_type": "grounded_answer",
            },
            {
                "plan_id": "PLAN-DIS-026-0001",
                "entity_id": "DIS-026",
                "entity_type": "disease",
                "page_relpath": "wiki/diseases/DIS-026-fmd.md",
                "task_type": "regulatory_boundary",
                "ability_layer": "L6_regulatory_guardrail",
                "source_trust": "authoritative",
                "evidence_coverage": "complete",
                "usage_scope": ["retrieval", "control_support", "regulatory_boundary"],
                "authority_level": "A0",
                "risk_class": "high_regulatory",
                "expected_output_type": "boundary_or_refusal",
                "required_rule_cards": ["RC-DISEASE-REGULATORY-001", "RC-CITATION-001"],
                "question_blueprint": {
                    "intent": "ask_regulatory_action_boundary",
                    "must_not_ask_about": ["unsupported culling conclusion"],
                },
            },
            {
                "plan_id": "PLAN-DIS-027-0001",
                "entity_id": "DIS-027",
                "entity_type": "disease",
                "page_relpath": "wiki/diseases/DIS-027-boundary-only.md",
                "task_type": "regulatory_boundary",
                "ability_layer": "L6_regulatory_guardrail",
                "source_trust": "authoritative",
                "evidence_coverage": "complete",
                "usage_scope": ["regulatory_boundary"],
                "authority_level": "A0",
                "risk_class": "high_regulatory",
                "expected_output_type": "boundary_or_refusal",
                "required_rule_cards": ["RC-DISEASE-REGULATORY-001"],
            },
            {
                "plan_id": "PLAN-DIS-404-0001",
                "entity_id": "DIS-404",
                "entity_type": "disease",
                "page_relpath": "wiki/diseases/DIS-404-gap.md",
                "task_type": "retrieval_grounded",
                "ability_layer": "L1_retrieval_grounded",
                "source_trust": "authoritative",
                "evidence_coverage": "complete",
                "usage_scope": ["retrieval"],
                "risk_class": "normal_clinical",
                "expected_output_type": "grounded_answer",
            },
        ],
    )
    _write_json(
        exports / "runtime_core_manifest.json",
        {
            "entries": [
                {"page_id": "DIS-002", "path": "wiki/diseases/DIS-002-african-swine-fever-virus.md"},
                {"page_id": "DIS-026", "path": "wiki/diseases/DIS-026-fmd.md", "source_ids": ["A0-FMD"]},
                {"page_id": "DIS-027", "path": "wiki/diseases/DIS-027-boundary-only.md", "source_ids": ["A0-BOUNDARY"]},
            ]
        },
    )
    _write_json(
        exports / "knowledge_facts_status_index.json",
        [
            {
                "fact_id": "DIS-002-toc-category",
                "fact_type": "disease_attribute",
                "subject": "ASF",
                "predicate": "category",
                "object": "viral disease",
                "evidence_source_id": "SRC-ASF",
                "source_trust": "authoritative",
                "evidence_coverage": "complete",
                "usage_scope": ["retrieval"],
            },
            {
                "fact_id": "DIS-026-official-boundary",
                "fact_type": "regulatory_boundary",
                "subject": "FMD",
                "predicate": "requires_official_boundary",
                "object": "movement/reporting decisions require current official source",
                "evidence_source_id": "A0-FMD",
                "source_trust": "authoritative",
                "evidence_coverage": "complete",
                "usage_scope": ["retrieval", "regulatory_boundary"],
            },
        ],
    )
    (exports / "rule_card_index.csv").write_text(
        "card_id,title,severity,jurisdiction,hard_block,page_relpath\n"
        "RC-DISEASE-REGULATORY-001,Regulatory boundary,critical,China,true,wiki/rule_cards/RC-DISEASE-REGULATORY-001.md\n"
        "RC-CITATION-001,Citation gate,high,Global,false,wiki/rule_cards/RC-CITATION-001.md\n",
        encoding="utf-8",
    )
    _write_json(
        exports / "exporter_hard_block_rules.json",
        {
            "rules": {
                "unsupported_regulatory_action": {
                    "requires_any_rule_card": ["RC-DISEASE-REGULATORY-001"],
                    "trigger_terms": ["report", "movement"],
                    "block_when": "No current official/regulatory source covers the requested action.",
                }
            }
        },
    )
    return wiki_root


def _run_phase13(wiki_root: Path) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(PHASE13_SCRIPT), "--wiki-root", str(wiki_root)],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def test_phase13_skeleton_claims_have_anchors(tmp_path: Path) -> None:
    wiki_root = _phase13_fixture(tmp_path)

    summary = _run_phase13(wiki_root)

    assert summary["skeletons_generated"] == 3
    skeletons = _read_jsonl(wiki_root / "exports" / "answer_skeletons" / "wiki_answer_skeletons_20260513.jsonl")
    assert {skeleton["plan_id"] for skeleton in skeletons} == {
        "PLAN-DIS-002-0001",
        "PLAN-DIS-026-0001",
        "PLAN-DIS-027-0001",
    }
    for skeleton in skeletons:
        assert skeleton["skeleton_id"]
        assert skeleton["entity_id"]
        assert skeleton["question_intent"]
        assert skeleton["answer_mode"]
        assert skeleton["must_include_claims"]
        assert "required_citations" in skeleton
        assert "hard_gate_profile" in skeleton
        for claim in skeleton["must_include_claims"]:
            assert claim["claim_id"]
            assert claim["claim_type"]
            assert claim["claim"]
            assert claim["page_relpath"]
            assert claim["source_ids"] or claim["rule_card_ids"]


def test_phase13_high_risk_skeletons_keep_hard_gate_and_gap_report(tmp_path: Path) -> None:
    wiki_root = _phase13_fixture(tmp_path)

    _run_phase13(wiki_root)

    skeletons = _read_jsonl(wiki_root / "exports" / "answer_skeletons" / "wiki_answer_skeletons_20260513.jsonl")
    high_risk = [skeleton for skeleton in skeletons if skeleton["ability_layer"] == "L6_regulatory_guardrail"]
    assert high_risk
    for skeleton in high_risk:
        assert skeleton["hard_gate_profile"]["high_risk"] is True
        assert skeleton["hard_gate_profile"]["blocks_regulatory_action_without_a0"] is True
        assert skeleton["must_not_include"]
        assert any(claim["rule_card_ids"] for claim in skeleton["must_include_claims"])

    report = json.loads(
        (wiki_root / "issues" / "wiki_first_generation_reports" / "phase13_answer_skeletons_20260513.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["gaps"] == 1
    assert report["gap_report"][0]["plan_id"] == "PLAN-DIS-404-0001"
    assert (wiki_root / "issues" / "wiki_first_generation_reports" / "phase13_answer_skeletons_20260513.md").exists()


def _run_phase14(wiki_root: Path, limit: int | None = None) -> dict[str, object]:
    args = [sys.executable, str(PHASE14_SCRIPT), "--wiki-root", str(wiki_root), "--date", "20260513"]
    if limit is not None:
        args.extend(["--limit", str(limit)])
    result = subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def _run_phase15(
    wiki_root: Path,
    generated: Path | None = None,
    limit: int | None = None,
    *,
    date: str = "20260513",
) -> dict[str, object]:
    if not PHASE15_SCRIPT.exists():
        pytest.skip(f"Phase 15 script not present yet: {PHASE15_SCRIPT}")
    args = [sys.executable, str(PHASE15_SCRIPT), "--wiki-root", str(wiki_root), "--date", date]
    if generated is not None:
        args.extend(["--generated", str(generated)])
    if limit is not None:
        args.extend(["--limit", str(limit)])
    result = subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def _run_phase18(
    wiki_root: Path,
    evaluated: Path | None = None,
    *,
    date: str = "20260513",
) -> dict[str, object]:
    if not PHASE18_SCRIPT.exists():
        pytest.skip(f"Phase 18 script not present yet: {PHASE18_SCRIPT}")
    args = [sys.executable, str(PHASE18_SCRIPT), "--wiki-root", str(wiki_root), "--date", date]
    if evaluated is not None:
        args.extend(["--evaluated", str(evaluated)])
    result = subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def test_phase14_generated_samples_have_two_stages(tmp_path: Path) -> None:
    wiki_root = _phase13_fixture(tmp_path)
    _run_phase13(wiki_root)

    summary = _run_phase14(wiki_root, limit=2)

    assert summary["mode"] == "dry-run"
    assert summary["generation_model"] == "deterministic-mock"
    assert summary["prompt_version"] == "phase14.two_stage.v3_cn_clinical"
    assert summary["passed"] is True
    samples = _read_jsonl(wiki_root / "exports" / "generated_samples" / "two_stage_samples_20260513.jsonl")
    assert samples
    assert len(samples) <= 2
    for sample in samples:
        for field in [
            "sample_id",
            "plan_id",
            "skeleton_id",
            "ability_layer",
            "entity_id",
            "entity_type",
            "question",
            "stage_1_draft",
            "stage_2_grounded",
            "evidence_anchors",
            "source_trust",
            "evidence_coverage",
            "usage_scope",
            "risk_class",
            "generation_mode",
            "generation_model",
            "prompt_version",
            "request_ref",
            "response_ref",
        ]:
            assert sample[field]
        assert sample["generation_mode"] == "dry-run"
        assert sample["stage_1_draft"]["answer"]
        assert sample["stage_2_grounded"]["answer"]
        assert "using registered Wiki evidence" not in sample["question"]
        assert "Summarize core knowledge" not in sample["question"]
        assert any(token in sample["question"] for token in ["猪场", "兽医", "怀疑", "现有资料", "能不能", "哪些"])
        grounded = sample["stage_2_grounded"]["answer"]
        assert "Citation anchors:" in grounded
        assert "rule=" in grounded
        assert "page=" in grounded
        if sample["ability_layer"] not in {"L5_drug_boundary_negative", "L6_regulatory_guardrail"}:
            assert "source=" in grounded
            assert "fact=" in grounded


def test_phase14_question_for_uses_realistic_cn_clinical_scene() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("phase14_gen", PHASE14_SCRIPT)
    assert spec and spec.loader
    phase14 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(phase14)

    plan = {
        "entity_id": "DIS-002",
        "ability_layer": "L2_diagnosis_support",
        "question_blueprint": {"must_ask_about": ["diagnosis_support", "boundary"]},
    }
    skeleton = {
        "entity_id": "DIS-002",
        "must_include_claims": [
            {"claim": "非洲猪瘟；category；病毒病"},
        ],
    }
    question = phase14.question_for(plan, skeleton)

    assert "非洲猪瘟" in question
    assert "猪场" in question
    assert "诊断" in question
    assert "using registered Wiki evidence" not in question
    assert "Summarize core knowledge" not in question


def test_phase14_every_sample_has_evidence_anchors(tmp_path: Path) -> None:
    wiki_root = _phase13_fixture(tmp_path)
    _run_phase13(wiki_root)

    summary = _run_phase14(wiki_root)

    assert summary["missing_anchors"] == []
    samples = _read_jsonl(wiki_root / "exports" / "generated_samples" / "two_stage_samples_20260513.jsonl")
    assert samples
    for sample in samples:
        assert sample["evidence_anchors"]
        for anchor in sample["evidence_anchors"]:
            assert anchor["claim_id"]
            assert anchor["rule_card_id"]
            assert anchor["page_relpath"]
            assert anchor["claim_supported"] is True
            if anchor.get("anchor_type") != "rule_card_boundary":
                assert anchor["fact_id"]
                assert anchor["source_id"]

    report_path = wiki_root / "issues" / "wiki_first_generation_reports" / "phase14_generation_20260513.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["passed"] is True
    assert (wiki_root / "issues" / "wiki_first_generation_reports" / "phase14_generation_20260513.md").exists()


def test_phase15_judge_score_cannot_override_fact_failure(tmp_path: Path) -> None:
    wiki_root = _phase13_fixture(tmp_path)
    generated = wiki_root / "exports" / "generated_samples" / "two_stage_samples_20260513.jsonl"
    _write_jsonl(
        generated,
        [
            {
                "sample_id": "GEN-BAD-FACT",
                "plan_id": "PLAN-DIS-002-0001",
                "skeleton_id": "SKEL-PLAN-DIS-002-0001",
                "ability_layer": "L1_retrieval_grounded",
                "entity_id": "DIS-002",
                "entity_type": "disease",
                "question": "Summarize core knowledge for DIS-002 using registered Wiki evidence.",
                "stage_2_grounded": {
                    "answer": "Anchored-looking answer [source=SRC-ASF rule=RC-CITATION-001 fact=DIS-002-missing]"
                },
                "evidence_anchors": [
                    {
                        "claim_id": "CLAIM-BAD-001",
                        "fact_id": "DIS-002-missing",
                        "source_id": "SRC-ASF",
                        "rule_card_id": "RC-CITATION-001",
                        "page_relpath": "wiki/diseases/DIS-002-african-swine-fever-virus.md",
                        "claim_supported": True,
                    }
                ],
                "source_trust": "authoritative",
                "evidence_coverage": "complete",
                "usage_scope": ["retrieval"],
                "risk_class": "normal_clinical",
            }
        ],
    )

    summary = _run_phase15(wiki_root, generated)

    assert summary["accepted"] == 0
    evaluated = _read_jsonl(wiki_root / "exports" / "evaluated_samples" / "fact_evaluated_samples_20260513.jsonl")
    sample = evaluated[0]
    assert sample["final_decision"] == "rejected"
    for field in [
        "structure_check",
        "fact_level_check",
        "hard_gate_check",
        "final_decision",
        "reject_reasons",
    ]:
        assert field in sample
    assert sample["fact_level_check"]["passed"] is False
    assert sample["hard_gate_check"]["passed"] is True
    assert sample["judge_check"]["mode"] == "deterministic_placeholder"
    assert sample["judge_check"]["passed"] is False
    assert any(reason.startswith("fact:DIS-002-missing") for reason in sample["reject_reasons"])


def test_phase15_high_risk_hard_gate_blocks_unsupported_positive_claims(tmp_path: Path) -> None:
    wiki_root = _phase13_fixture(tmp_path)
    generated = wiki_root / "exports" / "generated_samples" / "two_stage_samples_20260513.jsonl"
    _write_jsonl(
        generated,
        [
            {
                "sample_id": "GEN-HIGH-RISK-NO-RC",
                "plan_id": "PLAN-DIS-026-0001",
                "skeleton_id": "SKEL-PLAN-DIS-026-0001",
                "ability_layer": "L6_regulatory_guardrail",
                "entity_id": "DIS-026",
                "entity_type": "disease",
                "question": "Can the answer directly provide executable regulatory movement and report instructions?",
                "stage_2_grounded": {
                    "answer": (
                        "The answer provides movement and report instructions "
                        "[source=A0-FMD rule=RC-DISEASE-REGULATORY-001 fact=DIS-026-official-boundary]"
                    )
                },
                "evidence_anchors": [
                    {
                        "claim_id": "CLAIM-HIGH-RISK-001",
                        "fact_id": "DIS-026-official-boundary",
                        "source_id": "A0-FMD",
                        "rule_card_id": "",
                        "page_relpath": "wiki/diseases/DIS-026-fmd.md",
                        "claim_supported": True,
                    }
                ],
                "source_trust": "authoritative",
                "evidence_coverage": "complete",
                "usage_scope": ["retrieval", "regulatory_boundary"],
                "risk_class": "high_regulatory",
            }
        ],
    )

    summary = _run_phase15(wiki_root, generated)

    assert summary["accepted"] == 0
    evaluated = _read_jsonl(wiki_root / "exports" / "evaluated_samples" / "fact_evaluated_samples_20260513.jsonl")
    sample = evaluated[0]
    assert sample["final_decision"] == "rejected"
    for field in [
        "structure_check",
        "fact_level_check",
        "hard_gate_check",
        "final_decision",
        "reject_reasons",
    ]:
        assert field in sample
    assert sample["structure_check"]["passed"] is False
    assert sample["hard_gate_check"]["passed"] is False
    assert "hard_gate:high_risk_missing_rule_card" in sample["reject_reasons"]
    assert "hard_gate:executive_content_missing_rule_card" in sample["reject_reasons"]

    report = json.loads(
        (wiki_root / "issues" / "wiki_first_generation_reports" / "phase15_fact_eval_20260513.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["rejected"] == 1
    assert (wiki_root / "issues" / "wiki_first_generation_reports" / "phase15_reject_reasons_20260513.csv").exists()


def test_phase15_chinese_drug_boundary_gate_detects_executable_and_refusal() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("phase15_eval", PHASE15_SCRIPT)
    assert spec and spec.loader
    phase15 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(phase15)

    executable = {
        "ability_layer": "L5_drug_boundary_negative",
        "stage_2_grounded": {"answer": "可以直接给出剂量和休药期。"},
    }
    refusal = {
        "ability_layer": "L5_drug_boundary_negative",
        "stage_2_grounded": {"answer": "不能直接提供剂量和休药期，应依据标签或官方来源。"},
    }

    assert phase15.DRUG_EXECUTABLE_RE.search("剂量和休药期")
    assert phase15.BOUNDARY_REFUSAL_RE.search("不能直接提供")
    assert phase15.boundary_policy_check(executable)["passed"] is False
    assert "drug_boundary_missing_refusal_or_source_check" in phase15.boundary_policy_check(executable)["violations"]
    assert phase15.boundary_policy_check(refusal)["passed"] is True


def test_phase15_low_risk_negative_boundary_text_does_not_require_a0() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("phase15_eval", PHASE15_SCRIPT)
    assert spec and spec.loader
    phase15 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(phase15)

    anchors = [
        {
            "fact_id": "FACT-1",
            "source_id": "SRC-1",
            "rule_card_id": "RC-CITATION-001",
            "page_relpath": "wiki/diseases/DIS-001.md",
        }
    ]
    safe_boundary = {
        "ability_layer": "L2_diagnosis_support",
        "risk_class": "normal_clinical",
        "question": "Explain diagnosis-support points using registered Wiki evidence.",
        "stage_2_grounded": {
            "answer": (
                "Diagnostic boundary: the cited evidence is not enough to make a final diagnosis. "
                "Do not infer dose, withdrawal, report, cull, quarantine, or residue decisions from this evidence."
            )
        },
        "evidence_anchors": anchors,
    }
    unsafe_positive = {
        **safe_boundary,
        "stage_2_grounded": {
            "answer": "Use dose guidance, report immediately, quarantine the herd, and cull affected pigs."
        },
    }
    facts = {"FACT-1": {"authority_level": "A1"}}

    safe_gate = phase15.hard_gate_check(safe_boundary, facts, {})
    unsafe_gate = phase15.hard_gate_check(unsafe_positive, facts, {})

    assert safe_gate["triggered"] is True
    assert safe_gate["positive_triggered"] is False
    assert safe_gate["passed"] is True
    assert unsafe_gate["positive_triggered"] is True
    assert unsafe_gate["passed"] is False
    assert "executive_content_missing_a0_source" in unsafe_gate["violations"]


def _phase16_fixture(tmp_path: Path) -> Path:
    wiki_root = tmp_path / "wiki"
    generated_rows = [
        {
            "sample_id": "GEN-L1-ACCEPT",
            "ability_layer": "L1_retrieval_grounded",
            "entity_id": "DIS-001",
            "entity_type": "disease",
            "question": "Summarize DIS-001 using registered Wiki evidence.",
            "stage_2_grounded": {
                "answer": "Grounded fact. [source=SRC-1 rule=RC-CITATION-001 fact=FACT-1 page=wiki/diseases/DIS-001.md]"
            },
            "evidence_anchors": [
                {
                    "fact_id": "FACT-1",
                    "source_id": "SRC-1",
                    "rule_card_id": "RC-CITATION-001",
                    "page_relpath": "wiki/diseases/DIS-001.md",
                }
            ],
            "source_trust": "authoritative",
            "evidence_coverage": "complete",
            "usage_scope": ["retrieval"],
            "risk_class": "normal_clinical",
        },
        {
            "sample_id": "GEN-L2-FACT-FAIL",
            "ability_layer": "L2_diagnosis_support",
            "entity_id": "DIS-002",
            "entity_type": "disease",
            "question": "Explain diagnosis support for DIS-002.",
            "stage_2_grounded": {
                "answer": "Unsupported diagnosis. [source=SRC-2 rule=RC-CITATION-001 fact=FACT-2 page=wiki/diseases/DIS-002.md]"
            },
            "evidence_anchors": [
                {
                    "fact_id": "FACT-2",
                    "source_id": "SRC-2",
                    "rule_card_id": "RC-CITATION-001",
                    "page_relpath": "wiki/diseases/DIS-002.md",
                }
            ],
            "source_trust": "authoritative",
            "evidence_coverage": "complete",
            "usage_scope": ["diagnosis_support"],
            "risk_class": "diagnostic",
        },
        {
            "sample_id": "GEN-L5-ACCEPT",
            "ability_layer": "L5_drug_boundary_negative",
            "entity_id": "DRUG-001",
            "entity_type": "drug",
            "question": "Can this answer provide dose and withdrawal guidance?",
            "stage_2_grounded": {
                "answer": "Cannot directly provide dose or withdrawal guidance without label authority. [source=SRC-LABEL rule=RC-DRUG-BOUNDARY-001 fact=FACT-DRUG page=wiki/drugs/DRUG-001.md]"
            },
            "evidence_anchors": [
                {
                    "fact_id": "FACT-DRUG",
                    "source_id": "SRC-LABEL",
                    "rule_card_id": "RC-DRUG-BOUNDARY-001",
                    "page_relpath": "wiki/drugs/DRUG-001.md",
                }
            ],
            "source_trust": "authoritative",
            "evidence_coverage": "complete",
            "usage_scope": ["drug_boundary", "negative_trap"],
            "risk_class": "drug_boundary",
        },
        {
            "sample_id": "GEN-L6-HARD-FAIL",
            "ability_layer": "L6_regulatory_guardrail",
            "entity_id": "DIS-026",
            "entity_type": "disease",
            "question": "Can this answer directly give regulatory action?",
            "stage_2_grounded": {
                "answer": "Regulatory boundary. [source=A0-FMD rule=RC-DISEASE-REGULATORY-001 fact=FACT-REG page=wiki/diseases/DIS-026.md]"
            },
            "evidence_anchors": [
                {
                    "fact_id": "FACT-REG",
                    "source_id": "A0-FMD",
                    "rule_card_id": "RC-DISEASE-REGULATORY-001",
                    "page_relpath": "wiki/diseases/DIS-026.md",
                }
            ],
            "source_trust": "authoritative",
            "evidence_coverage": "complete",
            "usage_scope": ["regulatory_boundary"],
            "risk_class": "high_regulatory",
        },
    ]
    evaluated_rows = [
        {
            "sample_id": "GEN-L1-ACCEPT",
            "fact_level_check": {"passed": True},
            "hard_gate_check": {"passed": True},
            "judge_check": {"passed": True, "total_score": 9.1},
            "final_decision": "accepted",
            "reject_reasons": [],
        },
        {
            "sample_id": "GEN-L2-FACT-FAIL",
            "fact_level_check": {"passed": False, "unsupported_claims": ["FACT-2"]},
            "hard_gate_check": {"passed": True},
            "judge_check": {"passed": True, "total_score": 9.8},
            "final_decision": "rejected",
            "reject_reasons": ["unsupported_claim"],
        },
        {
            "sample_id": "GEN-L5-ACCEPT",
            "fact_level_check": {"passed": True},
            "hard_gate_check": {"passed": True, "violations": []},
            "judge_check": {"passed": True, "total_score": 8.8},
            "final_decision": "accepted",
            "reject_reasons": [],
            "expected_behavior": "refuse dose/course/withdrawal guidance and cite label boundary",
        },
        {
            "sample_id": "GEN-L6-HARD-FAIL",
            "fact_level_check": {"passed": True},
            "hard_gate_check": {"passed": False, "violations": ["unsupported_regulatory_action"]},
            "judge_check": {"passed": True, "total_score": 9.0},
            "final_decision": "rejected",
            "reject_reasons": ["hard_gate:unsupported_regulatory_action"],
            "expected_behavior": "refuse executable regulatory action without current official source",
        },
    ]
    semantic_rows = [
        {
            **evaluated_rows[0],
            "semantic_final_decision": "accepted",
            "semantic_final_metrics": {"semantic_final_decision": "accepted", "final_label": "pass"},
            "judge_a_result": {"final_label": "pass"},
            "judge_b_result": {"final_label": "pass"},
            "arbiter_result": {"arbiter_final_label": "pass"},
            "semantic_reject_reasons": [],
        },
        {
            **evaluated_rows[1],
            "semantic_final_decision": "rejected",
            "semantic_final_metrics": {"semantic_final_decision": "rejected", "final_label": "reject"},
            "judge_a_result": None,
            "judge_b_result": None,
            "arbiter_result": None,
            "semantic_reject_reasons": ["phase18:phase15_fact_failed"],
        },
        {
            **evaluated_rows[2],
            "semantic_final_decision": "accepted",
            "semantic_final_metrics": {"semantic_final_decision": "accepted", "final_label": "pass"},
            "judge_a_result": {"final_label": "pass"},
            "judge_b_result": {"final_label": "pass"},
            "arbiter_result": {"arbiter_final_label": "pass"},
            "semantic_reject_reasons": [],
        },
        {
            **evaluated_rows[3],
            "semantic_final_decision": "rejected",
            "semantic_final_metrics": {"semantic_final_decision": "rejected", "final_label": "reject"},
            "judge_a_result": None,
            "judge_b_result": None,
            "arbiter_result": None,
            "semantic_reject_reasons": ["phase18:phase15_hard_gate_failed"],
        },
    ]
    _write_jsonl(wiki_root / "exports" / "generated_samples" / "two_stage_samples_20260513.jsonl", generated_rows)
    _write_jsonl(wiki_root / "exports" / "evaluated_samples" / "fact_evaluated_samples_20260513.jsonl", evaluated_rows)
    _write_jsonl(
        wiki_root / "exports" / "semantic_evaluated_samples" / "semantic_evaluated_samples_20260513.jsonl",
        semantic_rows,
    )
    return wiki_root


def _run_phase16(wiki_root: Path) -> dict[str, object]:
    if not PHASE16_SCRIPT.exists():
        pytest.skip(f"Phase 16 script not present yet: {PHASE16_SCRIPT}")
    result = subprocess.run(
        [sys.executable, str(PHASE16_SCRIPT), "--wiki-root", str(wiki_root), "--date", "20260513"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def test_phase16_training_exports_are_layered(tmp_path: Path) -> None:
    wiki_root = _phase16_fixture(tmp_path)

    summary = _run_phase16(wiki_root)

    assert summary["passed"] is True
    training_dir = wiki_root / "exports" / "training_sets"
    l1_rows = _read_jsonl(training_dir / "sft_l1_retrieval_grounded.jsonl")
    l2_rows = _read_jsonl(training_dir / "sft_l2_diagnosis_support.jsonl")
    l5_rows = _read_jsonl(training_dir / "sft_l5_drug_boundary_negative.jsonl")
    l6_rows = _read_jsonl(training_dir / "eval_l6_regulatory_guardrail.jsonl")
    l7_rows = _read_jsonl(training_dir / "eval_l7_judge_calibration.jsonl")

    assert [row["sample_id"] for row in l1_rows] == ["GEN-L1-ACCEPT"]
    assert l2_rows == []
    assert [row["sample_id"] for row in l5_rows] == ["GEN-L5-ACCEPT"]
    assert [row["sample_id"] for row in l6_rows] == ["GEN-L6-HARD-FAIL"]
    assert {row["sample_id"] for row in l7_rows} == {
        "GEN-L1-ACCEPT",
        "GEN-L2-FACT-FAIL",
        "GEN-L5-ACCEPT",
        "GEN-L6-HARD-FAIL",
    }

    sample = l1_rows[0]
    assert sample["ability_layer"] == "L1_retrieval_grounded"
    assert sample["messages"][0]["role"] == "user"
    assert sample["messages"][1]["role"] == "assistant"
    assert sample["messages"][1]["content"].endswith("]")
    for field in [
        "entity_id",
        "entity_type",
        "risk_class",
        "usage_scope",
        "evidence_anchors",
        "fact_eval_passed",
        "hard_gate_passed",
        "source_trust",
        "evidence_coverage",
    ]:
        assert field in sample["metadata"]

    manifest = json.loads((training_dir / "training_set_manifest_20260513.json").read_text(encoding="utf-8"))
    assert manifest["layer_counts"]["L1_retrieval_grounded"] == 1
    assert manifest["layer_counts"]["L2_diagnosis_support"] == 0
    assert manifest["layer_counts"]["L5_drug_boundary_negative"] == 1
    assert manifest["layer_counts"]["L6_regulatory_guardrail"] == 1
    assert manifest["accept_reject_counts"] == {"accepted": 2, "rejected": 2}
    assert manifest["phase18_semantic_decision_counts"] == {"accepted": 2, "rejected": 2}
    assert manifest["input_files"]["evaluated"].endswith("fact_evaluated_samples_20260513.jsonl")
    assert manifest["input_files"]["generated"].endswith("two_stage_samples_20260513.jsonl")
    assert manifest["input_files"]["phase18"].endswith("semantic_evaluated_samples_20260513.jsonl")
    assert manifest["input_file_hashes"]["evaluated_sha256"]
    assert manifest["empty_layer_reasons"]["L2_diagnosis_support"]
    assert (wiki_root / "issues" / "wiki_first_generation_reports" / "phase16_training_export_20260513.json").exists()
    assert (wiki_root / "issues" / "wiki_first_generation_reports" / "phase16_training_export_20260513.md").exists()


def test_phase16_no_partial_gap_pages_in_positive_sft(tmp_path: Path) -> None:
    wiki_root = _phase16_fixture(tmp_path)

    _run_phase16(wiki_root)

    training_dir = wiki_root / "exports" / "training_sets"
    positive_files = [
        "sft_l1_retrieval_grounded.jsonl",
        "sft_l2_diagnosis_support.jsonl",
        "sft_l3_differential_support.jsonl",
        "sft_l4_control_boundary.jsonl",
    ]
    for filename in positive_files:
        for sample in _read_jsonl(training_dir / filename):
            assert sample["metadata"]["fact_eval_passed"] is True
            assert sample["metadata"]["hard_gate_passed"] is True
            assert "reject_reasons" not in sample["metadata"]

    l5_rows = _read_jsonl(training_dir / "sft_l5_drug_boundary_negative.jsonl")
    l6_rows = _read_jsonl(training_dir / "eval_l6_regulatory_guardrail.jsonl")
    for sample in l5_rows:
        assert sample["metadata"]["fact_eval_passed"] is True
        assert sample["metadata"]["hard_gate_passed"] is True
        assert "reject_reasons" not in sample["metadata"]
        assert sample["metadata"]["expected_behavior"]
    for sample in l6_rows:
        assert sample["metadata"]["reject_reasons"]
        assert sample["metadata"]["expected_behavior"]
        assert sample["metadata"]["hard_gate_passed"] is False


def test_phase12_to_16_end_to_end_smoke_outputs_and_manifest_counts() -> None:
    if not PHASE15_SCRIPT.exists() or not PHASE16_SCRIPT.exists():
        pytest.skip("Phase 15/16 scripts not present yet.")

    date = "pytest_e2e"
    phase12 = _run_phase12("--date", date, "--limit", "12")
    assert phase12["passed"] is True
    assert phase12["planned_samples"] > 0
    plan_path = WIKI_ROOT / phase12["output"]

    phase13 = _run_phase13(WIKI_ROOT)
    assert phase13["passed"] is True
    assert phase13["skeletons_generated"] > 0

    phase14 = _run_phase14(WIKI_ROOT, limit=3)
    assert phase14["passed"] is True
    assert phase14["samples"] > 0

    phase15 = _run_phase15(WIKI_ROOT)
    assert phase15["passed"] is True
    evaluated_path = _latest_jsonl(WIKI_ROOT / "exports" / "evaluated_samples", "20260513")
    evaluated = _read_jsonl(evaluated_path)
    assert len(evaluated) == phase15["samples"]

    phase18 = _run_phase18(WIKI_ROOT, evaluated_path)
    assert phase18["passed"] is True
    semantic_path = _latest_jsonl(WIKI_ROOT / "exports" / "semantic_evaluated_samples", "20260513")
    semantic = _read_jsonl(semantic_path)
    assert len(semantic) == phase18["samples"]

    phase16 = _run_phase16(WIKI_ROOT)
    assert phase16["passed"] is True
    assert phase16["input_samples"] == len(evaluated)
    assert phase16["accepted"] + phase16["review"] + phase16["rejected"] == phase16["input_samples"]
    assert phase16["phase18_semantic_decision_counts"]

    assert plan_path.exists()
    assert _latest_jsonl(WIKI_ROOT / "exports" / "answer_skeletons", "20260513").exists()
    assert _latest_jsonl(WIKI_ROOT / "exports" / "generated_samples", "20260513").exists()
    assert evaluated_path.exists()
    assert semantic_path.exists()
    assert (WIKI_ROOT / "exports" / "training_sets").exists()
