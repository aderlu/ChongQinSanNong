from __future__ import annotations

from collections.abc import Sequence

from chicken_data_synthesis.application.use_cases import (
    PipelineUseCaseHooks,
    PipelineUseCaseInput,
    PipelineUseCaseResult,
    run_pipeline_use_case,
)
from chicken_data_synthesis.application.use_cases.pipeline_runtime import PipelineExecutionContext


PipelineEntrypointResult = PipelineExecutionContext | PipelineUseCaseResult | None


def run(
    argv: Sequence[str] | None = None,
    *,
    runtime_input: PipelineUseCaseInput | None = None,
    hooks: PipelineUseCaseHooks | None = None,
) -> PipelineEntrypointResult:
    """Run the package pipeline entrypoint through the application-layer use case."""

    return run_pipeline_use_case(argv=argv, runtime_input=runtime_input, hooks=hooks)


def main(
    argv: Sequence[str] | None = None,
    *,
    runtime_input: PipelineUseCaseInput | None = None,
    hooks: PipelineUseCaseHooks | None = None,
) -> PipelineEntrypointResult:
    """Primary CLI adapter for the chicken data synthesis package."""

    return run(argv=argv, runtime_input=runtime_input, hooks=hooks)


__all__ = ["PipelineEntrypointResult", "main", "run"]
