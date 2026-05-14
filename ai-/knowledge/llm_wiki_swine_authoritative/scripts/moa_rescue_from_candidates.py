#!/usr/bin/env python
"""Rescore and download MOA candidates that were already discovered.

This is useful when the MOA search API is temporarily unavailable but prior
candidate CSVs contain official URLs worth reprocessing.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from moa_batch_authority_crawl import (
    Entity,
    discover_links,
    download_attachment,
    ensure_dirs,
    fetch_url,
    is_attachment_url,
    safe_filename,
    score_candidate,
    write_csv,
    write_report,
)


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--entities", default="")
    parser.add_argument("--entity-type", choices=["drug", "disease"], required=True)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--min-score", type=int, default=20)
    parser.add_argument("--batch-name", required=True)
    args = parser.parse_args()
    args.discover_only = False

    wanted = [x.strip() for x in args.entities.split(",") if x.strip()]
    wanted_set = set(wanted)
    source_rows = read_csv(Path(args.candidates))
    if wanted_set:
        source_rows = [row for row in source_rows if row.get("entity_name") in wanted_set]

    out = ROOT / "raw" / "web" / args.batch_name
    ensure_dirs(out)

    entities = [
        Entity(f"RESCUE-{i + 1:03d}", name, args.entity_type, [name], "rescued")
        for i, name in enumerate(wanted or sorted({row["entity_name"] for row in source_rows}))
    ]
    entity_by_name = {entity.name: entity for entity in entities}

    candidates: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for row in source_rows:
        entity = entity_by_name.get(row["entity_name"])
        if not entity:
            continue
        row = dict(row)
        row["entity_id"] = entity.entity_id
        row["entity_type"] = entity.entity_type
        key = (entity.entity_id, row["url"])
        if key in seen:
            continue
        seen.add(key)
        score, reasons = score_candidate(row, entity)
        row["score"] = score
        row["matched_terms"] = ";".join(reasons)
        row["error"] = ""
        candidates.append(row)

    pages: list[dict[str, Any]] = []
    attachments: list[dict[str, Any]] = []
    for entity in entities:
        rows = [r for r in candidates if r["entity_id"] == entity.entity_id and int(r["score"]) >= args.min_score]
        rows = sorted(rows, key=lambda r: int(r["score"]), reverse=True)[: args.top_k]
        for row in rows:
            url = row["url"]
            status, content, ctype = fetch_url(url)
            is_direct = is_attachment_url(url)
            html_file = text_file = attachment_file = ""
            text_chars = 0
            page_links: list[tuple[str, str]] = []
            if is_direct:
                suffix = Path(url).suffix or ".bin"
                fname = safe_filename(url, row["title"], suffix)
                rel = Path("attachments") / fname
                if status == 200:
                    (out / rel).write_bytes(content)
                attachment_file = str(rel) if status == 200 else ""
            else:
                fname = safe_filename(url, row["title"], ".html")
                html_rel = Path("pages_html") / fname
                txt_rel = Path("pages_text") / (fname + ".txt")
                if status == 200:
                    (out / html_rel).write_bytes(content)
                    text, page_links = discover_links(url, content)
                    header = f"URL: {url}\nTITLE: {row['title']}\nENTITY: {row['entity_name']}\nQUERY: {row['query']}\nSCORE: {row['score']}\n\n"
                    (out / txt_rel).write_text(header + text, encoding="utf-8")
                    html_file = str(html_rel)
                    text_file = str(txt_rel)
                    text_chars = len(text)

            pages.append({
                **row,
                "status": status,
                "content_type": ctype,
                "bytes": len(content),
                "text_chars": text_chars,
                "attachments": len(page_links),
                "html_file": html_file,
                "text_file": text_file,
                "is_direct_attachment": is_direct,
                "attachment_file": attachment_file,
                "skipped": "" if status == 200 else "fetch_failed",
            })

            api_attachments = json.loads(row.get("api_attachments") or "{}")
            for link_url, link_text in list(api_attachments.items())[:8]:
                download_attachment(out, attachments, str(link_text), str(link_url), url)
            for link_text, link_url in page_links[:8]:
                download_attachment(out, attachments, link_text, link_url, url)
            time.sleep(0.3)

    candidate_fields = [
        "entity_id", "entity_name", "entity_type", "query", "title", "url", "summary", "doc_date",
        "channel", "file_type", "source_site", "api_attachments", "score", "matched_terms", "error",
    ]
    page_fields = candidate_fields + [
        "status", "content_type", "bytes", "text_chars", "attachments", "html_file", "text_file",
        "is_direct_attachment", "attachment_file", "skipped",
    ]
    att_fields = ["link_text", "url", "source_page", "status", "content_type", "bytes", "file", "error"]

    write_csv(out / "metadata" / "entities.csv", [e.__dict__ for e in entities], ["entity_id", "name", "entity_type", "aliases", "priority"])
    write_csv(out / "metadata" / "candidates.csv", candidates, candidate_fields)
    write_csv(out / "metadata" / "pages.csv", pages, page_fields)
    write_csv(out / "metadata" / "attachments.csv", attachments, att_fields)
    write_report(out, entities, candidates, pages, attachments, args)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
