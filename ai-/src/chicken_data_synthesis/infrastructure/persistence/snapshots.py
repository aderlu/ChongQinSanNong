from __future__ import annotations

import copy
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Set, Union

PathInput = Union[str, Path]


def _coerce_index(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _format_saved_at(saved_at: Optional[Union[str, datetime]]) -> str:
    if isinstance(saved_at, datetime):
        return saved_at.isoformat(timespec="seconds")
    if isinstance(saved_at, str) and saved_at.strip():
        return saved_at.strip()
    return datetime.now().isoformat(timespec="seconds")


def _format_timestamp(timestamp: Optional[Union[str, datetime]]) -> str:
    if isinstance(timestamp, datetime):
        return timestamp.strftime("%Y%m%d_%H%M%S")
    if isinstance(timestamp, str) and timestamp.strip():
        return timestamp.strip()
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _normalize_prefix(snapshot_kind: str, prefix: Optional[str] = None) -> str:
    if isinstance(prefix, str) and prefix.strip():
        return prefix.strip()
    snapshot_kind = str(snapshot_kind).strip() or "progress"
    return f"{snapshot_kind}_snapshot"


def build_runtime_state(
    mode: str,
    sample_count: int,
    results: Iterable[Mapping[str, Any]],
    completed_target: int,
    parallel_count: int,
    milestones: Optional[Iterable[int]] = None,
    *,
    saved_at: Optional[Union[str, datetime]] = None,
    **extra_fields: Any,
) -> Dict[str, Any]:
    state: Dict[str, Any] = {
        "saved_at": _format_saved_at(saved_at),
        "mode": mode,
        "sample_count": int(sample_count),
        "completed_target": int(completed_target),
        "parallel_count": int(parallel_count),
        "milestones": copy.deepcopy(list(milestones or [])),
        "results": copy.deepcopy(list(results)),
    }
    if extra_fields:
        state.update(copy.deepcopy(extra_fields))
    return state


def build_progress_snapshot_state(
    mode: str,
    sample_count: int,
    results: Iterable[Mapping[str, Any]],
    completed_target: int,
    parallel_count: int,
    milestones: Optional[Iterable[int]] = None,
    *,
    saved_at: Optional[Union[str, datetime]] = None,
    dedupe_results: bool = True,
    **extra_fields: Any,
) -> Dict[str, Any]:
    snapshot_results = dedupe_results_by_index(results) if dedupe_results else list(results)
    return build_runtime_state(
        mode=mode,
        sample_count=sample_count,
        results=snapshot_results,
        completed_target=completed_target,
        parallel_count=parallel_count,
        milestones=milestones,
        saved_at=saved_at,
        **extra_fields,
    )


def build_snapshot_save_kwargs(
    *,
    latest_filename: str = "latest_progress_snapshot.json",
    keep_latest: Optional[int] = None,
    target_hint: Optional[int] = None,
    timestamp: Optional[Union[str, datetime]] = None,
    prefix: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "latest_filename": latest_filename,
        "keep_latest": keep_latest,
        "target_hint": target_hint,
        "timestamp": timestamp,
        "prefix": prefix,
    }


def build_progress_snapshot_save_request(
    *,
    mode: str,
    sample_count: int,
    results: Iterable[Mapping[str, Any]],
    completed_target: int,
    parallel_count: int,
    directory: PathInput,
    snapshot_kind: str,
    milestones: Optional[Iterable[int]] = None,
    latest_filename: str = "latest_progress_snapshot.json",
    keep_latest: Optional[int] = None,
    target_hint: Optional[int] = None,
    timestamp: Optional[Union[str, datetime]] = None,
    prefix: Optional[str] = None,
    saved_at: Optional[Union[str, datetime]] = None,
    dedupe_results: bool = True,
    **extra_fields: Any,
) -> Dict[str, Any]:
    return {
        "state": build_progress_snapshot_state(
            mode=mode,
            sample_count=sample_count,
            results=results,
            completed_target=completed_target,
            parallel_count=parallel_count,
            milestones=milestones,
            saved_at=saved_at,
            dedupe_results=dedupe_results,
            **extra_fields,
        ),
        "directory": directory,
        "snapshot_kind": snapshot_kind,
        **build_snapshot_save_kwargs(
            latest_filename=latest_filename,
            keep_latest=keep_latest,
            target_hint=target_hint if target_hint is not None else completed_target,
            timestamp=timestamp,
            prefix=prefix,
        ),
    }


def save_snapshot(
    state: Mapping[str, Any],
    directory: PathInput,
    snapshot_kind: str,
    *,
    latest_filename: str = "latest_progress_snapshot.json",
    keep_latest: Optional[int] = None,
    target_hint: Optional[int] = None,
    timestamp: Optional[Union[str, datetime]] = None,
    prefix: Optional[str] = None,
) -> str:
    snapshot_dir = Path(directory)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    payload = copy.deepcopy(dict(state))
    payload.setdefault("saved_at", _format_saved_at(None))

    snapshot_prefix = _normalize_prefix(snapshot_kind, prefix=prefix)
    stamp = _format_timestamp(timestamp)
    suffix = f"_{int(target_hint)}" if target_hint is not None else ""
    snapshot_path = snapshot_dir / f"{snapshot_prefix}{suffix}_{stamp}.json"
    latest_path = snapshot_dir / latest_filename

    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    snapshot_path.write_text(serialized, encoding="utf-8")
    latest_path.write_text(serialized, encoding="utf-8")

    if keep_latest is not None:
        trim_snapshot_history(
            snapshot_dir,
            snapshot_prefix,
            keep_latest,
            exclude_filenames=(latest_filename,),
        )

    return str(snapshot_path)


def load_snapshot(snapshot_path: PathInput) -> Dict[str, Any]:
    payload = json.loads(Path(snapshot_path).read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("Snapshot payload must be a JSON object.")
    return payload


def trim_snapshot_history(
    directory: PathInput,
    prefix: str,
    keep_latest: int,
    *,
    suffix: str = ".json",
    exclude_filenames: Iterable[str] = (),
) -> list[str]:
    if keep_latest <= 0:
        return []

    snapshot_dir = Path(directory)
    if not snapshot_dir.exists():
        return []

    excluded = {name for name in exclude_filenames if name}
    paths = [
        path
        for path in snapshot_dir.iterdir()
        if path.is_file()
        and path.name.startswith(prefix)
        and path.name.endswith(suffix)
        and path.name not in excluded
    ]
    paths.sort(key=lambda path: (path.stat().st_mtime_ns, path.name), reverse=True)

    removed_paths: list[str] = []
    for path in paths[keep_latest:]:
        path.unlink(missing_ok=True)
        removed_paths.append(str(path))
    return removed_paths


def dedupe_results_by_index(results: Iterable[Mapping[str, Any]]) -> list[Dict[str, Any]]:
    deduped: Dict[int, Dict[str, Any]] = {}
    for item in results:
        index = _coerce_index(item.get("index")) if isinstance(item, Mapping) else None
        if index is None:
            continue
        deduped[index] = copy.deepcopy(dict(item))
    return [deduped[index] for index in sorted(deduped)]


def get_completed_indexes(results: Iterable[Mapping[str, Any]]) -> Set[int]:
    completed: Set[int] = set()
    for item in results:
        index = _coerce_index(item.get("index")) if isinstance(item, Mapping) else None
        if index is not None:
            completed.add(index)
    return completed


def save_progress_snapshot(
    state: Mapping[str, Any],
    snapshot_kind: str,
    target_hint: Optional[int] = None,
    *,
    directory: PathInput,
    latest_filename: str = "latest_progress_snapshot.json",
    keep_latest: Optional[int] = None,
    timestamp: Optional[Union[str, datetime]] = None,
    prefix: Optional[str] = None,
) -> str:
    return save_snapshot(
        state,
        directory,
        snapshot_kind,
        latest_filename=latest_filename,
        keep_latest=keep_latest,
        target_hint=target_hint,
        timestamp=timestamp,
        prefix=prefix,
    )


def save_progress_runtime_snapshot(
    *,
    mode: str,
    sample_count: int,
    results: Iterable[Mapping[str, Any]],
    completed_target: int,
    parallel_count: int,
    directory: PathInput,
    snapshot_kind: str,
    milestones: Optional[Iterable[int]] = None,
    latest_filename: str = "latest_progress_snapshot.json",
    keep_latest: Optional[int] = None,
    target_hint: Optional[int] = None,
    timestamp: Optional[Union[str, datetime]] = None,
    prefix: Optional[str] = None,
    saved_at: Optional[Union[str, datetime]] = None,
    dedupe_results: bool = True,
    **extra_fields: Any,
) -> str:
    snapshot_request = build_progress_snapshot_save_request(
        mode=mode,
        sample_count=sample_count,
        results=results,
        completed_target=completed_target,
        parallel_count=parallel_count,
        directory=directory,
        snapshot_kind=snapshot_kind,
        milestones=milestones,
        latest_filename=latest_filename,
        keep_latest=keep_latest,
        target_hint=target_hint,
        timestamp=timestamp,
        prefix=prefix,
        saved_at=saved_at,
        dedupe_results=dedupe_results,
        **extra_fields,
    )
    return save_snapshot(
        snapshot_request["state"],
        snapshot_request["directory"],
        snapshot_request["snapshot_kind"],
        latest_filename=snapshot_request["latest_filename"],
        keep_latest=snapshot_request["keep_latest"],
        target_hint=snapshot_request["target_hint"],
        timestamp=snapshot_request["timestamp"],
        prefix=snapshot_request["prefix"],
    )


load_progress_snapshot = load_snapshot
dedupe_results = dedupe_results_by_index


__all__ = [
    "build_progress_snapshot_save_request",
    "build_runtime_state",
    "build_progress_snapshot_state",
    "build_snapshot_save_kwargs",
    "dedupe_results",
    "dedupe_results_by_index",
    "get_completed_indexes",
    "load_progress_snapshot",
    "load_snapshot",
    "save_progress_snapshot",
    "save_progress_runtime_snapshot",
    "save_snapshot",
    "trim_snapshot_history",
]
