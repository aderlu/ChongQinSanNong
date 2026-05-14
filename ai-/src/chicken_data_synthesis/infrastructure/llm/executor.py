from __future__ import annotations

import random
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Mapping, Optional, Sequence

from .budgeting import estimate_usage_cost, extract_token_usage, resolve_model_pricing
from .runtime import KeyPoolRegistry, build_openai_client, classify_llm_error


Message = Mapping[str, str]


@dataclass(slots=True)
class RetryPolicy:
    max_retries: int = 3
    request_interval_seconds: float = 0.0
    backoff_base_seconds: float = 1.0
    backoff_jitter_seconds: float = 1.0

    def normalized_max_attempts(self) -> int:
        return max(int(self.max_retries), 1)


@dataclass(slots=True)
class ChatCompletionResult:
    success: bool
    content: Optional[str]
    reasoning: Optional[str]
    elapsed_seconds: float
    attempts: int
    api_key: str = ""
    error: str = ""
    error_category: str = ""
    finish_reason: str = ""
    response: Any = None
    usage: Dict[str, Any] = field(default_factory=dict)
    cost: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


def build_retry_policy(
    *,
    max_retries: int = 3,
    request_interval_seconds: float = 0.0,
    backoff_base_seconds: float = 1.0,
    backoff_jitter_seconds: float = 1.0,
) -> RetryPolicy:
    return RetryPolicy(
        max_retries=int(max_retries),
        request_interval_seconds=float(request_interval_seconds),
        backoff_base_seconds=float(backoff_base_seconds),
        backoff_jitter_seconds=float(backoff_jitter_seconds),
    )


def build_chat_completion_extra_body(
    *,
    expected_output: str = "",
    task_id: str = "",
    extra_body: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = dict(extra_body or {})
    payload.setdefault("task_id", task_id or str(uuid.uuid4()))
    if expected_output:
        payload["expected_output"] = expected_output
    return payload


def build_chat_completion_request_kwargs(
    model_config: Mapping[str, Any],
    messages: Sequence[Message],
    *,
    expected_output: str = "",
    task_id: str = "",
    extra_body: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "model": model_config["name"],
        "messages": list(messages),
        "temperature": model_config["temperature"],
        "max_tokens": model_config["max_tokens"],
        "timeout": model_config["timeout"],
        "extra_body": build_chat_completion_extra_body(
            expected_output=expected_output,
            task_id=task_id,
            extra_body=extra_body,
        ),
    }


def compute_retry_delay(attempt_index: int, policy: RetryPolicy, *, rng: Optional[random.Random] = None) -> float:
    base_delay = max(float(policy.backoff_base_seconds), 0.0) * (2 ** max(attempt_index, 0))
    jitter_window = max(float(policy.backoff_jitter_seconds), 0.0)
    if jitter_window <= 0:
        return base_delay
    random_source = rng or random.Random()
    return base_delay + random_source.uniform(0.0, jitter_window)


def call_chat_completion_with_retry(
    model_config: Mapping[str, Any],
    messages: Sequence[Message],
    *,
    expected_output: str = "",
    retry_policy: Optional[RetryPolicy] = None,
    extra_body: Optional[Mapping[str, Any]] = None,
    registry: Optional[KeyPoolRegistry] = None,
    client_builder: Callable[..., Any] = build_openai_client,
    sleep: Callable[[float], None] = time.sleep,
    perf_counter: Callable[[], float] = time.perf_counter,
    rng: Optional[random.Random] = None,
    task_id_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
) -> ChatCompletionResult:
    policy = retry_policy or RetryPolicy()
    started_at = perf_counter()
    attempts = 0
    last_error = ""
    last_error_category = ""
    last_api_key = ""
    request_kwargs = build_chat_completion_request_kwargs(
        model_config,
        messages,
        expected_output=expected_output,
        task_id=task_id_factory(),
        extra_body=extra_body,
    )

    for attempt_index in range(policy.normalized_max_attempts()):
        attempts = attempt_index + 1
        selected_api_key = ""
        try:
            selected_api_key = registry.choose_api_key(dict(model_config)) if registry is not None else ""
            last_api_key = selected_api_key
            client = client_builder(
                dict(model_config),
                api_key=selected_api_key or None,
                registry=registry,
            )
            request_interval = max(float(policy.request_interval_seconds), 0.0)
            if request_interval > 0:
                sleep(request_interval)

            response = client.chat.completions.create(**request_kwargs)
            elapsed = perf_counter() - started_at
            message = response.choices[0].message
            finish_reason = getattr(response.choices[0], "finish_reason", "") or ""
            reasoning = getattr(message, "reasoning_content", None)
            content = getattr(message, "content", None)
            usage = extract_token_usage(response)
            pricing = resolve_model_pricing(model_config)
            cost = estimate_usage_cost(usage, pricing) if pricing is not None else None
            if registry is not None and selected_api_key:
                registry.mark_result(dict(model_config), selected_api_key, success=True)
            return ChatCompletionResult(
                success=True,
                content=content,
                reasoning=reasoning,
                elapsed_seconds=elapsed,
                attempts=attempts,
                api_key=selected_api_key,
                finish_reason=finish_reason,
                response=response,
                usage=usage.to_dict(),
                cost=cost.to_dict() if cost is not None else {},
                metadata={
                    "expected_output": expected_output,
                    "task_id": request_kwargs["extra_body"]["task_id"],
                    "usage": usage.to_dict(),
                    "cost": cost.to_dict() if cost is not None else {},
                },
            )
        except Exception as exc:
            last_error = str(exc)
            last_error_category = classify_llm_error(exc)
            last_api_key = selected_api_key or last_api_key
            if registry is not None and selected_api_key:
                registry.mark_result(
                    dict(model_config),
                    selected_api_key,
                    success=False,
                    reason=last_error_category,
                )
            if attempt_index >= policy.normalized_max_attempts() - 1:
                break
            delay = compute_retry_delay(attempt_index, policy, rng=rng)
            if delay > 0:
                sleep(delay)

    return ChatCompletionResult(
        success=False,
        content=None,
        reasoning=None,
        elapsed_seconds=perf_counter() - started_at,
        attempts=attempts,
        api_key=last_api_key,
        error=last_error,
        error_category=last_error_category,
        metadata={
            "expected_output": expected_output,
            "task_id": request_kwargs["extra_body"]["task_id"],
        },
    )
