from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from _compat_loader import load_relative


_MODULE = load_relative(
    "pipeline/test_phase19_layered_export_admission.py",
    "pipeline_test_phase19_layered_export_admission",
)
globals().update({k: v for k, v in vars(_MODULE).items() if not k.startswith("__")})
