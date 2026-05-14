from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("phase16_export_layered_training_sets.py")
SPEC = importlib.util.spec_from_file_location("phase16_export_layered_training_sets", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def make_generated(sample_id: str, layer: str) -> dict[str, object]:
    return {
        "sample_id": sample_id,
        "ability_layer": layer,
        "entity_id": f"ENT-{sample_id}",
        "entity_type": "disease",
        "question": f"Question for {sample_id}",
        "stage_2_grounded": {"answer": f"Answer for {sample_id}"},
        "evidence_anchors": [],
        "source_trust": "authoritative",
        "evidence_coverage": "complete",
        "usage_scope": ["retrieval"],
        "risk_class": "normal_clinical",
    }


def make_evaluated(sample_id: str, layer: str, final_decision: str = "accepted") -> dict[str, object]:
    return {
        "sample_id": sample_id,
        "ability_layer": layer,
        "final_decision": final_decision,
        "fact_level_check": {"passed": final_decision == "accepted"},
        "hard_gate_check": {"passed": final_decision == "accepted"},
        "reject_reasons": [] if final_decision == "accepted" else ["phase15:failed"],
    }


def test_phase19_routes_samples_by_phase15_and_phase18() -> None:
    generated = [
        make_generated("GEN-A", "L1_retrieval_grounded"),
        make_generated("GEN-B", "L2_diagnosis_support"),
        make_generated("GEN-C", "L6_regulatory_guardrail"),
        make_generated("GEN-D", "L7_judge_calibration"),
    ]
    evaluated = [
        make_evaluated("GEN-A", "L1_retrieval_grounded"),
        make_evaluated("GEN-B", "L2_diagnosis_support"),
        make_evaluated("GEN-C", "L6_regulatory_guardrail"),
        make_evaluated("GEN-D", "L7_judge_calibration", final_decision="rejected"),
    ]
    phase18 = {
        "GEN-A": {
            "sample_id": "GEN-A",
            "semantic_decision": "accepted",
            "judge_a_status": "passed",
            "judge_b_status": "passed",
            "judge_status": "passed",
            "arbiter_status": "accepted",
        },
        "GEN-B": {
            "sample_id": "GEN-B",
            "semantic_decision": "review",
            "judge_a_status": "passed",
            "judge_b_status": "failed",
            "judge_status": "split",
            "arbiter_status": "review",
            "review_reasons": ["phase18:needs_human_check"],
        },
        "GEN-C": {
            "sample_id": "GEN-C",
            "semantic_decision": "accepted",
            "judge_a_status": "passed",
            "judge_b_status": "passed",
            "judge_status": "passed",
            "arbiter_status": "accepted",
        },
        "GEN-D": {
            "sample_id": "GEN-D",
            "semantic_decision": "rejected",
            "judge_a_status": "failed",
            "judge_b_status": "failed",
            "judge_status": "failed",
            "arbiter_status": "rejected",
            "reject_reasons": ["phase18:semantic_reject"],
        },
    }
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        evaluated_path = out_dir / "evaluated.jsonl"
        generated_path = out_dir / "generated.jsonl"
        phase18_path = out_dir / "phase18.jsonl"
        MODULE.write_jsonl(evaluated_path, evaluated)
        MODULE.write_jsonl(generated_path, generated)
        MODULE.write_jsonl(phase18_path, list(phase18.values()))
        buckets, queue_buckets, routing_rows = MODULE.export_layers(evaluated, generated, phase18, out_dir)
        assert [row["sample_id"] for row in buckets["L1_retrieval_grounded"]] == ["GEN-A"]
        assert buckets["L2_diagnosis_support"] == []
        assert [row["sample_id"] for row in buckets["L6_regulatory_guardrail"]] == ["GEN-C"]
        assert buckets["L7_judge_calibration"]
        assert [row["sample_id"] for row in queue_buckets["review_queue"]] == ["GEN-B"]
        assert [row["sample_id"] for row in queue_buckets["rejected_queue"]] == ["GEN-D"]
        l6_metadata = buckets["L6_regulatory_guardrail"][0]["metadata"]
        assert l6_metadata["export_bucket"] == "L6_regulatory_guardrail"
        assert l6_metadata["phase18"]["semantic_decision"] == "accepted"
        summary = MODULE.manifest(
            buckets,
            queue_buckets,
            routing_rows,
            evaluated,
            evaluated_path,
            generated_path,
            phase18_path,
            out_dir / "manifest.json",
            out_dir,
        )
        assert summary["accept_review_reject_counts"] == {"accepted": 2, "review": 1, "rejected": 1}
        assert summary["phase18_semantic_decision_counts"] == {"accepted": 2, "review": 1, "rejected": 1}
        assert summary["phase18_arbiter_status_counts"]["accepted"] == 2
        assert summary["files"]["review_queue"].endswith("training_set_review_queue.jsonl")


def test_phase19_requires_phase18_signal_when_no_external_file() -> None:
    try:
        MODULE.load_phase18_lookup(None, [make_evaluated("GEN-X", "L1_retrieval_grounded")])
    except FileNotFoundError as exc:
        assert "Phase18 semantic review results are required" in str(exc)
    else:
        raise AssertionError("Expected FileNotFoundError when Phase18 signal is missing")


if __name__ == "__main__":
    test_phase19_routes_samples_by_phase15_and_phase18()
    test_phase19_requires_phase18_signal_when_no_external_file()
    print(json.dumps({"passed": True}, ensure_ascii=False))
