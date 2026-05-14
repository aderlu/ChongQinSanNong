from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

DEFAULT_BASE_CONFIG_FILENAME = "config.json"
DEFAULT_LOCAL_CONFIG_FILENAME = "config.local.json"
DEFAULT_MODEL_ROLES = ("generator", "judge_a", "judge_b", "arbiter")


def discover_repo_root(
    start_path: str | Path | None = None,
    *,
    config_filename: str = DEFAULT_BASE_CONFIG_FILENAME,
) -> Path:
    """Find the nearest parent directory that contains the base config file."""
    start = Path(start_path) if start_path is not None else Path(__file__).resolve()
    search_root = start if start.is_dir() else start.parent

    for candidate in (search_root, *search_root.parents):
        if (candidate / config_filename).is_file():
            return candidate

    raise FileNotFoundError(
        f"Unable to find {config_filename!r} starting from {search_root}."
    )


def read_json_config(path: str | Path) -> dict[str, Any]:
    """Read a JSON config file using utf-8-sig so BOM-prefixed files work."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise TypeError(f"Expected top-level JSON object in {config_path}, got {type(data).__name__}.")

    return data


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively merge override into base without mutating the inputs."""
    merged = copy.deepcopy(dict(base))

    for key, override_value in override.items():
        base_value = merged.get(key)
        if isinstance(base_value, Mapping) and isinstance(override_value, Mapping):
            merged[key] = deep_merge(base_value, override_value)
            continue
        merged[key] = copy.deepcopy(override_value)

    return merged


def load_config(
    repo_root: str | Path | None = None,
    *,
    include_local: bool = True,
    base_filename: str = DEFAULT_BASE_CONFIG_FILENAME,
    local_filename: str = DEFAULT_LOCAL_CONFIG_FILENAME,
) -> dict[str, Any]:
    """Load the repository config and optionally overlay the local config."""
    root = (
        Path(repo_root).resolve()
        if repo_root is not None
        else discover_repo_root(config_filename=base_filename)
    )
    base_path = root / base_filename
    config = read_json_config(base_path)

    if not include_local:
        return config

    local_path = root / local_filename
    if not local_path.is_file():
        return config

    local_config = read_json_config(local_path)
    return deep_merge(config, local_config)


@dataclass
class ModelRegistry:
    """Resolve model configs by fixed role or candidate key."""

    role_models: dict[str, dict[str, Any]] = field(default_factory=dict)
    candidate_models: dict[str, dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> ModelRegistry:
        api_config = config.get("api")
        api_mapping = api_config if isinstance(api_config, Mapping) else {}

        direct_models = config.get("models")
        role_source = direct_models if isinstance(direct_models, Mapping) else api_mapping.get("models")

        direct_candidates = config.get("candidate_models")
        candidate_source = (
            direct_candidates
            if isinstance(direct_candidates, Mapping)
            else api_mapping.get("candidate_models")
        )

        registry = cls()

        if isinstance(role_source, Mapping):
            for role, model_config in role_source.items():
                registry.register_role(role, model_config)

        if isinstance(candidate_source, Mapping):
            for key, model_config in candidate_source.items():
                registry.register_candidate(key, model_config)

        return registry

    def register_role(self, role: str, model_config: Mapping[str, Any]) -> None:
        self.role_models[role] = copy.deepcopy(dict(model_config))

    def register_candidate(self, key: str, model_config: Mapping[str, Any]) -> None:
        self.candidate_models[key] = copy.deepcopy(dict(model_config))

    def get_role(self, role: str) -> dict[str, Any]:
        try:
            return copy.deepcopy(self.role_models[role])
        except KeyError as exc:
            raise KeyError(f"Unknown model role: {role}") from exc

    def get_candidate(self, key: str) -> dict[str, Any]:
        try:
            return copy.deepcopy(self.candidate_models[key])
        except KeyError as exc:
            raise KeyError(f"Unknown candidate model key: {key}") from exc

    def get(self, identifier: str) -> dict[str, Any]:
        if identifier in self.role_models:
            return self.get_role(identifier)
        if identifier in self.candidate_models:
            return self.get_candidate(identifier)
        raise KeyError(f"Unknown model identifier: {identifier}")

    def has_role(self, role: str) -> bool:
        return role in self.role_models

    def has_candidate(self, key: str) -> bool:
        return key in self.candidate_models

    def list_roles(self) -> tuple[str, ...]:
        return tuple(self.role_models.keys())

    def list_candidates(self) -> tuple[str, ...]:
        return tuple(self.candidate_models.keys())


def load_model_registry(
    repo_root: str | Path | None = None,
    *,
    include_local: bool = True,
    base_filename: str = DEFAULT_BASE_CONFIG_FILENAME,
    local_filename: str = DEFAULT_LOCAL_CONFIG_FILENAME,
) -> ModelRegistry:
    """Convenience wrapper that loads config first and then builds the registry."""
    config = load_config(
        repo_root=repo_root,
        include_local=include_local,
        base_filename=base_filename,
        local_filename=local_filename,
    )
    return ModelRegistry.from_config(config)
