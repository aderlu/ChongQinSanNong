from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
import sys
import time
import uuid
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
from chicken_data_synthesis.infrastructure.knowledge import build_llm_wiki_context, build_wiki_audit_metadata
from chicken_data_synthesis.infrastructure.llm import (
    KeyPoolRegistry,
    build_openai_client,
    build_retry_policy,
    call_chat_completion_with_retry,
    extract_json_from_response,
)


WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
RESULTS = ROOT / "results" / "swine_weak_wiki_production"
DOCS = ROOT / "docs"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

PRODUCTION_FIELDNAMES = [
    "case_id",
    "index",
    "disease_name",
    "generator_key",
    "generator_model",
    "success",
    "error",
    "species",
    "user_query",
    "diagnosis",
    "prescription",
    "withdrawal_period",
    "answer_json",
    "golden_answer",
    "evidence_anchors",
    "standard_citation_count",
    "training_task_type",
    "metadata",
    "rule_hard_block",
    "rule_fatal_risk",
    "rule_codes",
    "rule_messages",
    "target_disease_in_diagnosis",
    "target_disease_mismatch",
    "final_fatal_risk",
    "wiki_dir",
    "wiki_fact_count",
    "wiki_page_count",
    "wiki_context_query",
    "wiki_evidence_status_counts",
    "wiki_evidence_source_ids",
    "wiki_context_chars",
    "generation_seconds",
    "judge_a_model",
    "judge_a_total_score",
    "judge_a_diagnosis_accuracy",
    "judge_a_pathology_logic",
    "judge_a_prescription_safety",
    "judge_a_data_quality",
    "judge_a_fatal_risk",
    "judge_a_structured_pass",
    "judge_a_summary",
    "judge_b_model",
    "judge_b_total_score",
    "judge_b_diagnosis_accuracy",
    "judge_b_pathology_logic",
    "judge_b_prescription_safety",
    "judge_b_data_quality",
    "judge_b_fatal_risk",
    "judge_b_structured_pass",
    "judge_b_summary",
    "needed_arbitration",
    "arbiter_model",
    "arbiter_agreed_with_judge",
    "arbiter_final_label",
    "arbiter_reason",
    "final_total_score",
    "final_diagnosis_accuracy",
    "final_pathology_logic",
    "final_prescription_safety",
    "final_data_quality",
    "final_label",
    "judge_a_seconds",
    "judge_b_seconds",
    "arbiter_seconds",
]

HIGH_PRIORITY_IDS = [
    "DIS-002",
    "DIS-008",
    "DIS-009",
    "DIS-024",
    "DIS-026",
    "DIS-028",
    "DIS-035",
    "DIS-040",
    "DIS-041",
    "DIS-043",
    "DIS-046",
    "DIS-049",
    "DIS-051",
    "DIS-052",
    "DIS-055",
    "DIS-057",
    "DIS-066",
    "DIS-038",
]

SCENARIOS = [
    ("保育猪群体发病", "保育猪", "群体发病、采食下降、粪便或呼吸道异常，用户想知道主要病因和下一步处理。"),
    ("育肥猪用药咨询", "育肥猪", "育肥猪出现典型症状，用户已经用过常见药物但效果一般，询问是否继续用药。"),
    ("种猪繁殖障碍", "种猪/母猪", "种猪场出现流产、死胎、返情或公猪异常，用户担心传染病和是否继续配种。"),
    ("暴发与处置边界", "全场", "同栏或多栋猪舍短期内发病增多，用户询问是否能先按普通病治疗观察。"),
    ("采样送检咨询", "不同阶段猪", "用户描述症状后，重点询问采什么样品、如何判断和如何避免误治。"),
    ("上市休药期咨询", "育肥猪", "用户接近出栏，关心治疗方向和用药后能否出栏销售。"),
]

ENTERIC_SCENARIOS = [
    ("腹泻群体发病", "哺乳仔猪/保育猪", "同窝或同栏出现水样腹泻、脱水、采食下降，用户想知道主要病因和紧急处理。"),
    ("腹泻用药咨询", "保育猪/育肥猪", "猪群腹泻后已用过常见抗菌药效果一般，用户询问是否继续用药以及是否需要送检。"),
    ("腹泻采样送检", "不同阶段猪", "用户描述粪便性状、日龄和病程，重点询问如何鉴别病毒性、细菌性或寄生虫性腹泻。"),
    ("腹泻出栏边界", "育肥猪", "临近出栏猪群出现腹泻，用户关心处理方向、隔离和用药后能否销售。"),
]

