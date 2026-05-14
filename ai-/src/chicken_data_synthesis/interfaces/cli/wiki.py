from __future__ import annotations
"""鸡病 LLM Wiki 的命令行维护入口。

这个模块是演示、脚本和人工维护时使用的操作入口。它暴露 status、lint、
schema-check、ingest、authority-discover、query、delete-source、graph-build
等安全命令。

安全模型：
    摄取来源或发现权威来源的命令只会写入 raw/source/candidate 三层。
    它们不会把 LLM 发现的信息直接提升为正式权威事实。
"""

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Sequence

from chicken_data_synthesis.infrastructure.config import load_config
from chicken_data_synthesis.infrastructure.knowledge import (
    build_runtime_context,
    build_status_report,
    batch_ingest_sources,
    check_adapter,
    check_cache,
    coverage_report,
    crystallize_session,
    delete_source,
    digest_wiki,
    discover_authority_sources,
    ingest_source,
    ingest_text_source,
    ingest_url_source,
    inspect_compat,
    init_wiki,
    lint_wiki,
    list_sources,
    match_source,
    query_wiki,
    rebuild_graph,
    resolve_llm_wiki_dir,
    review_candidate_facts,
    run_daily_maintenance,
    save_query_result,
    schema_check,
    source_create,
    update_cache,
    validate_step1_analysis,
    watch_graph,
)
from chicken_data_synthesis.paths import PROJECT_ROOT


