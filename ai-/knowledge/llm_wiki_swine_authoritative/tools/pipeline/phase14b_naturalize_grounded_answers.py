from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TZ = timezone(timedelta(hours=8))
DICT_LIKE_RE = re.compile(r'^\s*\{|\}\s*$|"\s*[^"]+\s*"\s*:\s*|^[A-Za-z][A-Za-z _-]{2,40}:\s', re.M)
EN_LABEL_RE = re.compile(
    r"(?i)\b(Evidence basis|Citation anchors|Diagnosis-support evidence|Differential-boundary evidence|"
    r"Differential boundary|Control-boundary evidence|Control boundary|Required boundary|Do not infer|"
    r"Do not over-diagnose|Do not prescribe beyond evidence|Cannot directly provide)\b"
)


def now() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def today() -> str:
    return datetime.now(TZ).strftime("%Y%m%d")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            if isinstance(item, dict):
                rows.append(item)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def resolve_path(value: str, root: Path, default_dir: Path, prefix: str) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else root / path
    files = sorted(default_dir.glob(f"{prefix}_*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No {prefix}_*.jsonl under {default_dir}")
    return files[0]


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def naturalness_score(answer: str) -> float:
    text = answer.strip()
    if not text:
        return 0.0
    score = 1.0
    if DICT_LIKE_RE.search(text):
        score -= 0.35
    if EN_LABEL_RE.search(text):
        score -= 0.2
    if text.count("[source=") < 1:
        score -= 0.15
    if len(text) < 120:
        score -= 0.1
    return max(0.0, min(1.0, round(score, 2)))


def naturalize_answer(answer: str, ability_layer: str) -> tuple[str, list[str]]:
    rewrites: list[str] = []
    text = answer.strip()
    if not text:
        return text, rewrites
    if DICT_LIKE_RE.search(text):
        rewrites.append("dict_like_to_prose")
    text = re.sub(r"(?im)^\s*Diagnosis\s*-\s*support evidence\s*:\s*", "依据当前锚定证据，", text)
    text = re.sub(r"(?im)^\s*Differential\s*-\s*boundary evidence\s*:\s*", "依据当前锚定证据，", text)
    text = re.sub(r"(?im)^\s*Control\s*-\s*boundary evidence\s*:\s*", "依据当前锚定证据，", text)
    text = re.sub(r"(?im)^\s*Evidence basis\s*:\s*", "依据当前锚定证据，", text)
    text = re.sub(r"(?im)^\s*Diagnostic boundary\s*:\s*", "当前能够支持的诊断边界是：", text)
    text = re.sub(r"(?im)^\s*Differential boundary\s*:\s*", "当前能够支持的鉴别边界是：", text)
    text = re.sub(r"(?im)^\s*Control boundary\s*:\s*", "当前能够支持的防控边界是：", text)
    text = re.sub(r"(?im)^\s*Required boundary\s*:\s*", "必须明确的边界是：", text)
    text = re.sub(r"(?im)^\s*Do not infer\s*:\s*", "不能直接外推的是：", text)
    text = re.sub(r"(?im)^\s*Do not over-diagnose\s*:\s*", "不能直接下结论的是：", text)
    text = re.sub(r"(?im)^\s*Do not prescribe beyond evidence\s*:\s*", "不能直接给出的是：", text)
    text = re.sub(r"(?im)^\s*Cannot directly provide\s*:\s*", "目前不能直接提供的是：", text)
    text = re.sub(r"(?im)^\s*Citation anchors\s*:\s*", "对应锚点：", text)
    text = text.replace("{", "").replace("}", "").replace('"', "")
    text = re.sub(r"\s{2,}", " ", text).strip()
    if ability_layer in {"L1_retrieval_grounded", "L2_diagnosis_support", "L3_differential_support", "L4_control_boundary"}:
        text = text.replace("对应锚点：", "引用锚点：")
    return text, rewrites


def process_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    rewrite_counts: dict[str, int] = {}
    processed: list[dict[str, Any]] = []
    for row in rows:
        stage_2 = row.get("stage_2_grounded") or {}
        answer = str(stage_2.get("answer") or "")
        new_answer, rewrites = naturalize_answer(answer, str(row.get("ability_layer") or ""))
        score = naturalness_score(new_answer)
        style_flags = {
            "dict_like_detected": bool(DICT_LIKE_RE.search(new_answer)),
            "english_label_detected": bool(EN_LABEL_RE.search(new_answer)),
            "clinical_conversation_score": score,
            "naturalized": bool(rewrites),
        }
        for item in rewrites:
            rewrite_counts[item] = rewrite_counts.get(item, 0) + 1
        processed.append(
            {
                **row,
                "stage_2_grounded": {
                    **stage_2,
                    "answer": new_answer,
                },
                "style_flags": style_flags,
                "style_rewrites": rewrites,
            }
        )
    return processed, rewrite_counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-root", type=Path, default=ROOT)
    parser.add_argument("--date", default=today())
    parser.add_argument("--generated", default="")
    args = parser.parse_args()

    root = args.wiki_root.resolve()
    exports = root / "exports"
    issues = root / "issues" / "wiki_first_generation_reports"
    generated_path = resolve_path(args.generated, root, exports / "generated_samples", "two_stage_samples")
    rows = read_jsonl(generated_path)
    processed, rewrite_counts = process_rows(rows)

    output = exports / "generated_samples" / f"naturalized_samples_{args.date}.jsonl"
    write_jsonl(output, processed)
    summary = {
        "generated_at": now(),
        "phase": "phase14b_naturalize_grounded_answers",
        "input_generated": relative(generated_path, root),
        "output": relative(output, root),
        "samples": len(processed),
        "rewritten_samples": sum(1 for row in processed if row.get("style_rewrites")),
        "rewrite_counts": rewrite_counts,
        "passed": bool(processed),
    }
    report_json = issues / f"phase14b_naturalize_{args.date}.json"
    report_md = issues / f"phase14b_naturalize_{args.date}.md"
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md.write_text(
        "\n".join(
            [
                "# Phase 14b Naturalize Grounded Answers",
                "",
                f"- Generated: {summary['generated_at']}",
                f"- Samples: {summary['samples']}",
                f"- Rewritten samples: {summary['rewritten_samples']}",
                f"- Input: `{summary['input_generated']}`",
                f"- Output: `{summary['output']}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