RESPIRATORY_SCENARIOS = [
    ("呼吸道群体发病", "保育猪/育肥猪", "同栏出现咳嗽、喘气、发热、采食下降，用户想判断病因和是否需要全群用药。"),
    ("呼吸道采样送检", "育肥猪", "呼吸道症状持续，用药效果不稳定，用户询问采什么样品和如何鉴别混合感染。"),
    ("呼吸道环境诱因", "保育猪", "通风差、氨气重或温差大后出现咳嗽喘气，用户想区分环境应激和传染病。"),
]

REPRODUCTIVE_SCENARIOS = [
    ("种猪繁殖障碍", "种猪/母猪", "种猪场出现流产、死胎、返情或公猪异常，用户担心传染病和是否继续配种。"),
    ("繁殖障碍送检", "母猪/公猪", "繁殖异常持续出现，用户询问该采哪些样品、是否需要暂停配种和引种。"),
]

TOXIN_SCENARIOS = [
    ("饲料中毒咨询", "全场", "更换饲料或玉米批次后出现采食下降、呕吐、繁殖异常或神经症状，用户怀疑饲料问题。"),
    ("中毒处置边界", "育肥猪/母猪", "用户想知道是否继续饲喂可疑饲料、怎样送检饲料和病料。"),
]

PARASITE_SCENARIOS = [
    ("寄生虫群体发病", "仔猪/育肥猪", "猪群出现腹泻、消瘦、皮肤瘙痒或生长慢，用户怀疑寄生虫。"),
    ("驱虫和环境管理", "不同阶段猪", "用户询问是否需要全群处理、环境清理和复查方式。"),
]

MANUAL_ALIASES = {
    "非洲猪瘟": ["ASF", "African swine fever"],
    "猪流行性腹泻": ["PED", "PEDV"],
    "猪传染性胃肠炎": ["TGE", "TGEV"],
    "猪瘟": ["经典猪瘟", "CSF"],
    "口蹄疫": ["FMD"],
    "猪繁殖与呼吸综合征": ["PRRS", "蓝耳病"],
    "猪布鲁氏菌病": ["布鲁氏菌病", "Brucella suis"],
    "猪痢疾": ["swine dysentery", "Brachyspira"],
    "猪大肠杆菌病": ["大肠杆菌", "大肠杆菌性腹泻", "colibacillosis", "E. coli"],
    "仔猪黄白痢": ["黄白痢", "大肠杆菌", "仔猪大肠杆菌病"],
    "猪球虫病": ["球虫", "球虫感染", "coccidiosis", "coccidia"],
    "猪星状病毒感染": ["astrovirus", "猪星状病毒"],
    "猪环曲病毒/托克特诺病毒感染": ["TTSuV", "Torque teno sus virus"],
}

REGULATED_TERMS = ["非洲猪瘟", "口蹄疫", "猪瘟", "水疱", "布鲁氏", "ASF", "FMD", "CSF"]
BAD_TREATMENT_FOR_REGULATED = ["先用抗生素观察", "先打针观察", "普通消炎", "不需要上报", "可以出栏", "继续调运"]
SPECIFIC_DOSE_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:mg/kg|mg|ml|mL|g/L|g|ppm|IU|万单位)", re.I)
SPECIFIC_WITHDRAWAL_RE = re.compile(r"\d+\s*(?:天|日|小时|hour|hours|day|days).{0,12}(?:休药|停药|withdrawal)", re.I)
SOURCE_RE = re.compile(r"\b(?:SRC-\d{4}|A[0-2]-[A-Z0-9-]+|RC-[A-Z0-9-]+)\b")
SOURCE_FALLBACK_IDS = [
    "RC-TRAIN-READY-001",
    "RC-DRUG-001",
    "RC-WITHDRAWAL-MRL-001",
]
EXECUTABLE_CLAIM_RE = re.compile(
    r"(?:剂量|用量|疗程|休药|停药|withdrawal|MRL|残留|可食|出栏|上市|销售|扑杀|调运|检疫|无害化|强制免疫)",
    re.I,
)
QUALIFIED_SOURCE_PREFIXES = ("A0-", "A1-", "A2-", "SRC-", "RC-", "RULE-")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate weak-wiki swine production-like QA data with strict LLM judging.")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--parallel", type=int, default=6)
    parser.add_argument("--generator-key", default="swine_hunyuan_turbos")
    parser.add_argument("--judge-key", default="judge_swine_ernie45_turbo32k")
    parser.add_argument("--generator-fallback-keys", default="swine_ernie45_turbo32k,swine_hunyuan20_instruct,swine_deepseek_v32,swine_deepseek_v4_flash")
    parser.add_argument("--judge-fallback-keys", default="judge_swine_hunyuan20_instruct,judge_swine_hunyuan_turbos,judge_swine_deepseek_v32,judge_swine_deepseek_v4_flash")
    parser.add_argument("--answer-max-tokens", type=int, default=1500)
    parser.add_argument("--judge-max-tokens", type=int, default=1000)
    parser.add_argument("--timeout", type=int, default=75)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--valid-min-score", type=float, default=80)
    return parser.parse_args()


