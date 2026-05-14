from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from openai import OpenAI


ROOT = Path(__file__).resolve().parents[2]
TZ = timezone(timedelta(hours=8))
DEFAULT_BASE_URL = "https://api.nonelinear.com/v1"
DEFAULT_MODEL = "hunyuan-turbos-20250926"


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            if isinstance(item, dict):
                rows.append(item)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def latest_jsonl(directory: Path, prefix: str) -> Path:
    files = sorted(directory.glob(f"{prefix}_*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No {prefix}_*.jsonl under {directory}")
    return files[0]


def resolve_path(value: str, root: Path, default_dir: Path, prefix: str) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else root / path
    return latest_jsonl(default_dir, prefix)


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def load_phase14_module() -> Any:
    path = Path(__file__).with_name("phase14_generate_two_stage_samples.py")
    spec = importlib.util.spec_from_file_location("phase14_generate_two_stage_samples", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def balanced_skeletons(skeletons: list[dict[str, Any]], plans: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    plan_map = {str(plan.get("plan_id")): plan for plan in plans if plan.get("plan_id")}
    buckets: dict[str, list[dict[str, Any]]] = {}
    for skeleton in skeletons:
        plan = plan_map.get(str(skeleton.get("plan_id"))) or {}
        layer = str(plan.get("ability_layer") or skeleton.get("ability_layer") or "")
        buckets.setdefault(layer, []).append(skeleton)
    order = [
        "L1_retrieval_grounded",
        "L2_diagnosis_support",
        "L3_differential_support",
        "L4_control_boundary",
        "L5_drug_boundary_negative",
        "L6_regulatory_guardrail",
        "L7_judge_calibration",
    ]
    selected: list[dict[str, Any]] = []
    cursor = 0
    while len(selected) < limit:
        progressed = False
        for layer in order:
            bucket = buckets.get(layer, [])
            if cursor < len(bucket):
                selected.append(bucket[cursor])
                progressed = True
                if len(selected) >= limit:
                    break
        if not progressed:
            break
        cursor += 1
    return selected


def extract_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if not match:
            raise ValueError("model output did not contain JSON")
        payload = json.loads(match.group(0))
    if not isinstance(payload, dict):
        raise ValueError("model JSON output is not an object")
    return payload


def prompt_for(sample: dict[str, Any]) -> str:
    anchors = sample.get("evidence_anchors", [])
    anchor_lines = []
    for index, anchor in enumerate(anchors, start=1):
        citation = []
        if anchor.get("source_id"):
            citation.append(f"source={anchor['source_id']}")
        if anchor.get("rule_card_id"):
            citation.append(f"rule={anchor['rule_card_id']}")
        if anchor.get("fact_id"):
            citation.append(f"fact={anchor['fact_id']}")
        if anchor.get("page_relpath"):
            citation.append(f"page={anchor['page_relpath']}")
        if anchor.get("anchor_type") == "rule_card_boundary":
            citation.append("anchor=rule_card_boundary")
        anchor_lines.append(f"{index}. [{ ' '.join(citation) }]")
    deterministic_answer = str((sample.get("stage_2_grounded") or {}).get("answer") or "")
    return (
        "你是猪病知识库数据生成助手。只能基于给定 Wiki 骨架和证据锚点改写，不得引入新事实、药物剂量、疗程、休药期或监管执行结论。\n"
        "输出必须是 JSON 对象，字段为 stage_1_answer 和 stage_2_answer。\n"
        "stage_1_answer: 用自然中文草拟回答，可概括但不得增加事实，要像真实猪场兽医问诊交流，不要像任务说明。\n"
        "stage_2_answer: 必须保留下列每一个引用锚点原文，引用格式不得改写；高风险/药物边界问题必须明确拒绝执行性建议。\n"
        "stage_2_answer 必须写成自然、连贯、专业的中文回答，不要写成字典、键值对、伪 JSON、英文标签分节或结构化对象转字符串的样子。\n"
        "对于低风险正样本，优先给出有训练价值的诊断支持、鉴别边界、防控边界或证据缺口说明，不要整段只有保守拒答。\n"
        "除引用锚点中的 source=/rule=/fact=/page= 外，不要使用英文标题、英文字段名或英文标签开头。\n"
        "不要输出 JSON 以外的文字。\n\n"
        f"能力层: {sample.get('ability_layer')}\n"
        f"实体: {sample.get('entity_id')} ({sample.get('entity_type')})\n"
        f"风险类别: {sample.get('risk_class')}\n"
        f"用户问题: {sample.get('question')}\n\n"
        "必须使用的引用锚点:\n"
        + "\n".join(anchor_lines)
        + "\n\n"
        "标准答案骨架:\n"
        + deterministic_answer
    )


def call_model(client: OpenAI, model: str, prompt: str, temperature: float, max_tokens: int, timeout: int) -> dict[str, Any]:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        extra_body={"task_id": str(uuid.uuid4())},
    )
    text = response.choices[0].message.content or ""
    return extract_json(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a 30-sample real API smoke generation from Phase 13 skeletons.")
    parser.add_argument("--wiki-root", type=Path, default=ROOT)
    parser.add_argument("--date", default=datetime.now(TZ).strftime("%Y%m%d"))
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--skeletons", default="")
    parser.add_argument("--plan", default="")
    parser.add_argument("--base-url", default=os.environ.get("NONELINEAR_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model", default=os.environ.get("NONELINEAR_MODEL", DEFAULT_MODEL))
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--sleep", type=float, default=0.2)
    args = parser.parse_args()

    api_key = os.environ.get("NONELINEAR_API_KEY")
    if not api_key:
        raise RuntimeError("NONELINEAR_API_KEY is not configured")

    root = args.wiki_root.resolve()
    exports = root / "exports"
    issues = root / "issues" / "wiki_first_generation_reports"
    skeleton_path = resolve_path(args.skeletons, root, exports / "answer_skeletons", "wiki_answer_skeletons")
    plan_path = resolve_path(args.plan, root, exports / "planned_samples", "wiki_sample_plan")
    phase14 = load_phase14_module()
    skeletons = read_jsonl(skeleton_path)
    plans = read_jsonl(plan_path)
    plan_map = {str(plan.get("plan_id")): plan for plan in plans if plan.get("plan_id")}
    selected = balanced_skeletons(skeletons, plans, max(args.limit * 3, args.limit))
    client = OpenAI(api_key=api_key, base_url=args.base_url)

    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for index, skeleton in enumerate(selected, start=1):
        if len(rows) >= args.limit:
            break
        plan = plan_map.get(str(skeleton.get("plan_id"))) or {}
        stage_1_seed, stage_2_seed, anchors = phase14.build_stage_answers(skeleton, plan)
        if not anchors:
            failures.append({"plan_id": skeleton.get("plan_id"), "reason": "no_phase14_anchors"})
            continue
        sample = {
            "sample_id": f"REALAPI30-{index:03d}",
            "plan_id": skeleton.get("plan_id", ""),
            "skeleton_id": skeleton.get("skeleton_id", ""),
            "ability_layer": plan.get("ability_layer") or skeleton.get("ability_layer", ""),
            "entity_id": plan.get("entity_id") or skeleton.get("entity_id", ""),
            "entity_type": plan.get("entity_type") or skeleton.get("entity_type", ""),
            "question": phase14.question_for(plan, skeleton),
            "stage_1_draft": stage_1_seed,
            "stage_2_grounded": stage_2_seed,
            "evidence_anchors": anchors,
            "source_trust": plan.get("source_trust", ""),
            "evidence_coverage": plan.get("evidence_coverage", ""),
            "usage_scope": phase14.split_list(plan.get("usage_scope")),
            "risk_class": plan.get("risk_class", ""),
            "authority_level": plan.get("authority_level", ""),
            "expected_output_type": plan.get("expected_output_type", ""),
            "generation_mode": "real_api",
            "model": args.model,
        }
        try:
            payload = call_model(client, args.model, prompt_for(sample), args.temperature, args.max_tokens, args.timeout)
            sample["stage_1_draft"] = {
                **stage_1_seed,
                "answer": str(payload.get("stage_1_answer") or "").strip(),
                "generator": args.model,
            }
            sample["stage_2_grounded"] = {
                **stage_2_seed,
                "answer": str(payload.get("stage_2_answer") or "").strip(),
                "generator": args.model,
            }
            rows.append(sample)
        except Exception as exc:
            failures.append({"sample_id": sample["sample_id"], "plan_id": sample["plan_id"], "reason": type(exc).__name__, "message": str(exc)[:300]})
        time.sleep(args.sleep)

    out = exports / "generated_samples" / f"real_api_samples_{args.date}_30.jsonl"
    report_path = issues / f"phase14_real_api_generation_{args.date}_30.json"
    write_jsonl(out, rows)
    layer_counts: dict[str, int] = {}
    for row in rows:
        layer = str(row.get("ability_layer") or "")
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
    summary = {
        "generated_at": now(),
        "phase": "phase14_real_api_generate_30",
        "model": args.model,
        "input_skeletons": rel(skeleton_path, root),
        "input_plan": rel(plan_path, root),
        "output": rel(out, root),
        "requested": args.limit,
        "generated": len(rows),
        "failed": len(failures),
        "ability_layer_counts": layer_counts,
        "failures": failures,
        "passed": len(rows) == args.limit,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
