from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from _compat_loader import load_relative


_MODULE = load_relative("wiki_ops/run_guarded_wiki_update.py", "run_guarded_wiki_update_impl")
globals().update({k: v for k, v in vars(_MODULE).items() if not k.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(_MODULE.main())