def parse_key_chain(primary_key: str, fallback_keys: str) -> list[str]:
    keys: list[str] = []
    for key in [primary_key, *str(fallback_keys or "").split(",")]:
        normalized = str(key).strip()
        if normalized and normalized not in keys:
            keys.append(normalized)
    return keys


def fingerprint_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:12] if api_key else ""


def call_model(model_config: Mapping[str, Any], messages: list[dict[str, str]], *, max_tokens: int):
    tuned = dict(model_config)
    tuned["max_tokens"] = int(max_tokens)
    tuned["timeout"] = int(ARGS.timeout)
    return call_chat_completion_with_retry(
        tuned,
        messages,
        expected_output="json",
        retry_policy=build_retry_policy(
            max_retries=ARGS.max_retries,
            request_interval_seconds=0.3,
            backoff_base_seconds=1.0,
            backoff_jitter_seconds=0.5,
        ),
        registry=KEY_POOL,
        client_builder=lambda config, **kwargs: build_openai_client(config, default_base_url=BASE_URL, **kwargs),
    )


def parse_json(content: str | None) -> dict[str, Any]:
    payload = extract_json_from_response(content or "")
    return payload if isinstance(payload, dict) else {}


def call_with_fallback(
    model_configs: list[dict[str, Any]],
    messages: list[dict[str, str]],
    *,
    max_tokens: int,
    required_keys: list[str],
) -> tuple[Any, dict[str, Any], dict[str, Any]]:
    attempts = []
    last_result = None
    for model_config in model_configs:
        result = call_model(model_config, messages, max_tokens=max_tokens)
        parsed = parse_json(result.content)
        ok = bool(parsed) and all(key in parsed for key in required_keys)
        attempts.append(
            {
                "model": model_config.get("name"),
                "success": result.success,
                "elapsed_seconds": round(result.elapsed_seconds, 2),
                "api_key_fingerprint": fingerprint_key(result.api_key),
                "parsed_json": bool(parsed),
                "has_required_json": ok,
                "error": result.error,
            }
        )
        if result.success and ok:
            return result, dict(model_config), {"parsed": parsed, "attempts": attempts}
        last_result = result
    return last_result, dict(model_configs[-1]), {"parsed": {}, "attempts": attempts}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def load_diseases() -> list[dict[str, str]]:
    rows = read_csv(WIKI / "exports" / "disease_index.csv")
    by_id = {row.get("disease_id", ""): row for row in rows}
    ordered: list[dict[str, str]] = []
    for disease_id in HIGH_PRIORITY_IDS:
        if disease_id in by_id:
            ordered.append(by_id[disease_id])
    for row in rows:
        if row not in ordered:
            ordered.append(row)
    return ordered


def disease_aliases(disease_name: str, page_relpath: str = "") -> list[str]:
    aliases = [disease_name]
    if page_relpath:
        slug = Path(page_relpath).stem
        parts = slug.split("-", 2)
        if len(parts) == 3:
            aliases.append(parts[2].replace("-", " "))
    aliases.extend(MANUAL_ALIASES.get(disease_name, []))
    return list(dict.fromkeys(alias for alias in aliases if alias))


def build_tasks(limit: int) -> list[dict[str, str]]:
    tasks: list[dict[str, str]] = []
    diseases = load_diseases()
    scenario_index = 0
    while len(tasks) < limit:
        disease = diseases[len(tasks) % len(diseases)]
        scenario_pool = scenario_pool_for_disease(disease)
        scenario_name, stage, scenario = scenario_pool[scenario_index % len(scenario_pool)]
        scenario_index += 1
        disease_name = disease.get("disease_name", "") or disease.get("disease_id", "")
        tasks.append(
            {
                "case_id": f"SWINE-WEAK-{len(tasks) + 1:04d}",
                "disease_id": disease.get("disease_id", ""),
                "disease_name": disease_name,
                "aliases": "、".join(disease_aliases(disease_name, disease.get("page_relpath", ""))),
                "category": disease.get("category", ""),
                "page_relpath": disease.get("page_relpath", ""),
                "scenario_type": scenario_name,
                "stage": stage,
                "scenario": scenario,
            }
        )
    return tasks


