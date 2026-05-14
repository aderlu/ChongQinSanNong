from __future__ import annotations

import subprocess
import sys
from typing import Any


_ORIGINAL_RUN = subprocess.run


def _needs_safe_stdin(kwargs: dict[str, Any]) -> bool:
    if "stdin" in kwargs:
        return False
    if kwargs.get("input") is not None:
        return False
    if kwargs.get("capture_output"):
        return True
    return kwargs.get("stdout") == subprocess.PIPE or kwargs.get("stderr") == subprocess.PIPE


def _safe_run(*popenargs: Any, **kwargs: Any):
    if sys.platform == "win32" and _needs_safe_stdin(kwargs):
        kwargs["stdin"] = subprocess.DEVNULL
    return _ORIGINAL_RUN(*popenargs, **kwargs)


subprocess.run = _safe_run
