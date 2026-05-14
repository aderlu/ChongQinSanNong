from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "exports"
ISSUES = ROOT / "issues" / "wiki_first_generation_reports"
TZ = timezone(timedelta(hours=8))
DRY_RUN_MODE = "dry-run"
REAL_API_MODE = "real-api"
PROMPT_VERSION = "phase14.two_stage.v3_cn_clinical"
DEFAULT_BASE_URL = "https://api.nonelinear.com/v1"
DEFAULT_MODEL = "hunyuan-turbos-20250926"
LOW_RISK_NO_EXPANSION_TERMS = "unsupported diagnosis, clinical execution, product-use detail, or authority action"
MOJIBAKE_RE = re.compile(r"[\uFFFD]|锛\?|銆\?|鏈|璇ยู|鐚|涓嶅|瑙勮寖")


def today() -> str:
    return datetime.now(TZ).strftime("%Y%m%d")


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            item = json.loads(line.lstrip("\ufeff"))
            if isinstance(item, dict):
                rows.append(item)
    return rows


def ensure_recent_nonempty_jsonl(path: Path, *, max_age_seconds: int = 300) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Required upstream file is missing: {path}")
    rows = read_jsonl(path)
    if not rows:
        raise RuntimeError(f"Required upstream file is empty or unreadable: {path}")
    age_seconds = (datetime.now(TZ) - datetime.fromtimestamp(path.stat().st_mtime, TZ)).total_seconds()
    if age_seconds > max_age_seconds:
        raise RuntimeError(
            f"Upstream file looks stale ({age_seconds:.1f}s old > {max_age_seconds}s): {path}. "
            "Re-run the previous phase before continuing."
        )
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def latest_jsonl(directory: Path, prefix: str) -> Path:
    files = sorted(directory.glob(f"{prefix}_*.jsonl"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No {prefix}_*.jsonl under {directory}")
    return files[0]


def resolve_path(value: str, root: Path, default_dir: Path, prefix: str) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else root / path
    return latest_jsonl(default_dir, prefix)


def split_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value or "").replace(",", ";").split(";") if item.strip()]


def first(values: list[str], default: str = "") -> str:
    return values[0] if values else default


def preferred_rule_card(values: Any) -> str:
    cards = split_list(values)
    for prefix in ("RC-DRUG", "RC-WITHDRAWAL", "RC-DISEASE-REGULATORY"):
        for card in cards:
            if card.startswith(prefix):
                return card
    return first(cards)


def plans_by_id(plans: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(plan.get("plan_id")): plan for plan in plans if plan.get("plan_id")}


def entity_name_for(plan: dict[str, Any], skeleton: dict[str, Any]) -> str:
    for claim in skeleton.get("must_include_claims", []):
        if not isinstance(claim, dict):
            continue
        claim_text = str(claim.get("claim") or "").strip()
        if not claim_text:
            continue
        for sep in ("；", ";"):
            if sep in claim_text:
                head = claim_text.split(sep, 1)[0].strip()
                if head:
                    return head
        if claim_text:
            return claim_text
    return str(plan.get("entity_id") or skeleton.get("entity_id") or "该病")


def question_topic_cn(values: list[str]) -> str:
    mapping = {
        "reporting_boundary": "是否需要上报",
        "movement_boundary": "是否涉及限制调运",
        "disposal_boundary": "是否能直接下处置结论",
        "dose_course_boundary": "能否直接给出剂量和疗程",
        "withdrawal_or_mrl_boundary": "能否直接给出休药期或残留相关结论",
        "label_or_a0_source_check": "是否必须核对标签或 A0 来源",
    }
    items = [mapping.get(str(value), str(value)) for value in values if str(value).strip()]
    return "、".join(items)