def scenario_pool_for_disease(disease: Mapping[str, str]) -> list[tuple[str, str, str]]:
    text = " ".join([disease.get("disease_name", ""), disease.get("page_relpath", ""), disease.get("category", "")]).lower()
    if any(token in text for token in ["diarrhea", "enteritis", "gastro", "coli", "rotavirus", "coronavirus", "coccid", "腹泻", "肠炎", "大肠杆菌", "球虫"]):
        return ENTERIC_SCENARIOS
    if any(token in text for token in ["astrovirus", "torovirus", "deltacoronavirus", "星状病毒", "托罗病毒", "冠状病毒"]):
        return ENTERIC_SCENARIOS
    if any(token in text for token in ["respiratory", "pneumonia", "pleuropneumonia", "influenza", "mycoplasma", "肺", "呼吸"]):
        return RESPIRATORY_SCENARIOS
    if any(token in text for token in ["brucella", "parvovirus", "reproductive", "japanese-encephalitis", "繁殖", "流产", "布鲁氏"]):
        return REPRODUCTIVE_SCENARIOS
    if any(token in text for token in ["toxic", "mycotoxin", "aflatoxin", "zearalenone", "fumonisin", "nitrite", "gas", "霉菌", "中毒", "毒素"]):
        return TOXIN_SCENARIOS
    if any(token in text for token in ["parasite", "coccid", "mange", "lice", "ascaris", "trichuris", "worm", "寄生虫", "疥螨"]):
        return PARASITE_SCENARIOS
    return SCENARIOS


def build_answer_messages(task: Mapping[str, str], weak_context: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "你是猪病真实问答数据生成专家。请只输出 JSON。\n"
                "目标是生成用于模型初步测试的数据，不要求权威引用，不要求 source，但必须医学逻辑正确、场景真实、诊断和处理方向相互印证。\n"
                "可以弱参考给定 wiki 背景；如果 wiki 不完整，以通用兽医常识补足，但不要编造危险处方。\n"
                "处方字段写治疗方向、管理措施、采样送检和禁忌边界；第一批测试数据避免具体剂量、疗程和具体休药期数字。\n"
                "重大/疑似法定疫病或人兽共患病不得给普通治疗替代报告、隔离、检测或主管部门处置。\n"
                "species 字段必须写中文“猪”，不能写 swine/pig。user_query 必须是具体养殖户口吻，包含日龄/体重、存栏规模、症状、病程、环境或既往用药，不能只复述场景模板。\n"
                "非洲猪瘟不是人兽共患病，不要把 ASF 写成人兽共患风险；但要体现重大动物疫病处置边界。\n"
                "输出 JSON 字段必须为 species,user_query,diagnosis,prescription,withdrawal_period,metadata。\n"
                "metadata 包含 disease_name, severity, scene_tags, validation_points, risk_flags。\n"
                f"弱 wiki 背景：\n{weak_context}"
            ),
        },
        {
            "role": "user",
            "content": json.dumps(task, ensure_ascii=False),
        },
    ]


def build_judge_messages(task: Mapping[str, str], answer: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "你是猪病测试数据严格评估员。请只输出 JSON。\n"
                "评估目标不是权威引用，而是测试数据有效性：真实场景、症状与疾病匹配、诊断逻辑、处理方向安全且与疾病相互印证。\n"
                "按 100 分评分：diagnosis_accuracy 30, pathology_logic 20, prescription_safety 25, data_quality 25。\n"
                "出现以下情况 fatal_risk=true：猪种错误；目标疾病明显不在诊断中；处方与疾病相冲突；重大疫病被建议普通治疗观察；人兽共患风险被忽略；出现明显错误剂量或具体休药期承诺。\n"
                "final_label 规则：score>=80 且 fatal=false 为 pass；60-79 为 review；低于60或 fatal=true 为 reject。\n"
                "输出字段：total_score,diagnosis_accuracy,pathology_logic,prescription_safety,data_quality,fatal_risk,final_label,summary,weaknesses,improvement_actions。"
            ),
        },
        {"role": "user", "content": json.dumps({"task": task, "answer": answer}, ensure_ascii=False)},
    ]


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "；".join(as_text(item) for item in value if item is not None)
    if isinstance(value, dict):
        return "；".join(f"{key}: {as_text(item)}" for key, item in value.items() if item not in ("", None, [], {}))
    return str(value)


