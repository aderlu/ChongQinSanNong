from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from chicken_data_synthesis.infrastructure.knowledge import (
    build_llm_wiki_context,
    build_maintenance_queries,
    build_runtime_context,
    build_status_report,
    check_adapter,
    check_cache,
    coverage_report,
    batch_ingest_sources,
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
    load_llm_wiki,
    match_source,
    NonelinearAuthorityClient,
    query_wiki,
    rebuild_graph,
    review_candidate_facts,
    run_daily_maintenance,
    save_query_result,
    schema_check,
    source_create,
    validate_step1_analysis,
)
from chicken_data_synthesis.infrastructure.knowledge import authority as authority_module
from chicken_data_synthesis.infrastructure.knowledge import maintenance as maintenance_module
from chicken_data_synthesis.application.services import apply_final_quality_gates
from chicken_data_synthesis.infrastructure.persistence.csv_artifacts import build_final_result_row
from chicken_data_synthesis.infrastructure.prompts import build_blind_completion_messages
from chicken_data_synthesis.application.services.task_planning import build_case_tasks
from deepeval_integration.evaluator import _build_deepeval_wiki_context, _build_test_case
from llm_foundation.tools import rule_base_check_tool


def _write_wiki_fixture(root: Path) -> Path:
    wiki_root = root / "llm_wiki"
    (wiki_root / "wiki" / "diseases").mkdir(parents=True)
    (wiki_root / "wiki" / "drugs").mkdir(parents=True)
    (wiki_root / "wiki" / "rules").mkdir(parents=True)
    (wiki_root / "exports").mkdir(parents=True)
    (wiki_root / "index.md").write_text("# Index\n", encoding="utf-8")
    (wiki_root / ".wiki-schema.md").write_text("# Wiki Schema\n", encoding="utf-8")
    (wiki_root / "purpose.md").write_text("# Purpose\n", encoding="utf-8")
    (wiki_root / "wiki" / "diseases" / "DIS-001-test.md").write_text(
        "# 新城疫\n\n呼吸道症状、神经症状、产蛋下降，需与禽流感鉴别。",
        encoding="utf-8",
    )
    (wiki_root / "wiki" / "rules" / "banned.md").write_text(
        "# 禁用药规则\n\n产蛋鸡不得使用氯霉素。",
        encoding="utf-8",
    )
    (wiki_root / "wiki" / "drugs" / "chloramphenicol.md").write_text(
        "# 氯霉素\n\n禁用药，不得用于产蛋鸡。",
        encoding="utf-8",
    )
    (wiki_root / "exports" / "knowledge_facts.json").write_text(
        json.dumps(
            [
                {
                    "subject": "氯霉素",
                    "predicate": "regulatory_status",
                    "object": "禁用药",
                    "evidence_source_id": "SRC-001",
                    "evidence_status": "EXTRACTED",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (wiki_root / "exports" / "disease_index.csv").write_text(
        "disease_id,disease_name,page_relpath\nDIS-001,新城疫,wiki/diseases/DIS-001-test.md\n",
        encoding="utf-8",
    )
    (wiki_root / "exports" / "rule_index.csv").write_text(
        "title,page_relpath,source_count\n禁用药规则,wiki/rules/banned.md,1\n",
        encoding="utf-8",
    )
    (wiki_root / "exports" / "drug_page_index.csv").write_text(
        "title,page_relpath\n氯霉素,wiki/drugs/chloramphenicol.md\n",
        encoding="utf-8",
    )
    return wiki_root


def test_llm_wiki_loads_pages_indexes_and_facts(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)

    kb = load_llm_wiki(wiki_root)

    assert "新城疫" in kb.disease_names()
    assert kb.search("新城疫 呼吸道", top_k=1)[0].title == "新城疫"
    assert kb.search_facts("氯霉素 禁用", top_k=1)[0]["subject"] == "氯霉素"


def test_llm_wiki_context_is_prompt_ready(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)

    context = build_llm_wiki_context("产蛋鸡 新城疫 氯霉素", wiki_dir=wiki_root)

    assert "LLM Wiki 知识上下文" in context
    assert "新城疫" in context
    assert "氯霉素" in context


def test_rule_base_attaches_wiki_risk_context(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)
    result = rule_base_check_tool(
        {
            "species": "鸡",
            "user_query": "产蛋鸡出现呼吸道症状和产蛋下降",
            "diagnosis": "疑似新城疫",
            "prescription": "氯霉素饮水",
            "withdrawal_period": "无",
            "metadata": {"disease_name": "新城疫", "severity": "high", "scene_tags": ["产蛋鸡"]},
        },
        {
            "enabled": True,
            "llm_wiki_dir": str(wiki_root),
            "required_case_fields": ["species", "user_query", "diagnosis", "prescription", "withdrawal_period"],
            "required_metadata_keys": ["disease_name", "severity", "scene_tags"],
            "fatal_block_codes": ["banned_drug", "banned_drug_wiki_evidence"],
            "banned_drug_keywords": [],
            "laying_hen_keywords": ["产蛋鸡"],
            "egg_withdrawal_keywords": ["弃蛋"],
            "antibiotic_keywords": ["氯霉素"],
        },
    )

    assert "llm_wiki_context" in result
    assert "banned_drug_wiki_evidence" in result["codes"]
    assert result["hard_block"] is True


def test_rule_base_does_not_flag_zero_day_supplement_when_antibiotic_withdrawal_is_positive(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)
    result = rule_base_check_tool(
        {
            "species": "鸡",
            "user_query": "肉鸡跛行，关节肿胀，站立不稳。",
            "diagnosis": "主要诊断：病毒性关节炎。",
            "prescription": "阿莫西林可溶性粉防继发感染，配合电解多维。",
            "withdrawal_period": "阿莫西林休药期7天；电解多维休药期0天。整体按7天执行。",
            "metadata": {"disease_name": "病毒性关节炎", "severity": "medium", "scene_tags": ["肉鸡"]},
        },
        {
            "enabled": True,
            "llm_wiki_dir": str(wiki_root),
            "required_case_fields": ["species", "user_query", "diagnosis", "prescription", "withdrawal_period"],
            "required_metadata_keys": ["disease_name", "severity", "scene_tags"],
            "fatal_block_codes": ["banned_drug"],
            "banned_drug_keywords": [],
            "laying_hen_keywords": ["产蛋鸡"],
            "egg_withdrawal_keywords": ["弃蛋"],
            "antibiotic_keywords": ["阿莫西林"],
        },
    )

    assert "withdrawal_conflict" not in result["codes"]
    assert "weak_evidence" not in result["codes"]


def test_production_tasks_use_default_judges_not_pilot_judge_candidates() -> None:
    defaults = {
        "generator": {"name": "default-generator"},
        "judge_a": {"name": "default-a"},
        "judge_b": {"name": "default-b"},
        "arbiter": {"name": "default-arbiter"},
    }
    candidates = {
        "pilot_a": {"name": "pilot-a"},
        "pilot_b": {"name": "pilot-b"},
        "pilot_arbiter": {"name": "pilot-arbiter"},
    }

    task = build_case_tasks(
        mode="production",
        start_index=0,
        sample_count=1,
        evaluation_mode="legacy",
        diseases=["新城疫"],
        pilot_config={"primary_judges": ["pilot_a", "pilot_b"], "arbiter": "pilot_arbiter"},
        candidate_models=candidates,
        default_models=defaults,
    )[0]

    assert task[4]["name"] == "default-a"
    assert task[5]["name"] == "default-b"
    assert task[6]["name"] == "default-arbiter"


def test_llm_wiki_status_lint_query_and_runtime_context(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)

    status = build_status_report(wiki_root)
    lint = lint_wiki(wiki_root)
    query = query_wiki("新城疫 产蛋下降", wiki_dir=wiki_root)
    runtime_context = build_runtime_context(wiki_root)

    assert status.disease_count == 1
    assert status.fact_count == 1
    assert lint.ok is True
    assert query["hits"]
    assert "fact_hits" in query
    assert query["wiki_dir"] == str(wiki_root)
    assert "鸡病 LLM Wiki 运行时上下文" in runtime_context


def test_save_query_result_writes_derived_page_and_log(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)

    path = save_query_result("新城疫如何鉴别", "需结合呼吸道、神经症状与实验室检测。", wiki_dir=wiki_root)

    assert path.is_file()
    assert "新城疫如何鉴别" in path.read_text(encoding="utf-8")
    assert "query | 新城疫如何鉴别" in (wiki_root / "log.md").read_text(encoding="utf-8")


def test_validate_step1_analysis_requires_confidence() -> None:
    ok, errors, warnings = validate_step1_analysis(
        {
            "entities": [{"name": "新城疫", "confidence": "EXTRACTED"}],
            "topics": [],
            "connections": [{"from": "新城疫", "to": "呼吸道症状"}],
        }
    )

    assert ok is False
    assert "connection_missing_confidence:0" in errors
    assert "entity_missing_evidence:新城疫" in warnings


def test_graph_rebuild_reflects_wiki_data_changes(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)

    first = rebuild_graph(wiki_root)
    first_data = json.loads(Path(first.graph_data_path).read_text(encoding="utf-8"))
    assert "```mermaid" in Path(first.mermaid_path).read_text(encoding="utf-8")
    assert any(node["label"] == "新城疫" for node in first_data["nodes"])
    assert first_data["metadata"]["facts_in_graph"] == first_data["metadata"]["facts"]
    assert any(link["type"] == "regulatory_status" for link in first_data["links"])
    assert "Chicken Disease LLM Wiki Graph" in Path(first.html_path).read_text(encoding="utf-8")

    disease_index = wiki_root / "exports" / "disease_index.csv"
    disease_index.write_text(
        disease_index.read_text(encoding="utf-8")
        + "DIS-999,演示病,wiki/diseases/DIS-999-demo.md\n",
        encoding="utf-8",
    )
    (wiki_root / "wiki" / "diseases" / "DIS-999-demo.md").write_text("# 演示病\n\n用于图谱同步测试。", encoding="utf-8")

    second = rebuild_graph(wiki_root)
    second_data = json.loads(Path(second.graph_data_path).read_text(encoding="utf-8"))
    second_html = Path(second.html_path).read_text(encoding="utf-8")

    assert second.node_count == first.node_count + 1
    assert any(node["label"] == "演示病" for node in second_data["nodes"])
    assert "演示病" in second_html


def test_graph_includes_unmatched_facts_sources_and_candidate_layer(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)
    (wiki_root / "wiki" / "sources").mkdir(parents=True, exist_ok=True)
    (wiki_root / "wiki" / "sources" / "SRC-0999-extra.md").write_text(
        "---\ntype: source\nsource_id: SRC-0999\nsource_path: raw/notes/extra.txt\nsource_type: text\nauthority_level: official\nevidence_status: EXTRACTED\ncreated: 2026-05-04\nupdated: 2026-05-04\nsources: []\n---\n\n# Extra authority source\n",
        encoding="utf-8",
    )
    facts_path = wiki_root / "exports" / "knowledge_facts.json"
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    facts.append(
        {
            "fact_id": "SYM-001",
            "subject": "产蛋下降",
            "predicate": "differential_diagnosis",
            "object": "需要结合新城疫、禽流感和管理因素复核",
            "evidence_source_id": "SRC-0999",
            "evidence_status": "EXTRACTED",
        }
    )
    facts_path.write_text(json.dumps(facts, ensure_ascii=False), encoding="utf-8")
    (wiki_root / "exports" / "knowledge_facts.candidates.json").write_text(
        json.dumps(
            [
                {
                    "fact_id": "CAND-0001",
                    "subject": "候选来源",
                    "predicate": "source_imported",
                    "object": "pending_review",
                    "evidence_source_id": "SRC-0999",
                    "evidence_status": "NEEDS_REVIEW",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    report = rebuild_graph(wiki_root)
    data = json.loads(Path(report.graph_data_path).read_text(encoding="utf-8"))

    assert data["metadata"]["facts_in_graph"] == data["metadata"]["facts"]
    assert data["metadata"]["candidate_facts_in_graph"] == 1
    assert any(node["id"] == "SRC-0999" for node in data["nodes"])
    assert any(node["group"] == "concept" and node["label"] == "产蛋下降" for node in data["nodes"])
    assert any(node["group"] == "candidate" for node in data["nodes"])


def test_query_excludes_generated_graph_artifacts_and_prefers_domain_pages(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)
    graph_path = wiki_root / "wiki" / "knowledge-graph.md"
    graph_path.write_text(
        "# Chicken Disease LLM Wiki Graph\n\n新城疫 新城疫 新城疫 氯霉素 产蛋下降\n",
        encoding="utf-8",
    )

    result = query_wiki("新城疫 氯霉素", wiki_dir=wiki_root, top_k=3)

    assert all(hit["relpath"] != "wiki/knowledge-graph.md" for hit in result["hits"])
    assert result["hits"][0]["section"] in {"diseases", "drugs", "rules"}


def test_wiki_lifecycle_init_source_cache_ingest_digest_and_coverage(tmp_path: Path) -> None:
    wiki_root = tmp_path / "new_wiki"

    init_report = init_wiki(wiki_root)

    assert (wiki_root / "wiki" / "sources").is_dir()
    assert (wiki_root / ".wiki-cache.json").is_file()
    assert "index.md" in init_report.created_files
    assert match_source("sample.pdf")["source_id"] == "pdf"
    assert any(item["source_id"] == "markdown" for item in list_sources())
    assert check_adapter("markdown")["state"] == "available"

    raw = tmp_path / "material.md"
    raw.write_text("# Newcastle note\n\nRespiratory signs and egg drop.\n", encoding="utf-8")
    source_page = source_create(wiki_root, raw, title="Newcastle note")

    cache_result = check_cache(wiki_root, raw)
    assert cache_result["hit"] is True
    assert source_page.is_file()

    imported = ingest_source(wiki_root, raw, title="Imported note")
    assert Path(imported.source_page).is_file()
    assert Path(imported.candidates_path).is_file()

    url_imported = ingest_url_source(wiki_root, "https://example.com/source", title="Example URL")
    text_imported = ingest_text_source(wiki_root, "Short pasted note.", title="Pasted")
    assert url_imported.source_type == "url"
    assert text_imported.source_type == "plain_text"

    digest = digest_wiki(wiki_root, "Newcastle", save=True)
    assert Path(digest.saved_path).is_file()
    assert "derived: true" in Path(digest.saved_path).read_text(encoding="utf-8")

    coverage = coverage_report(wiki_root)
    assert coverage["source_page_count"] >= 1
    assert "page_source_signal_summary" in coverage


def test_authority_discovery_accepts_allowlisted_llm_urls_as_candidates_only(tmp_path: Path) -> None:
    wiki_root = tmp_path / "authority_wiki"
    init_wiki(wiki_root)
    suggestions = json.dumps(
        {
            "sources": [
                {
                    "url": "https://www.moa.gov.cn/govpublic/xmsyj/authority-demo.html",
                    "title": "MOA authority demo",
                    "reason": "Official ministry domain for poultry disease policy evidence.",
                    "evidence_role": "official source candidate",
                },
                {
                    "url": "https://example.com/untrusted-demo",
                    "title": "Untrusted demo",
                },
            ]
        },
        ensure_ascii=False,
    )

    report = discover_authority_sources(
        wiki_root,
        "Newcastle disease diagnostic authority source",
        llm_suggestions_json=suggestions,
        fetch=False,
    )

    assert report.accepted_count == 1
    assert report.rejected_count == 1
    assert report.rejected_candidates[0]["reason"] == "domain_not_allowlisted"
    source_page = Path(report.created_sources[0])
    assert source_page.is_file()
    source_text = source_page.read_text(encoding="utf-8")
    assert "external_url: https://www.moa.gov.cn/govpublic/xmsyj/authority-demo.html" in source_text
    assert "authority_level: official" in source_text
    assert Path(report.candidates_path).is_file()
    assert json.loads((wiki_root / "exports" / "knowledge_facts.json").read_text(encoding="utf-8")) == []


def test_daily_maintenance_uses_llm_candidates_without_promoting_facts(tmp_path: Path) -> None:
    wiki_root = tmp_path / "daily_wiki"
    init_wiki(wiki_root)

    class FakeAuthorityClient:
        def suggest_sources(self, query: str, *, max_sources: int = 5) -> str:
            return json.dumps(
                {
                    "sources": [
                        {
                            "url": "https://www.moa.gov.cn/govpublic/xmsyj/daily-demo.html",
                            "title": "Daily MOA demo",
                            "reason": "Official ministry domain.",
                            "evidence_role": "regulation",
                        },
                        {
                            "url": "https://example.com/not-allowed",
                            "title": "Rejected",
                        },
                    ]
                },
                ensure_ascii=False,
            )

    report = run_daily_maintenance(
        wiki_root,
        queries=("demo daily maintenance",),
        client=FakeAuthorityClient(),
        model="gpt-5.4-mini-medium",
        fetch=False,
    )

    assert report.accepted_count == 1
    assert report.rejected_count == 1
    assert report.schema_ok is True
    assert report.lint_ok is True
    assert report.review_report["total_count"] == 1
    assert report.review_report["decision_counts"]["LEGACY_NEEDS_FETCH"] == 1
    assert report.graph_change_report["reason"] == "graph_rebuilt_from_current_wiki_files_after_maintenance"
    assert Path(report.graph_report["graph_data_path"]).is_file()
    assert Path(report.graph_report["html_path"]).is_file()
    candidates = json.loads((wiki_root / "exports" / "knowledge_facts.candidates.json").read_text(encoding="utf-8"))
    assert candidates[0]["evidence_status"] == "NEEDS_REVIEW"
    assert json.loads((wiki_root / "exports" / "knowledge_facts.json").read_text(encoding="utf-8")) == []
    log_text = (wiki_root / "log.md").read_text(encoding="utf-8")
    assert "maintenance-task" in log_text
    assert "accepted=1" in log_text
    assert "rejected=1" in log_text
    assert "graph-diff" in log_text


def test_dynamic_maintenance_queries_cover_wiki_gaps(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)
    (wiki_root / "wiki" / "diseases" / "DIS-002-coccidiosis.md").write_text(
        "# 鸡球虫病\n\n需要补充诊断标准和权威来源。",
        encoding="utf-8",
    )
    (wiki_root / "wiki" / "drugs" / "amprolium.md").write_text(
        "# 氨丙啉\n\n需要补充休药期和监管来源。",
        encoding="utf-8",
    )
    candidates_path = wiki_root / "exports" / "knowledge_facts.candidates.json"
    candidates_path.write_text(
        json.dumps(
            [
                {
                    "fact_id": "CAND-GAP",
                    "subject": "历史候选来源",
                    "review_decision": "LEGACY_NEEDS_FETCH",
                    "evidence_status": "NEEDS_REVIEW",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    queries = build_maintenance_queries(wiki_root, limit=5)

    assert queries[0].startswith("历史候选来源")
    assert any("鸡球虫病" in query and "诊断标准" in query for query in queries)
    assert any("氨丙啉" in query and "休药期" in query for query in queries)


def test_delete_source_requires_auditable_reason_when_applied(tmp_path: Path) -> None:
    wiki_root = tmp_path / "delete_reason_wiki"
    init_wiki(wiki_root)
    raw_path = tmp_path / "obsolete.html"
    raw_path.write_text("<html>obsolete portal page</html>", encoding="utf-8")
    imported = ingest_source(wiki_root, raw_path, title="Obsolete portal")

    try:
        delete_source(wiki_root, source_page=imported.source_page, dry_run=False)
    except ValueError as exc:
        assert "reason is required" in str(exc)
    else:
        raise AssertionError("delete_source should require an auditable reason when dry_run=False")

    report = delete_source(
        wiki_root,
        source_page=imported.source_page,
        reason="source_replaced_by_more_specific_page",
        evidence="review:old page was only a portal and did not contain extractable evidence",
        dry_run=False,
    )

    assert report.reason == "source_replaced_by_more_specific_page"
    assert report.deleted_paths
    log_text = (wiki_root / "log.md").read_text(encoding="utf-8")
    assert "reason=source_replaced_by_more_specific_page" in log_text
    assert "evidence=review:old page was only a portal and did not contain extractable evidence" in log_text


def test_source_create_and_candidate_review_write_audit_basis(tmp_path: Path) -> None:
    wiki_root = tmp_path / "audit_basis_wiki"
    init_wiki(wiki_root)
    raw_dir = wiki_root / "raw" / "html"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_file = raw_dir / "manual.html"
    raw_file.write_text("<html>manual reviewed authority evidence</html>", encoding="utf-8")

    source_page = source_create(
        wiki_root,
        raw_file,
        title="Manual authority",
        reason="manual_authority_review",
        evidence="review-ticket:AUTH-001",
    )
    write_path = wiki_root / "exports" / "knowledge_facts.candidates.json"
    write_path.write_text(
        json.dumps(
            [
                {
                    "fact_id": "CAND-AUDIT",
                    "subject": "Manual authority",
                    "predicate": "source_imported",
                    "object": "pending_review",
                    "source_page": source_page.relative_to(wiki_root).as_posix(),
                    "external_url": "https://www.fao.org/manual-authority",
                    "evidence_role": "general_source",
                    "evidence_excerpt": "manual reviewed authority evidence",
                    "evidence_status": "NEEDS_REVIEW",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    review_candidate_facts(wiki_root)
    log_text = (wiki_root / "log.md").read_text(encoding="utf-8")

    assert "source-create" in log_text
    assert "reason=manual_authority_review" in log_text
    assert "evidence=review-ticket:AUTH-001" in log_text
    assert "candidate-review" in log_text
    assert "reason=layered_program_review" in log_text
    assert "evidence=exports/knowledge_facts.review_report.json" in log_text


def test_authority_discover_fetches_raw_excerpt_and_skips_existing_url(tmp_path: Path, monkeypatch) -> None:
    wiki_root = tmp_path / "fetch_wiki"
    init_wiki(wiki_root)

    class FakeHeaders:
        def get_content_type(self) -> str:
            return "text/html"

        def get_content_charset(self) -> str:
            return "utf-8"

    class FakeResponse:
        headers = FakeHeaders()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback) -> None:
            return None

        def read(self, size: int = -1) -> bytes:
            return (
                "<html><body><h1>Newcastle disease</h1>"
                "<p>Official diagnostic manual evidence excerpt for review.</p>"
                "</body></html>"
            ).encode("utf-8")

    def fake_urlopen(request, timeout):
        return FakeResponse()

    monkeypatch.setattr(authority_module, "urlopen", fake_urlopen)

    suggestions = json.dumps(
        {
            "sources": [
                {
                    "url": "https://www.woah.org/en/disease/newcastle-disease/",
                    "title": "WOAH Newcastle disease",
                    "evidence_role": "diagnosis_standard",
                },
                {
                    "url": "https://www.woah.org/",
                    "title": "WOAH home",
                    "evidence_role": "clinical_reference",
                },
            ]
        },
        ensure_ascii=False,
    )

    first = discover_authority_sources(wiki_root, "newcastle authority data", llm_suggestions_json=suggestions, fetch=True)
    assert first.accepted_count == 2
    assert len(first.fetched_raw_paths) == 2
    source_text = Path(first.created_sources[0]).read_text(encoding="utf-8")
    assert "Official diagnostic manual evidence excerpt for review." in source_text
    candidates = json.loads((wiki_root / "exports" / "knowledge_facts.candidates.json").read_text(encoding="utf-8"))
    assert candidates[0]["external_url"] == "https://www.woah.org/en/disease/newcastle-disease/"
    assert "Official diagnostic manual evidence excerpt for review." in candidates[0]["evidence_excerpt"]

    second = discover_authority_sources(wiki_root, "newcastle authority data", llm_suggestions_json=suggestions, fetch=True)
    assert second.accepted_count == 0
    assert second.rejected_count == 2
    assert {item["reason"] for item in second.rejected_candidates} == {"duplicate_existing_source"}


def test_candidate_review_layers_program_risk_and_rejection(tmp_path: Path) -> None:
    wiki_root = tmp_path / "review_wiki"
    init_wiki(wiki_root)
    raw_dir = wiki_root / "raw" / "html"
    raw_dir.mkdir(parents=True, exist_ok=True)
    source_dir = wiki_root / "wiki" / "sources"
    source_dir.mkdir(parents=True, exist_ok=True)

    raw_ok = raw_dir / "safe.html"
    raw_ok.write_text("<html>general poultry glossary source</html>", encoding="utf-8")
    (source_dir / "SRC-0001-safe.md").write_text(
        "---\n"
        "type: source\n"
        "source_id: SRC-0001\n"
        "source_path: raw/html/safe.html\n"
        "external_url: https://www.fao.org/safe\n"
        "source_type: html\n"
        "authority_level: guideline\n"
        "evidence_status: NEEDS_REVIEW\n"
        "created: 2026-05-05\n"
        "updated: 2026-05-05\n"
        "sources: []\n"
        "---\n\n"
        "# Safe\n\n## Excerpt\n\ngeneral poultry glossary source\n",
        encoding="utf-8",
    )
    raw_risk = raw_dir / "risk.html"
    raw_risk.write_text("<html>newcastle disease diagnostic manual</html>", encoding="utf-8")
    (source_dir / "SRC-0002-risk.md").write_text(
        "---\n"
        "type: source\n"
        "source_id: SRC-0002\n"
        "source_path: raw/html/risk.html\n"
        "external_url: https://www.woah.org/en/disease/newcastle-disease/\n"
        "source_type: html\n"
        "authority_level: guideline\n"
        "evidence_status: NEEDS_REVIEW\n"
        "created: 2026-05-05\n"
        "updated: 2026-05-05\n"
        "sources: []\n"
        "---\n\n"
        "# Risk\n\n## Excerpt\n\nnewcastle disease diagnostic manual\n",
        encoding="utf-8",
    )
    candidates_path = wiki_root / "exports" / "knowledge_facts.candidates.json"
    candidates_path.write_text(
        json.dumps(
            [
                {
                    "fact_id": "CAND-0001",
                    "subject": "general glossary source",
                    "predicate": "source_imported",
                    "object": "pending_review",
                    "source_page": "wiki/sources/SRC-0001-safe.md",
                    "external_url": "https://www.fao.org/safe",
                    "evidence_role": "general_source",
                    "evidence_excerpt": "general poultry glossary source",
                    "evidence_status": "NEEDS_REVIEW",
                },
                {
                    "fact_id": "CAND-0002",
                    "subject": "Newcastle diagnostic source",
                    "predicate": "source_imported",
                    "object": "pending_review",
                    "source_page": "wiki/sources/SRC-0002-risk.md",
                    "external_url": "https://www.woah.org/en/disease/newcastle-disease/",
                    "evidence_role": "diagnosis_standard",
                    "evidence_excerpt": "newcastle disease diagnostic manual",
                    "evidence_status": "NEEDS_REVIEW",
                },
                {
                    "fact_id": "CAND-0003",
                    "subject": "broken source",
                    "predicate": "source_imported",
                    "object": "pending_review",
                    "source_page": "wiki/sources/MISSING.md",
                    "external_url": "https://www.fao.org/missing",
                    "evidence_status": "NEEDS_REVIEW",
                },
            ],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    report = review_candidate_facts(wiki_root)
    assert report.auto_ready_count == 1
    assert report.human_required_count == 1
    assert report.rejected_count == 1
    reviewed = json.loads(candidates_path.read_text(encoding="utf-8"))
    decisions = {item["fact_id"]: item["review_decision"] for item in reviewed}
    assert decisions == {
        "CAND-0001": "AUTO_READY_SOURCE",
        "CAND-0002": "HUMAN_REQUIRED",
        "CAND-0003": "REJECTED",
    }
    assert reviewed[0]["formal_promotion_allowed"] is True
    assert reviewed[0]["formal_fact_write_allowed"] is False


def test_nonelinear_client_does_not_send_unsupported_temperature(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(
                {"choices": [{"message": {"content": '{"sources":[]}'}}]},
                ensure_ascii=False,
            ).encode("utf-8")

    def fake_urlopen(request, timeout):
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(maintenance_module, "urlopen", fake_urlopen)

    client = NonelinearAuthorityClient(api_key="test-key", model="gpt-5.4-mini-medium")
    assert client.suggest_sources("新城疫 权威来源") == '{"sources":[]}'

    body = captured["body"]
    assert isinstance(body, dict)
    assert body["model"] == "gpt-5.4-mini-medium"
    assert "temperature" not in body
    assert body["response_format"] == {"type": "json_object"}


def test_wiki_batch_delete_compat_and_crystallize(tmp_path: Path) -> None:
    wiki_root = tmp_path / "workflow_wiki"
    init_wiki(wiki_root)
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "one.md").write_text("# One\n\nNewcastle note.\n", encoding="utf-8")
    (inputs / "two.txt").write_text("Coccidiosis note.", encoding="utf-8")

    batch = batch_ingest_sources(wiki_root, inputs)
    compat = inspect_compat(wiki_root, ensure_source_id="html")
    crystal = crystallize_session(wiki_root, "Newcastle", notes="Session note.")
    delete_preview = delete_source(wiki_root, source_page=batch.results[0]["source_page"], dry_run=True)

    assert batch.processed_count == 2
    assert compat.ok is True
    assert (wiki_root / "raw" / "html").is_dir()
    assert Path(crystal.saved_path).is_file()
    assert delete_preview.dry_run is True
    assert delete_preview.source_page


def test_llm_wiki_schema_check_matches_initialized_wiki(tmp_path: Path) -> None:
    wiki_root = tmp_path / "schema_wiki"
    init_wiki(wiki_root)

    report = schema_check(wiki_root)

    assert report.ok is True
    assert report.declared_version == "1.0.0"
    assert any(check["path"] == "wiki_root.required_directories" for check in report.checks)


def test_strict_lint_reports_unreviewed_facts(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)
    facts_path = wiki_root / "exports" / "knowledge_facts.json"
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    facts.append(
        {
            "fact_id": "F-NEEDS-REVIEW",
            "subject": "reviewed later",
            "predicate": "status",
            "object": "pending",
            "evidence_status": "NEEDS_REVIEW",
        }
    )
    facts_path.write_text(json.dumps(facts, ensure_ascii=False), encoding="utf-8")

    report = lint_wiki(wiki_root, strict=True)

    assert report.ok is False
    assert any("fact_unverified_in_strict_mode" in error for error in report.errors)


def test_final_quality_gates_merge_rule_risk_and_target_mismatch() -> None:
    final = apply_final_quality_gates(
        {
            "final_total_score": 88,
            "final_diagnosis_accuracy": 28,
            "final_label": "pass",
        },
        disease_name="禽丹毒",
        case_data={"diagnosis": "主要诊断：禽霍乱。鉴别诊断：大肠杆菌病。"},
        rule_base_result={"fatal_risk": True},
        judge_a_result={"fatal_risk": False},
        judge_b_result={"fatal_risk": False},
    )

    assert final["fatal_risk"] is True
    assert final["rule_fatal_risk"] is True
    assert final["target_disease_in_diagnosis"] is False
    assert final["target_disease_mismatch"] is True
    assert final["final_label"] == "review"
    assert final["final_diagnosis_accuracy"] == 20.0


def test_final_csv_contains_wiki_audit_fields() -> None:
    row = build_final_result_row(
        {
            "index": 0,
            "disease_name": "新城疫",
            "success": True,
            "case_data": {
                "diagnosis": "主要诊断：新城疫。",
                "metadata": {"disease_name": "新城疫"},
            },
            "rule_base_result": {
                "fatal_risk": True,
                "codes": ["withdrawal_conflict"],
                "wiki_audit": {
                    "wiki_dir": "knowledge/llm_wiki_chicken_authoritative",
                    "wiki_fact_count": 1748,
                    "wiki_page_count": 340,
                    "wiki_context_query": "新城疫\n症状",
                    "wiki_evidence_status_counts": {"EXTRACTED": 8},
                    "wiki_evidence_source_ids": ["SRC-0012", "SRC-0031"],
                    "wiki_context_chars": 3600,
                },
            },
            "judge_a_result": {},
            "judge_b_result": {},
            "final_metrics": {
                "target_disease_in_diagnosis": True,
                "target_disease_mismatch": False,
                "fatal_risk": True,
            },
        }
    )

    assert row["wiki_fact_count"] == 1748
    assert row["wiki_evidence_source_ids"] == "SRC-0012|SRC-0031"
    assert row["wiki_evidence_status_counts"] == '{"EXTRACTED": 8}'
    assert row["final_fatal_risk"] is True
    assert row["target_disease_in_diagnosis"] is True


def test_deepeval_path_attaches_llm_wiki_context(tmp_path: Path) -> None:
    wiki_root = _write_wiki_fixture(tmp_path)
    case_data = {
        "species": "鸡",
        "user_query": "产蛋鸡出现呼吸道症状和产蛋下降，能不能用氯霉素？",
        "diagnosis": "主要诊断：新城疫。鉴别诊断：禽流感。",
        "prescription": "禁止使用氯霉素，建议隔离并送检确认。",
        "withdrawal_period": "涉及产蛋鸡，鸡蛋上市需按合规兽药标签和监管要求处理。",
        "metadata": {"disease_name": "新城疫", "severity": "high", "scene_tags": ["产蛋鸡"]},
    }

    context, audit = _build_deepeval_wiki_context(
        case_data,
        {"rule_base": {"llm_wiki_dir": str(wiki_root)}},
    )
    test_case = _build_test_case(case_data, knowledge_context=context)

    assert "LLM Wiki 知识上下文" in context
    assert "氯霉素" in context
    assert audit["wiki_fact_count"] == 1
    assert audit["wiki_evidence_source_ids"] == ["SRC-001"]
    assert test_case.context == [context]
    assert test_case.retrieval_context == [context]
    assert test_case.additional_metadata["llm_wiki_context_attached"] is True


def test_completion_prompt_keeps_target_disease_contract() -> None:
    messages = build_blind_completion_messages(
        user_query="鸡群精神沉郁，排绿色稀粪。",
        metadata={"severity": "high"},
        disease_name="新城疫",
        knowledge_context="source=SRC-0012 | status=EXTRACTED",
    )

    system_prompt = messages[0]["content"]
    assert "目标疾病一致性约束" in system_prompt
    assert "新城疫" in system_prompt
    assert "LLM Wiki" in system_prompt
