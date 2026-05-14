from __future__ import annotations

import copy
from typing import Any, Callable, Mapping


GenerationCase = dict[str, Any]
GenerationMessages = list[dict[str, str]]
GenerationPayload = Mapping[str, Any] | None
GenerationResponse = tuple[str | None, str | None, float]
GenerationCaller = Callable[[dict[str, Any], GenerationMessages, str], GenerationResponse]
GenerationPromptBuilder = Callable[[str], GenerationMessages]
CompletionPromptBuilder = Callable[[str, Mapping[str, Any]], GenerationMessages]
GenerationPayloadExtractor = Callable[[str], GenerationPayload]


def normalize_generation_case(
    disease_name: str,
    payload: Mapping[str, Any],
    generator_key: str,
    generator_model: str,
) -> GenerationCase:
    metadata = payload.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
    else:
        metadata = dict(metadata)

    metadata.setdefault("disease_name", disease_name)
    metadata.setdefault("severity", "medium")

    scene_tags = metadata.get("scene_tags", [])
    if not isinstance(scene_tags, list):
        metadata["scene_tags"] = [str(scene_tags)] if scene_tags else []

    return {
        "species": payload.get("species", "猪"),
        "user_query": str(payload.get("user_query", "")).strip(),
        "diagnosis": str(payload.get("diagnosis", "")).strip(),
        "prescription": str(payload.get("prescription", "")).strip(),
        "withdrawal_period": str(payload.get("withdrawal_period", "")).strip(),
        "answer_json": payload.get("answer_json", {}),
        "evidence_anchors": payload.get("evidence_anchors", []),
        "metadata": metadata,
        "generator_key": generator_key,
        "generator_model": generator_model,
    }


def build_completion_visible_metadata(
    query_draft: Mapping[str, Any],
    visible_keys: list[str] | tuple[str, ...] | None,
) -> dict[str, Any]:
    metadata = query_draft.get("metadata", {})
    if not isinstance(metadata, Mapping):
        return {}
    if not isinstance(visible_keys, (list, tuple)) or not visible_keys:
        return {}

    return {
        str(key): metadata.get(key)
        for key in visible_keys
        if str(key) in metadata
    }


def merge_staged_generation_metadata(
    query_draft: Mapping[str, Any],
    completion_payload: Mapping[str, Any],
) -> dict[str, Any]:
    merged_metadata: dict[str, Any] = {}
    for payload in (query_draft, completion_payload):
        metadata = payload.get("metadata", {})
        if isinstance(metadata, Mapping):
            merged_metadata.update(dict(metadata))
    return merged_metadata