def question_for(plan: dict[str, Any], skeleton: dict[str, Any]) -> str:
    entity_name = entity_name_for(plan, skeleton)
    layer = str(plan.get("ability_layer") or skeleton.get("ability_layer") or "")
    expected_output_type = str(plan.get("expected_output_type") or "")
    blueprint = plan.get("question_blueprint") or {}
    must = question_topic_cn(list(blueprint.get("must_ask_about", [])[:3]))
    if layer == "L1_retrieval_grounded" and expected_output_type == "retrieval_gap_or_eval":
        return f"猪场现场咨询：围绕{entity_name}，现有资料目前能确认哪些可靠信息，哪些地方还证据不足，暂时不适合直接下结论？"
    if layer == "L5_drug_boundary_negative":
        return f"猪场在咨询{entity_name}相关处置时，现有资料能不能直接给出具体用药剂量、疗程、给药方式或休药期建议？"
    if layer == "L6_regulatory_guardrail":
        return f"如果猪场怀疑是{entity_name}，现有资料能不能直接给出关于{must or '上报、调运或处置'}的执行性结论？"
    if layer == "L3_differential_support":
        return f"猪场兽医咨询：针对{entity_name}，现有资料能支持做到什么程度的鉴别诊断判断，哪些内容还不能下结论？"
    if layer == "L2_diagnosis_support":
        return f"猪场现场咨询：如果怀疑{entity_name}，现有资料能提供哪些诊断支持信息，哪些内容还不足以直接确诊？"
    if layer == "L4_control_boundary":
        return f"猪场想先了解{entity_name}的防控边界，现有资料能支持哪些原则性判断，哪些措施还不能直接给出？"
    return f"猪场兽医咨询：请基于现有资料，概括{entity_name}目前可以确认的核心信息。"


def anchor_from_claim(claim: dict[str, Any]) -> dict[str, Any]:
    fact_id = first(split_list(claim.get("fact_ids")))
    source_id = first(split_list(claim.get("source_ids")))
    anchor_type = "fact" if fact_id and source_id else "rule_card_boundary"
    rule_card_id = preferred_rule_card(claim.get("rule_card_ids")) if anchor_type == "rule_card_boundary" else first(split_list(claim.get("rule_card_ids")))
    return {
        "anchor_type": anchor_type,
        "claim_id": claim.get("claim_id", ""),
        "fact_id": fact_id,
        "source_id": source_id,
        "rule_card_id": rule_card_id,
        "page_relpath": claim.get("page_relpath", ""),
        "evidence_quote_span": claim.get("evidence_quote_span", ""),
        "claim_supported": bool(
            (anchor_type == "fact" and fact_id and source_id and claim.get("page_relpath"))
            or (anchor_type == "rule_card_boundary" and rule_card_id and claim.get("page_relpath"))
        ),
    }


def citation(anchor: dict[str, Any]) -> str:
    parts: list[str] = []
    if anchor.get("source_id"):
        parts.append(f"source={anchor['source_id']}")
    if anchor.get("rule_card_id"):
        parts.append(f"rule={anchor['rule_card_id']}")
    if anchor.get("fact_id"):
        parts.append(f"fact={anchor['fact_id']}")
    if anchor.get("page_relpath"):
        parts.append(f"page={anchor['page_relpath']}")
    if anchor.get("anchor_type") == "rule_card_boundary":
        parts.append("anchor=rule_card_boundary")
    return " ".join(parts)


def answer_structure_for(plan: dict[str, Any], skeleton: dict[str, Any]) -> dict[str, str]:
    layer = str(plan.get("ability_layer") or skeleton.get("ability_layer") or "")
    if layer == "L2_diagnosis_support":
        return {
            "evidence": "依据当前证据",
            "boundary": "诊断边界",
            "do_not_extend": "不能直接外推",
            "anchors": "引用锚点",
        }
    if layer == "L3_differential_support":
        return {
            "evidence": "依据当前证据",
            "boundary": "鉴别边界",
            "do_not_extend": "不能直接下结论",
            "anchors": "引用锚点",
        }
    if layer == "L4_control_boundary":
        return {
            "evidence": "依据当前证据",
            "boundary": "防控边界",
            "do_not_extend": "不能直接给出",
            "anchors": "引用锚点",
        }
    if layer in {"L5_drug_boundary_negative", "L6_regulatory_guardrail"} or str(plan.get("expected_output_type") or "") == "boundary_or_refusal":
        return {
            "evidence": "依据当前证据",
            "boundary": "必须明确的边界",
            "do_not_extend": "目前不能直接提供",
            "anchors": "引用锚点",
        }
    return {
        "evidence": "依据当前证据",
        "boundary": "回答边界",
        "do_not_extend": "不能直接扩展",
        "anchors": "引用锚点",
    }


