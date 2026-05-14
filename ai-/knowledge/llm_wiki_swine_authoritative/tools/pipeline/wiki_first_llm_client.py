from __future__ import annotations

import json
import os
import re
import uuid
from dataclasses import dataclass
from typing import Any


DEFAULT_BASE_URL = "https://api.nonelinear.com/v1"
DEFAULT_MODEL = "hunyuan-turbos-20250926"


def resolve_api_key(explicit_api_key: str = "") -> str:
    if explicit_api_key:
        return explicit_api_key
    for name in ("WIKI_FIRST_API_KEY", "NONELINEAR_API_KEY", "OPENAI_API_KEY"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


def extract_json_object(text: str) -> dict[str, Any]:
    cleaned = (text or "").strip()
    if not cleaned:
        raise ValueError("empty model output")
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if not match:
            raise ValueError("model output did not contain a JSON object")
        payload = json.loads(match.group(0))
    if not isinstance(payload, dict):
        raise ValueError("model JSON output is not an object")
    return payload


def extract_text_content(response: Any) -> str:
    choices = getattr(response, "choices", None) or []
    if choices:
        message = getattr(choices[0], "message", None)
        content = getattr(message, "content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            chunks: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        chunks.append(str(item.get("text") or ""))
                else:
                    text = getattr(item, "text", "")
                    if text:
                        chunks.append(str(text))
            return "".join(chunks)
    output = getattr(response, "output_text", "")
    return output if isinstance(output, str) else str(output or "")


@dataclass
class LLMResult:
    payload: dict[str, Any]
    model: str
    request_ref: str
    response_ref: str


class WikiFirstLLMClient:
    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        base_url: str = "",
        api_key: str = "",
        temperature: float = 0.2,
        max_tokens: int = 1200,
        timeout: int = 90,
    ) -> None:
        resolved_api_key = resolve_api_key(api_key)
        if not resolved_api_key:
            raise RuntimeError("Missing API key. Set WIKI_FIRST_API_KEY, NONELINEAR_API_KEY, or OPENAI_API_KEY.")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("The openai package is required for --mode real-api.") from exc

        resolved_base_url = (
            base_url
            or os.environ.get("NONELINEAR_BASE_URL", "").strip()
            or os.environ.get("OPENAI_BASE_URL", "").strip()
            or DEFAULT_BASE_URL
        )

        client_kwargs: dict[str, Any] = {
            "api_key": resolved_api_key,
            "base_url": resolved_base_url,
        }
        self._client = OpenAI(**client_kwargs)
        self.model = model or DEFAULT_MODEL
        self.base_url = resolved_base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    def generate_json(self, *, stage: str, system_prompt: str, user_prompt: str) -> LLMResult:
        request_ref = f"req-{stage}-{uuid.uuid4().hex[:12]}"
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            extra_body={"task_id": request_ref},
        )
        text = extract_text_content(response)
        payload = extract_json_object(text)
        response_id = getattr(response, "id", "") or f"resp-{stage}-{uuid.uuid4().hex[:12]}"
        response_model = getattr(response, "model", "") or self.model
        return LLMResult(
            payload=payload,
            model=str(response_model),
            request_ref=request_ref,
            response_ref=str(response_id),
        )
