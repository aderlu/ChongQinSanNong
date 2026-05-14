from __future__ import annotations

import json
import os
import random
import threading
from dataclasses import dataclass, field
from json import JSONDecodeError, JSONDecoder
from typing import Any, Callable, Dict, Literal, Optional, Sequence

from openai import OpenAI


ErrorCategory = Literal["rate_limit", "timeout", "auth", "other"]


@dataclass(slots=True)
class KeyPoolSettings:
    rotation_strategy: str = "round_robin"
    cooldown_seconds: int = 90
    max_consecutive_failures: int = 2

    @classmethod
    def from_model_config(cls, model_config: Dict[str, Any]) -> "KeyPoolSettings":
        return cls(
            rotation_strategy=str(model_config.get("rotation_strategy", "round_robin")),
            cooldown_seconds=int(model_config.get("cooldown_seconds", 90)),
            max_consecutive_failures=int(model_config.get("max_consecutive_failures", 2)),
        )


@dataclass(slots=True)
class KeyPoolState:
    index: int = 0
    fail_counts: Dict[str, int] = field(default_factory=dict)
    cooldowns: Dict[str, float] = field(default_factory=dict)

    def ensure_keys(self, keys: Sequence[str]) -> None:
        for key in keys:
            self.fail_counts.setdefault(key, 0)
            self.cooldowns.setdefault(key, 0.0)


class ApiKeyPool:
    def __init__(
        self,
        keys: Sequence[str],
        settings: Optional[KeyPoolSettings] = None,
        *,
        state: Optional[KeyPoolState] = None,
        rng: Optional[random.Random] = None,
        clock: Optional[Callable[[], float]] = None,
    ) -> None:
        normalized_keys = [str(key).strip() for key in keys if str(key).strip()]
        if not normalized_keys:
            raise ValueError("API key pool requires at least one non-empty key.")

        self.keys = normalized_keys
        self.settings = settings or KeyPoolSettings()
        self.state = state or KeyPoolState()
        self.state.ensure_keys(self.keys)
        self._rng = rng or random.Random()
        self._clock = clock or __import__("time").time

    def available_keys(self, now: Optional[float] = None) -> list[str]:
        current_time = self._clock() if now is None else now
        available = [key for key in self.keys if self.state.cooldowns.get(key, 0.0) <= current_time]
        return available or list(self.keys)

    def choose_key(self, now: Optional[float] = None) -> str:
        available = self.available_keys(now=now)
        if self.settings.rotation_strategy == "random":
            return self._rng.choice(available)

        start_index = self.state.index % len(self.keys)
        for offset in range(len(self.keys)):
            candidate_index = (start_index + offset) % len(self.keys)
            candidate = self.keys[candidate_index]
            if candidate in available:
                self.state.index = (candidate_index + 1) % len(self.keys)
                return candidate

        chosen = self.keys[start_index]
        self.state.index = (start_index + 1) % len(self.keys)
        return chosen

    def mark_success(self, api_key: str) -> None:
        if api_key not in self.state.fail_counts:
            return
        self.state.fail_counts[api_key] = 0
        self.state.cooldowns[api_key] = 0.0

    def mark_failure(self, api_key: str, reason: ErrorCategory = "other", now: Optional[float] = None) -> None:
        if api_key not in self.state.fail_counts:
            return

        self.state.fail_counts[api_key] = self.state.fail_counts.get(api_key, 0) + 1
        current_time = self._clock() if now is None else now
        should_cooldown = reason in {"rate_limit", "timeout"} or (
            self.state.fail_counts[api_key] >= self.settings.max_consecutive_failures
        )
        if should_cooldown:
            self.state.cooldowns[api_key] = current_time + self.settings.cooldown_seconds

    def mark_result(self, api_key: str, success: bool, reason: ErrorCategory = "other", now: Optional[float] = None) -> None:
        if success:
            self.mark_success(api_key)
            return
        self.mark_failure(api_key, reason=reason, now=now)