def structure_requirements_for(plan: dict[str, Any], skeleton: dict[str, Any]) -> list[str]:
    labels = answer_structure_for(plan, skeleton)
    return [
        f"{labels['evidence']}: 用一到两句自然中文说明当前证据实际支持什么。",
        f"{labels['boundary']}: 明确说明证据边界、目前仍然不能确认什么。",
        f"{labels['do_not_extend']}: 明确避免超出已锚定证据去补充 {LOW_RISK_NO_EXPANSION_TERMS}。",
        f"{labels['anchors']}: 保留方括号引用，使用 source=、rule=、fact= 和 page=。",
    ]


def structured_answer(
    plan: dict[str, Any],
    skeleton: dict[str, Any],
    supported_pairs: list[tuple[dict[str, Any], dict[str, Any]]],
) -> str:
    labels = answer_structure_for(plan, skeleton)
    cited_claims = [f"{claim.get('claim', '')} [{citation(anchor)}]" for claim, anchor in supported_pairs]
    claim_text = " ".join(part for part in cited_claims if part).strip()
    if not claim_text:
        claim_text = "当前保留下来的锚定证据不足以支持正向结论。"

    layer = str(plan.get("ability_layer") or skeleton.get("ability_layer") or "")
    expected_output_type = str(plan.get("expected_output_type") or "")
    boundary_required = expected_output_type == "boundary_or_refusal" or layer in {
        "L5_drug_boundary_negative",
        "L6_regulatory_guardrail",
    }
    if layer == "L2_diagnosis_support":
        boundary = "基于当前证据，这些信息可用于支持诊断讨论，但还不足以单独形成明确确诊结论。"
        do_not = "不得超出已引用事实，擅自推断病因、病原、处置细节、产品使用细节或官方处置要求。"
    elif layer == "L3_differential_support":
        boundary = "当前证据只能帮助划定鉴别诊断边界，可用于比较可能性，但不足以直接指向单一疾病结论。"
        do_not = "不得补充未引用的鉴别特征、处置选择、产品使用细节或官方处置要求。"
    elif layer == "L4_control_boundary":
        boundary = "当前证据仅支持原则性的防控讨论，不足以直接转化为可执行的现场处置指令。"
        do_not = "不得给出无锚定依据的产品使用细节、现场执行动作、猪群处置、隔离分群或调运决策。"
    elif boundary_required:
        boundary = "这是高风险边界场景，回答必须保持审慎，并明确说明需要核对标签、A0 或官方来源。"
        do_not = "在缺少锚定权威依据时，不能直接给出临床执行、用药、剂量、休药期、残留限量或监管执行结论。"
    else:
        boundary = "回答应严格限制在已引用证据范围内，不得做无依据的临床外推。"
        do_not = "不得补充未被证据锚定的诊断、处置、产品使用或监管行动。"

    anchor_text = "; ".join(citation(anchor) for _, anchor in supported_pairs if citation(anchor))
    return (
        f"{labels['evidence']}：{claim_text}\n"
        f"{labels['boundary']}：{boundary}\n"
        f"{labels['do_not_extend']}：{do_not}\n"
        f"{labels['anchors']}：{anchor_text}"
    ).strip()