def normalize_stage_generator_configs(
    query_config: Mapping[str, Any],
    completion_config: Mapping[str, Any],
    generation_config: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    query_result = copy.deepcopy(dict(query_config))
    completion_result = copy.deepcopy(dict(completion_config))

    query_max_tokens = generation_config.get("query_stage_max_tokens")
    completion_max_tokens = generation_config.get("completion_stage_max_tokens")
    if query_max_tokens not in (None, ""):
        query_result["max_tokens"] = int(query_max_tokens)
    if completion_max_tokens not in (None, ""):
        completion_result["max_tokens"] = int(completion_max_tokens)

    return query_result, completion_result


def resolve_stage_generator_configs(
    default_generator_config: Mapping[str, Any],
    candidate_models: Mapping[str, Mapping[str, Any]],
    generation_config: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    query_key = str(generation_config.get("query_generator_key", "")).strip()
    completion_key = str(generation_config.get("completion_generator_key", "")).strip()
    query_config = copy.deepcopy(candidate_models.get(query_key, default_generator_config))
    completion_config = copy.deepcopy(candidate_models.get(completion_key, default_generator_config))
    return normalize_stage_generator_configs(query_config, completion_config, generation_config)


def merge_staged_generation_result(
    disease_name: str,
    generator_key: str,
    generator_model: str,
    query_draft: Mapping[str, Any],
    completion_payload: Mapping[str, Any],
    *,
    strategy: str = "staged",
) -> GenerationCase:
    merged_metadata = merge_staged_generation_metadata(query_draft, completion_payload)

    merged_payload = {
        "species": query_draft.get("species", "猪"),
        "user_query": query_draft.get("user_query", ""),
        "diagnosis": completion_payload.get("diagnosis", ""),
        "prescription": completion_payload.get("prescription", ""),
        "withdrawal_period": completion_payload.get("withdrawal_period", ""),
        "answer_json": completion_payload.get("answer_json", {}),
        "evidence_anchors": completion_payload.get("evidence_anchors", []),
        "metadata": merged_metadata,
    }
    result = normalize_generation_case(disease_name, merged_payload, generator_key, generator_model)
    result["metadata"]["generation_strategy"] = strategy
    result["metadata"]["query_generator_model"] = query_draft.get("query_generator_model", generator_model)
    result["metadata"]["completion_generator_model"] = completion_payload.get(
        "completion_generator_model",
        generator_model,
    )
    return result


def apply_generation_strategy_metadata(
    case_data: Mapping[str, Any] | None,
    *,
    strategy: str,
    generator_model: str,
    query_generator_model: str | None = None,
    completion_generator_model: str | None = None,
) -> GenerationCase | None:
    if case_data is None:
        return None

    result = dict(case_data)
    metadata = result.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
    else:
        metadata = dict(metadata)

    metadata["generation_strategy"] = strategy
    metadata["query_generator_model"] = query_generator_model or generator_model
    metadata["completion_generator_model"] = completion_generator_model or generator_model
    result["metadata"] = metadata
    return result


def build_staged_generation_result(
    disease_name: str,
    generator_key: str,
    generator_model: str,
    query_draft: Mapping[str, Any],
    completion_payload: Mapping[str, Any],
    *,
    strategy: str = "staged",
    query_generator_model: str | None = None,
    completion_generator_model: str | None = None,
) -> GenerationCase:
    draft_payload = dict(query_draft)
    completion_result = dict(completion_payload)

    if query_generator_model:
        draft_payload["query_generator_model"] = query_generator_model
    if completion_generator_model:
        completion_result["completion_generator_model"] = completion_generator_model

    return merge_staged_generation_result(
        disease_name,
        generator_key,
        generator_model,
        draft_payload,
        completion_result,
        strategy=strategy,
    )


def run_single_generation(
    disease_name: str,
    generator_key: str,
    generator_config: Mapping[str, Any],
    *,
    call_model: GenerationCaller,
    build_messages: GenerationPromptBuilder,
    parse_payload: GenerationPayloadExtractor,
) -> tuple[GenerationCase | None, float]:
    content, _, elapsed = call_model(
        dict(generator_config),
        build_messages(disease_name),
        "json",
    )
    if not content:
        return None, elapsed

    payload = parse_payload(content)
    if not isinstance(payload, Mapping):
        return None, elapsed

    return (
        normalize_generation_case(
            disease_name,
            payload,
            generator_key,
            str(generator_config.get("name", "")),
        ),
        elapsed,
    )


def run_staged_generation(
    disease_name: str,
    generator_key: str,
    generator_config: Mapping[str, Any],
    *,
    candidate_models: Mapping[str, Mapping[str, Any]],
    generation_config: Mapping[str, Any],
    call_model: GenerationCaller,
    parse_payload: GenerationPayloadExtractor,
    build_query_messages: GenerationPromptBuilder,
    build_completion_messages: CompletionPromptBuilder,
) -> tuple[GenerationCase | None, float]:
    total_elapsed = 0.0
    query_stage_config, completion_stage_config = resolve_stage_generator_configs(
        generator_config,
        candidate_models,
        generation_config,
    )

    draft_content, _, draft_elapsed = call_model(
        query_stage_config,
        build_query_messages(disease_name),
        "json",
    )
    total_elapsed += draft_elapsed
    if not draft_content:
        return None, total_elapsed

    query_draft = parse_payload(draft_content)
    if not isinstance(query_draft, Mapping):
        return None, total_elapsed
    query_payload = dict(query_draft)
    query_payload["query_generator_model"] = query_stage_config.get("name", "")

    completion_content, _, completion_elapsed = call_model(
        completion_stage_config,
        build_completion_messages(disease_name, query_payload),
        "json",
    )
    total_elapsed += completion_elapsed
    if not completion_content:
        return None, total_elapsed

    completion_payload = parse_payload(completion_content)
    if not isinstance(completion_payload, Mapping):
        return None, total_elapsed
    completion_result = dict(completion_payload)
    completion_result["completion_generator_model"] = completion_stage_config.get("name", "")

    return (
        merge_staged_generation_result(
            disease_name,
            generator_key,
            str(generator_config.get("name", "")),
            query_payload,
            completion_result,
            strategy=str(generation_config.get("strategy", "staged")),
        ),
        total_elapsed,
    )


def run_generation_with_strategy(
    disease_name: str,
    generator_key: str,
    generator_config: Mapping[str, Any],
    *,
    candidate_models: Mapping[str, Mapping[str, Any]],
    generation_config: Mapping[str, Any],
    call_model: GenerationCaller,
    parse_payload: GenerationPayloadExtractor,
    build_messages: GenerationPromptBuilder,
    build_query_messages: GenerationPromptBuilder,
    build_completion_messages: CompletionPromptBuilder,
) -> tuple[GenerationCase | None, float]:
    strategy = str(generation_config.get("strategy", "single")).strip().lower()

    if strategy == "single":
        case_data, elapsed = run_single_generation(
            disease_name,
            generator_key,
            generator_config,
            call_model=call_model,
            build_messages=build_messages,
            parse_payload=parse_payload,
        )
        return (
            apply_generation_strategy_metadata(
                case_data,
                strategy="single",
                generator_model=str(generator_config.get("name", "")),
            ),
            elapsed,
        )

    if strategy == "staged":
        return run_staged_generation(
            disease_name,
            generator_key,
            generator_config,
            candidate_models=candidate_models,
            generation_config=generation_config,
            call_model=call_model,
            parse_payload=parse_payload,
            build_query_messages=build_query_messages,
            build_completion_messages=build_completion_messages,
        )

    if strategy == "staged_with_fallback":
        staged_case, staged_elapsed = run_staged_generation(
            disease_name,
            generator_key,
            generator_config,
            candidate_models=candidate_models,
            generation_config=generation_config,
            call_model=call_model,
            parse_payload=parse_payload,
            build_query_messages=build_query_messages,
            build_completion_messages=build_completion_messages,
        )
        if staged_case is not None:
            return staged_case, staged_elapsed

        single_case, single_elapsed = run_single_generation(
            disease_name,
            generator_key,
            generator_config,
            call_model=call_model,
            build_messages=build_messages,
            parse_payload=parse_payload,
        )
        return (
            apply_generation_strategy_metadata(
                single_case,
                strategy="single_fallback",
                generator_model=str(generator_config.get("name", "")),
            ),
            staged_elapsed + single_elapsed,
        )

    if strategy == "staged_blind_with_fallback":
        staged_case, staged_elapsed = run_staged_generation(
            disease_name,
            generator_key,
            generator_config,
            candidate_models=candidate_models,
            generation_config=generation_config,
            call_model=call_model,
            parse_payload=parse_payload,
            build_query_messages=build_query_messages,
            build_completion_messages=build_completion_messages,
        )
        if staged_case is not None:
            return (
                apply_generation_strategy_metadata(
                    staged_case,
                    strategy="staged_blind",
                    generator_model=str(generator_config.get("name", "")),
                    query_generator_model=staged_case.get("metadata", {}).get("query_generator_model"),
                    completion_generator_model=staged_case.get("metadata", {}).get("completion_generator_model"),
                ),
                staged_elapsed,
            )

        single_case, single_elapsed = run_single_generation(
            disease_name,
            generator_key,
            generator_config,
            call_model=call_model,
            build_messages=build_messages,
            parse_payload=parse_payload,
        )
        return (
            apply_generation_strategy_metadata(
                single_case,
                strategy="single_fallback",
                generator_model=str(generator_config.get("name", "")),
            ),
            staged_elapsed + single_elapsed,
        )

    return run_single_generation(
        disease_name,
        generator_key,
        generator_config,
        call_model=call_model,
        build_messages=build_messages,
        parse_payload=parse_payload,
    )


__all__ = [
    "GenerationCase",
    "GenerationCaller",
    "GenerationPayloadExtractor",
    "GenerationPromptBuilder",
    "apply_generation_strategy_metadata",
    "build_completion_visible_metadata",
    "build_staged_generation_result",
    "merge_staged_generation_metadata",
    "merge_staged_generation_result",
    "normalize_generation_case",
    "normalize_stage_generator_configs",
    "resolve_stage_generator_configs",
    "run_generation_with_strategy",
    "run_single_generation",
    "run_staged_generation",
]
