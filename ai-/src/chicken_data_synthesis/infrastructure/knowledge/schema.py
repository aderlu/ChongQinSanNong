from __future__ import annotations
"""LLM Wiki 操作 schema 的校验模块。

``knowledge/schemas/llm_wiki_schema.yaml`` 不是普通说明文档，它同时承担
“设计说明”和“运行时契约”两种角色。本模块负责检查 schema 中声明的目录、
导出文件、页面类型、来源类型、权威白名单和审计字段是否与代码常量一致，
并进一步检查当前 Wiki 包是否满足严格约束。
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from chicken_data_synthesis.paths import PROJECT_ROOT

from .contracts import (
    AUTHORITY_ALLOWED_DOMAINS,
    CACHE_FILE_NAME,
    CACHE_VERSION,
    PAGE_TYPES,
    REQUIRED_DIRECTORIES,
    REQUIRED_EXPORTS,
    ROOT_MARKDOWN_FILES,
    SOURCE_FRONTMATTER_FIELDS,
)
from .linting import json_loadable_exports, run_strict_checks
from .registry import list_source_types


DEFAULT_SCHEMA_PATH = PROJECT_ROOT / "knowledge" / "schemas" / "llm_wiki_schema.yaml"
REQUIRED_AUDIT_FIELDS = (
    "wiki_dir",
    "wiki_fact_count",
    "wiki_page_count",
    "wiki_context_query",
    "wiki_evidence_status_counts",
    "wiki_evidence_source_ids",
    "wiki_context_chars",
    "target_disease_in_diagnosis",
    "target_disease_mismatch",
    "final_fatal_risk",
)
ADAPTER_STATES = (
    "available",
    "missing_dependency",
    "manual_only",
    "failed_retryable",
    "failed_manual_fallback",
)


@dataclass(frozen=True)
class LlmWikiSchemaCheckReport:
    """schema-check 命令和测试使用的机器可读报告。

    报告中包含 schema 路径、Wiki 路径、声明版本、错误、警告和每一项检查
    的详细结果，方便汇报时说明“到底检查了什么”。
    """
    schema_path: str
    wiki_dir: str
    ok: bool
    declared_version: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    checks: tuple[dict[str, Any], ...]


def schema_check(
    wiki_dir: str | Path,
    *,
    schema_path: str | Path | None = None,
) -> LlmWikiSchemaCheckReport:
    """把声明式 schema 同代码常量和磁盘上的 Wiki 包进行校验。

    校验分两层：
        1. schema 与代码契约是否一致，例如必需目录、导出文件、页面类型、
           来源类型、权威域名白名单等。
        2. 当前 Wiki 文件是否健康，例如 JSON 是否可加载、严格 lint 是否通过、
           source/cache/fact 等约束是否满足。

    这样可以防止出现“文档说一套、代码跑一套、磁盘数据又是另一套”的问题。
    """

    schema_file = Path(schema_path) if schema_path else DEFAULT_SCHEMA_PATH
    root = Path(wiki_dir)
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []

    if not schema_file.is_file():
        return LlmWikiSchemaCheckReport(
            schema_path=str(schema_file),
            wiki_dir=str(root),
            ok=False,
            declared_version="",
            errors=(f"schema_file_missing:{schema_file}",),
            warnings=(),
            checks=(),
        )

    schema = _load_yaml_mapping(schema_file)
    declared_version = str(schema.get("version") or "")

    _check_exact_list(
        schema,
        "wiki_root.required_root_files",
        ROOT_MARKDOWN_FILES,
        errors,
        checks,
    )
    _check_exact_list(
        schema,
        "wiki_root.required_directories",
        REQUIRED_DIRECTORIES,
        errors,
        checks,
    )
    _check_exact_list(
        schema,
        "wiki_root.required_exports",
        REQUIRED_EXPORTS,
        errors,
        checks,
    )
    _check_value(schema, "wiki_root.cache_file", CACHE_FILE_NAME, errors, checks)
    _check_value(schema, "wiki_root.cache_version", CACHE_VERSION, errors, checks)
    _check_mapping_keys(
        schema,
        "organization.page_types",
        PAGE_TYPES,
        errors,
        checks,
    )
    _check_contains_list(
        schema,
        "source_contract.required_frontmatter_fields",
        SOURCE_FRONTMATTER_FIELDS,
        errors,
        checks,
    )
    _check_mapping_keys(
        schema,
        "source_contract.source_types",
        tuple(item.source_id for item in list_source_types()),
        errors,
        checks,
    )
    _check_contains_list(schema, "source_contract.adapter_states", ADAPTER_STATES, errors, checks)
    _check_exact_list(schema, "maintenance.authority_discovery.allowed_domains", AUTHORITY_ALLOWED_DOMAINS, errors, checks)
    _check_value(schema, "maintenance.authority_discovery.llm_may_propose_sources", True, errors, checks)
    _check_value(schema, "maintenance.authority_discovery.allowlist_required", True, errors, checks)
    _check_value(schema, "maintenance.authority_discovery.candidate_only", True, errors, checks)
    _check_value(schema, "maintenance.authority_discovery.must_not_write_authoritative_facts", True, errors, checks)
    _check_contains_list(schema, "audit.output_csv_fields", REQUIRED_AUDIT_FIELDS, errors, checks)

    for check in (*json_loadable_exports(root), *run_strict_checks(root, fix=False)):
        payload = check.to_dict()
        checks.append(payload)
        if check.severity == "error":
            errors.append(f"wiki:{check.code}:{check.path or check.message}")
        else:
            warnings.append(f"wiki:{check.code}:{check.path or check.message}")

    return LlmWikiSchemaCheckReport(
        schema_path=str(schema_file),
        wiki_dir=str(root),
        ok=not errors,
        declared_version=declared_version,
        errors=tuple(errors),
        warnings=tuple(warnings),
        checks=tuple(checks),
    )


def _load_yaml_mapping(path: Path) -> Mapping[str, Any]:
    """读取 schema YAML，并要求顶层必须是映射对象。"""
    raw = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(raw, Mapping):
        raise TypeError(f"LLM Wiki schema must be a mapping: {path}")
    return raw


def _check_value(
    schema: Mapping[str, Any],
    dotted_path: str,
    expected: Any,
    errors: list[str],
    checks: list[dict[str, Any]],
) -> None:
    """记录一个 schema 标量值与代码常量的相等性检查。"""
    actual = _get_path(schema, dotted_path)
    ok = actual == expected
    checks.append({"code": "schema_value_matches", "path": dotted_path, "ok": ok, "expected": expected, "actual": actual})
    if not ok:
        errors.append(f"schema_value_mismatch:{dotted_path}")


def _check_exact_list(
    schema: Mapping[str, Any],
    dotted_path: str,
    expected: tuple[str, ...],
    errors: list[str],
    checks: list[dict[str, Any]],
) -> None:
    """要求 schema 中的列表与代码中的元组完全一致。

    适用于目录、导出文件、白名单等顺序和内容都需要稳定的契约。
    """
    actual = _as_str_tuple(_get_path(schema, dotted_path))
    ok = actual == expected
    checks.append({"code": "schema_list_exact", "path": dotted_path, "ok": ok, "expected": expected, "actual": actual})
    if not ok:
        errors.append(f"schema_list_mismatch:{dotted_path}")


def _check_contains_list(
    schema: Mapping[str, Any],
    dotted_path: str,
    expected_items: tuple[str, ...],
    errors: list[str],
    checks: list[dict[str, Any]],
) -> None:
    """要求 schema 列表至少包含代码要求的全部项目。

    适用于审计字段、frontmatter 字段等可能允许扩展但不能缺少核心字段的场景。
    """
    actual = set(_as_str_tuple(_get_path(schema, dotted_path)))
    missing = tuple(item for item in expected_items if item not in actual)
    ok = not missing
    checks.append({"code": "schema_list_contains", "path": dotted_path, "ok": ok, "missing": missing})
    if missing:
        errors.append(f"schema_list_missing_items:{dotted_path}:{','.join(missing)}")


def _check_mapping_keys(
    schema: Mapping[str, Any],
    dotted_path: str,
    expected_keys: tuple[str, ...],
    errors: list[str],
    checks: list[dict[str, Any]],
) -> None:
    """要求 schema 映射中定义指定的键。

    例如页面类型和来源类型必须在 schema 中都有解释，否则汇报和自动校验会
    缺少设计依据。
    """
    actual = _get_path(schema, dotted_path)
    actual_keys = tuple(actual.keys()) if isinstance(actual, Mapping) else ()
    missing = tuple(key for key in expected_keys if key not in actual_keys)
    ok = not missing
    checks.append({"code": "schema_mapping_keys", "path": dotted_path, "ok": ok, "missing": missing, "actual": actual_keys})
    if missing:
        errors.append(f"schema_mapping_missing_keys:{dotted_path}:{','.join(missing)}")


def _get_path(schema: Mapping[str, Any], dotted_path: str) -> Any:
    """通过点分路径读取 schema 中的嵌套值。"""
    current: Any = schema
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping):
            return None
        current = current.get(part)
    return current


def _as_str_tuple(value: Any) -> tuple[str, ...]:
    """把 YAML 列表或元组统一转换为字符串元组，方便比较。"""
    if not isinstance(value, list | tuple):
        return ()
    return tuple(str(item) for item in value)


__all__ = ["DEFAULT_SCHEMA_PATH", "LlmWikiSchemaCheckReport", "schema_check"]