def build_stage_answers(
    skeleton: dict[str, Any],
    plan: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    claims = [claim for claim in skeleton.get("must_include_claims", []) if isinstance(claim, dict)]
    anchors = [anchor_from_claim(claim) for claim in claims]
    layer = str(plan.get("ability_layer") or skeleton.get("ability_layer") or "")
    expected_output_type = str(plan.get("expected_output_type") or "")
    allow_rule_boundary = layer in {"L5_drug_boundary_negative", "L6_regulatory_guardrail", "L7_judge_calibration"} or (
        expected_output_type == "boundary_or_refusal"
    )
    supported_pairs = [
        (claim, anchor)
        for claim, anchor in zip(claims, anchors)
        if anchor.get("claim_supported") and (anchor.get("anchor_type") != "rule_card_boundary" or allow_rule_boundary)
    ]
    unsupported = [claim.get("claim_id", "") for claim, anchor in zip(claims, anchors) if not anchor.get("claim_supported")]

    draft_sentences = [str(claim.get("claim") or "") for claim in claims if claim.get("claim")]
    if not draft_sentences:
        draft_sentences = [
            "当前 Wiki skeleton 没有足够的锚定证据支持正向结论，应按边界或缺口场景处理。"
        ]

    stage_1 = {
        "answer": "; ".join(draft_sentences),
        "used_claim_ids": [str(claim.get("claim_id")) for claim in claims if claim.get("claim_id")],
        "used_source_ids": list(dict.fromkeys(anchor["source_id"] for anchor in anchors if anchor.get("source_id"))),
        "used_rule_card_ids": list(dict.fromkeys(anchor["rule_card_id"] for anchor in anchors if anchor.get("rule_card_id"))),
    }

    stage_2 = {
        "answer": structured_answer(plan, skeleton, supported_pairs),
        "removed_unsupported_claims": unsupported,
        "boundary_rewrites": ["high_risk_boundary"] if plan.get("expected_output_type") == "boundary_or_refusal" else [],
    }
    return stage_1, stage_2, [anchor for _, anchor in supported_pairs]


def load_llm_client_module():
    path = Path(__file__).with_name("wiki_first_llm_client.py")
    spec = importlib.util.spec_from_file_location("wiki_first_llm_client", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def stage_1_schema() -> dict[str, Any]:
    return {
        "stage_1_answer": "string",
        "used_claim_ids": ["string"],
    }


def stage_2_schema() -> dict[str, Any]:
    return {
        "stage_2_answer": "string",
        "removed_unsupported_claims": ["string"],
        "boundary_rewrites": ["string"],
    }


def format_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def prompt_header(skeleton: dict[str, Any], plan: dict[str, Any], question: str, anchors: list[dict[str, Any]]) -> str:
    payload = {
        "question": question,
        "ability_layer": plan.get("ability_layer") or skeleton.get("ability_layer", ""),
        "entity_id": plan.get("entity_id") or skeleton.get("entity_id", ""),
        "entity_type": plan.get("entity_type") or skeleton.get("entity_type", ""),
        "expected_output_type": plan.get("expected_output_type", ""),
        "must_include_claims": skeleton.get("must_include_claims", []),
        "must_not_include": skeleton.get("must_not_include", []),
        "required_citations": skeleton.get("required_citations", {}),
        "hard_gate_profile": skeleton.get("hard_gate_profile", {}),
        "evidence_anchors": anchors,
        "required_answer_structure": structure_requirements_for(plan, skeleton),
    }
    return format_json(payload)


def stage_1_system_prompt() -> str:
    return (
        "你是 Phase14 第一阶段生成器，负责生成有锚定证据约束的猪病知识问答。"
        "输出必须像中国大陆真实猪场兽医咨询中的专业中文回答，"
        "不能像任务说明、翻译练习、系统摘要、对象字段拼接或伪 JSON 文本。"
        "只能使用提供的 answer skeleton、must_include_claims、must_not_include、required_citations、"
        "hard_gate_profile 和 evidence_anchors，不得杜撰事实。仅返回 JSON。"
    )


def stage_1_user_prompt(skeleton: dict[str, Any], plan: dict[str, Any], question: str, anchors: list[dict[str, Any]]) -> str:
    return (
        "请生成 stage_1 草稿回答，并仅返回 JSON。\n"
        f"Prompt version: {PROMPT_VERSION}\n"
        f"Required JSON schema: {format_json(stage_1_schema())}\n\n"
        "Context:\n"
        f"{prompt_header(skeleton, plan, question, anchors)}\n\n"
        "Requirements:\n"
        "1. stage_1_answer 只能用 must_include_claims 中已有且被支持的内容回答用户问题。\n"
        "2. 必须写成自然、专业、临床交流感明确的中文，像真实猪场咨询，不要像模板说明。\n"
        "3. 除引用字段外不要使用英文标签、英文标题或英文结构化表达。\n"
        f"4. 不得补充 skeleton 未约束的事实，也不得扩展 {LOW_RISK_NO_EXPANSION_TERMS}。\n"
        "5. 避免出现“总结核心知识”“基于注册 Wiki 证据”之类机械措辞，也不要把实体 ID 当主句子来写。\n"
        "6. 不要输出字典样式、键值对拼接、伪 JSON 文本或像对象序列化后的回答。\n"
        "7. used_claim_ids 必须是 must_include_claims.claim_id 的子集。\n"
        "8. 对 boundary_or_refusal 样本，要明确保持边界或拒绝语义。\n"
    )


def stage_2_system_prompt() -> str:
    return (
        "你是 Phase14 第二阶段 grounded answer 生成器。"
        "你必须保留引用约束、显式保留高风险安全边界，并把回答改写成自然、专业、谨慎的中文猪场兽医咨询回复。"
        "回答不能像字段模板、对象字符串或英文标签分节文本。仅返回 JSON。"
    )


def stage_2_user_prompt(
    skeleton: dict[str, Any],
    plan: dict[str, Any],
    question: str,
    anchors: list[dict[str, Any]],
    stage_1_answer: dict[str, Any],
    stage_2_seed: dict[str, Any],
) -> str:
    payload = {
        "question": question,
        "stage_1_answer": stage_1_answer,
        "target_grounding_style": stage_2_seed,
        "must_include_claims": skeleton.get("must_include_claims", []),
        "must_not_include": skeleton.get("must_not_include", []),
        "required_citations": skeleton.get("required_citations", {}),
        "hard_gate_profile": skeleton.get("hard_gate_profile", {}),
        "evidence_anchors": anchors,
        "expected_output_type": plan.get("expected_output_type", ""),
        "required_answer_structure": structure_requirements_for(plan, skeleton),
        "section_labels": answer_structure_for(plan, skeleton),
    }
    return (
        "请生成 stage_2 grounded answer，并仅返回 JSON。\n"
        f"Prompt version: {PROMPT_VERSION}\n"
        f"Required JSON schema: {format_json(stage_2_schema())}\n\n"
        "Context:\n"
        f"{format_json(payload)}\n\n"
        "Requirements:\n"
        "1. stage_2_answer 必须按 required_answer_structure 给出的顺序表达。\n"
        "2. 每一部分都要写成自然、专业的中文临床交流表达，不要出现英文标签、对象键值对、伪 JSON 或结构化对象转字符串痕迹。\n"
        "3. 证据部分必须包含显式锚点引用，并保留现有方括号格式。\n"
        "4. 每一个保留事实都必须能回溯到 evidence_anchors；其余内容要么删除，要么改写为边界表达。\n"
        "5. 边界部分和不能扩展部分必须明确说清楚目前不能据此推断、不能据此执行什么。\n"
        "6. 不要使用系统任务措辞、翻译腔、抽象提示词腔或模板化机械表达。\n"
        "7. 对 L2，不要给出无锚定依据的最终诊断，只说明诊断支持点和限制。\n"
        "8. 对 L3，只讨论鉴别边界，不补充未引用的鉴别特征，不做过度诊断。\n"
        "9. 对 L4，只讨论防控边界，不给出可执行的产品使用细节、猪群处置、物流或官方指令。\n"
        "10. 对 boundary_or_refusal 样本，要保留明确的边界/拒绝表达；但不要整段只剩空泛保守表述。\n"
        "11. 对低风险正样本，优先输出有训练价值的信息密度：说明能支持什么、不能支持什么、为什么不能外推。\n"
        "12. removed_unsupported_claims 和 boundary_rewrites 必须与回答内容一致。\n"
    )


def normalize_claim_ids(value: Any, fallback: list[str]) -> list[str]:
    allowed = set(fallback)
    ids = [str(item).strip() for item in value if str(item).strip()] if isinstance(value, list) else []
    normalized = [item for item in ids if item in allowed]
    return normalized or fallback


def normalize_string_list(value: Any, fallback: list[str]) -> list[str]:
    if not isinstance(value, list):
        return fallback
    items = [str(item).strip() for item in value if str(item).strip()]
    return items if items else fallback


def ensure_boundary_sentence(answer: str) -> str:
    sentence = "Cannot directly provide executable clinical, drug, dose, withdrawal, MRL, or regulatory instructions without anchored authority."
    text = answer.strip()
    if not text:
        return sentence
    if sentence in text:
        return text
    return f"{text}; {sentence}"


def answer_has_required_structure(answer: str, plan: dict[str, Any], skeleton: dict[str, Any]) -> bool:
    labels = answer_structure_for(plan, skeleton)
    return all((f"{label}：" in answer) or (f"{label}:" in answer) for label in labels.values())


def ensure_structured_stage2_answer(
    answer: str,
    plan: dict[str, Any],
    skeleton: dict[str, Any],
    stage_2_seed: dict[str, Any],
) -> tuple[str, list[str]]:
    rewrites: list[str] = []
    text = answer.strip()
    if not text:
        return str(stage_2_seed.get("answer") or ""), ["empty_stage2_rewritten"]
    if answer_has_required_structure(text, plan, skeleton):
        return text, rewrites
    seed_answer = str(stage_2_seed.get("answer") or "").strip()
    if seed_answer and answer_has_required_structure(seed_answer, plan, skeleton):
        rewrites.append("structure_template_rewrite")
        return seed_answer, rewrites
    return text, rewrites


def reconcile_stage_payloads(
    *,
    plan: dict[str, Any],
    stage_1_seed: dict[str, Any],
    stage_2_seed: dict[str, Any],
    stage_1_payload: dict[str, Any],
    stage_2_payload: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    stage_1_answer_text = str(stage_1_payload.get("stage_1_answer") or "").strip() or stage_1_seed["answer"]
    stage_1 = {
        **stage_1_seed,
        "answer": stage_1_answer_text,
        "used_claim_ids": normalize_claim_ids(stage_1_payload.get("used_claim_ids"), stage_1_seed.get("used_claim_ids", [])),
    }
    stage_2_answer_text = str(stage_2_payload.get("stage_2_answer") or "").strip() or stage_2_seed["answer"]
    stage_2_answer_text, structure_rewrites = ensure_structured_stage2_answer(
        stage_2_answer_text,
        plan,
        {"ability_layer": plan.get("ability_layer", "")},
        stage_2_seed,
    )
    if plan.get("expected_output_type") == "boundary_or_refusal":
        stage_2_answer_text = ensure_boundary_sentence(stage_2_answer_text)
        structure_rewrites.append("boundary_sentence_enforced")
    stage_2 = {
        **stage_2_seed,
        "answer": stage_2_answer_text,
        "removed_unsupported_claims": normalize_string_list(
            stage_2_payload.get("removed_unsupported_claims"),
            stage_2_seed.get("removed_unsupported_claims", []),
        ),
        "boundary_rewrites": normalize_string_list(
            stage_2_payload.get("boundary_rewrites"),
            stage_2_seed.get("boundary_rewrites", []),
        ) + [rewrite for rewrite in structure_rewrites if rewrite],
    }
    return stage_1, stage_2


def dry_run_traces(sample_id: str) -> tuple[dict[str, str], dict[str, str]]:
    return (
        {
            "request_ref": f"dryrun-stage1-{sample_id}",
            "response_ref": f"dryrun-stage1-{sample_id}",
        },
        {
            "request_ref": f"dryrun-stage2-{sample_id}",
            "response_ref": f"dryrun-stage2-{sample_id}",
        },
    )


def sample_contains_mojibake(sample: dict[str, Any]) -> bool:
    texts = [
        str(sample.get("question") or ""),
        str((sample.get("stage_1_draft") or {}).get("answer") or ""),
        str((sample.get("stage_2_grounded") or {}).get("answer") or ""),
    ]
    return any(MOJIBAKE_RE.search(text) for text in texts)


def generate_sample(
    *,
    sample_id: str,
    skeleton: dict[str, Any],
    plan: dict[str, Any],
    mode: str,
    llm_client: Any = None,
) -> dict[str, Any] | None:
    stage_1_seed, stage_2_seed, anchors = build_stage_answers(skeleton, plan)
    if not anchors:
        return None

    question = question_for(plan, skeleton)
    stage_1 = dict(stage_1_seed)
    stage_2 = dict(stage_2_seed)
    generation_model = "deterministic-mock"
    generation_error = ""
    stage_1_trace, stage_2_trace = dry_run_traces(sample_id)

    if mode == REAL_API_MODE:
        if llm_client is None:
            raise RuntimeError("LLM client is required for real-api mode")
        try:
            stage_1_result = llm_client.generate_json(
                stage="stage1",
                system_prompt=stage_1_system_prompt(),
                user_prompt=stage_1_user_prompt(skeleton, plan, question, anchors),
            )
            stage_2_result = llm_client.generate_json(
                stage="stage2",
                system_prompt=stage_2_system_prompt(),
                user_prompt=stage_2_user_prompt(
                    skeleton,
                    plan,
                    question,
                    anchors,
                    stage_1_result.payload,
                    stage_2_seed,
                ),
            )
            stage_1, stage_2 = reconcile_stage_payloads(
                plan=plan,
                stage_1_seed=stage_1_seed,
                stage_2_seed=stage_2_seed,
                stage_1_payload=stage_1_result.payload,
                stage_2_payload=stage_2_result.payload,
            )
            generation_model = stage_2_result.model or stage_1_result.model or llm_client.model
            stage_1_trace = {
                "request_ref": stage_1_result.request_ref,
                "response_ref": stage_1_result.response_ref,
            }
            stage_2_trace = {
                "request_ref": stage_2_result.request_ref,
                "response_ref": stage_2_result.response_ref,
            }
        except Exception as exc:
            generation_error = f"{type(exc).__name__}: {str(exc)}"
            generation_model = getattr(llm_client, "model", "") or generation_model
            stage_1_trace = {
                "request_ref": f"realapi-stage1-fallback-{sample_id}",
                "response_ref": "",
            }
            stage_2_trace = {
                "request_ref": f"realapi-stage2-fallback-{sample_id}",
                "response_ref": "",
            }

    sample = {
        "sample_id": sample_id,
        "plan_id": skeleton.get("plan_id", ""),
        "skeleton_id": skeleton.get("skeleton_id", ""),
        "ability_layer": plan.get("ability_layer") or skeleton.get("ability_layer", ""),
        "entity_id": plan.get("entity_id") or skeleton.get("entity_id", ""),
        "entity_type": plan.get("entity_type") or skeleton.get("entity_type", ""),
        "question": question,
        "stage_1_draft": stage_1,
        "stage_2_grounded": stage_2,
        "evidence_anchors": anchors,
        "source_trust": plan.get("source_trust", ""),
        "evidence_coverage": plan.get("evidence_coverage", ""),
        "usage_scope": split_list(plan.get("usage_scope")),
        "risk_class": plan.get("risk_class", ""),
        "authority_level": plan.get("authority_level", ""),
        "expected_output_type": plan.get("expected_output_type", ""),
        "generation_mode": mode,
        "generation_model": generation_model,
        "prompt_version": PROMPT_VERSION,
        "request_ref": {
            "stage_1": stage_1_trace["request_ref"],
            "stage_2": stage_2_trace["request_ref"],
        },
        "response_ref": {
            "stage_1": stage_1_trace["response_ref"],
            "stage_2": stage_2_trace["response_ref"],
        },
    }
    if generation_error:
        sample["generation_error"] = generation_error
        sample["generation_fallback"] = "deterministic_seed_preserved"
    return sample


def generate_samples(
    skeletons: list[dict[str, Any]],
    plans: list[dict[str, Any]],
    *,
    mode: str,
    limit: int | None = None,
    llm_client: Any = None,
) -> list[dict[str, Any]]:
    plan_map = plans_by_id(plans)
    samples: list[dict[str, Any]] = []
    for index, skeleton in enumerate(skeletons, start=1):
        plan = plan_map.get(str(skeleton.get("plan_id"))) or {}
        sample = generate_sample(
            sample_id=f"GEN-{index:06d}",
            skeleton=skeleton,
            plan=plan,
            mode=mode,
            llm_client=llm_client,
        )
        if sample is None:
            continue
        if sample_contains_mojibake(sample):
            raise RuntimeError(
                f"Generated sample contains mojibake-like text: {sample.get('sample_id')}. "
                "Stop export and clean the source template or upstream facts first."
            )
        samples.append(sample)
        if limit and len(samples) >= limit:
            break
    return samples


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def summarize(
    samples: list[dict[str, Any]],
    skeleton_path: Path,
    plan_path: Path,
    output: Path,
    root: Path,
    *,
    mode: str,
    generation_model: str,
) -> dict[str, Any]:
    layer_counts: dict[str, int] = {}
    missing_anchors = []
    missing_grounded_citations = []
    fallback_samples = []
    for sample in samples:
        layer = str(sample.get("ability_layer") or "")
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
        if not sample.get("evidence_anchors"):
            missing_anchors.append(sample.get("sample_id"))
        answer = str((sample.get("stage_2_grounded") or {}).get("answer") or "")
        has_rule_boundary_anchor = any(
            isinstance(anchor, dict) and anchor.get("anchor_type") == "rule_card_boundary"
            for anchor in sample.get("evidence_anchors", [])
        )
        required_markers = ("rule=", "page=") if has_rule_boundary_anchor else ("source=", "rule=", "fact=")
        if not all(marker in answer for marker in required_markers):
            missing_grounded_citations.append(sample.get("sample_id"))
        if sample.get("generation_fallback"):
            fallback_samples.append(sample.get("sample_id"))
    return {
        "generated_at": now(),
        "phase": "phase14_generate_two_stage_samples",
        "mode": mode,
        "generation_model": generation_model,
        "prompt_version": PROMPT_VERSION,
        "input_skeletons": relative(skeleton_path, root),
        "input_plan": relative(plan_path, root),
        "output": relative(output, root),
        "samples": len(samples),
        "samples_generated": len(samples),
        "ability_layer_counts": layer_counts,
        "missing_anchors": missing_anchors,
        "missing_grounded_citations": missing_grounded_citations,
        "fallback_samples": fallback_samples,
        "passed": bool(samples) and not missing_anchors and not missing_grounded_citations,
    }


def write_report(summary: dict[str, Any], report_json: Path, report_md: Path) -> None:
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Phase 14 Two Stage Generation",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Mode: {summary['mode']}",
        f"- Generation model: {summary['generation_model']}",
        f"- Prompt version: {summary['prompt_version']}",
        f"- Samples: {summary['samples']}",
        f"- Passed: {summary['passed']}",
        "",
        "## Ability Layers",
        "",
    ]
    for key, value in sorted(summary["ability_layer_counts"].items()):
        lines.append(f"- {key}: {value}")
    if summary["fallback_samples"]:
        lines.extend(["", "## Fallback Samples", ""])
        lines.extend(f"- {item}" for item in summary["fallback_samples"])
    if summary["missing_anchors"]:
        lines.extend(["", "## Missing Anchors", ""])
        lines.extend(f"- {item}" for item in summary["missing_anchors"])
    if summary["missing_grounded_citations"]:
        lines.extend(["", "## Missing Grounded Citations", ""])
        lines.extend(f"- {item}" for item in summary["missing_grounded_citations"])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_llm_client(args: argparse.Namespace):
    if args.mode != REAL_API_MODE:
        return None
    module = load_llm_client_module()
    return module.WikiFirstLLMClient(
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        timeout=args.timeout,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-root", type=Path, default=ROOT)
    parser.add_argument("--date", default=today())
    parser.add_argument("--skeletons", default="")
    parser.add_argument("--plan", default="")
    parser.add_argument("--plans", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--mode", choices=[DRY_RUN_MODE, REAL_API_MODE], default=DRY_RUN_MODE)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--api-key", default="")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--max-upstream-age-seconds", type=int, default=300)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    wiki_root = args.wiki_root.resolve()
    exports = wiki_root / "exports"
    issues = wiki_root / "issues" / "wiki_first_generation_reports"
    skeleton_path = resolve_path(args.skeletons, wiki_root, exports / "answer_skeletons", "wiki_answer_skeletons")
    plan_path = resolve_path(args.plan or args.plans, wiki_root, exports / "planned_samples", "wiki_sample_plan")
    llm_client = build_llm_client(args)

    skeleton_rows = ensure_recent_nonempty_jsonl(skeleton_path, max_age_seconds=args.max_upstream_age_seconds)
    plan_rows = ensure_recent_nonempty_jsonl(plan_path, max_age_seconds=args.max_upstream_age_seconds)
    samples = generate_samples(
        skeleton_rows,
        plan_rows,
        mode=args.mode,
        limit=args.limit or None,
        llm_client=llm_client,
    )
    if not samples:
        raise RuntimeError(
            f"Phase14 generated zero samples from skeletons {skeleton_path}. "
            "This usually indicates stale input, an upstream race, or all anchors being filtered out."
        )

    output = exports / "generated_samples" / f"two_stage_samples_{args.date}.jsonl"
    write_jsonl(output, samples)
    summary = summarize(
        samples,
        skeleton_path,
        plan_path,
        output,
        wiki_root,
        mode=args.mode,
        generation_model=(getattr(llm_client, "model", "") if llm_client else "deterministic-mock"),
    )
    write_report(
        summary,
        issues / f"phase14_generation_{args.date}.json",
        issues / f"phase14_generation_{args.date}.md",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