def main(argv: Sequence[str] | None = None) -> int:
    """解析 CLI 参数，解析 Wiki 目录，并执行对应维护命令。

    所有子命令都在这里注册，因此文档中的演示命令可以直接回溯到本函数。
    """
    parser = argparse.ArgumentParser(description="LLM Wiki maintenance tools.")
    parser.add_argument("--wiki-dir", default="", help="Override LLM Wiki directory.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Print LLM Wiki package status.")
    init_parser = subparsers.add_parser("init", help="Create or refresh a standard Wiki package.")
    init_parser.add_argument("--domain", default="chicken_disease")
    init_parser.add_argument("--force-template-sync", action="store_true")

    lint_parser = subparsers.add_parser("lint", help="Run LLM Wiki health checks.")
    lint_parser.add_argument("--strict", action="store_true")
    lint_parser.add_argument("--fix", action="store_true")

    subparsers.add_parser("coverage", help="Print source signal coverage.")
    subparsers.add_parser("context", help="Print runtime SessionStart-style context.")
    subparsers.add_parser("graph-build", help="Rebuild graph-data.json and knowledge-graph.html.")
    schema_parser = subparsers.add_parser("schema-check", help="Validate the LLM Wiki operations schema.")
    schema_parser.add_argument("--schema-file", default="", help="Override schema YAML path.")

    source_parser = subparsers.add_parser("source", help="Source registry tools.")
    source_subparsers = source_parser.add_subparsers(dest="source_command", required=True)
    source_subparsers.add_parser("list", help="List source types.")
    source_match_parser = source_subparsers.add_parser("match", help="Match an input path or URL to a source type.")
    source_match_parser.add_argument("--input", required=True)

    adapter_parser = subparsers.add_parser("adapter", help="Adapter status tools.")
    adapter_subparsers = adapter_parser.add_subparsers(dest="adapter_command", required=True)
    adapter_check_parser = adapter_subparsers.add_parser("check", help="Check source adapter status.")
    adapter_check_parser.add_argument("--source-id", required=True)

    cache_parser = subparsers.add_parser("cache", help="Cache tools.")
    cache_subparsers = cache_parser.add_subparsers(dest="cache_command", required=True)
    cache_check_parser = cache_subparsers.add_parser("check")
    cache_check_parser.add_argument("raw_file")
    cache_update_parser = cache_subparsers.add_parser("update")
    cache_update_parser.add_argument("raw_file")
    cache_update_parser.add_argument("source_page")
    cache_update_parser.add_argument("--reason", required=True, help="Auditable reason for changing cache mapping.")
    cache_update_parser.add_argument("--evidence", required=True, help="Traceable evidence for changing cache mapping.")

    source_create_parser = subparsers.add_parser("source-create", help="Create a source page for a raw file.")
    source_create_parser.add_argument("raw_file")
    source_create_parser.add_argument("--title", default="")
    source_create_parser.add_argument("--summary", default="")
    source_create_parser.add_argument("--reason", required=True, help="Auditable reason for registering this source.")
    source_create_parser.add_argument("--evidence", required=True, help="Evidence URL, review note, or issue id for this source registration.")

    ingest_parser = subparsers.add_parser("ingest", help="Ingest a local file into raw/source/candidates.")
    ingest_parser.add_argument("input")
    ingest_parser.add_argument("--title", default="")
    ingest_parser.add_argument("--summary", default="")
    ingest_parser.add_argument("--reason", required=True, help="Auditable reason for adding this source.")
    ingest_parser.add_argument("--evidence", required=True, help="Evidence URL, issue id, review note, or protocol reference.")

    ingest_url_parser = subparsers.add_parser("ingest-url", help="Create a manual source record for a URL.")
    ingest_url_parser.add_argument("url")
    ingest_url_parser.add_argument("--title", default="")
    ingest_url_parser.add_argument("--summary", default="")
    ingest_url_parser.add_argument("--reason", required=True, help="Auditable reason for adding this URL source.")
    ingest_url_parser.add_argument("--evidence", default="", help="Evidence URL, issue id, review note, or protocol reference. Defaults to the URL.")

    ingest_text_parser = subparsers.add_parser("ingest-text", help="Ingest pasted plain text as a source.")
    ingest_text_parser.add_argument("text")
    ingest_text_parser.add_argument("--title", default="pasted-text")
    ingest_text_parser.add_argument("--summary", default="")
    ingest_text_parser.add_argument("--reason", required=True, help="Auditable reason for adding pasted text.")
    ingest_text_parser.add_argument("--evidence", required=True, help="Traceable evidence for pasted text provenance.")

    authority_parser = subparsers.add_parser(
        "authority-discover",
        help="Accept LLM-proposed authority URLs after allowlist validation and write source candidates.",
    )
    authority_parser.add_argument("query", help="Knowledge gap or topic used for LLM authority discovery.")
    authority_parser.add_argument("--url", action="append", default=[], help="Candidate authority URL. Can be repeated.")
    authority_parser.add_argument("--llm-suggestions-json", default="", help="Raw JSON array/object produced by the LLM.")
    authority_parser.add_argument("--llm-suggestions-file", default="", help="Path to a JSON file produced by the LLM.")
    authority_parser.add_argument("--fetch", action="store_true", help="Fetch accepted URL content into raw/html or raw/pdfs.")
    authority_parser.add_argument("--timeout", type=int, default=20, help="Fetch timeout in seconds.")

    batch_parser = subparsers.add_parser("batch-ingest", help="Ingest supported files from a folder.")
    batch_parser.add_argument("input_dir")
    batch_parser.add_argument("--recursive", action="store_true")
    batch_parser.add_argument("--reason", required=True, help="Auditable reason for batch ingestion.")
    batch_parser.add_argument("--evidence", required=True, help="Evidence, protocol, issue id, or review note for batch ingestion.")

    digest_parser = subparsers.add_parser("digest", help="Build a derived synthesis from Wiki search results.")
    digest_parser.add_argument("query")
    digest_parser.add_argument("--format", choices=("quick", "report", "comparison"), default="quick")
    digest_parser.add_argument("--save", action="store_true")

    crystallize_parser = subparsers.add_parser("crystallize", help="Save a derived session crystallization.")
    crystallize_parser.add_argument("topic")
    crystallize_parser.add_argument("--notes", default="")

    watch_parser = subparsers.add_parser("graph-watch", help="Watch Wiki files and rebuild the graph on change.")
    watch_parser.add_argument("--interval", type=float, default=2.0)
    watch_parser.add_argument("--once", action="store_true", help="Run one rebuild and exit.")

    query_parser = subparsers.add_parser("query", help="Retrieve relevant Wiki context for a query.")
    query_parser.add_argument("query")
    query_parser.add_argument("--top-k", type=int, default=5)

    save_parser = subparsers.add_parser("query-save", help="Save a query answer as a derived Wiki page.")
    save_parser.add_argument("query")
    save_parser.add_argument("answer")
    save_parser.add_argument("--top-k", type=int, default=5)

    delete_parser = subparsers.add_parser("delete-source", help="Delete or preview deleting a raw/source pair.")
    delete_parser.add_argument("--raw-file", default="")
    delete_parser.add_argument("--source-page", default="")
    delete_parser.add_argument("--reason", default="", help="Required with --apply. Auditable deletion reason.")
    delete_parser.add_argument("--evidence", default="", help="Optional evidence URL, issue id, or review note for deletion.")
    delete_parser.add_argument("--replacement-source", default="", help="Optional replacement source page or raw file path.")
    delete_parser.add_argument("--apply", action="store_true", help="Actually delete files and invalidate cache.")

    subparsers.add_parser("review-candidates", help="Run layered automatic review for candidate facts.")

    compat_parser = subparsers.add_parser("compat", help="Inspect or validate Wiki compatibility.")
    compat_subparsers = compat_parser.add_subparsers(dest="compat_command", required=True)
    compat_subparsers.add_parser("inspect")
    compat_subparsers.add_parser("validate")
    compat_ensure = compat_subparsers.add_parser("ensure-source-dir")
    compat_ensure.add_argument("source_id")

    validate_parser = subparsers.add_parser("step1-validate", help="Validate Step1 entity/topic/connection JSON.")
    validate_parser.add_argument("json_file")

    daily_parser = subparsers.add_parser(
        "daily-maintain",
        help="Run one scheduled LLM Wiki maintenance cycle with the Nonelinear model.",
    )
    daily_parser.add_argument("--base-url", default="https://api.nonelinear.com/v1")
    daily_parser.add_argument("--model", default="gpt-5.4-mini-medium")
    daily_parser.add_argument("--query", action="append", default=[], help="Maintenance knowledge query. Can be repeated.")
    daily_parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Only record accepted URLs without fetching raw/html or raw/pdfs. Weekly maintenance fetches by default.",
    )
    daily_parser.add_argument("--max-sources", type=int, default=5)
    daily_parser.add_argument(
        "--max-queries",
        type=int,
        default=8,
        help="Maximum dynamically generated maintenance queries when --query is not provided.",
    )
    daily_parser.add_argument("--timeout", type=int, default=60)
    daily_parser.add_argument(
        "--protocol-file",
        default="",
        help="Maintenance protocol or deep gap review file used to prioritize missing content.",
    )
    daily_parser.add_argument(
        "--no-gap-first",
        action="store_true",
        help="Disable readiness/gap-review-first query generation.",
    )

    args = parser.parse_args(argv)
    config = load_config(PROJECT_ROOT, include_local=True)
    wiki_dir = Path(args.wiki_dir).resolve() if args.wiki_dir else resolve_llm_wiki_dir(config, PROJECT_ROOT)

    if args.command == "status":
        report = build_status_report(wiki_dir)
        _print_payload(asdict(report), json_mode=args.json)
        return 0

    if args.command == "init":
        report = init_wiki(wiki_dir, domain=args.domain, force_template_sync=args.force_template_sync)
        _print_payload(asdict(report), json_mode=args.json)
        return 0

    if args.command == "lint":
        report = lint_wiki(wiki_dir, strict=args.strict, fix=args.fix)
        _print_payload(asdict(report), json_mode=args.json)
        return 0 if report.ok else 1

    if args.command == "coverage":
        _print_payload(coverage_report(wiki_dir), json_mode=args.json)
        return 0

    if args.command == "schema-check":
        report = schema_check(wiki_dir, schema_path=args.schema_file or None)
        _print_payload(asdict(report), json_mode=args.json)
        return 0 if report.ok else 1

    if args.command == "context":
        context = build_runtime_context(wiki_dir)
        if args.json:
            _print_payload({"context": context}, json_mode=True)
        else:
            print(context)
        return 0

    if args.command == "query":
        payload = query_wiki(args.query, wiki_dir=wiki_dir, top_k=args.top_k)
        _print_payload(payload, json_mode=args.json)
        return 0

    if args.command == "source":
        if args.source_command == "list":
            _print_payload({"sources": list_sources()}, json_mode=args.json)
            return 0
        if args.source_command == "match":
            _print_payload(match_source(args.input), json_mode=args.json)
            return 0

    if args.command == "adapter":
        if args.adapter_command == "check":
            _print_payload(check_adapter(args.source_id), json_mode=args.json)
            return 0

    if args.command == "cache":
        if args.cache_command == "check":
            _print_payload(check_cache(wiki_dir, args.raw_file), json_mode=args.json)
            return 0
        if args.cache_command == "update":
            _print_payload(update_cache(wiki_dir, args.raw_file, args.source_page, reason=args.reason, evidence=args.evidence), json_mode=args.json)
            return 0

    if args.command == "source-create":
        path = source_create(wiki_dir, args.raw_file, title=args.title, summary=args.summary, reason=args.reason, evidence=args.evidence)
        _print_payload({"source_page": str(path)}, json_mode=args.json)
        return 0

    if args.command == "ingest":
        report = ingest_source(wiki_dir, args.input, title=args.title, summary=args.summary, reason=args.reason, evidence=args.evidence)
        _print_payload(asdict(report), json_mode=args.json)
        return 0

    if args.command == "ingest-url":
        report = ingest_url_source(wiki_dir, args.url, title=args.title, summary=args.summary, reason=args.reason, evidence=args.evidence)
        _print_payload(asdict(report), json_mode=args.json)
        return 0

    if args.command == "ingest-text":
        report = ingest_text_source(wiki_dir, args.text, title=args.title, summary=args.summary, reason=args.reason, evidence=args.evidence)
        _print_payload(asdict(report), json_mode=args.json)
        return 0

    if args.command == "authority-discover":
        suggestions = args.llm_suggestions_json
        if args.llm_suggestions_file:
            suggestions = Path(args.llm_suggestions_file).read_text(encoding="utf-8-sig")
        report = discover_authority_sources(
            wiki_dir,
            args.query,
            candidate_urls=tuple(args.url or ()),
            llm_suggestions_json=suggestions,
            fetch=args.fetch,
            timeout_seconds=args.timeout,
        )
        _print_payload(asdict(report), json_mode=args.json)
        return 0 if report.accepted_count or not report.rejected_count else 1

    if args.command == "batch-ingest":
        report = batch_ingest_sources(wiki_dir, args.input_dir, recursive=args.recursive, reason=args.reason, evidence=args.evidence)
        _print_payload(asdict(report), json_mode=args.json)
        return 0 if not report.warnings else 1

    if args.command == "digest":
        result = digest_wiki(wiki_dir, args.query, output_format=args.format, save=args.save)
        _print_payload(asdict(result) if hasattr(result, "__dataclass_fields__") else result, json_mode=args.json)
        return 0

    if args.command == "crystallize":
        result = crystallize_session(wiki_dir, args.topic, notes=args.notes)
        _print_payload(asdict(result), json_mode=args.json)
        return 0

    if args.command == "graph-build":
        report = rebuild_graph(wiki_dir)
        _print_payload(asdict(report), json_mode=args.json)
        return 0

    if args.command == "graph-watch":
        report = watch_graph(wiki_dir, interval_seconds=args.interval, once=args.once)
        _print_payload(asdict(report), json_mode=args.json)
        return 0

    if args.command == "query-save":
        payload = query_wiki(args.query, wiki_dir=wiki_dir, top_k=args.top_k)
        path = save_query_result(
            args.query,
            args.answer,
            wiki_dir=wiki_dir,
            source_hits=(),
        )
        payload["saved_path"] = str(path)
        _print_payload(payload, json_mode=args.json)
        return 0

    if args.command == "delete-source":
        report = delete_source(
            wiki_dir,
            raw_file=args.raw_file,
            source_page=args.source_page,
            reason=args.reason,
            evidence=args.evidence,
            replacement_source=args.replacement_source,
            dry_run=not args.apply,
        )
        _print_payload(asdict(report), json_mode=args.json)
        return 0

    if args.command == "review-candidates":
        report = review_candidate_facts(wiki_dir)
        _print_payload(asdict(report), json_mode=args.json)
        return 0

    if args.command == "compat":
        if args.compat_command in {"inspect", "validate"}:
            report = inspect_compat(wiki_dir)
            _print_payload(asdict(report), json_mode=args.json)
            return 0 if report.ok else 1
        if args.compat_command == "ensure-source-dir":
            report = inspect_compat(wiki_dir, ensure_source_id=args.source_id)
            _print_payload(asdict(report), json_mode=args.json)
            return 0 if report.ok else 1

    if args.command == "step1-validate":
        raw = Path(args.json_file).read_text(encoding="utf-8-sig")
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise TypeError("Step1 JSON must be an object.")
        ok, errors, warnings = validate_step1_analysis(payload)
        _print_payload({"ok": ok, "errors": errors, "warnings": warnings}, json_mode=args.json)
        return 0 if ok else 1

    if args.command == "daily-maintain":
        report = run_daily_maintenance(
            wiki_dir,
            base_url=args.base_url,
            model=args.model,
            queries=tuple(args.query or ()),
            query_limit=args.max_queries,
            fetch=not args.no_fetch,
            max_sources_per_query=args.max_sources,
            timeout_seconds=args.timeout,
            protocol_path=args.protocol_file or None,
            gap_first=not args.no_gap_first,
        )
        _print_payload(asdict(report), json_mode=args.json)
        return 0 if report.schema_ok and report.lint_ok else 1

    return 2


def _print_payload(payload: Any, *, json_mode: bool) -> None:
    """根据输出模式打印结果。

    ``json_mode=True`` 时输出机器可读 JSON；否则输出更适合人工阅读的
    key/value 文本。
    """
    if json_mode:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if isinstance(payload, dict):
        for key, value in payload.items():
            print(f"{key}: {value}")
        return
    print(payload)


__all__ = ["main"]
