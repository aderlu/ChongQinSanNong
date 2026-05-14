import csv
import json
import statistics
from collections import Counter
from pathlib import Path


ROOT = Path(r"D:\XF-ChongQin\ai-")
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"
OUT_DIR = WIKI / "issues"

PROD_RAW = ROOT / "results" / "swine_weak_wiki_production" / "swine_weak_wiki_production_raw_20260508_164033.json"
PROD_CSV = ROOT / "results" / "swine_weak_wiki_production" / "swine_disease_dataset_production_20260508_164033.csv"
PROD_SUMMARY = ROOT / "results" / "swine_weak_wiki_production" / "swine_disease_dataset_production_summary_20260508_164033.json"
DUAL_RAW = ROOT / "results" / "swine_weak_wiki_production" / "swine_disease_dataset_production_20260508_164033_dual_review_raw_20260508_164705.json"
DUAL_FULL = ROOT / "results" / "swine_weak_wiki_production" / "swine_disease_dataset_production_20260508_164033_dual_reviewed_20260508_164705.csv"
DUAL_FINAL = ROOT / "results" / "swine_weak_wiki_production" / "swine_disease_dataset_production_20260508_164033_dual_final100_20260508_164705.csv"
DUAL_REJECTS = ROOT / "results" / "swine_weak_wiki_production" / "swine_disease_dataset_production_20260508_164033_dual_rejects_20260508_164705.csv"
DUAL_SUMMARY = ROOT / "results" / "swine_weak_wiki_production" / "swine_disease_dataset_production_20260508_164033_dual_review_summary_20260508_164705.json"
TRAIN_SUMMARY = ROOT / "results" / "swine_qa_dataset" / "swine_train_ready_20260508_165018.summary.json"
TRAIN_REJECTS = ROOT / "results" / "swine_qa_dataset" / "swine_train_ready_rejects_20260508_165018.csv"

REPORT = OUT_DIR / "swine_100_parallel_generation_dual_review_arbitration_analysis_2026-05-08.md"
SUMMARY = OUT_DIR / "swine_100_parallel_generation_dual_review_arbitration_analysis_2026-05-08.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def mean(values):
    vals = [float(v) for v in values if v is not None]
    return round(statistics.mean(vals), 2) if vals else 0.0


def percentile(values, p):
    vals = sorted(float(v) for v in values if v is not None)
    if not vals:
        return 0.0
    k = (len(vals) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(vals) - 1)
    if lo == hi:
        return round(vals[lo], 2)
    return round(vals[lo] + (vals[hi] - vals[lo]) * (k - lo), 2)


def counter_from_rows(rows, key):
    c = Counter(str(r.get(key, "")) for r in rows)
    return dict(c)


def number_list(rows, key):
    values = []
    for row in rows:
        value = str(row.get(key, "")).strip()
        if not value:
            continue
        try:
            values.append(float(value))
        except ValueError:
            continue
    return values


