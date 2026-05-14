"""
Dify API 集成模块
用于调用公司模型进行诊断，以及裁判模型进行评估打分
"""

import json
import time
import requests
from typing import Any, Dict, Optional, List
from dataclasses import dataclass


@dataclass
class DifyResponse:
    success: bool
    data: Any
    error: str = ""


class DifyClient:
    """Dify API 客户端"""

    def __init__(self, base_url: str, api_key: str, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _call_v1(self, endpoint: str, inputs: Dict[str, Any], response_mode: str = "blocking") -> DifyResponse:
        """调用 Dify v1 API"""
        url = f"{self.base_url}/v1/messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": inputs,
            "response_mode": response_mode,
            "user": "chicken-disease-system"
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()

            # 阻塞模式返回完整响应
            if response_mode == "blocking":
                return DifyResponse(
                    success=True,
                    data=data.get("data", {})
                )
            else:
                return DifyResponse(success=True, data=data)

        except requests.exceptions.Timeout:
            return DifyResponse(success=False, data=None, error="请求超时")
        except requests.exceptions.RequestException as e:
            return DifyResponse(success=False, data=None, error=str(e))

    def chat(self, query: str, inputs: Optional[Dict[str, Any]] = None) -> DifyResponse:
        """发送聊天消息"""
        all_inputs = inputs or {}
        all_inputs["query"] = query
        return self._call_v1("/chat", all_inputs)


def create_company_model_client() -> DifyClient:
    """创建公司模型客户端 (诊断和处方)"""
    return DifyClient(
        base_url="http://dify.amdu.dtyunxi.cn/v1",
        api_key="app-lh3ByE1G9M0PIU4c2509iG1Y",
        timeout=120
    )


def create_judge_model_client() -> DifyClient:
    """创建裁判模型客户端 (评估打分)"""
    return DifyClient(
        base_url="http://dify.amdu.dtyunxi.cn/v1",
        api_key="app-18c7e697-ca19-4653-bbd2-7bdcfd422b50",
        timeout=120
    )


def extract_text_from_dify_response(response_data: Dict) -> str:
    """从 Dify 响应中提取文本内容"""
    if not response_data:
        return ""

    # 尝试从 answer 字段获取
    if "answer":
        return response_data["answer"]

    # 尝试从 outputs 获取
    if "outputs":
        outputs = response_data["outputs"]
        for key in ["result", "diagnosis", "text", "content", "response"]:
            if key in outputs:
                return outputs[key]
        # 返回第一个非空字段
        for v in outputs.values():
            if isinstance(v, str) and v.strip():
                return v

    return str(response_data)


def diagnose_and_prescribe(client: DifyClient, user_query: str) -> DifyResponse:
    """调用公司模型进行诊断和开方"""
    return client.chat(
        query=user_query,
        inputs={
            "query": user_query,
            "task": "diagnose_and_prescribe"
        }
    )


def evaluate_response(client: DifyClient, user_query: str, diagnosis: str, prescription: str) -> DifyResponse:
    """调用裁判模型评估诊断和处方质量"""
    return client.chat(
        query=f"请评估以下诊断和处方的质量",
        inputs={
            "query": user_query,
            "diagnosis": diagnosis,
            "prescription": prescription,
            "task": "evaluate"
        }
    )
