"""DeepEval-based evaluation adapters for the chicken disease dataset pipeline."""

from .evaluator import ChickenCaseDeepEvalEvaluator, evaluate_case_with_deepeval

__all__ = ["ChickenCaseDeepEvalEvaluator", "evaluate_case_with_deepeval"]
