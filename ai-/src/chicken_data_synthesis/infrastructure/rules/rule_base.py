from __future__ import annotations

from typing import Any, Dict

from llm_foundation.tools import rule_base_check_tool


def evaluate_rule_base(case_data: Dict[str, Any], rule_base_config: Dict[str, Any]) -> Dict[str, Any]:
    """Compatibility adapter around the current rule-base tool implementation."""

    return rule_base_check_tool(case_data, rule_base_config)
