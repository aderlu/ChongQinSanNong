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
    # Windows Store / Python 3.14 environments can expose invalid inherited
    # std handles under IDE-driven pytest sessions. When a child process is
    # spawned with captured stdout/stderr but inherited stdin, subprocess may
    # fail before exec with WinError 6 on DuplicateHandle(stdin). Redirecting
    # unspecified stdin to DEVNULL keeps business scripts unchanged while
    # stabilizing CLI-style test and tool execution.
    if sys.platform == "win32" and _needs_safe_stdin(kwargs):
        kwargs["stdin"] = subprocess.DEVNULL
    return _ORIGINAL_RUN(*popenargs, **kwargs)


subprocess.run = _safe_run
