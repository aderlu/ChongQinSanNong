from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
for item in (str(ROOT), str(SRC_DIR)):
    if item not in sys.path:
        sys.path.insert(0, item)

from chicken_data_synthesis.infrastructure.config import ModelRegistry, load_config
from chicken_data_synthesis.infrastructure.llm import (
    KeyPoolRegistry,
    build_openai_client,
    build_retry_policy,
    call_chat_completion_with_retry,
    extract_json_from_response,
)


RESULTS = ROOT / "results" / "swine_weak_wiki_production"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
DOSE_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:mg/kg|mg|ml|mL|g/L|g|ppm|IU|万单位)", re.I)
WITHDRAW_RE = re.compile(r"\d+\s*(?:天|日|小时|hour|hours|day|days).{0,12}(?:休药|停药|withdrawal)", re.I)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Second-review and select best weak-wiki swine rows.")
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--target", type=int, default=300)
    parser.add_argument("--parallel", type=int, default=8)
    parser.add_argument("--judge-b-key", default="judge_swine_hunyuan_turbos")
    parser.add_argument("--arbiter-key", default="judge_swine_ernie45_turbo32k")
    parser.add_argument("--judge-b-fallback-keys", default="judge_swine_hunyuan20_instruct,judge_swine_ernie45_turbo32k,judge_swine_deepseek_v32")
    parser.add_argument("--arbiter-fallback-keys", default="judge_swine_hunyuan_turbos,judge_swine_hunyuan20_instruct,judge_swine_deepseek_v32")
    parser.add_argument("--judge-max-tokens", type=int, default=950)
    parser.add_argument("--arbiter-max-tokens", type=int, default=800)
    parser.add_argument("--timeout", type=int, default=75)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--review-extra", type=int, default=80, help="Review target+extra best first-pass rows to save time.")
    parser.add_argument("--review-all", action="store_true", help="Send every input row into Judge B instead of only first-pass candidates.")
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_key_chain(primary_key: str, fallback_keys: str) -> list[str]:
    keys: list[str] = []
    for key in [primary_key, *str(fallback_keys or "").split(",")]:
        normalized = str(key).strip()
        if normalized and normalized not in keys:
            keys.append(normalized)
    return keys


def fingerprint_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:12] if api_key else ""


def parse_json(content: str | None) -> dict[str, Any]:
    payload = extract_json_from_response(content or "")
    return payload if isinstance(payload, dict) else {}


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    normalized = str(value).strip().lower()
    return normalized in {"true", "1", "yes", "y", "是", "有", "高风险"}


def call_model(model_config: Mapping[str, Any], messages: list[dict[str, str]], *, max_tokens: int):
    tuned = dict(model_config)
    tuned["max_tokens"] = max_tokens
    tuned["timeout"] = ARGS.timeout
    return call_chat_completion_with_retry(
        tuned,
        messages,
        expected_output="json",
        retry_policy=build_retry_policy(
            max_retries=ARGS.max_retries,
            request_interval_seconds=0.25,
            backoff_base_seconds=1.0,
            backoff_jitter_seconds=0.5,
        ),
        registry=KEY_POOL,
        client_builder=lambda config, **kwargs: build_openai_client(config, default_base_url=BASE_URL, **kwargs),
    )


def call_with_fallback(model_configs: list[dict[str, Any]], messages: list[dict[str, str]], *, max_tokens: int, required: list[str]):
    attempts = []
    last_result = None
    for model_config in model_configs:
        result = call_model(model_config, messages, max_tokens=max_tokens)
        parsed = parse_json(result.content)
        ok = bool(parsed) and all(key in parsed for key in required)
        attempts.append(
            {
                "model": model_config.get("name", ""),
                "success": result.success,
                "elapsed_seconds": round(result.elapsed_seconds, 2),
                "api_key_fingerprint": fingerprint_key(result.api_key),
                "parsed_json": bool(parsed),
                "has_required_json": ok,
                "error": result.error,
            }
        )
        if result.success and ok:
            return result, dict(model_config), parsed, attempts
        last_result = result
    return last_result, dict(model_configs[-1]), {}, attempts


def row_text(row: Mapping[str, str]) -> str:
    return "\n".join([row.get("user_query", ""), row.get("diagnosis", ""), row.get("prescription", ""), row.get("withdrawal_period", "")])


