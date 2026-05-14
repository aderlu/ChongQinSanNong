from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI


class BaseChatModel(ABC):
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        raise NotImplementedError


class BaseEmbeddingModel(ABC):
    @abstractmethod
    def embed(self, texts: List[str], **kwargs: Any) -> List[List[float]]:
        raise NotImplementedError


@dataclass
class OpenAICompatibleChatModel(BaseChatModel):
    base_url: str
    api_key: str
    model: str
    timeout: int = 60

    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.2),
            max_tokens=kwargs.get("max_tokens", 1600),
            timeout=kwargs.get("timeout", self.timeout),
            extra_body=kwargs.get("extra_body"),
        )
        message = response.choices[0].message
        return {
            "content": message.content or "",
            "reasoning_content": getattr(message, "reasoning_content", None),
            "raw_response": response,
        }


@dataclass
class OpenAICompatibleEmbeddingModel(BaseEmbeddingModel):
    base_url: str
    api_key: str
    model: str
    timeout: int = 60

    def embed(self, texts: List[str], **kwargs: Any) -> List[List[float]]:
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.embeddings.create(
            model=self.model,
            input=texts,
            timeout=kwargs.get("timeout", self.timeout),
        )
        return [item.embedding for item in response.data]
