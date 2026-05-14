from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List

try:
    from chicken_data_synthesis.infrastructure.knowledge import build_llm_wiki_context, resolve_llm_wiki_dir
except ImportError:  # pragma: no cover - legacy script compatibility
    build_llm_wiki_context = None
    resolve_llm_wiki_dir = None


@dataclass
class ToolSpec:
    name: str
    description: str
    func: Callable[..., Any]


TOOL_REGISTRY: Dict[str, ToolSpec] = {}


def tool(name: str, description: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        TOOL_REGISTRY[name] = ToolSpec(name=name, description=description, func=func)
        return func

    return decorator


def get_registered_tools() -> List[ToolSpec]:
    return list(TOOL_REGISTRY.values())


def _contains_any(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword and keyword in text for keyword in keywords)


def _has_positive_withdrawal_days(text: str) -> bool:
    """Return true when withdrawal text contains a non-zero day requirement."""

    for match in re.finditer(r"(\d+(?:\.\d+)?)\s*天", str(text or "")):
        try:
            if float(match.group(1)) > 0:
                return True
        except ValueError:
            continue
    return False


def _tokenize_query(query: str) -> List[str]:
    normalized = str(query or "")
    for token in ["，", "。", "、", "：", "；", ",", ".", ":", ";", "\n", "\t"]:
        normalized = normalized.replace(token, " ")
    return [token for token in normalized.split() if token]


def _read_knowledge_blocks(path: Path) -> List[Dict[str, Any]]:
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        return [{"source": str(path), "title": path.name, "text": line.strip()} for line in text.splitlines() if line.strip()]

    blocks: List[Dict[str, Any]] = []
    for file_path in sorted(path.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in {".md", ".txt", ".json"}:
            continue
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if file_path.suffix.lower() == ".json":
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                payload = None
            if isinstance(payload, dict) and isinstance(payload.get("pages"), list):
                for page in payload["pages"]:
                    blocks.append(
                        {
                            "source": str(file_path),
                            "title": str(page.get("title", file_path.stem)),
                            "text": json.dumps(page, ensure_ascii=False),
                        }
                    )
                continue

        sections = [section.strip() for section in text.split("\n## ") if section.strip()]
        if sections:
            for index, section in enumerate(sections, start=1):
                title = section.splitlines()[0].replace("#", "").strip() or f"{file_path.stem}-{index}"
                blocks.append({"source": str(file_path), "title": title, "text": section})
        else:
            blocks.append({"source": str(file_path), "title": file_path.stem, "text": text})
    return blocks


def _search_knowledge_blocks(query: str, text_blocks: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    keywords = _tokenize_query(query)
    matches: List[Dict[str, Any]] = []
    for block in text_blocks:
        text = str(block.get("text", "") or "").strip()
        if not text:
            continue
        score = sum(1 for token in keywords if token in text)
        if score == 0 and str(query or "").strip() and str(query).strip() in text:
            score = 1
        if score > 0:
            match = dict(block)
            match["score"] = score
            matches.append(match)
    matches.sort(key=lambda item: item["score"], reverse=True)
    return matches[:top_k]


def _resolve_config_path(path_value: str) -> Path:
    path = Path(str(path_value or ""))
    if path.is_absolute():
        return path
    return Path.cwd() / path


def _load_llm_wiki_context_for_case(case_data: Dict[str, Any], rule_base_config: Dict[str, Any]) -> str:
    if build_llm_wiki_context is None:
        return ""
    query = "\n".join(
        [
            str(case_data.get("user_query", "") or ""),
            str(case_data.get("diagnosis", "") or ""),
            str(case_data.get("prescription", "") or ""),
            json.dumps(case_data.get("metadata") or {}, ensure_ascii=False),
        ]
    )
    try:
        wiki_dir = (
            resolve_llm_wiki_dir({"rule_base": rule_base_config}, Path.cwd())
            if resolve_llm_wiki_dir is not None
            else _resolve_config_path(str(rule_base_config.get("llm_wiki_dir", "")))
        )
        return build_llm_wiki_context(query, wiki_dir=wiki_dir, top_k_pages=4, top_k_facts=8)
    except Exception:
        return ""


def _collect_banned_hits_from_wiki_context(prescription_text: str, wiki_context: str) -> List[str]:
    if not prescription_text or not wiki_context:
        return []
    hits: List[str] = []
    for line in str(wiki_context).splitlines():
        if not any(marker in line for marker in ["禁用", "不得", "banned", "prohibited", "禁止"]):
            continue
        if any(token and token in prescription_text for token in _tokenize_query(line)):
            hits.append(line.strip()[:160])
    return hits[:5]


@tool("rule_base_check", "检查病例是否命中规则底座的硬约束与风险项。")
def rule_base_check_tool(case_data: Dict[str, Any], rule_base_config: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        "enabled": bool(rule_base_config.get("enabled", False)),
        "hard_block": False,
        "fatal_risk": False,
        "codes": [],
        "messages": [],
    }
    if not result["enabled"]:
        return result

    required_fields = rule_base_config.get("required_case_fields", []) or []
    required_metadata_keys = rule_base_config.get("required_metadata_keys", []) or []
    fatal_block_codes = set(rule_base_config.get("fatal_block_codes", []) or [])
    metadata = case_data.get("metadata") or {}
    if not isinstance(metadata, dict):
        metadata = {}

    for field in required_fields:
        value = str(case_data.get(field, "") or "").strip()
        if not value:
            result["codes"].append("missing_required_field")
            result["messages"].append(f"缺少必填字段:{field}")

    for key in required_metadata_keys:
        value = metadata.get(key)
        if value in (None, "", []):
            result["codes"].append("missing_metadata_key")
            result["messages"].append(f"缺少metadata字段:{key}")

    query_text = str(case_data.get("user_query", "") or "")
    diagnosis_text = str(case_data.get("diagnosis", "") or "")
    prescription_text = str(case_data.get("prescription", "") or "")
    withdrawal_text = str(case_data.get("withdrawal_period", "") or "")
    merged_text = "\n".join([query_text, diagnosis_text, prescription_text, withdrawal_text])
    wiki_context = _load_llm_wiki_context_for_case(case_data, rule_base_config)
    if wiki_context:
        result["llm_wiki_context"] = wiki_context

    banned_keywords = rule_base_config.get("banned_drug_keywords", []) or []
    for keyword in banned_keywords:
        if keyword and keyword in prescription_text:
            result["codes"].append("banned_drug")
            result["messages"].append(f"命中禁用药关键词:{keyword}")
    for wiki_hit in _collect_banned_hits_from_wiki_context(prescription_text, wiki_context):
        result["codes"].append("banned_drug_wiki_evidence")
        result["messages"].append(f"LLM Wiki 禁用/限制证据命中:{wiki_hit}")

    laying_keywords = rule_base_config.get("laying_hen_keywords", []) or []
    egg_keywords = rule_base_config.get("egg_withdrawal_keywords", []) or []
    if _contains_any(merged_text, laying_keywords) and not _contains_any(withdrawal_text, egg_keywords):
        result["codes"].append("egg_withdrawal_missing")
        result["messages"].append("产蛋/蛋鸡场景缺少鸡蛋相关休药或弃蛋说明")

    antibiotic_keywords = rule_base_config.get("antibiotic_keywords", []) or []
    if _contains_any(prescription_text, antibiotic_keywords):
        lowered_withdrawal = withdrawal_text.lower()
        if not withdrawal_text.strip():
            result["codes"].append("withdrawal_missing")
            result["messages"].append("处方含常见抗菌药，但休药期缺失")
        elif (
            any(token in lowered_withdrawal for token in ["0天", "无", "无需", "none"])
            and not _has_positive_withdrawal_days(withdrawal_text)
        ):
            result["codes"].append("withdrawal_conflict")
            result["messages"].append("处方含常见抗菌药，但休药期表述疑似冲突")

    evidence_keywords = [
        "症状",
        "精神",
        "采食",
        "呼吸",
        "腹泻",
        "死亡",
        "剖检",
        "粪便",
        "跛",
        "瘸",
        "关节",
        "站立",
        "站着不稳",
        "肿",
    ]
    if not _contains_any(query_text, evidence_keywords):
        result["codes"].append("weak_evidence")
        result["messages"].append("问诊描述缺少明显症状或证据线索")
    if wiki_context and "NEEDS_REVIEW" in wiki_context:
        result["codes"].append("wiki_needs_review")
        result["messages"].append("LLM Wiki 相关事实包含 NEEDS_REVIEW，建议人工复核后进入黄金集")

    result["codes"] = list(dict.fromkeys(result["codes"]))
    result["messages"] = list(dict.fromkeys(result["messages"]))
    result["hard_block"] = any(code in fatal_block_codes for code in result["codes"])
    result["fatal_risk"] = result["hard_block"] or ("withdrawal_conflict" in result["codes"])
    return result


@tool("banned_drug_lookup", "根据处方文本查询禁用药关键词。")
def banned_drug_lookup_tool(prescription_text: str, rule_base_config: Dict[str, Any]) -> Dict[str, Any]:
    banned_keywords = rule_base_config.get("banned_drug_keywords", []) or []
    hits = [keyword for keyword in banned_keywords if keyword and keyword in str(prescription_text or "")]
    return {"hits": hits, "is_banned": bool(hits)}


@tool("withdrawal_period_check", "检查休药期是否缺失或与常见抗菌药冲突。")
def withdrawal_period_check_tool(case_data: Dict[str, Any], rule_base_config: Dict[str, Any]) -> Dict[str, Any]:
    prescription_text = str(case_data.get("prescription", "") or "")
    withdrawal_text = str(case_data.get("withdrawal_period", "") or "")
    antibiotic_keywords = rule_base_config.get("antibiotic_keywords", []) or []
    has_antibiotic = _contains_any(prescription_text, antibiotic_keywords)
    lowered_withdrawal = withdrawal_text.lower()
    return {
        "has_antibiotic": has_antibiotic,
        "withdrawal_missing": has_antibiotic and not withdrawal_text.strip(),
        "withdrawal_conflict": has_antibiotic and any(token in lowered_withdrawal for token in ["0天", "无", "无需", "none"]),
    }


@tool("case_template_generation", "生成病例模板骨架，供执行模型扩写。")
def case_template_generation_tool(disease_name: str, scenario_hint: str = "") -> Dict[str, Any]:
    return {
        "species": "鸡",
        "user_query": f"请根据{disease_name}和场景提示生成真实养殖户问诊：{scenario_hint}",
        "diagnosis": "请输出主要诊断、鉴别诊断和病理逻辑。",
        "prescription": "请输出药名、剂量、频次、疗程，并避免禁用药。",
        "withdrawal_period": "请明确休药期或弃蛋建议。",
        "metadata": {
            "disease_name": disease_name,
            "severity": "medium",
            "scene_tags": [],
        },
    }


@tool("knowledge_retrieval", "从知识底座参考文件中检索相关法规或规则片段。")
def knowledge_retrieval_tool(query: str, references_file: str, top_k: int = 5) -> Dict[str, Any]:
    path = Path(references_file)
    if not path.exists():
        return {"matches": [], "error": "references_file_not_found"}
    text = path.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    keywords = [token for token in str(query).replace("，", " ").replace("、", " ").split() if token]
    matches = []
    for line in lines:
        score = sum(1 for token in keywords if token in line)
        if score > 0:
            matches.append({"line": line, "score": score})
    matches.sort(key=lambda item: item["score"], reverse=True)
    return {"matches": matches[:top_k]}


@tool("golden_dataset_screening", "按质量阈值筛选黄金数据集候选样本。")
def golden_dataset_screening_tool(rows: List[Dict[str, Any]], min_score: float = 90.0) -> Dict[str, Any]:
    accepted = []
    for row in rows:
        try:
            score = float(row.get("final_total_score", row.get("avg_total_score", 0)) or 0)
        except (TypeError, ValueError):
            score = 0.0
        success = str(row.get("success", row.get("generator_success", ""))).lower() not in {"false", "0", ""}
        fatal_risk = str(row.get("rule_fatal_risk", row.get("fatal_risk", "false"))).lower() in {"true", "1"}
        structured_pass = str(row.get("structured_pass", row.get("judge_a_structured_pass", "true"))).lower() not in {"false", "0"}
        if success and not fatal_risk and structured_pass and score >= min_score:
            accepted.append(row)
    return {"accepted_count": len(accepted), "rows": accepted}


@tool("knowledge_retrieval", "从知识底座参考文件或目录中检索相关法规、规则或 wiki 片段。")
def knowledge_retrieval_tool_v2(query: str, references_file: str, top_k: int = 5) -> Dict[str, Any]:
    path = Path(references_file)
    if not path.exists():
        return {"matches": [], "error": "references_file_not_found"}
    text_blocks = _read_knowledge_blocks(path)
    matches = _search_knowledge_blocks(query, text_blocks, top_k=top_k)
    return {"matches": matches}


@tool("llm_wiki_lookup", "从 LLM Wiki 知识底座目录中检索相关页面和片段。")
def llm_wiki_lookup_tool(query: str, wiki_dir: str, top_k: int = 5) -> Dict[str, Any]:
    path = Path(wiki_dir)
    if not path.exists():
        return {"matches": [], "error": "wiki_dir_not_found"}
    text_blocks = _read_knowledge_blocks(path)
    matches = _search_knowledge_blocks(query, text_blocks, top_k=top_k)
    return {"matches": matches}


knowledge_retrieval_tool = knowledge_retrieval_tool_v2
