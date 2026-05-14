from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cached_input_tokens: int = 0
    reasoning_tokens: int = 0

    @property
    def uncached_input_tokens(self) -> int:
        return max(self.input_tokens - self.cached_input_tokens, 0)

    def to_dict(self) -> dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "reasoning_tokens": self.reasoning_tokens,
        }


@dataclass(slots=True, frozen=True)
class ModelPricing:
    input_cost_per_million: float
    output_cost_per_million: float
    cached_input_cost_per_million: float = 0.0
    currency: str = "CNY"

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_cost_per_million": self.input_cost_per_million,
            "output_cost_per_million": self.output_cost_per_million,
            "cached_input_cost_per_million": self.cached_input_cost_per_million,
            "currency": self.currency,
        }


@dataclass(slots=True, frozen=True)
class CostEstimate:
    input_cost: float
    cached_input_cost: float
    output_cost: float
    total_cost: float
    currency: str = "CNY"

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_cost": self.input_cost,
            "cached_input_cost": self.cached_input_cost,
            "output_cost": self.output_cost,
            "total_cost": self.total_cost,
            "currency": self.currency,
        }


@dataclass(slots=True, frozen=True)
class BudgetLineItem:
    label: str
    model_name: str
    request_count: int
    usage_per_request: TokenUsage
    total_usage: TokenUsage
    pricing: ModelPricing
    cost: CostEstimate

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "model_name": self.model_name,
            "request_count": self.request_count,
            "usage_per_request": self.usage_per_request.to_dict(),
            "total_usage": self.total_usage.to_dict(),
            "pricing": self.pricing.to_dict(),
            "cost": self.cost.to_dict(),
        }


@dataclass(slots=True, frozen=True)
class BudgetSummary:
    total_requests: int
    total_usage: TokenUsage
    total_cost: CostEstimate

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "total_usage": self.total_usage.to_dict(),
            "total_cost": self.total_cost.to_dict(),
        }


def extract_token_usage(response_or_usage: Any) -> TokenUsage:
    usage_mapping = _extract_usage_mapping(response_or_usage)
    if not usage_mapping:
        return TokenUsage()

    input_tokens = _coerce_int(
        usage_mapping.get("input_tokens", usage_mapping.get("prompt_tokens", 0))
    )
    output_tokens = _coerce_int(
        usage_mapping.get("output_tokens", usage_mapping.get("completion_tokens", 0))
    )
    total_tokens = _coerce_int(
        usage_mapping.get("total_tokens", input_tokens + output_tokens)
    )

    prompt_details = _as_mapping(
        usage_mapping.get("prompt_tokens_details", usage_mapping.get("input_tokens_details"))
    )
    completion_details = _as_mapping(
        usage_mapping.get("completion_tokens_details", usage_mapping.get("output_tokens_details"))
    )

    cached_input_tokens = _coerce_int(prompt_details.get("cached_tokens", 0))
    reasoning_tokens = _coerce_int(completion_details.get("reasoning_tokens", 0))

    return TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        cached_input_tokens=cached_input_tokens,
        reasoning_tokens=reasoning_tokens,
    )


def resolve_model_pricing(model_config: Mapping[str, Any]) -> ModelPricing | None:
    pricing_block = _as_mapping(model_config.get("pricing"))

    input_cost = _first_number(
        pricing_block,
        "input_cost_per_million",
        "input_price_per_million",
        "input_price",
        fallback_mapping=model_config,
    )
    output_cost = _first_number(
        pricing_block,
        "output_cost_per_million",
        "output_price_per_million",
        "output_price",
        fallback_mapping=model_config,
    )
    cached_input_cost = _first_number(
        pricing_block,
        "cached_input_cost_per_million",
        "cache_hit_cost_per_million",
        "cache_hit_price_per_million",
        "cache_hit_price",
        fallback_mapping=model_config,
        default=0.0,
    )

    if input_cost is None or output_cost is None:
        return None

    currency = str(
        pricing_block.get("currency", model_config.get("pricing_currency", model_config.get("currency", "CNY")))
    ).strip() or "CNY"
    return ModelPricing(
        input_cost_per_million=input_cost,
        output_cost_per_million=output_cost,
        cached_input_cost_per_million=cached_input_cost or 0.0,
        currency=currency,
    )