def local_fatal(row: Mapping[str, str]) -> list[str]:
    reasons: list[str] = []
    text = row_text(row)
    if row.get("species") != "猪":
        reasons.append("species_not_swine")
    if row.get("target_disease_mismatch") == "True":
        reasons.append("target_disease_mismatch")
    if DOSE_RE.search(text):
        reasons.append("specific_dose")
    if WITHDRAW_RE.search(row.get("withdrawal_period", "")):
        reasons.append("specific_withdrawal")
    if row.get("final_fatal_risk") == "True" or row.get("judge_a_fatal_risk") == "True":
        reasons.append("first_pass_fatal")
    return reasons


def score(row: Mapping[str, str]) -> float:
    try:
        return float(row.get("final_total_score") or 0)
    except Exception:
        return 0.0


def build_judge_b_messages(row: Mapping[str, str]) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "你是猪病弱监督数据的第二评审员。请只输出 JSON。"
                "不要按权威引用扣分，本任务只判断测试/初步微调数据是否有效。"
                "重点检查：场景真实性、症状和目标疾病是否匹配、诊断与处理方向是否相互印证、是否有危险建议。"
                "处方不要求具体药名、剂量或休药期；相反，出现具体剂量或具体休药期承诺应视为风险。"
                "重大疫病、疑似法定疫病、人兽共患病、中毒和临近出栏场景必须有安全边界。"
                "输出字段：total_score,diagnosis_accuracy,pathology_logic,prescription_safety,data_quality,fatal_risk,final_label,summary,weaknesses,improvement_actions。"
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "disease_name": row.get("disease_name", ""),
                    "user_query": row.get("user_query", ""),
                    "diagnosis": row.get("diagnosis", ""),
                    "prescription": row.get("prescription", ""),
                    "withdrawal_period": row.get("withdrawal_period", ""),
                    "judge_a_score": row.get("judge_a_total_score", ""),
                    "judge_a_summary": row.get("judge_a_summary", ""),
                },
                ensure_ascii=False,
            ),
        },
    ]


def build_arbiter_messages(row: Mapping[str, str], judge_b: Mapping[str, Any], local_reasons: list[str]) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "你是猪病数据仲裁员。请只输出 JSON。"
                "你需要在 judge_a、judge_b 和本地规则之间作最终裁决。"
                "本阶段目标是筛选模型测试/弱监督微调数据，不要求 source 引用或具体剂量。"
                "若诊断和处置方向安全且疾病匹配，可判 pass；若存在轻微不足但可参考，判 review；若跑题、危险或明显错误，判 reject。"
                "输出字段：arbiter_final_label,arbiter_final_score,arbiter_fatal_risk,arbiter_agreed_with_judge,arbiter_reason,required_fix。"
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "row": {
                        "disease_name": row.get("disease_name", ""),
                        "user_query": row.get("user_query", ""),
                        "diagnosis": row.get("diagnosis", ""),
                        "prescription": row.get("prescription", ""),
                        "withdrawal_period": row.get("withdrawal_period", ""),
                    },
                    "judge_a": {
                        "score": row.get("judge_a_total_score", ""),
                        "label": row.get("final_label", ""),
                        "fatal": row.get("judge_a_fatal_risk", ""),
                        "summary": row.get("judge_a_summary", ""),
                    },
                    "judge_b": judge_b,
                    "local_reasons": local_reasons,
                },
                ensure_ascii=False,
            ),
        },
    ]


def needs_arbitration(row: Mapping[str, str], judge_b: Mapping[str, Any], local_reasons: list[str]) -> bool:
    a_label = row.get("final_label", "")
    b_label = str(judge_b.get("final_label", ""))
    a_score = score(row)
    b_score = float(judge_b.get("total_score") or 0)
    a_fatal = row.get("judge_a_fatal_risk") == "True" or row.get("final_fatal_risk") == "True"
    b_fatal = as_bool(judge_b.get("fatal_risk"))
    high_risk = any(term in row.get("disease_name", "") for term in ["非洲猪瘟", "口蹄疫", "猪瘟", "布鲁氏", "狂犬", "中毒"])
    return bool(
        local_reasons
        or a_label != b_label
        or abs(a_score - b_score) >= 8
        or a_fatal != b_fatal
        or high_risk
    )


