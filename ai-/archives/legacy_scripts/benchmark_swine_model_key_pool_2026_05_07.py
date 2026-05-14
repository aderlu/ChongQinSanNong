from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
for item in (str(ROOT), str(SRC_DIR)):
    if item not in sys.path:
        sys.path.insert(0, item)

from chicken_data_synthesis.infrastructure.config import ModelRegistry, load_config
from chicken_data_synthesis.infrastructure.llm import build_openai_client, extract_json_from_response


DEFAULT_MODELS = (
    "swine_ernie45_turbo32k",
    "swine_hunyuan20_instruct",
    "swine_hunyuan_turbos",
    "swine_deepseek_v4_flash",
    "swine_deepseek_v32",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark swine model candidates and the configured key pool.")
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS), help="Comma-separated candidate model keys.")
    parser.add_argument("--max-keys", type=int, default=0, help="Limit tested keys; 0 means all keys.")
    parser.add_argument("--timeout", type=int, default=35)
    parser.add_argument("--max-tokens", type=int, default=96)
    parser.add_argument("--repeats", type=int, default=1)
    return parser.parse_args()


def fingerprint(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def parse_model_keys(raw: str) -> list[str]:
    return [item.strip() for item in str(raw or "").split(",") if item.strip()]


def summarize(items: list[dict[str, Any]], group_key: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        grouped.setdefault(str(item[group_key]), []).append(item)
    rows = []
    for key, group in grouped.items():
        successes = [item for item in group if item["success"] and item["parsed_json"]]
        elapsed = [float(item["elapsed_seconds"]) for item in successes]
        rows.append(
            {
                group_key: key,
                "calls": len(group),
                "successes": len(successes),
                "success_rate": round(len(successes) / len(group), 4) if group else 0,
                "avg_elapsed_seconds": round(statistics.mean(elapsed), 3) if elapsed else None,
                "min_elapsed_seconds": round(min(elapsed), 3) if elapsed else None,
                "errors": sorted({item["error_category"] or item["error"][:80] for item in group if not item["success"]}),
            }
        )
    rows.sort(key=lambda row: (-(row["success_rate"] or 0), row["avg_elapsed_seconds"] if row["avg_elapsed_seconds"] is not None else 9999))
    return rows


def main() -> None:
    args = parse_args()
    cfg = load_config(ROOT, include_local=True)
    registry = ModelRegistry.from_config(cfg)
    model_keys = parse_model_keys(args.models)
    model_configs = [(key, registry.get_candidate(key)) for key in model_keys]

    key_pool = []
    for _key, model in model_configs:
        if isinstance(model.get("api_keys"), list) and model["api_keys"]:
            key_pool = [str(key).strip() for key in model["api_keys"] if str(key).strip()]
            break
    if args.max_keys and args.max_keys > 0:
        key_pool = key_pool[: args.max_keys]
    if not key_pool:
        raise RuntimeError("No api_keys configured for benchmark.")

    prompt = (
        "只输出 JSON："
        "{\"ok\": true, \"task\": \"swine_model_key_benchmark\", "
        "\"note\": \"猪病黄金数据集生成评估连通性测试\"}"
    )
    records: list[dict[str, Any]] = []
    for model_key, model_config in model_configs:
        for index, api_key in enumerate(key_pool, start=1):
            for repeat in range(1, max(args.repeats, 1) + 1):
                tuned = dict(model_config)
                tuned["api_key"] = api_key
                tuned["api_keys"] = [api_key]
                tuned["max_tokens"] = args.max_tokens
                tuned["timeout"] = args.timeout
                started = time.perf_counter()
                record = {
                    "model_key": model_key,
                    "model": tuned.get("name"),
                    "key_index": index,
                    "key_fingerprint": fingerprint(api_key),
                    "repeat": repeat,
                    "success": False,
                    "parsed_json": False,
                    "elapsed_seconds": None,
                    "error": "",
                    "error_category": "",
                    "usage": {},
                }
                try:
                    client = build_openai_client(tuned, default_base_url=cfg["api"]["base_url"], api_key=api_key)
                    response = client.chat.completions.create(
                        model=tuned["name"],
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0,
                        max_tokens=tuned["max_tokens"],
                        timeout=tuned["timeout"],
                        extra_body={"task_id": f"swine-benchmark-{model_key}-{index}-{repeat}"},
                    )
                    content = response.choices[0].message.content or ""
                    record["success"] = True
                    record["parsed_json"] = isinstance(extract_json_from_response(content), dict)
                    usage = getattr(response, "usage", None)
                    record["usage"] = usage.model_dump() if hasattr(usage, "model_dump") else {}
                except Exception as exc:
                    record["error"] = str(exc)[:300]
                    lowered = str(exc).lower()
                    if any(token in lowered for token in ("429", "rate limit", "quota")):
                        record["error_category"] = "rate_limit"
                    elif any(token in lowered for token in ("timeout", "timed out")):
                        record["error_category"] = "timeout"
                    elif any(token in lowered for token in ("401", "unauthorized", "invalid api key")):
                        record["error_category"] = "auth"
                    else:
                        record["error_category"] = "other"
                finally:
                    record["elapsed_seconds"] = round(time.perf_counter() - started, 3)
                    records.append(record)
                    status = "ok" if record["success"] and record["parsed_json"] else "fail"
                    print(
                        f"{status} model={record['model']} key_index={index} "
                        f"elapsed={record['elapsed_seconds']} category={record['error_category']}",
                        flush=True,
                    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = ROOT / "results" / "swine_model_key_benchmark"
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": timestamp,
        "models": model_keys,
        "key_count": len(key_pool),
        "records": records,
        "model_summary": summarize(records, "model_key"),
        "key_summary": summarize(records, "key_fingerprint"),
    }
    out_path = out_dir / f"swine_model_key_benchmark_{timestamp}.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out_path), "model_summary": payload["model_summary"][:5], "key_summary": payload["key_summary"][:5]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