class KeyPoolRegistry:
    def __init__(
        self,
        *,
        rng: Optional[random.Random] = None,
        clock: Optional[Callable[[], float]] = None,
    ) -> None:
        self._pools: Dict[str, ApiKeyPool] = {}
        self._rng = rng
        self._clock = clock
        self._lock = threading.RLock()

    def get_pool(self, model_config: Dict[str, Any]) -> ApiKeyPool:
        with self._lock:
            pool_id = get_key_pool_id(model_config)
            keys = resolve_api_keys(model_config)
            if pool_id not in self._pools:
                self._pools[pool_id] = ApiKeyPool(
                    keys,
                    settings=KeyPoolSettings.from_model_config(model_config),
                    rng=self._rng,
                    clock=self._clock,
                )
            else:
                self._pools[pool_id].state.ensure_keys(keys)
            return self._pools[pool_id]

    def choose_api_key(self, model_config: Dict[str, Any], now: Optional[float] = None) -> str:
        with self._lock:
            return self.get_pool(model_config).choose_key(now=now)

    def mark_result(
        self,
        model_config: Dict[str, Any],
        api_key: str,
        success: bool,
        reason: ErrorCategory = "other",
        now: Optional[float] = None,
    ) -> None:
        with self._lock:
            if len(resolve_api_keys(model_config)) <= 1 or not api_key:
                return
            self.get_pool(model_config).mark_result(api_key, success=success, reason=reason, now=now)


def get_key_pool_id(model_config: Dict[str, Any]) -> str:
    return str(model_config.get("key_pool_name") or model_config.get("name") or "default")


def _resolve_env_key(env_name: str) -> str:
    normalized_name = str(env_name).strip()
    if not normalized_name:
        return ""
    return str(os.environ.get(normalized_name, "")).strip()


def resolve_api_keys(model_config: Dict[str, Any]) -> list[str]:
    env_keys = model_config.get("api_keys_env")
    if isinstance(env_keys, list):
        resolved_env_keys = [_resolve_env_key(env_name) for env_name in env_keys]
        normalized_env_keys = [key for key in resolved_env_keys if key]
        if normalized_env_keys:
            return normalized_env_keys

    keys = model_config.get("api_keys")
    if isinstance(keys, list):
        normalized = [str(key).strip() for key in keys if str(key).strip()]
        if normalized:
            return normalized

    env_key_name = model_config.get("api_key_env")
    if env_key_name is not None:
        resolved_env_key = _resolve_env_key(str(env_key_name))
        if resolved_env_key:
            return [resolved_env_key]

    api_key = str(model_config.get("api_key", "")).strip()
    if api_key:
        return [api_key]

    raise ValueError(f"Model {model_config.get('name', '')} is missing api_key or api_keys.")


def classify_llm_error(error: Exception | str) -> ErrorCategory:
    message = str(error).lower()
    if any(token in message for token in ("rate limit", "429", "too many requests", "quota", "exceeded")):
        return "rate_limit"
    if any(token in message for token in ("timeout", "timed out", "read timeout", "connect timeout")):
        return "timeout"
    if any(token in message for token in ("unauthorized", "invalid api key", "401", "permission")):
        return "auth"
    return "other"


def extract_json_from_response(response_text: str) -> Optional[Any]:
    text = (response_text or "").strip()
    if not text:
        return None

    try:
        return json.loads(text)
    except JSONDecodeError:
        pass

    decoder = JSONDecoder()
    for index, char in enumerate(text):
        if char not in "[{":
            continue
        try:
            payload, _ = decoder.raw_decode(text[index:])
            return payload
        except JSONDecodeError:
            continue
    return None


def build_openai_client(
    model_config: Dict[str, Any],
    *,
    api_key: Optional[str] = None,
    default_base_url: Optional[str] = None,
    client_factory: Callable[..., Any] = OpenAI,
    registry: Optional[KeyPoolRegistry] = None,
) -> Any:
    resolved_api_key = api_key or (
        registry.choose_api_key(model_config) if registry is not None else resolve_api_keys(model_config)[0]
    )
    base_url = model_config.get("base_url") or default_base_url
    kwargs: Dict[str, Any] = {"api_key": resolved_api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return client_factory(**kwargs)
