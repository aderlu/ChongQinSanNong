from __future__ import annotations

import sys
import time
from pathlib import Path


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
)


def main() -> None:
    cfg = load_config(ROOT, include_local=True)
    model = ModelRegistry.from_config(cfg).get_candidate("deepseek_v32")
    model["max_tokens"] = 32
    model["timeout"] = 20
    started = time.perf_counter()
    result = call_chat_completion_with_retry(
        model,
        [{"role": "user", "content": '只输出 JSON：{"ok": true}'}],
        expected_output="json",
        retry_policy=build_retry_policy(max_retries=1, request_interval_seconds=0),
        registry=KeyPoolRegistry(),
        client_builder=lambda config, **kwargs: build_openai_client(
            config,
            default_base_url=cfg["api"]["base_url"],
            **kwargs,
        ),
    )
    print(
        {
            "success": result.success,
            "elapsed": round(time.perf_counter() - started, 2),
            "error": result.error,
            "category": result.error_category,
            "content_preview": (result.content or "")[:120],
            "model": model.get("name"),
        }
    )


if __name__ == "__main__":
    main()
