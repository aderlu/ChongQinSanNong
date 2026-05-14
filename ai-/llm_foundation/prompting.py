from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, StrictUndefined


PROMPT_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "prompt_templates"

_ENV = Environment(
    loader=FileSystemLoader(str(PROMPT_TEMPLATE_DIR)),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=StrictUndefined,
)


def render_prompt_template(template_name: str, **context: Any) -> str:
    template = _ENV.get_template(template_name)
    return template.render(**context).strip()
