#!/usr/bin/env python
"""Batch MOA authority source discovery and focused download.

This crawler uses the public search endpoint called by www.moa.gov.cn/so/s.
It keeps the ASF batch output shape while limiting downloads by score and Top K.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEARCH_URL = "https://api.so-gov.cn/query/s"
SITE_CODE = "bm21000007"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

DISEASE_SUFFIXES = ["通知", "公告", "技术指南", "通报", "实施方案", "诊断规范", "防控", "监测", "应急"]
DRUG_SUFFIXES = ["公告", "禁用", "停用", "限用", "兽药", "质量标准", "最大残留限量", "休药期", "批准文号", "说明书"]
HIGH_VALUE_HINTS = ["印发", "诊断规范", "防控技术", "应急", "名录", "清单", "技术指南", "实施方案"]
LOW_VALUE_HINTS = ["会议", "视频会", "日报", "新发", "解除封锁", "科普知识", "消费", "行情"]
ATTACHMENT_EXTS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ofd", ".ceb", ".zip", ".rar")
CONFUSION_TERMS = {
    "猪瘟": ["非洲猪瘟", "非典型猪瘟"],
    "口蹄疫": ["小反刍兽疫"],
}


@dataclass
class Entity:
    entity_id: str
    name: str
    entity_type: str
    aliases: list[str] = field(default_factory=list)
    priority: str = ""


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            attr = dict(attrs)
            self._href = attr.get("href")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a":
            self._href = None

    def handle_data(self, data: str) -> None:
        text = re.sub(r"\s+", " ", data).strip()
        if not text:
            return
        self.parts.append(text)
        if self._href:
            self.links.append((text, self._href))

    @property
    def text(self) -> str:
        return "\n".join(self.parts)


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def sha12(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8", errors="ignore")).hexdigest()[:12]


def ensure_dirs(base: Path) -> None:
    for rel in ["attachments", "metadata", "pages_html", "pages_text"]:
        (base / rel).mkdir(parents=True, exist_ok=True)


def load_entities(max_entities: int | None, explicit: list[str] | None, pilot: bool) -> list[Entity]:
    known_entities, alias_map = load_known_entity_maps()
    if explicit:
        resolved: list[Entity] = []
        for i, raw_name in enumerate(explicit):
            name = raw_name.strip()
            if not name:
                continue
            matched = known_entities.get(name)
            if matched:
                resolved.append(matched)
            else:
                resolved.append(Entity(f"MANUAL-{i+1:03d}", name, guess_entity_type(name), [name], "manual"))
        return resolved

    entities: list[Entity] = []
    disease_csv = ROOT / "exports" / "disease_index.csv"
    with disease_csv.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            is_priority = row.get("coverage_target") == "core" or row.get("regulatory_anchor_required") == "yes"
            if pilot and not is_priority:
                continue
            entities.append(Entity(
                row["disease_id"],
                row["disease_name"],
                "disease",
                sorted(set(alias_map.get(row["disease_id"], [row["disease_name"]]))),
                row.get("coverage_target", ""),
            ))

    if not pilot:
        for path in sorted((ROOT / "wiki" / "drugs").glob("DRUG-*.md")):
            title = read_first_heading(path)
            if title:
                entities.append(Entity(path.stem.split("-")[0], title, "drug", [title], "drug"))

    if max_entities:
        entities = entities[:max_entities]
    return entities


def load_known_entity_maps() -> tuple[dict[str, Entity], dict[str, list[str]]]:
    alias_map: dict[str, list[str]] = {}
    alias_csv = ROOT / "exports" / "alias_index.csv"
    with alias_csv.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            alias_map.setdefault(row["canonical_id"], []).append(row["alias"])

    by_name: dict[str, Entity] = {}
    disease_csv = ROOT / "exports" / "disease_index.csv"
    with disease_csv.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            entity = Entity(
                row["disease_id"],
                row["disease_name"],
                "disease",
                sorted(set(alias_map.get(row["disease_id"], [row["disease_name"]]))),
                row.get("coverage_target", ""),
            )
            by_name[row["disease_name"]] = entity
            for alias in entity.aliases:
                if alias:
                    by_name.setdefault(alias, entity)
    return by_name, alias_map


def guess_entity_type(name: str) -> str:
    for path in sorted((ROOT / "wiki" / "drugs").glob("*.md")):
        title = read_first_heading(path)
        if name and name in title:
            return "drug"
    drug_markers = ["素", "沙星", "霉素", "菌素", "磺胺", "泰妙", "氟苯", "阿莫", "青霉"]
    return "drug" if any(marker in name for marker in drug_markers) else "disease"


def read_first_heading(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return ""


def post_search(query: str, page_size: int) -> dict[str, Any]:
    data = urllib.parse.urlencode({
        "siteCode": SITE_CODE,
        "tab": "all",
        "qt": query,
        "page": "1",
        "pageSize": str(page_size),
        "sort": "relevance",
        "keyPlace": "0",
    }).encode("utf-8")
    req = urllib.request.Request(
        SEARCH_URL,
        data=data,
        method="POST",
        headers={
            "User-Agent": UA,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.moa.gov.cn",
            "Referer": "https://www.moa.gov.cn/so/s",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def iter_docs(response: dict[str, Any]) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            if obj.get("url") and (obj.get("title") or obj.get("titleO")):
                docs.append(obj)
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(response.get("resultDocs", []))
    walk(response.get("sceneResult", {}))
    return docs


def normalize_doc(raw: dict[str, Any], entity: Entity, query: str) -> dict[str, Any]:
    data = raw.get("data") if isinstance(raw.get("data"), dict) else raw
    title = clean_text(data.get("titleO") or data.get("title"))
    summary = clean_text(data.get("summary") or data.get("QUICKDESCRIPTION") or data.get("myValues", {}).get("QUICKDESCRIPTION"))
    url = data.get("url") or data.get("URL") or ""
    my_values = data.get("myValues", {}) if isinstance(data.get("myValues"), dict) else {}
    attachments = my_values.get("ATTACHMENTS", {})
    if not isinstance(attachments, dict):
        attachments = {}
    doc_date = data.get("docDate") or my_values.get("DOCOPENDATE") or ""
    channel = my_values.get("CHANNEL1") or data.get("dbName") or ""
    return {
        "entity_id": entity.entity_id,
        "entity_name": entity.name,
        "entity_type": entity.entity_type,
        "query": query,
        "title": title,
        "url": url,
        "summary": summary,
        "doc_date": doc_date,
        "channel": channel,
        "file_type": data.get("fileType") or my_values.get("FILETYPE") or "",
        "source_site": my_values.get("WEBSITE") or urllib.parse.urlparse(url).netloc,
        "api_attachments": json.dumps(attachments, ensure_ascii=False),
    }


def score_candidate(row: dict[str, str], entity: Entity) -> tuple[int, list[str]]:
    title = row["title"]
    summary = row["summary"]
    url = row["url"]
    haystack = f"{title} {summary}"
    aliases = [a for a in [entity.name] + entity.aliases if a and len(a) > 1]
    suffixes = DRUG_SUFFIXES if entity.entity_type == "drug" else DISEASE_SUFFIXES
    score = 0
    reasons: list[str] = []

    if not is_official_moa_url(url):
        return -999, ["non_moa_domain"]

    entity_in_title = any(alias in title for alias in aliases)
    if entity_in_title:
        score += 30
        reasons.append("entity_in_title")
    elif any(alias in haystack for alias in aliases):
        score += 10
        reasons.append("entity_in_summary")
    else:
        score -= 50
        reasons.append("entity_not_found")

    if entity.entity_type == "disease" and not entity_in_title:
        score -= 25
        reasons.append("disease_title_miss")

    confusions = [term for term in CONFUSION_TERMS.get(entity.name, []) if term in title and term not in aliases]
    if confusions:
        score -= 80
        reasons.append("confusion:" + "|".join(confusions))

    matched_suffix = [s for s in suffixes if s in title]
    if matched_suffix:
        score += 15 + len(matched_suffix) * 3
        reasons.append("suffix:" + "|".join(matched_suffix))

    if any(hint in title for hint in HIGH_VALUE_HINTS):
        score += 12
        reasons.append("high_value_title")

    if any(hint in title for hint in LOW_VALUE_HINTS):
        score -= 12
        reasons.append("low_value_title")

    if re.search(r"govpublic|nybgb|gk/tzgg|xmsyj\.moa\.gov\.cn/(gzdt|zcjd)|fgs\.moa\.gov\.cn/flfg", url):
        score += 10
        reasons.append("priority_channel")

    if row.get("api_attachments") and row["api_attachments"] != "{}":
        score += 8
        reasons.append("has_api_attachments")

    return score, reasons


def is_official_moa_url(url: str) -> bool:
    host = urllib.parse.urlparse(url).netloc.lower()
    return host == "moa.gov.cn" or host.endswith(".moa.gov.cn") or host == "www.moa.gov.cn"


def fetch_url(url: str) -> tuple[int, bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return resp.status, resp.read(), resp.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get("Content-Type", "")
    except Exception as e:
        return 0, str(e).encode("utf-8"), ""


def safe_filename(url: str, title: str, suffix: str) -> str:
    parsed = urllib.parse.urlparse(url)
    name = Path(parsed.path).name or re.sub(r"\W+", "_", title)[:40] or "download"
    if suffix and not name.lower().endswith(suffix.lower()):
        name += suffix
    return f"{sha12(url)}_{name}"


def absolute_url(base_url: str, href: str) -> str:
    return urllib.parse.urljoin(base_url, href)


def discover_links(page_url: str, content: bytes) -> tuple[str, list[tuple[str, str]]]:
    parser = TextExtractor()
    parser.feed(content.decode("utf-8", errors="replace"))
    links = []
    for text, href in parser.links:
        href_abs = absolute_url(page_url, href)
        if is_attachment_url(href_abs):
            links.append((text, href_abs))
    return parser.text, links


def is_attachment_url(url: str) -> bool:
    lower = urllib.parse.urlparse(url).path.lower()
    return lower.endswith(ATTACHMENT_EXTS) or "/p020" in lower


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--max-entities", type=int, default=None)
    parser.add_argument("--entities", default="")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--page-size", type=int, default=10)
    parser.add_argument("--max-suffixes", type=int, default=5)
    parser.add_argument("--max-query-names", type=int, default=2)
    parser.add_argument("--min-score", type=int, default=25)
    parser.add_argument("--discover-only", action="store_true")
    parser.add_argument("--batch-name", default="")
    args = parser.parse_args()

    explicit = [x.strip() for x in args.entities.split(",") if x.strip()] if args.entities else None
    entities = load_entities(args.max_entities, explicit, args.pilot)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_name = args.batch_name or f"moa_batch_authority_{stamp}"
    out = ROOT / "raw" / "web" / batch_name
    ensure_dirs(out)

    candidates: list[dict[str, Any]] = []
    seen_query_url: set[tuple[str, str]] = set()
    for entity in entities:
        suffixes = (DRUG_SUFFIXES if entity.entity_type == "drug" else DISEASE_SUFFIXES)[: args.max_suffixes]
        for query_name in query_names(entity, args.max_query_names):
            for suffix in suffixes:
                query = f"{query_name}{suffix}"
                run_search_for_query(entity, query, args, candidates, seen_query_url)

    candidate_fields = [
        "entity_id", "entity_name", "entity_type", "query", "title", "url", "summary", "doc_date",
        "channel", "file_type", "source_site", "api_attachments", "score", "matched_terms", "error",
    ]
    write_csv(out / "metadata" / "entities.csv", [e.__dict__ for e in entities], ["entity_id", "name", "entity_type", "aliases", "priority"])
    write_csv(out / "metadata" / "candidates.csv", candidates, candidate_fields)

    pages: list[dict[str, Any]] = []
    attachments: list[dict[str, Any]] = []

    if not args.discover_only:
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
                    suffix = Path(urllib.parse.urlparse(url).path).suffix or ".bin"
                    fname = safe_filename(url, row["title"], suffix)
                    rel = Path("attachments") / fname
                    (out / rel).write_bytes(content)
                    attachment_file = str(rel)
                else:
                    fname = safe_filename(url, row["title"], ".html")
                    html_rel = Path("pages_html") / fname
                    txt_rel = Path("pages_text") / (fname + ".txt")
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

    page_fields = candidate_fields + [
        "status", "content_type", "bytes", "text_chars", "attachments", "html_file", "text_file",
        "is_direct_attachment", "attachment_file", "skipped",
    ]
    att_fields = ["link_text", "url", "source_page", "status", "content_type", "bytes", "file", "error"]
    write_csv(out / "metadata" / "pages.csv", pages, page_fields)
    write_csv(out / "metadata" / "attachments.csv", attachments, att_fields)
    write_report(out, entities, candidates, pages, attachments, args)
    print(out)
    return 0


def query_names(entity: Entity, max_names: int) -> list[str]:
    names = []
    for value in [entity.name] + entity.aliases:
        if value and re.search(r"[\u4e00-\u9fff]", value):
            names.append(value)
    names = sorted(set(names), key=lambda x: (-len(x), x))
    if entity.name not in names:
        names.append(entity.name)
    return names[:max_names]


def run_search_for_query(entity: Entity, query: str, args: argparse.Namespace, candidates: list[dict[str, Any]], seen_query_url: set[tuple[str, str]]) -> None:
            try:
                response = post_search(query, args.page_size)
            except Exception as e:
                candidates.append({
                    "entity_id": entity.entity_id,
                    "entity_name": entity.name,
                    "entity_type": entity.entity_type,
                    "query": query,
                    "title": "",
                    "url": "",
                    "summary": "",
                    "doc_date": "",
                    "channel": "",
                    "file_type": "",
                    "source_site": "",
                    "api_attachments": "{}",
                    "score": -999,
                    "matched_terms": "search_error",
                    "error": str(e),
                })
                return
            for raw in iter_docs(response):
                row = normalize_doc(raw, entity, query)
                key = (entity.entity_id, row["url"])
                if not row["url"] or key in seen_query_url:
                    continue
                seen_query_url.add(key)
                score, reasons = score_candidate(row, entity)
                row["score"] = score
                row["matched_terms"] = ";".join(reasons)
                row["error"] = ""
                candidates.append(row)
            time.sleep(0.4)


def download_attachment(out: Path, rows: list[dict[str, Any]], link_text: str, url: str, source_page: str) -> None:
    if not is_official_moa_url(url):
        rows.append({"link_text": link_text, "url": url, "source_page": source_page, "status": "", "content_type": "", "bytes": "", "file": "", "error": "non_moa_domain"})
        return
    if any(r["url"] == url for r in rows):
        return
    status, content, ctype = fetch_url(url)
    if len(content) > 30 * 1024 * 1024:
        rows.append({"link_text": link_text, "url": url, "source_page": source_page, "status": status, "content_type": ctype, "bytes": len(content), "file": "", "error": "too_large"})
        return
    suffix = Path(urllib.parse.urlparse(url).path).suffix or ".bin"
    fname = safe_filename(url, link_text, suffix)
    rel = Path("attachments") / fname
    if status == 200:
        (out / rel).write_bytes(content)
    rows.append({"link_text": link_text, "url": url, "source_page": source_page, "status": status, "content_type": ctype, "bytes": len(content), "file": str(rel) if status == 200 else "", "error": "" if status == 200 else "download_failed"})


def write_report(out: Path, entities: list[Entity], candidates: list[dict[str, Any]], pages: list[dict[str, Any]], attachments: list[dict[str, Any]], args: argparse.Namespace) -> None:
    lines = [
        "# MOA batch authority crawl report",
        "",
        f"- Date: {datetime.now().isoformat(timespec='seconds')}",
        f"- Entities: {len(entities)}",
        f"- Candidates: {len(candidates)}",
        f"- Downloaded pages/direct documents: {len(pages)}",
        f"- Downloaded/recorded attachments: {len(attachments)}",
        f"- Top K per entity: {args.top_k}",
        f"- Min score: {args.min_score}",
        f"- Discover only: {args.discover_only}",
        "",
        "## Entity summary",
        "",
    ]
    for entity in entities:
        cand_count = sum(1 for r in candidates if r["entity_id"] == entity.entity_id)
        page_count = sum(1 for r in pages if r["entity_id"] == entity.entity_id)
        lines.append(f"- {entity.entity_id} {entity.name} ({entity.entity_type}): candidates={cand_count}, saved={page_count}")
    lines.extend(["", "## Saved pages", ""])
    for row in pages:
        lines.append(f"- [{row['entity_name']}] score={row['score']} | {row['title']} | {row['url']}")
    (out / "crawl_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
