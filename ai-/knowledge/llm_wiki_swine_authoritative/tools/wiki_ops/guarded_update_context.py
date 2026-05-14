from __future__ import annotations

"""写库脚本共享的 guarded update 上下文检查工具。

`run_guarded_wiki_update.py` 在真正执行更新命令前，会注入两个环境变量：

- `SWINE_WIKI_GUARDED_UPDATE=1`
- `SWINE_WIKI_CRUD_DECISION=<本次决策文件路径>`

任何会修改 Wiki 内容的脚本都应在 `main()` 开头调用
`require_guarded_update()`。这样即使有人绕过固定入口直接运行写库脚本，
脚本也会在写入前立即退出。

这个文件本身不判断 CRUD 字段是否合规；那是 `audit_crud_decision.py` 的职责。
它只负责确认“当前进程确实是固定入口放行后启动的”。
"""

import os
import sys
from pathlib import Path


# 固定入口注入的开关变量。值必须为字符串 "1"。
GUARDED_ENV = "SWINE_WIKI_GUARDED_UPDATE"

# 固定入口注入的决策文件路径。写库脚本可以把它用于审计报告或留痕。
DECISION_ENV = "SWINE_WIKI_CRUD_DECISION"


def require_guarded_update() -> Path:
    """阻止写库脚本被直接运行。

    返回值是本次更新绑定的 CRUD 决策文件路径。调用方通常不需要解析它；
    只要这个函数成功返回，就说明固定入口已经完成 preflight 并注入了上下文。
    """
    if os.environ.get(GUARDED_ENV) != "1":
        raise SystemExit(
            "This swine Wiki write script must be executed through "
            "tools/run_guarded_wiki_update.py with --decision <decision-file>."
        )
    decision = os.environ.get(DECISION_ENV, "").strip()
    if not decision:
        raise SystemExit(f"Missing {DECISION_ENV}; guarded update context is incomplete.")
    path = Path(decision)
    if not path.exists():
        raise SystemExit(f"CRUD decision file from {DECISION_ENV} does not exist: {path}")
    return path


def import_guard() -> None:
    """给从 tools 目录直接运行的脚本补充 import 路径。

    某些维护脚本可能被 `python tools/foo.py` 方式启动，Python 默认只把脚本所在
    目录放进 `sys.path`。这个小工具用于确保同目录辅助模块可以稳定导入。
    """
    tools_dir = Path(__file__).resolve().parent
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
