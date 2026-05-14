from __future__ import annotations

from typing import Any

from llm_foundation.prompting import render_prompt_template


def render_template(template_name: str, /, **context: Any) -> str:
    """Render a prompt template through the shared legacy Jinja environment."""
    return render_prompt_template(template_name, **context)
