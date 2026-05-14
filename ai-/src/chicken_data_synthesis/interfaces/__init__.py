"""External interfaces such as CLI commands and public entry adapters."""

from .cli import (
    PipelineEntrypointResult,
    SEPARATOR,
    SUB_SEPARATOR,
    build_completion_lines,
    build_header_lines,
    build_resume_lines,
    build_simple_info_line,
    build_stage_summary_block,
    main,
    run,
)

__all__ = [
    "PipelineEntrypointResult",
    "SEPARATOR",
    "SUB_SEPARATOR",
    "build_completion_lines",
    "build_header_lines",
    "build_resume_lines",
    "build_simple_info_line",
    "build_stage_summary_block",
    "main",
    "run",
]