def main():
    prod_raw = load_json(PROD_RAW)
    prod_rows = load_csv(PROD_CSV)
    prod_summary = load_json(PROD_SUMMARY)
    dual_raw = load_json(DUAL_RAW)
    dual_rows = load_csv(DUAL_FULL)
    final_rows = load_csv(DUAL_FINAL)
    dual_rejects = load_csv(DUAL_REJECTS)
    dual_summary = load_json(DUAL_SUMMARY)
    train_summary = load_json(TRAIN_SUMMARY)
    train_rejects = load_csv(TRAIN_REJECTS)

    dual_elapsed = []
    for item in dual_raw:
        elapsed = item.get("elapsed")
        if isinstance(elapsed, (int, float)):
            dual_elapsed.append(float(elapsed))
        elif isinstance(elapsed, dict):
            value = elapsed.get("total_seconds") or elapsed.get("judge_b_seconds")
            if value is not None:
                dual_elapsed.append(float(value))

    stage = {
        "answer_seconds_avg": mean(x.get("stage_times", {}).get("answer_seconds") for x in prod_raw),
        "judge_a_seconds_avg": mean(x.get("stage_times", {}).get("judge_seconds") for x in prod_raw),
        "total_generation_judge_a_seconds_avg": mean(x.get("stage_times", {}).get("total_seconds") for x in prod_raw),
        "total_generation_judge_a_seconds_p50": percentile([x.get("stage_times", {}).get("total_seconds") for x in prod_raw], 0.5),
        "total_generation_judge_a_seconds_p90": percentile([x.get("stage_times", {}).get("total_seconds") for x in prod_raw], 0.9),
        "judge_b_seconds_avg": mean(number_list(dual_rows, "judge_b_seconds")),
        "arbiter_seconds_avg": None if not number_list(dual_rows, "arbiter_seconds") else mean(number_list(dual_rows, "arbiter_seconds")),
        "dual_total_seconds_avg": mean(dual_elapsed),
    }

    wiki_sources = Counter()
    wiki_chars = []
    wiki_fact_counts = []
    wiki_page_counts = []
    wiki_status = Counter()
    for item in prod_raw:
        audit = item.get("wiki_audit", {})
        wiki_sources.update(audit.get("wiki_evidence_source_ids", []) or [])
        wiki_chars.append(audit.get("wiki_context_chars", 0))
        wiki_fact_counts.append(audit.get("wiki_fact_count", 0))
        wiki_page_counts.append(audit.get("wiki_page_count", 0))
        wiki_status.update(audit.get("wiki_evidence_status_counts", {}) or {})
    wiki_usage = {
        "rows_with_wiki_dir": sum(1 for item in prod_raw if item.get("wiki_audit", {}).get("wiki_dir")),
        "avg_context_chars": mean(wiki_chars),
        "avg_wiki_fact_count": mean(wiki_fact_counts),
        "avg_wiki_page_count": mean(wiki_page_counts),
        "unique_evidence_sources_used": len(wiki_sources),
        "top_sources": dict(wiki_sources.most_common(20)),
        "evidence_status_counter": dict(wiki_status),
    }

    reject_reasons = Counter()
    for row in train_rejects:
        reject_reasons.update(x for x in row.get("reject_reasons", "").split("|") if x)

    dual_labels = counter_from_rows(dual_rows, "final_label")
    final_labels = counter_from_rows(final_rows, "final_label")
    generation_labels = counter_from_rows(prod_rows, "final_label")
    judge_a_scores = [float(r.get("judge_a_total_score") or 0) for r in prod_rows]
    final_scores = [float(r.get("final_total_score") or 0) for r in final_rows]

    model_success = {
        "answer_success": sum(1 for x in prod_raw if x.get("model_usage", {}).get("answer_success")),
        "judge_a_success": sum(1 for x in prod_raw if x.get("model_usage", {}).get("judge_success")),
        "judge_b_reviewed": len(dual_raw),
        "arbiter_invoked": sum(1 for x in dual_raw if x.get("needed_arbitration")),
    }

    summary = {
        "production": prod_summary,
        "dual_review": dual_summary,
        "train_ready": train_summary,
        "wall_seconds_observed": {"generation_judge_a": 374.1, "dual_review_arbitration": 182.7, "train_ready_export": 0.8, "total": 557.6},
        "stage_seconds": stage,
        "wiki_usage": wiki_usage,
        "model_success": model_success,
        "labels": {"generation_judge_a": generation_labels, "dual_reviewed": dual_labels, "final_selected": final_labels},
        "scores": {
            "judge_a_avg": round(statistics.mean(judge_a_scores), 2),
            "judge_a_min": min(judge_a_scores),
            "judge_a_max": max(judge_a_scores),
            "final_selected_avg": round(statistics.mean(final_scores), 2) if final_scores else 0,
            "final_selected_min": min(final_scores) if final_scores else 0,
            "final_selected_max": max(final_scores) if final_scores else 0,
        },
        "train_ready_reject_reasons": dict(reject_reasons),
        "files": {
            "production_csv": str(PROD_CSV),
            "production_raw_json": str(PROD_RAW),
            "dual_reviewed_csv": str(DUAL_FULL),
            "dual_final_csv": str(DUAL_FINAL),
            "dual_rejects_csv": str(DUAL_REJECTS),
            "dual_raw_json": str(DUAL_RAW),
            "train_ready_jsonl": train_summary["output_jsonl"],
            "train_ready_rejects_csv": train_summary["rejects_csv"],
        },
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 100 条猪病数据集八路并行生成-双评审-仲裁执行分析 / 2026-05-08",
        "",
        "## 运行结论",
        "",
        "- 已真实调用模型链路完成 100 条一阶段生成与 Judge A 初评。",
        "- 双评审脚本按一评 pass 候选进入 Judge B，因此实际二评 72 条；其中 71 条触发仲裁。",
        "- 双评审/仲裁后最终通过 50 条，平均分 87.97。",
        "- 严格 train-ready 导出为 0 条，主要原因是当前弱监督链路输出没有标准 source 引用写入答案正文，也没有 `answer_json` 字段。",
        "- 因此，本次产物适合作弱监督候选、评估样本和链路压测；不适合直接作为严格微调训练 JSONL。",
        "",
        "## 执行时间",
        "",
        f"- 一阶段生成 + Judge A 墙钟时间：{summary['wall_seconds_observed']['generation_judge_a']} 秒。",
        f"- 二评 + 仲裁墙钟时间：{summary['wall_seconds_observed']['dual_review_arbitration']} 秒。",
        f"- train-ready 导出时间：{summary['wall_seconds_observed']['train_ready_export']} 秒。",
        f"- 全链路墙钟总计：{summary['wall_seconds_observed']['total']} 秒。",
        f"- 单条一阶段平均：{stage['total_generation_judge_a_seconds_avg']} 秒；P50={stage['total_generation_judge_a_seconds_p50']} 秒；P90={stage['total_generation_judge_a_seconds_p90']} 秒。",
        f"- 单条回答生成平均：{stage['answer_seconds_avg']} 秒；Judge A 平均：{stage['judge_a_seconds_avg']} 秒。",
        f"- Judge B 平均：{stage['judge_b_seconds_avg']} 秒；仲裁平均：{stage['arbiter_seconds_avg']} 秒。",
        "",
        "## Wiki 参与度",
        "",
        f"- 100/100 条均记录了 wiki_dir 和 wiki_audit。",
        f"- 平均上下文字符数：{wiki_usage['avg_context_chars']}。",
        f"- 平均可检索 wiki fact count：{wiki_usage['avg_wiki_fact_count']}；平均 page count：{wiki_usage['avg_wiki_page_count']}。",
        f"- 本次检索用到唯一 evidence source：{wiki_usage['unique_evidence_sources_used']} 个。",
        f"- Top evidence sources: {wiki_usage['top_sources']}",
        "",
        "## 质量结果",
        "",
        f"- 一阶段标签：{generation_labels}。",
        f"- 双评审最终标签：{dual_labels}。",
        f"- 最终选中标签：{final_labels}。",
        f"- 一阶段 Judge A 平均分：{summary['scores']['judge_a_avg']}；范围 {summary['scores']['judge_a_min']} - {summary['scores']['judge_a_max']}。",
        f"- 最终选中平均分：{summary['scores']['final_selected_avg']}；范围 {summary['scores']['final_selected_min']} - {summary['scores']['final_selected_max']}。",
        f"- 一阶段无具体剂量条数风险：specific_dose_count={prod_summary['specific_dose_count']}；specific_withdrawal_count={prod_summary['specific_withdrawal_count']}。",
        "",
        "## Train-ready 门禁",
        "",
        f"- 输入最终候选：{train_summary['rejected']} + {train_summary['accepted']} 条。",
        f"- 通过严格训练导出：{train_summary['accepted']} 条。",
        f"- 拒绝原因计数：{dict(reject_reasons)}。",
        "",
        "## 文件",
        "",
    ]
    for k, v in summary["files"].items():
        lines.append(f"- {k}: `{v}`")
    lines.extend([
        "",
        "## 判断",
        "",
        "本次运行有效使用了猪病 LLM wiki 参与生成阶段和 Judge A 阶段：每条样本均有 wiki_audit、wiki_context_chars、wiki_evidence_source_ids 等记录。"
        "但现有弱监督脚本没有把 source_id/fact_id/page 标准引用强制写入最终答案字段，导致 train-ready 严格导出全拒。"
        "要生产大模型微调数据，应把 V11.1 source-first 约束前移到生成 prompt 和 CSV schema：输出 answer_json、evidence_anchors、must_include、must_not_include，并在答案正文保留至少 3 个标准 source/rule 引用。",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(REPORT), "summary": str(SUMMARY), **summary["production"], **summary["dual_review"], "train_ready_accepted": train_summary["accepted"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
