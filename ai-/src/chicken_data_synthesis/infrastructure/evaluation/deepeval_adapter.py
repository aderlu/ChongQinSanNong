from __future__ import annotations

from typing import Any, Dict

from deepeval_integration import evaluate_case_with_deepeval


def evaluate_case_with_deepeval_adapter(
    case_data: Dict[str, Any],
    judge_config: Dict[str, Any],
    judge_label: str,
    project_config: Dict[str, Any],
) -> Dict[str, Any]:
    """Compatibility adapter around the current DeepEval integration package."""

    return evaluate_case_with_deepeval(
        case_data=case_data,
        judge_config=judge_config,
        judge_label=judge_label,
        project_config=project_config,
    )
