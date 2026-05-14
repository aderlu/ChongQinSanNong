from __future__ import annotations

import json
import time
import urllib.error
import urllib.request


BASE_URL = "https://api.nonelinear.com/v1/chat/completions"
MODEL = "deepseek-v3.2"
KEYS = [
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
    "sk-2aee4f263dad2d98046bb67515e900c0",
]


def mask(key: str) -> str:
    return f"{key[:5]}...{key[-6:]}"


def check(key: str, index: int) -> dict[str, object]:
    payload = json.dumps(
        {
            "model": MODEL,
            "messages": [{"role": "user", "content": '只输出 JSON：{"ok":true}'}],
            "temperature": 0,
            "max_tokens": 16,
            "extra_body": {"expected_output": "json", "task_id": f"key-health-{index}"},
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "Codex key health check",
        },
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=18) as resp:
            body = resp.read(500).decode("utf-8", errors="replace")
            return {
                "index": index,
                "key": mask(key),
                "ok": 200 <= resp.status < 300,
                "status": resp.status,
                "elapsed": round(time.perf_counter() - started, 2),
                "error": "",
                "body_preview": body[:120],
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(500).decode("utf-8", errors="replace")
        return {
            "index": index,
            "key": mask(key),
            "ok": False,
            "status": exc.code,
            "elapsed": round(time.perf_counter() - started, 2),
            "error": str(exc),
            "body_preview": body[:160],
        }
    except Exception as exc:
        return {
            "index": index,
            "key": mask(key),
            "ok": False,
            "status": "",
            "elapsed": round(time.perf_counter() - started, 2),
            "error": str(exc),
            "body_preview": "",
        }


def main() -> None:
    rows = [check(key, i) for i, key in enumerate(KEYS, start=1)]
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