def estimate_usage_cost(usage: TokenUsage, pricing: ModelPricing) -> CostEstimate:
    input_cost = usage.uncached_input_tokens / 1_000_000 * pricing.input_cost_per_million
    cached_input_cost = usage.cached_input_tokens / 1_000_000 * pricing.cached_input_cost_per_million
    output_cost = usage.output_tokens / 1_000_000 * pricing.output_cost_per_million
    total_cost = input_cost + cached_input_cost + output_cost
    return CostEstimate(
        input_cost=round(input_cost, 6),
        cached_input_cost=round(cached_input_cost, 6),
        output_cost=round(output_cost, 6),
        total_cost=round(total_cost, 6),
        currency=pricing.currency,
    )


def scale_token_usage(usage: TokenUsage, multiplier: int | float) -> TokenUsage:
    factor = max(float(multiplier), 0.0)
    return TokenUsage(
        input_tokens=int(round(usage.input_tokens * factor)),
        output_tokens=int(round(usage.output_tokens * factor)),
        total_tokens=int(round(usage.total_tokens * factor)),
        cached_input_tokens=int(round(usage.cached_input_tokens * factor)),
        reasoning_tokens=int(round(usage.reasoning_tokens * factor)),
    )


def estimate_budget_line_item(
    *,
    label: str,
    model_name: str,
    request_count: int,
    usage_per_request: TokenUsage,
    pricing: ModelPricing,
) -> BudgetLineItem:
    normalized_request_count = max(int(request_count), 0)
    total_usage = scale_token_usage(usage_per_request, normalized_request_count)
    cost = estimate_usage_cost(total_usage, pricing)
    return BudgetLineItem(
        label=label,
        model_name=model_name,
        request_count=normalized_request_count,
        usage_per_request=usage_per_request,
        total_usage=total_usage,
        pricing=pricing,
        cost=cost,
    )


def estimate_budget_line_item_from_model_config(
    *,
    label: str,
    model_config: Mapping[str, Any],
    request_count: int,
    usage_per_request: TokenUsage,
) -> BudgetLineItem:
    pricing = resolve_model_pricing(model_config)
    if pricing is None:
        raise ValueError(f"Model {model_config.get('name', '')} is missing pricing metadata.")
    return estimate_budget_line_item(
        label=label,
        model_name=str(model_config.get("name", "")),
        request_count=request_count,
        usage_per_request=usage_per_request,
        pricing=pricing,
    )


def summarize_budget(items: list[BudgetLineItem] | tuple[BudgetLineItem, ...]) -> BudgetSummary:
    total_requests = sum(item.request_count for item in items)
    total_usage = TokenUsage(
        input_tokens=sum(item.total_usage.input_tokens for item in items),
        output_tokens=sum(item.total_usage.output_tokens for item in items),
        total_tokens=sum(item.total_usage.total_tokens for item in items),
        cached_input_tokens=sum(item.total_usage.cached_input_tokens for item in items),
        reasoning_tokens=sum(item.total_usage.reasoning_tokens for item in items),
    )
    currency = items[0].pricing.currency if items else "CNY"
    total_cost = CostEstimate(
        input_cost=round(sum(item.cost.input_cost for item in items), 6),
        cached_input_cost=round(sum(item.cost.cached_input_cost for item in items), 6),
        output_cost=round(sum(item.cost.output_cost for item in items), 6),
        total_cost=round(sum(item.cost.total_cost for item in items), 6),
        currency=currency,
    )
    return BudgetSummary(
        total_requests=total_requests,
        total_usage=total_usage,
        total_cost=total_cost,
    )


def _extract_usage_mapping(response_or_usage: Any) -> Mapping[str, Any]:
    if isinstance(response_or_usage, Mapping):
        nested_usage = response_or_usage.get("usage")
        if isinstance(nested_usage, Mapping):
            return nested_usage
        return response_or_usage

    usage_attr = getattr(response_or_usage, "usage", None)
    if usage_attr is not None:
        return _as_mapping(usage_attr)

    return {}


def _first_number(
    primary_mapping: Mapping[str, Any],
    *keys: str,
    fallback_mapping: Mapping[str, Any],
    default: float | None = None,
) -> float | None:
    for mapping in (primary_mapping, fallback_mapping):
        for key in keys:
            if key not in mapping:
                continue
            try:
                return float(mapping[key])
            except (TypeError, ValueError):
                continue
    return default


def _as_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if hasattr(value, "__dict__"):
        return {
            key: item
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return {}


def _coerce_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


__all__ = [
    "BudgetLineItem",
    "BudgetSummary",
    "CostEstimate",
    "ModelPricing",
    "TokenUsage",
    "estimate_budget_line_item",
    "estimate_budget_line_item_from_model_config",
    "estimate_usage_cost",
    "extract_token_usage",
    "resolve_model_pricing",
    "scale_token_usage",
    "summarize_budget",
]
