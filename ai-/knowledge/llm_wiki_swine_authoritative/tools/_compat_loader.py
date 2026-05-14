from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


TOOLS_DIR = Path(__file__).resolve().parent


def load_relative(module_relpath: str, module_name: str) -> ModuleType:
    target = TOOLS_DIR / module_relpath
    spec = importlib.util.spec_from_file_location(module_name, target)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {target}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