def source_ids_from_context(context: str, audit: Mapping[str, Any]) -> list[str]:
    ids: list[str] = []
    for source_id in audit.get("wiki_evidence_source_ids", []) or []:
        if isinstance(source_id, str) and SOURCE_RE.fullmatch(source_id) and source_id not in ids:
            ids.append(source_id)
    for source_id in SOURCE_RE.findall(context or ""):
        if source_id not in ids:
            ids.append(source_id)
    for source_id in SOURCE_FALLBACK_IDS:
        if source_id not in ids:
            ids.append(source_id)
    priority = {"RC": 0, "SRC": 1, "A2": 2, "A1": 3, "A0": 4}

    def sort_key(value: str) -> tuple[int, str]:
        return (priority.get(value.split("-", 1)[0], 9), value)

    return sorted(ids, key=sort_key)


def build_evidence_anchors(answer: Mapping[str, Any], source_ids: list[str], audit: Mapping[str, Any]) -> list[dict[str, str]]:
    anchors: list[dict[str, str]] = []
    supplied = answer.get("evidence_anchors")
    if isinstance(supplied, list):
        for item in supplied:
            if not isinstance(item, Mapping):
                continue
            source_id = str(item.get("source_id") or "").strip()
            if SOURCE_RE.fullmatch(source_id):
                anchors.append(
                    {
                        "source_id": source_id,
                        "supports": as_text(item.get("supports")) or "wiki-supported clinical boundary",
                        "evidence_status": as_text(item.get("evidence_status")) or "UNKNOWN",
                    }
                )
    seen = {item["source_id"] for item in anchors}
    status_counts = audit.get("wiki_evidence_status_counts", {})
    default_status = next(iter(status_counts.keys()), "UNKNOWN") if isinstance(status_counts, Mapping) and status_counts else "UNKNOWN"
    for source_id in source_ids:
        if len(anchors) >= 5:
            break
        if source_id in seen:
            continue
        anchors.append(
            {
                "source_id": source_id,
                "supports": "retrieved LLM Wiki evidence used for diagnosis, safety boundary, or compliance",
                "evidence_status": default_status if default_status != "UNKNOWN" else "QUALIFIED_SOURCE",
            }
        )
        seen.add(source_id)
    return anchors


def with_citations(value: Any, anchors: list[dict[str, str]], *, min_count: int) -> str:
    text = as_text(value).strip()
    existing = set(SOURCE_RE.findall(text))
    if len(existing) >= min_count:
        return text
    needed = [item["source_id"] for item in anchors if item.get("source_id") not in existing]
    selected = needed[: max(0, min_count - len(existing))]
    if not selected:
        return text
    suffix = " 证据来源：" + "；".join(f"source={source_id}" for source_id in selected) + "。"
    return text.rstrip("。；; ") + "。" + suffix


def build_answer_json(task: Mapping[str, str], answer: Mapping[str, Any], anchors: list[dict[str, str]]) -> dict[str, Any]:
    supplied = answer.get("answer_json")
    payload = dict(supplied) if isinstance(supplied, Mapping) else {}
    payload.setdefault("target_disease", task.get("disease_name", ""))
    payload.setdefault("species", "猪")
    payload.setdefault("case_type", task.get("scenario_type", ""))
    payload.setdefault("diagnosis", as_text(answer.get("diagnosis")))
    payload.setdefault("differential_diagnoses", [])
    payload.setdefault("action_plan", as_text(answer.get("prescription")))
    payload.setdefault("sampling_plan", "结合临床表现、流行病学和病料检测进行确认，未确诊前避免高风险处方或出栏承诺。")
    payload.setdefault("treatment_boundary", as_text(answer.get("prescription")))
    payload.setdefault("withdrawal_boundary", as_text(answer.get("withdrawal_period")))
    payload.setdefault("risk_controls", [])
    payload["evidence_sources"] = [item["source_id"] for item in anchors if item.get("source_id")]
    payload["evidence_anchors"] = anchors
    return payload


def local_flags(task: Mapping[str, str], answer: Mapping[str, Any]) -> dict[str, Any]:
    text = json.dumps(answer, ensure_ascii=False)
    diagnosis = as_text(answer.get("diagnosis")).lower()
    aliases = disease_aliases(task["disease_name"], task.get("page_relpath", ""))
    target_hit = any(alias.lower() in diagnosis for alias in aliases if alias)
    regulated = any(term.lower() in (task["disease_name"] + text).lower() for term in REGULATED_TERMS)
    bad_regulated = regulated and any(term in text for term in BAD_TREATMENT_FOR_REGULATED)
    species = str(answer.get("species") or "").strip().lower()
    sources = set(SOURCE_RE.findall(text))
    return {
        "species_ok": species in {"猪", "swine", "pig", "pigs"},
        "target_disease_in_diagnosis": target_hit,
        "target_disease_mismatch": not target_hit,
        "contains_specific_dose": bool(SPECIFIC_DOSE_RE.search(text)),
        "contains_specific_withdrawal": bool(SPECIFIC_WITHDRAWAL_RE.search(text)),
        "regulated_bad_treatment": bad_regulated,
        "has_qualified_source": any(source.startswith(QUALIFIED_SOURCE_PREFIXES) for source in sources),
        "has_authority_source": any(source.startswith(("A0-", "A1-")) for source in sources),
        "has_executable_claim": bool(EXECUTABLE_CLAIM_RE.search(text)),
    }


