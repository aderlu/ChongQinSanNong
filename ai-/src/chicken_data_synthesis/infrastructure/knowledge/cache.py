from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .contracts import CACHE_FILE_NAME, CACHE_VERSION
from .rendering import now_iso


# 缓存负责把“原始证据文件的指纹”和“生成出来的 source page”连接起来。
# 这里刻意使用文件哈希作为 key：如果原始文件内容发生变化，哈希也会变化，
# 自动维护流程就会重新摄取，而不会悄悄复用旧的来源元数据。

def ensure_cache(wiki_dir: str | Path) -> Path:
    """确保 ``.wiki-cache.json`` 存在；不存在时创建一个空缓存文件。"""
    root = Path(wiki_dir)
    cache_path = root / CACHE_FILE_NAME
    if not cache_path.is_file():
        write_cache(root, {"version": CACHE_VERSION, "updated_at": now_iso(), "entries": {}})
    return cache_path


def read_cache(wiki_dir: str | Path) -> dict[str, Any]:
    """读取缓存 JSON；如果内容损坏，则回退为空缓存结构。

    这样可以避免缓存文件异常导致整个 Wiki 查询或摄取流程中断。
    """
    cache_path = ensure_cache(wiki_dir)
    try:
        payload = json.loads(cache_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        payload = {"version": CACHE_VERSION, "entries": {}}
    if not isinstance(payload, dict):
        payload = {"version": CACHE_VERSION, "entries": {}}
    payload.setdefault("version", CACHE_VERSION)
    payload.setdefault("entries", {})
    return payload


def write_cache(wiki_dir: str | Path, payload: Mapping[str, Any]) -> Path:
    """写入缓存，并统一补齐版本号和更新时间。"""
    root = Path(wiki_dir)
    root.mkdir(parents=True, exist_ok=True)
    cache_path = root / CACHE_FILE_NAME
    data = dict(payload)
    data.setdefault("version", CACHE_VERSION)
    data.setdefault("entries", {})
    data["updated_at"] = now_iso()
    cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return cache_path


def hash_file(path: str | Path) -> str:
    """计算 raw 证据文件的 SHA-256 指纹。"""
    file_path = Path(path)
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def hash_text(text: str) -> str:
    """计算粘贴文本或人工文本证据的 SHA-256 指纹。"""
    return f"sha256:{hashlib.sha256(str(text or '').encode('utf-8')).hexdigest()}"


def cache_check(wiki_dir: str | Path, raw_file: str | Path) -> dict[str, Any]:
    """检查某个 raw 文件是否已经关联过 source page。"""
    key = hash_file(raw_file)
    cache = read_cache(wiki_dir)
    entry = cache.get("entries", {}).get(key)
    return {"hit": bool(entry), "key": key, "entry": entry}


def cache_update(
    wiki_dir: str | Path,
    raw_file: str | Path,
    source_page: str | Path,
    *,
    title: str = "",
) -> dict[str, Any]:
    """为一组 raw 文件和 source page 创建或刷新缓存记录。"""
    root = Path(wiki_dir)
    raw_path = Path(raw_file)
    source_path = Path(source_page)
    key = hash_file(raw_path)
    cache = read_cache(root)
    entries = dict(cache.get("entries") or {})
    now = now_iso()
    existing = dict(entries.get(key) or {})
    created = existing.get("created_at") or now
    entries[key] = {
        "source_path": _relpath(root, raw_path),
        "source_page": _relpath(root, source_path),
        "title": title or existing.get("title") or raw_path.stem,
        "created_at": created,
        "updated_at": now,
    }
    cache["entries"] = entries
    write_cache(root, cache)
    return {"key": key, "entry": entries[key]}


def cache_invalidate(wiki_dir: str | Path, raw_file: str | Path = "", *, source_page: str | Path = "") -> dict[str, Any]:
    """删除指向已删除 raw 文件或 source page 的缓存记录。"""
    root = Path(wiki_dir)
    cache = read_cache(root)
    entries = dict(cache.get("entries") or {})
    removed: dict[str, Any] = {}
    raw_rel = _relpath(root, Path(raw_file)) if raw_file else ""
    page_rel = _relpath(root, Path(source_page)) if source_page else ""
    raw_key = ""
    if raw_file and Path(raw_file).is_file():
        raw_key = hash_file(raw_file)

    for key, entry in list(entries.items()):
        if raw_key and key == raw_key:
            removed[key] = entries.pop(key)
            continue
        if not isinstance(entry, dict):
            continue
        if raw_rel and str(entry.get("source_path") or "") == raw_rel:
            removed[key] = entries.pop(key)
            continue
        if page_rel and str(entry.get("source_page") or "") == page_rel:
            removed[key] = entries.pop(key)

    if removed:
        cache["entries"] = entries
        write_cache(root, cache)
    return {"removed_count": len(removed), "removed_keys": tuple(removed.keys())}


def _relpath(root: Path, path: Path) -> str:
    """缓存中尽量保存相对于 Wiki 根目录的路径。"""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
