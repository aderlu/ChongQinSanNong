from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

"""编码完整性审计脚本。

由 run_swine_wiki_maintenance_checks.py 在更新后验收阶段调用。
它扫描文本文件中的乱码、编码异常和不允许的字符信号，确保新旧中文内容未损坏。
"""

ROOT = Path(__file__).resolve().parents[2]
ISSUES = ROOT / "issues"
REPORT_JSON = ISSUES / "encoding_integrity_audit_2026-05-09.json"
REPORT_MD = ISSUES / "encoding_integrity_audit_2026-05-09.md"
TZ = timezone(timedelta(hours=8))

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".csv",
    ".yaml",
    ".yml",
    ".py",
    ".ps1",
    ".toml",
}

SKIP_PARTS = {
    ".git",
    "__pycache__",
}

SKIP_FILENAMES = {
    REPORT_JSON.name,
    REPORT_MD.name,
}

MOJIBAKE_PATTERNS = [
    "鐚",
    "鍏",
    "銆",
    "锛",
    "鈥",
    "绛",
    "鏉",
    "闃",
    "浣",
    "涓",
    "灏",
    "璇",
    "鑽",
    "鐥",
    "楠",
    "浠",
]


def is_runtime_manifest_path(path: Path, runtime_paths: set[str]) -> bool:
    try:
        rel = path.relative_to(ROOT).as_posix()
    except ValueError:
        return False
    return rel in runtime_paths


def load_runtime_paths() -> set[str]:
    manifest = ROOT / "exports" / "runtime_core_manifest.json"
    if not manifest.exists():
        return set()
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception:
        return set()
    paths = set()
    for entry in payload.get("entries", []):
        rel = entry.get("path")
        if rel:
            paths.add(str(rel).replace("\\", "/"))
    return paths


def classify_file(path: Path, runtime_paths: set[str]) -> dict[str, object]:
    raw = path.read_bytes()
    decode_error = None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        decode_error = str(exc)
        text = raw.decode("utf-8", errors="replace")

    replacement_count = text.count("\ufffd")
    mojibake_hits = {pattern: text.count(pattern) for pattern in MOJIBAKE_PATTERNS if text.count(pattern)}
    mojibake_score = sum(mojibake_hits.values())
    suspicious_lines = []
    if replacement_count or mojibake_score:
        for idx, line in enumerate(text.splitlines(), start=1):
            if "\ufffd" in line or any(pattern in line for pattern in MOJIBAKE_PATTERNS):
                suspicious_lines.append(
                    {
                        "line": idx,
                        "preview": line[:180].encode("unicode_escape").decode("ascii"),
                    }
                )
                if len(suspicious_lines) >= 5:
                    break

    status = "encoding_ok"
    if decode_error or replacement_count:
        status = "decode_or_replacement_damage"
    elif mojibake_score >= 20:
        status = "mojibake_like_content"
    elif mojibake_score:
        status = "minor_mojibake_signal"

    rel = path.relative_to(ROOT).as_posix()
    return {
        "path": rel,
        "runtime_manifest_path": is_runtime_manifest_path(path, runtime_paths),
        "size_bytes": path.stat().st_size,
        "status": status,
        "decode_error": decode_error,
        "replacement_count": replacement_count,
        "mojibake_score": mojibake_score,
        "mojibake_hits": mojibake_hits,
        "suspicious_lines": suspicious_lines,
    }


def iter_text_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.name in SKIP_FILENAMES:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return sorted(files)


def main() -> None:
    """执行编码完整性检查并写入 JSON/Markdown 报告。"""
    runtime_paths = load_runtime_paths()
    records = [classify_file(path, runtime_paths) for path in iter_text_files()]
    damaged = [r for r in records if r["status"] in {"decode_or_replacement_damage", "mojibake_like_content"}]
    minor = [r for r in records if r["status"] == "minor_mojibake_signal"]
    runtime_damaged = [r for r in damaged if r["runtime_manifest_path"]]

    summary = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "knowledge_base": str(ROOT),
        "text_files_scanned": len(records),
        "runtime_manifest_paths_loaded": len(runtime_paths),
        "encoding_ok": sum(1 for r in records if r["status"] == "encoding_ok"),
        "decode_or_replacement_damage": sum(1 for r in records if r["status"] == "decode_or_replacement_damage"),
        "mojibake_like_content": sum(1 for r in records if r["status"] == "mojibake_like_content"),
        "minor_mojibake_signal": len(minor),
        "runtime_damaged_count": len(runtime_damaged),
    }
    payload = {
        "summary": summary,
        "damaged_or_high_signal_files": damaged,
        "minor_signal_files": minor[:100],
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Encoding Integrity Audit",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Text files scanned: {summary['text_files_scanned']}",
        f"- Runtime manifest paths loaded: {summary['runtime_manifest_paths_loaded']}",
        f"- Encoding OK: {summary['encoding_ok']}",
        f"- Decode or replacement damage: {summary['decode_or_replacement_damage']}",
        f"- Mojibake-like content: {summary['mojibake_like_content']}",
        f"- Minor mojibake signal: {summary['minor_mojibake_signal']}",
        f"- Runtime damaged count: {summary['runtime_damaged_count']}",
        "",
        "## Damaged Or High-Signal Files",
        "",
    ]
    if damaged:
        for item in damaged:
            lines.append(
                f"- `{item['path']}`: {item['status']}, replacement={item['replacement_count']}, mojibake_score={item['mojibake_score']}, runtime={item['runtime_manifest_path']}"
            )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `decode_or_replacement_damage` means UTF-8 decoding failed or replacement characters were found.",
            "- `mojibake_like_content` means text decoded as UTF-8 but contains a high count of common mojibake patterns.",
            "- Runtime manifest paths with damage should be fixed before production retrieval.",
            "- Raw archive damage should be isolated or reprocessed before it is used for new facts.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