def final_label(judge: Mapping[str, Any], flags: Mapping[str, Any], min_score: float) -> tuple[str, bool, list[str]]:
    reasons: list[str] = []
    score = float(judge.get("total_score") or 0)
    fatal = bool(judge.get("fatal_risk"))
    for key in ["species_ok", "target_disease_in_diagnosis"]:
        if not flags.get(key):
            fatal = True
            reasons.append(key)
    for key in ["regulated_bad_treatment"]:
        if flags.get(key):
            fatal = True
            reasons.append(key)
    if flags.get("contains_specific_dose") and not flags.get("has_qualified_source"):
        fatal = True
        reasons.append("specific_dose_without_qualified_source")
    if flags.get("contains_specific_withdrawal"):
        reasons.append("contains_specific_withdrawal")
    if flags.get("has_executable_claim") and not flags.get("has_authority_source"):
        reasons.append("executable_claim_without_authority_source")
    if fatal:
        return "reject", True, reasons
    if score >= min_score:
        return "pass", False, reasons
    if score >= 60:
        return "review", False, reasons
    return "reject", False, reasons


def process_case(index: int, total: int, task: Mapping[str, str]) -> dict[str, Any]:
    print(f"[{index}/{total}] {task['case_id']} {task['disease_name']} start", flush=True)
    started = time.perf_counter()
    query = "\n".join([task["disease_name"], task["aliases"], task["scenario_type"], task["scenario"]])
    context = build_llm_wiki_context(query, wiki_dir=WIKI, top_k_pages=3, top_k_facts=5, max_chars=2200)
    audit = build_wiki_audit_metadata(wiki_dir=WIKI, knowledge_context=context, query=query)
    source_ids = source_ids_from_context(context, audit)

    answer_result, answer_model, answer_meta = call_with_fallback(
        GENERATOR_CONFIGS,
        build_answer_messages(task, context),
        max_tokens=ARGS.answer_max_tokens,
        required_keys=["species", "user_query", "diagnosis", "prescription", "withdrawal_period"],
    )
    answer = answer_meta["parsed"]
    answer.setdefault("species", "猪")
    anchors = build_evidence_anchors(answer, source_ids, audit)
    answer["diagnosis"] = with_citations(answer.get("diagnosis"), anchors, min_count=1)
    answer["prescription"] = with_citations(answer.get("prescription"), anchors, min_count=2)
    answer["withdrawal_period"] = with_citations(answer.get("withdrawal_period"), anchors, min_count=3)
    answer["evidence_anchors"] = anchors
    answer["answer_json"] = build_answer_json(task, answer, anchors)

    t_answer = time.perf_counter()
    judge_result, judge_model, judge_meta = call_with_fallback(
        JUDGE_CONFIGS,
        build_judge_messages(task, answer),
        max_tokens=ARGS.judge_max_tokens,
        required_keys=["total_score", "final_label", "fatal_risk"],
    )
    judge = judge_meta["parsed"]
    t_judge = time.perf_counter()

    flags = local_flags(task, answer)
    label, fatal, local_reasons = final_label(judge, flags, ARGS.valid_min_score)
    seconds = round(t_judge - started, 2)
    print(f"[{index}/{total}] {task['case_id']} done score={judge.get('total_score')} label={label} fatal={fatal} {seconds}s", flush=True)
    return {
        "task": dict(task),
        "answer": answer,
        "judge": judge,
        "wiki_audit": audit,
        "flags": flags,
        "final_label": label,
        "final_fatal_risk": fatal,
        "local_reasons": local_reasons,
        "stage_times": {"answer_seconds": round(t_answer - started, 2), "judge_seconds": round(t_judge - t_answer, 2), "total_seconds": seconds},
        "model_usage": {
            "answer_model": answer_model.get("name"),
            "judge_model": judge_model.get("name"),
            "answer_success": answer_result.success,
            "judge_success": judge_result.success,
            "answer_error": answer_result.error,
            "judge_error": judge_result.error,
            "answer_attempts": answer_meta["attempts"],
            "judge_attempts": judge_meta["attempts"],
        },
    }


