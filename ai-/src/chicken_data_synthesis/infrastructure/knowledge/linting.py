from __future__ import annotations

import json
from dataclasses import asdict, dataclass
import re
from pathlib import Path

from .cache import read_cache, write_cache
from .contracts import REQUIRED_DIRECTORIES, REQUIRED_EXPORTS, ROOT_MARKDOWN_FILES
from .wiki import load_llm_wiki


# 健康检查是 LLM Wiki 自动维护的防御层。它会检查目录契约、JSON 导出文件、
# 证据状态、来源引用和缓存一致性。这样 LLM 产生的变更如果不可靠，可以在
# 进入正式生成/评估知识之前被拦截，或者被保留在待复核状态。

@dataclass(frozen=True)
class CheckResult:
    """一条机器可读的 lint 检查结果。

    ``code`` 是稳定的问题编码，方便自动化识别；``severity`` 决定严格模式
    是否失败；``fixable`` 表示 CLI 的 ``--fix`` 是否有机会自动修复该问题。
    """

    code: str
    severity: str
    message: str
    path: str = ""
    line: int | None = None
    fixable: bool = False

    def to_dict(self) -> dict[str, object]:
        """把检查结果转换为字典，供 CLI JSON 输出和报告使用。"""
        return asdict(self)


def run_strict_checks(wiki_dir: str | Path, *, fix: bool = False) -> tuple[CheckResult, ...]:
    """对 Wiki 目录运行严格结构检查和证据检查。

    严格模式会把未复核事实视为错误。这是有意设计的：演示可以展示候选事实
    和 NEEDS_REVIEW 内容，但生产生成和评估不能静默依赖没有通过来源规则和
    证据规则的信息。
    """
    root = Path(wiki_dir)
    checks: list[CheckResult] = []
    for relpath in ROOT_MARKDOWN_FILES:
        if not (root / relpath).is_file():
            checks.append(CheckResult("missing_root_file", "error", f"Missing root file: {relpath}", relpath, fixable=relpath == "log.md"))
    for relpath in REQUIRED_DIRECTORIES:
        path = root / relpath
        if not path.is_dir():
            checks.append(CheckResult("missing_directory", "error", f"Missing directory: {relpath}", relpath, fixable=True))
            if fix:
                path.mkdir(parents=True, exist_ok=True)
    for relpath in REQUIRED_EXPORTS:
        path = root / "exports" / relpath
        if not path.is_file():
            checks.append(CheckResult("missing_export", "warning", f"Missing export file: exports/{relpath}", f"exports/{relpath}"))

    kb = load_llm_wiki(root)
    for fact in kb.facts:
        fact_id = str(fact.get("fact_id") or "<unknown>")
        status = str(fact.get("evidence_status") or "").strip()
        if not status:
            checks.append(CheckResult("fact_missing_evidence_status", "error", f"Fact has no evidence_status: {fact_id}"))
        elif status in {"NEEDS_REVIEW", "UNVERIFIED"}:
            checks.append(CheckResult("fact_unverified_in_strict_mode", "error", f"Strict mode blocks {status} fact: {fact_id}"))

    source_page_ids = {_source_id_from_stem(path.stem) for path in (root / "wiki" / "sources").glob("*.md")}
    for fact in kb.facts:
        source_id = str(fact.get("evidence_source_id") or "").strip()
        if source_id and source_page_ids and source_id not in source_page_ids:
            checks.append(CheckResult("fact_source_not_found", "warning", f"Fact source not found: {source_id}"))

    checks.extend(_cache_checks(root, fix=fix))
    return tuple(checks)


def source_signal_coverage(wiki_dir: str | Path) -> dict[str, object]:
    """统计事实和页面是否携带可用的来源信号。

    这个报告回答一个关键审计问题：重要知识是否能追溯到 source page？
    它本身不能证明临床结论一定正确，但能暴露缺少来源、来源无效、来源无法
    解析等问题，这些问题会阻碍可信的自动维护。
    """
    root = Path(wiki_dir)
    kb = load_llm_wiki(root)
    source_ids = {_source_id_from_stem(path.stem) for path in (root / "wiki" / "sources").glob("*.md")}
    facts_with_source = [fact for fact in kb.facts if str(fact.get("evidence_source_id") or "").strip()]
    unresolved = [
        str(fact.get("evidence_source_id"))
        for fact in facts_with_source
        if str(fact.get("evidence_source_id")) not in source_ids
    ]
    page_summary = _page_source_signal_summary(root)
    return {
        "wiki_dir": str(root),
        "source_page_count": len(source_ids),
        "fact_count": len(kb.facts),
        "facts_with_source_count": len(facts_with_source),
        "unresolved_source_count": len(unresolved),
        "unresolved_source_ids": sorted(set(unresolved)),
        "page_source_signal_summary": page_summary["summary"],
        "page_source_signal_pages": page_summary["pages"],
    }