def final_decision(row: Mapping[str, str], judge_b: Mapping[str, Any], arbiter: Mapping[str, Any] | None, local_reasons: list[str]) -> tuple[str, float, bool]:
    if arbiter:
        label = str(arbiter.get("arbiter_final_label") or "review")
        final_score = float(arbiter.get("arbiter_final_score") or min(score(row), float(judge_b.get("total_score") or 0)))
        fatal = as_bool(arbiter.get("arbiter_fatal_risk"))
        if local_reasons and "target_disease_mismatch" not in local_reasons:
            fatal = True
        return label, final_score, fatal
    if local_reasons:
        return "reject", min(score(row), float(judge_b.get("total_score") or 0)), True
    b_score = float(judge_b.get("total_score") or 0)
    if row.get("final_label") == "pass" and judge_b.get("final_label") == "pass" and score(row) >= 80 and b_score >= 80 and not as_bool(judge_b.get("fatal_risk")):
        return "pass", round((score(row) + b_score) / 2, 2), False
    if min(score(row), b_score) >= 75 and not as_bool(judge_b.get("fatal_risk")):
        return "review", round((score(row) + b_score) / 2, 2), False
    return "reject", round((score(row) + b_score) / 2, 2), as_bool(judge_b.get("fatal_risk"))


def process(index: int, total: int, row: dict[str, str]) -> dict[str, Any]:
    print(f"[{index}/{total}] second-review {row.get('index')} {row.get('disease_name')}", flush=True)
    started = time.perf_counter()
    judge_b_result, judge_b_model, judge_b, judge_b_attempts = call_with_fallback(
        JUDGE_B_CONFIGS,
        build_judge_b_messages(row),
        max_tokens=ARGS.judge_max_tokens,
        required=["total_score", "final_label", "fatal_risk"],
    )
    local_reasons = local_fatal(row)
    arbiter = {}
    arbiter_model = {}
    arbiter_attempts = []
    if needs_arbitration(row, judge_b, local_reasons):
        _, arbiter_model, arbiter, arbiter_attempts = call_with_fallback(
            ARBITER_CONFIGS,
            build_arbiter_messages(row, judge_b, local_reasons),
            max_tokens=ARGS.arbiter_max_tokens,
            required=["arbiter_final_label", "arbiter_final_score", "arbiter_fatal_risk", "arbiter_reason"],
        )
    label, final_score, fatal = final_decision(row, judge_b, arbiter, local_reasons)
    elapsed = round(time.perf_counter() - started, 2)
    print(f"[{index}/{total}] done row={row.get('index')} label={label} score={final_score} fatal={fatal} {elapsed}s", flush=True)
    return {
        "row": row,
        "judge_b": judge_b,
        "judge_b_model": judge_b_model.get("name", ""),
        "judge_b_attempts": judge_b_attempts,
        "arbiter": arbiter,
        "arbiter_model": arbiter_model.get("name", ""),
        "arbiter_attempts": arbiter_attempts,
        "needed_arbitration": bool(arbiter),
        "local_reasons": local_reasons,
        "final_label": label,
        "final_score": final_score,
        "final_fatal": fatal,
        "elapsed": elapsed,
    }


def update_csv_row(item: Mapping[str, Any], fieldnames: list[str]) -> dict[str, str]:
    row = dict(item["row"])
    judge_b = item.get("judge_b") or {}
    arbiter = item.get("arbiter") or {}
    row["judge_b_model"] = str(item.get("judge_b_model") or "")
    row["judge_b_total_score"] = str(judge_b.get("total_score", ""))
    row["judge_b_diagnosis_accuracy"] = str(judge_b.get("diagnosis_accuracy", ""))
    row["judge_b_pathology_logic"] = str(judge_b.get("pathology_logic", ""))
    row["judge_b_prescription_safety"] = str(judge_b.get("prescription_safety", ""))
    row["judge_b_data_quality"] = str(judge_b.get("data_quality", ""))
    row["judge_b_fatal_risk"] = "True" if as_bool(judge_b.get("fatal_risk")) else "False"
    row["judge_b_structured_pass"] = "True" if judge_b.get("final_label") == "pass" else "False"
    row["judge_b_summary"] = str(judge_b.get("summary") or "") + ("\n问题：" + "；".join(map(str, judge_b.get("weaknesses") or [])) if judge_b.get("weaknesses") else "")
    row["needed_arbitration"] = "True" if item.get("needed_arbitration") else "False"
    row["arbiter_model"] = str(item.get("arbiter_model") or "")
    row["arbiter_agreed_with_judge"] = str(arbiter.get("arbiter_agreed_with_judge", ""))
    row["arbiter_final_label"] = str(arbiter.get("arbiter_final_label", ""))
    row["arbiter_reason"] = str(arbiter.get("arbiter_reason", ""))
    row["final_total_score"] = str(item.get("final_score", ""))
    row["final_fatal_risk"] = "True" if item.get("final_fatal") else "False"
    row["final_label"] = str(item.get("final_label") or "")
    row["judge_b_seconds"] = str(item.get("elapsed", ""))
    row["rule_codes"] = "|".join(item.get("local_reasons") or [])
    row["rule_messages"] = "|".join(item.get("local_reasons") or [])
    return {key: row.get(key, "") for key in fieldnames}