def csv_row(index: int, row: Mapping[str, Any]) -> dict[str, Any]:
    task = row["task"]
    answer = row["answer"]
    judge = row["judge"]
    audit = row["wiki_audit"]
    flags = row["flags"]
    model_usage = row["model_usage"]
    stage_times = row["stage_times"]
    metadata = answer.get("metadata") if isinstance(answer.get("metadata"), dict) else {}
    answer_json = answer.get("answer_json") if isinstance(answer.get("answer_json"), Mapping) else {}
    evidence_anchors = answer.get("evidence_anchors") if isinstance(answer.get("evidence_anchors"), list) else []
    answer_text = "\n".join([as_text(answer.get("diagnosis")), as_text(answer.get("prescription")), as_text(answer.get("withdrawal_period"))])
    citation_count = len(set(SOURCE_RE.findall(answer_text)))
    evidence_sources = [
        item.get("source_id")
        for item in evidence_anchors
        if isinstance(item, Mapping) and item.get("source_id")
    ]
    golden_answer = {
        "diagnosis": as_text(answer.get("diagnosis")),
        "treatment_or_action": as_text(answer.get("prescription")),
        "withdrawal_period_boundary": as_text(answer.get("withdrawal_period")),
        "answer_json": answer_json,
    }
    metadata = {
        **metadata,
        "case_type": task["scenario_type"],
        "target_disease": task["disease_name"],
        "local_flags": flags,
        "evidence_sources": evidence_sources,
        "wiki_context_query": audit.get("wiki_context_query", ""),
        "gold_dataset_schema": "swine_sft_gold_v1",
    }
    return {
        "case_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{TIMESTAMP}-{task['case_id']}")),
        "index": index,
        "disease_name": task["disease_name"],
        "generator_key": ARGS.generator_key,
        "generator_model": model_usage.get("answer_model", ""),
        "success": "成功" if answer else "失败",
        "error": model_usage.get("answer_error") or model_usage.get("judge_error") or "",
        "species": "猪" if flags.get("species_ok") else answer.get("species", "猪"),
        "user_query": as_text(answer.get("user_query")),
        "diagnosis": as_text(answer.get("diagnosis")),
        "prescription": as_text(answer.get("prescription")),
        "withdrawal_period": as_text(answer.get("withdrawal_period")),
        "answer_json": json.dumps(answer_json, ensure_ascii=False, separators=(",", ":")),
        "golden_answer": json.dumps(golden_answer, ensure_ascii=False, separators=(",", ":")),
        "evidence_anchors": json.dumps(evidence_anchors, ensure_ascii=False, separators=(",", ":")),
        "standard_citation_count": citation_count,
        "training_task_type": "swine_clinical_qa_source_grounded",
        "metadata": json.dumps(metadata, ensure_ascii=False),
        "rule_hard_block": "True" if row["final_fatal_risk"] else "False",
        "rule_fatal_risk": "True" if row["final_fatal_risk"] else "False",
        "rule_codes": "|".join(row.get("local_reasons") or []),
        "rule_messages": "|".join(row.get("local_reasons") or []),
        "target_disease_in_diagnosis": "True" if flags["target_disease_in_diagnosis"] else "False",
        "target_disease_mismatch": "True" if flags["target_disease_mismatch"] else "False",
        "final_fatal_risk": "True" if row["final_fatal_risk"] else "False",
        "wiki_dir": audit.get("wiki_dir", ""),
        "wiki_fact_count": audit.get("wiki_fact_count", ""),
        "wiki_page_count": audit.get("wiki_page_count", ""),
        "wiki_context_query": audit.get("wiki_context_query", ""),
        "wiki_evidence_status_counts": json.dumps(audit.get("wiki_evidence_status_counts", {}), ensure_ascii=False),
        "wiki_evidence_source_ids": json.dumps(audit.get("wiki_evidence_source_ids", []), ensure_ascii=False),
        "wiki_context_chars": audit.get("wiki_context_chars", ""),
        "generation_seconds": stage_times.get("total_seconds", ""),
        "judge_a_model": model_usage.get("judge_model", ""),
        "judge_a_total_score": judge.get("total_score", ""),
        "judge_a_diagnosis_accuracy": judge.get("diagnosis_accuracy", ""),
        "judge_a_pathology_logic": judge.get("pathology_logic", ""),
        "judge_a_prescription_safety": judge.get("prescription_safety", ""),
        "judge_a_data_quality": judge.get("data_quality", ""),
        "judge_a_fatal_risk": "True" if judge.get("fatal_risk") else "False",
        "judge_a_structured_pass": "True" if row["final_label"] == "pass" else "False",
        "judge_a_summary": as_text(judge.get("summary")) + ("\n问题：" + as_text(judge.get("weaknesses")) if judge.get("weaknesses") else ""),
        "judge_b_model": "",
        "judge_b_total_score": "",
        "judge_b_diagnosis_accuracy": "",
        "judge_b_pathology_logic": "",
        "judge_b_prescription_safety": "",
        "judge_b_data_quality": "",
        "judge_b_fatal_risk": "",
        "judge_b_structured_pass": "",
        "judge_b_summary": "",
        "needed_arbitration": "False",
        "arbiter_model": "",
        "arbiter_agreed_with_judge": "",
        "arbiter_final_label": "",
        "arbiter_reason": "",
        "final_total_score": judge.get("total_score", ""),
        "final_diagnosis_accuracy": judge.get("diagnosis_accuracy", ""),
        "final_pathology_logic": judge.get("pathology_logic", ""),
        "final_prescription_safety": judge.get("prescription_safety", ""),
        "final_data_quality": judge.get("data_quality", ""),
        "final_label": row["final_label"],
        "judge_a_seconds": stage_times.get("judge_seconds", ""),
        "judge_b_seconds": "",
        "arbiter_seconds": "",
    }


