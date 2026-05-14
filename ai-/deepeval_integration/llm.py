from __future__ import annotations

import json
import random
import re
import time
import uuid
from typing import Any, Dict, Optional, Type

from openai import OpenAI

try:
    from deepeval.models.base_model import DeepEvalBaseLLM
except ImportError as exc:  # pragma: no cover - runtime dependency guard
    raise ImportError(
        "deepeval 未安装。请先执行 `pip install -r requirements.txt`。"
    ) from exc


def extract_json_payload(text: str) -> Dict[str, Any]:
    cleaned = (text or "").strip()
    if not cleaned:
        raise ValueError("模型返回为空，无法解析 JSON。")

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if not match:
            raise ValueError("模型输出中未找到有效 JSON。")
        return json.loads(match.group(0))


class NonlinearOpenAIDeepEvalLLM(DeepEvalBaseLLM):
    """Adapter for routing DeepEval judge prompts through the project's OpenAI-compatible API."""

    _KEY_POOL_STATE: Dict[str, Dict[str, Any]] = {}

    def __init__(self, base_url: str, model_config: Dict[str, Any]) -> None:
        self._base_url = model_config.get("base_url") or base_url
        self._model_config = dict(model_config)
        self._client: Optional[OpenAI] = None

    def _pool_id(self) -> str:
        return str(self._model_config.get("key_pool_name") or self._model_config.get("name") or uuid.uuid4())

    def _pool_keys(self) -> list[str]:
        keys = self._model_config.get("api_keys")
        if isinstance(keys, list) and keys:
            return [str(key).strip() for key in keys if str(key).strip()]
        api_key = str(self._model_config.get("api_key", "")).strip()
        return [api_key] if api_key else []

    def _pool_settings(self) -> Dict[str, Any]:
        return {
            "rotation_strategy": self._model_config.get("rotation_strategy", "round_robin"),
            "cooldown_seconds": int(self._model_config.get("cooldown_seconds", 90)),
            "max_consecutive_failures": int(self._model_config.get("max_consecutive_failures", 2)),
        }

    def _pool_state(self) -> Dict[str, Any]:
        pool_id = self._pool_id()
        keys = self._pool_keys()
        if pool_id not in self._KEY_POOL_STATE:
            self._KEY_POOL_STATE[pool_id] = {
                "index": 0,
                "cooldowns": {},
                "fail_counts": {key: 0 for key in keys},
            }
        else:
            state = self._KEY_POOL_STATE[pool_id]
            for key in keys:
                state["fail_counts"].setdefault(key, 0)
        return self._KEY_POOL_STATE[pool_id]

    def _choose_api_key(self) -> str:
        keys = self._pool_keys()
        if not keys:
            raise ValueError(f"模型 {self._model_config.get('name', '')} 未配置 api_key 或 api_keys")
        state = self._pool_state()
        now = time.time()
        available_keys = [key for key in keys if state["cooldowns"].get(key, 0) <= now]
        if not available_keys:
            available_keys = keys
        if self._pool_settings()["rotation_strategy"] == "random":
            return random.choice(available_keys)
        start = state["index"] % len(available_keys)
        chosen = available_keys[start]
        state["index"] = (start + 1) % len(available_keys)
        return chosen

    def _mark_key_result(self, api_key: str, success: bool, reason: str = "") -> None:
        keys = self._pool_keys()
        if len(keys) <= 1 or not api_key:
            return
        state = self._pool_state()
        settings = self._pool_settings()
        if success:
            state["fail_counts"][api_key] = 0
            state["cooldowns"][api_key] = 0
            return
        state["fail_counts"][api_key] = state["fail_counts"].get(api_key, 0) + 1
        if reason in {"rate_limit", "timeout"} or state["fail_counts"][api_key] >= settings["max_consecutive_failures"]:
            state["cooldowns"][api_key] = time.time() + settings["cooldown_seconds"]

    @staticmethod
    def _classify_error(exc: Exception) -> str:
        message = str(exc).lower()
        if any(token in message for token in ["rate limit", "429", "too many requests", "quota", "exceeded"]):
            return "rate_limit"
        if any(token in message for token in ["timeout", "timed out", "read timeout", "connect timeout"]):
            return "timeout"
        if any(token in message for token in ["unauthorized", "invalid api key", "401", "permission"]):
            return "auth"
        return "other"

    def _build_client(self, api_key: str) -> OpenAI:
        return OpenAI(api_key=api_key, base_url=self._base_url)

    def load_model(self) -> OpenAI:
        if self._client is None:
            self._client = self._build_client(self._choose_api_key())
        return self._client

    def get_model_name(self) -> str:
        return str(self._model_config["name"])

    def _complete(self, prompt: str) -> str:
        last_exc: Optional[Exception] = None
        for _ in range(3):
            selected_api_key = self._choose_api_key()
            client = self._build_client(selected_api_key)
            try:
                response = client.chat.completions.create(
                    model=self._model_config["name"],
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self._model_config.get("temperature", 0.2),
                    max_tokens=self._model_config.get("max_tokens", 1600),
                    timeout=self._model_config.get("timeout", 60),
                    extra_body={"task_id": str(uuid.uuid4())},
                )
                self._client = client
                self._mark_key_result(selected_api_key, success=True)
                return response.choices[0].message.content or ""
            except Exception as exc:
                last_exc = exc
                self._mark_key_result(selected_api_key, success=False, reason=self._classify_error(exc))
        if last_exc:
            raise last_exc
        return ""

    def generate(self, prompt: str, schema: Optional[Type[Any]] = None) -> Any:
        text = self._complete(prompt)
        if schema is None:
            return text

        payload = extract_json_payload(text)
        if isinstance(schema, type):
            return schema(**payload)
        return payload

    async def a_generate(self, prompt: str, schema: Optional[Type[Any]] = None) -> Any:
        return self.generate(prompt, schema=schema)
