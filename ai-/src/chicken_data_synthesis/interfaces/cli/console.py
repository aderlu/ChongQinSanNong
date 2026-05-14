from __future__ import annotations

from typing import Any, Mapping, Sequence


SEPARATOR = "=" * 72
SUB_SEPARATOR = "-" * 72


def _stringify_join(values: Sequence[Any]) -> str:
    return ", ".join(str(value) for value in values)


def build_header_lines(
    *,
    mode: str,
    sample_count: int,
    parallel_count: int,
    evaluation_mode: str = "legacy",
    project_name: str = "",
    version: str = "",
    request_interval: int | float = 0,
    snapshot_settings: Mapping[str, Any] | None = None,
    pilot_config: Mapping[str, Any] | None = None,
    production_models: Mapping[str, Mapping[str, Any]] | None = None,
    milestones: Sequence[int] | None = None,
    log_file: str = "",
    error_log_file: str = "",
    title: str = "鸡病黄金数据集构建系统",
) -> list[str]:
    snapshot_settings = snapshot_settings or {}
    pilot_config = pilot_config or {}
    production_models = production_models or {}
    lines = [
        SEPARATOR,
        f"  {title}",
        f"  项目: {project_name}",
        f"  版本: {version}",
        SUB_SEPARATOR,
        f"  模式: {mode}",
        f"  样本数: {sample_count}",
        f"  并行度: {parallel_count} 进程",
        f"  评估模式: {evaluation_mode}",
        f"  请求间隔: {request_interval} 秒",
        f"  分发块大小: {snapshot_settings.get('dispatch_chunk_size', '')}",
        f"  Worker 重建阈值: {snapshot_settings.get('worker_max_cases_per_child', '')} 条/子进程",
        f"  进度日志间隔: {snapshot_settings.get('progress_log_every', '')} 条",
        f"  快照间隔: {snapshot_settings.get('save_every_results', '')} 条",
    ]

    if mode == "pilot":
        lines.extend(
            [
                f"  候选执行模型: {_stringify_join(pilot_config.get('generator_candidates', []))}",
                f"  一级裁判: {_stringify_join(pilot_config.get('primary_judges', []))}",
                f"  二级仲裁: {pilot_config.get('arbiter', '')}",
            ]
        )
    else:
        generator = production_models.get("generator", {})
        judge_a = production_models.get("judge_a", {})
        judge_b = production_models.get("judge_b", {})
        arbiter = production_models.get("arbiter", {})
        lines.extend(
            [
                f"  执行模型: {generator.get('name', '')}",
                f"  一级裁判: {judge_a.get('name', '')} + {judge_b.get('name', '')}",
                f"  二级仲裁: {arbiter.get('name', '')}",
            ]
        )
        if milestones:
            lines.append(f"  里程碑: {_stringify_join(milestones)}")

    if log_file:
        lines.append(f"  实时日志: {log_file}")
    if error_log_file:
        lines.append(f"  错误日志: {error_log_file}")
    lines.append(SEPARATOR)
    return lines


def build_stage_summary_block(
    *,
    target_total: int,
    summary_lines: Sequence[str],
    snapshot_path: str = "",
) -> list[str]:
    lines = [f"  [阶段完成] 里程碑 {target_total} 条摘要:"]
    lines.extend(f"    {line}" for line in summary_lines)
    if snapshot_path:
        lines.append(f"  阶段快照: {snapshot_path}")
    return lines


def build_resume_lines(
    *,
    snapshot_path: str,
    result_count: int,
    completed_target: int,
) -> list[str]:
    return [
        f"[恢复] 已加载快照: {snapshot_path}",
        f"[恢复] 已恢复结果 {result_count} 条，最近完成里程碑 {completed_target}",
    ]


def build_simple_info_line(label: str, value: Any, suffix: str = "") -> str:
    tail = f" {suffix}" if suffix else ""
    return f"  {label}: {value}{tail}"


def build_completion_lines(
    *,
    mode: str,
    summary: Mapping[str, Any],
    elapsed_total_seconds: int | float,
    result_csv: str,
    summary_csv: str = "",
    sample_count: int | None = None,
) -> list[str]:
    completed_total = sample_count if mode == "production" and sample_count is not None else summary.get("total", 0)
    timing = _as_mapping(summary.get("timing"))
    lines = [
        "",
        "[4/4] 运行完成",
        SEPARATOR,
        f"  已完成: {summary.get('total', 0)} / {completed_total}",
        f"  成功: {summary.get('success_count', 0)}",
        f"  失败: {summary.get('failure_count', 0)}",
        f"  需要仲裁: {summary.get('arbitration_count', 0)}",
        f"  致命风险: {summary.get('fatal_risk_count', 0)}",
        f"  平均总分: {summary.get('avg_final_score', 0)}",
        f"  平均生成耗时: {summary.get('avg_generation_seconds', 0)} 秒",
        f"  平均评审耗时: {summary.get('avg_judge_seconds', 0)} 秒",
        f"  总耗时: {int(elapsed_total_seconds)} 秒",
        f"  明细结果: {result_csv}",
    ]
    if timing:
        lines.extend(
            [
                "  全链路耗时分析:",
                f"    生成: {_format_timing(timing.get('generation'))}",
                f"    Judge A: {_format_timing(timing.get('judge_a'))}",
                f"    Judge B: {_format_timing(timing.get('judge_b'))}",
                f"    仲裁: {_format_timing(timing.get('arbiter'))}",
                f"    评审合计: {_format_timing(timing.get('review_total'))}",
                f"    单条端到端: {_format_timing(timing.get('case_end_to_end'))}",
                (
                    f"    模型工作量/墙钟: {timing.get('total_model_work_seconds', 0)}s / "
                    f"{timing.get('wall_clock_seconds', round(float(elapsed_total_seconds), 2))}s | "
                    f"并发工作倍率 {timing.get('parallel_work_ratio', 0)}"
                    + (
                        f" | 并发效率 {timing.get('parallel_efficiency', 0)}"
                        if timing.get("parallel_efficiency") is not None
                        else ""
                    )
                ),
            ]
        )
    if summary_csv:
        lines.append(f"  对比汇总: {summary_csv}")
    lines.append(SEPARATOR)
    return lines


def _as_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _format_timing(value: Any) -> str:
    timing = _as_mapping(value)
    if not timing:
        return "n/a"
    return (
        f"avg {timing.get('avg', 0)}s | p50 {timing.get('p50', 0)}s | "
        f"p95 {timing.get('p95', 0)}s | max {timing.get('max', 0)}s | "
        f"total {timing.get('total', 0)}s"
    )


__all__ = [
    "SEPARATOR",
    "SUB_SEPARATOR",
    "build_completion_lines",
    "build_header_lines",
    "build_resume_lines",
    "build_simple_info_line",
    "build_stage_summary_block",
]