def main() -> None:
    input_path = Path(ARGS.input_csv)
    rows = read_rows(input_path)
    fieldnames = list(rows[0].keys())
    first_pass = [
        row for row in rows
        if row.get("final_label") == "pass"
        and row.get("final_fatal_risk") == "False"
        and row.get("target_disease_mismatch") == "False"
        and score(row) >= 80
        and not local_fatal(row)
    ]
    first_pass.sort(key=lambda row: score(row), reverse=True)
    if ARGS.review_all:
        candidates = sorted(rows, key=lambda row: (row.get("final_label") != "pass", -score(row), int(row.get("index") or 0)))
    else:
        review_count = min(len(first_pass), ARGS.target + ARGS.review_extra)
        candidates = first_pass[:review_count]
    print(json.dumps({"input_rows": len(rows), "first_pass_candidates": len(first_pass), "second_reviewing": len(candidates), "target": ARGS.target}, ensure_ascii=False), flush=True)

    reviewed: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, ARGS.parallel)) as executor:
        futures = {executor.submit(process, idx, len(candidates), row): idx for idx, row in enumerate(candidates, start=1)}
        for future in as_completed(futures):
            reviewed.append(future.result())
    reviewed.sort(key=lambda item: (item["final_label"] != "pass", -float(item["final_score"]), int(item["row"].get("index") or 0)))

    updated = [update_csv_row(item, fieldnames) for item in reviewed]
    valid = [row for row in updated if row.get("final_label") == "pass" and row.get("final_fatal_risk") == "False"]
    final300 = valid[: ARGS.target]
    rejects = [row for row in updated if row not in final300]

    stem = input_path.stem
    out_full = RESULTS / f"{stem}_dual_reviewed_{TIMESTAMP}.csv"
    out_final = RESULTS / f"{stem}_dual_final{ARGS.target}_{TIMESTAMP}.csv"
    out_rejects = RESULTS / f"{stem}_dual_rejects_{TIMESTAMP}.csv"
    raw = RESULTS / f"{stem}_dual_review_raw_{TIMESTAMP}.json"
    summary_path = RESULTS / f"{stem}_dual_review_summary_{TIMESTAMP}.json"

    write_rows(out_full, updated, fieldnames)
    write_rows(out_final, final300, fieldnames)
    write_rows(out_rejects, rejects, fieldnames)
    raw.write_text(json.dumps(reviewed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    valid_scores = [float(row.get("final_total_score") or 0) for row in final300]
    summary = {
        "input_csv": str(input_path),
        "input_rows": len(rows),
        "first_pass_candidates": len(first_pass),
        "second_reviewed": len(reviewed),
        "dual_valid": len(valid),
        "final_selected": len(final300),
        "target": ARGS.target,
        "final_score_avg": round(statistics.mean(valid_scores), 2) if valid_scores else 0,
        "final_score_min": min(valid_scores) if valid_scores else 0,
        "final_score_max": max(valid_scores) if valid_scores else 0,
        "arbitration_count": sum(1 for item in reviewed if item.get("needed_arbitration")),
        "output_full": str(out_full),
        "output_final": str(out_final),
        "output_rejects": str(out_rejects),
        "raw_json": str(raw),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({**summary, "summary": str(summary_path)}, ensure_ascii=False, indent=2))


CONFIG = load_config(ROOT, include_local=True)
MODEL_REGISTRY = ModelRegistry.from_config(CONFIG)
BASE_URL = CONFIG["api"]["base_url"]
KEY_POOL = KeyPoolRegistry()
ARGS = parse_args()
JUDGE_B_CONFIGS = [MODEL_REGISTRY.get_candidate(key) for key in parse_key_chain(ARGS.judge_b_key, ARGS.judge_b_fallback_keys)]
ARBITER_CONFIGS = [MODEL_REGISTRY.get_candidate(key) for key in parse_key_chain(ARGS.arbiter_key, ARGS.arbiter_fallback_keys)]


if __name__ == "__main__":
    main()
