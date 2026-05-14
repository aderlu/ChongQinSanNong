from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from _compat_loader import load_relative


_MODULE = load_relative("pipeline/wiki_first_judge_prompts.py", "pipeline_wiki_first_judge_prompts")
globals().update({k: v for k, v in vars(_MODULE).items() if not k.startswith("__")})