def _cache_checks(root: Path, *, fix: bool) -> tuple[CheckResult, ...]:
    """校验 ``.wiki-cache.json``，并在允许时清理过期缓存项。"""
    cache = read_cache(root)
    entries = dict(cache.get("entries") or {})
    checks: list[CheckResult] = []
    if not isinstance(entries, dict):
        return (CheckResult("cache_entries_invalid", "error", "Cache entries must be an object.", ".wiki-cache.json"),)
    kept = dict(entries)
    for key, entry in entries.items():
        if not isinstance(entry, dict):
            checks.append(CheckResult("cache_entry_invalid", "error", f"Invalid cache entry: {key}", ".wiki-cache.json", fixable=True))
            kept.pop(key, None)
            continue
        for field in ("source_path", "source_page"):
            relpath = str(entry.get(field) or "")
            if relpath and not (root / relpath).exists():
                checks.append(CheckResult("cache_target_missing", "warning", f"Cache {field} missing: {relpath}", relpath, fixable=True))
                if fix:
                    kept.pop(key, None)
    if fix and kept != entries:
        cache["entries"] = kept
        write_cache(root, cache)
    return tuple(checks)


def json_loadable_exports(wiki_dir: str | Path) -> tuple[CheckResult, ...]:
    """确保 exports 下的 JSON 文件在图谱和运行时使用前可以被解析。"""
    root = Path(wiki_dir)
    checks: list[CheckResult] = []
    for path in (root / "exports").glob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            checks.append(CheckResult("export_json_invalid", "error", str(exc), path.relative_to(root).as_posix()))
    return tuple(checks)


def _source_id_from_stem(stem: str) -> str:
    """从来源 Markdown 文件名中提取稳定的 source ID 前缀。"""
    match = re.match(r"^(SRC-\d+)", stem)
    return match.group(1) if match else stem


def _page_source_signal_summary(root: Path) -> dict[str, object]:
    """按来源元数据是否可用来分类 Wiki 页面。

    派生页面和操作页面不要求拥有权威来源；但疾病、药品、规则、主题等领域
    页面应该在 frontmatter 中声明 ``sources``，或者在正文中显式引用来源。
    """
    applicable_sections = {"diseases", "drugs", "rules", "rule_cards", "topics", "syndromes", "comparisons", "synthesis"}
    pages: list[dict[str, object]] = []
    summary = {
        "applicable_total": 0,
        "ok": 0,
        "missing_sources": 0,
        "empty_sources": 0,
        "invalid_sources": 0,
        "not_applicable": 0,
    }
    for path in (root / "wiki").rglob("*.md"):
        section = path.parent.name
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        frontmatter = _frontmatter_mapping(text)
        sources = frontmatter.get("sources")
        has_inline_source = bool(re.search(r"\bSRC-\d+\b|\.\./sources/|wiki/sources/", text))
        if section not in applicable_sections or str(frontmatter.get("derived") or "").lower() == "true":
            reason = "not_applicable"
        elif "sources" not in frontmatter:
            reason = "ok" if has_inline_source else "missing_sources"
        elif isinstance(sources, list) and sources:
            reason = "ok"
        elif isinstance(sources, str) and sources.strip() and sources.strip() != "[]":
            reason = "ok"
        elif sources in ([], "", None, "[]"):
            reason = "ok" if has_inline_source else "empty_sources"
        else:
            reason = "invalid_sources"
        summary[reason] += 1
        if reason != "not_applicable":
            summary["applicable_total"] += 1
        pages.append(
            {
                "path": path.relative_to(root).as_posix(),
                "page_type": section,
                "eligible": reason == "ok",
                "reason": reason,
            }
        )
    return {"summary": summary, "pages": pages}


def _frontmatter_mapping(text: str) -> dict[str, object]:
    """解析 Wiki 页面使用的简化 frontmatter。

    这里没有使用完整 YAML 解析器，因为 lint 只需要简单的标量和行内列表，
    用于判断页面是否携带来源信号。
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data: dict[str, object] = {}
    for raw_line in text[3:end].splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value == "[]":
            parsed: object = []
        elif value.startswith("[") and value.endswith("]"):
            parsed = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
        else:
            parsed = value
        data[key.strip()] = parsed
    return data