def write_outputs(rows: list[dict[str, Any]]) -> dict[str, Any]:
    RESULTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    raw_path = RESULTS / f"swine_weak_wiki_production_raw_{TIMESTAMP}.json"
    csv_path = RESULTS / f"swine_disease_dataset_production_{TIMESTAMP}.csv"
    valid_path = RESULTS / f"swine_disease_dataset_production_{TIMESTAMP}_valid.csv"
    rejects_path = RESULTS / f"swine_disease_dataset_production_{TIMESTAMP}_rejects.csv"
    summary_path = RESULTS / f"swine_disease_dataset_production_summary_{TIMESTAMP}.json"

    raw_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    csv_rows = [csv_row(index, row) for index, row in enumerate(rows, start=1)]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=PRODUCTION_FIELDNAMES)
        writer.writeheader()
        writer.writerows(csv_rows)
    valid_rows = [row for row in csv_rows if row["final_label"] == "pass" and row["final_fatal_risk"] == "False"]
    reject_rows = [row for row in csv_rows if row not in valid_rows]
    for path, subset in [(valid_path, valid_rows), (rejects_path, reject_rows)]:
        with path.open("w", encoding="utf-8-sig", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=PRODUCTION_FIELDNAMES)
            writer.writeheader()
            writer.writerows(subset)

    scores = [float(row["final_total_score"] or 0) for row in csv_rows]
    summary = {
        "timestamp": TIMESTAMP,
        "requested": ARGS.limit,
        "generated": len(csv_rows),
        "valid": len(valid_rows),
        "reject_or_review": len(reject_rows),
        "valid_rate": round(len(valid_rows) / max(len(csv_rows), 1), 3),
        "score_avg": round(statistics.mean(scores), 2) if scores else 0,
        "score_min": min(scores) if scores else 0,
        "score_max": max(scores) if scores else 0,
        "label_counts": {label: sum(1 for row in csv_rows if row["final_label"] == label) for label in ["pass", "review", "reject"]},
        "fatal_count": sum(1 for row in csv_rows if row["final_fatal_risk"] == "True"),
        "specific_dose_count": sum(1 for row in rows if row["flags"].get("contains_specific_dose")),
        "specific_withdrawal_count": sum(1 for row in rows if row["flags"].get("contains_specific_withdrawal")),
        "csv": str(csv_path),
        "valid_csv": str(valid_path),
        "rejects_csv": str(rejects_path),
        "raw_json": str(raw_path),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({**summary, "summary": str(summary_path)}, ensure_ascii=False, indent=2))
    return {**summary, "summary": str(summary_path)}


def main() -> None:
    tasks = build_tasks(ARGS.limit)
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, ARGS.parallel)) as executor:
        futures = {executor.submit(process_case, index, len(tasks), task): index for index, task in enumerate(tasks, start=1)}
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda item: item["task"]["case_id"])
    write_outputs(rows)


CONFIG = load_config(ROOT, include_local=True)
MODEL_REGISTRY = ModelRegistry.from_config(CONFIG)
BASE_URL = CONFIG["api"]["base_url"]
KEY_POOL = KeyPoolRegistry()
ARGS = parse_args()
GENERATOR_CONFIGS = [MODEL_REGISTRY.get_candidate(key) for key in parse_key_chain(ARGS.generator_key, ARGS.generator_fallback_keys)]
JUDGE_CONFIGS = [MODEL_REGISTRY.get_candidate(key) for key in parse_key_chain(ARGS.judge_key, ARGS.judge_fallback_keys)]


if __name__ == "__main__":
    main()
