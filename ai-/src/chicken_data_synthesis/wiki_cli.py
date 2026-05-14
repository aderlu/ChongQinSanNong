from __future__ import annotations

# 这是 ``python -m chicken_data_synthesis.wiki_cli`` 使用的轻量入口。
# 真正的命令解析逻辑在 ``interfaces.cli.wiki`` 中。这样测试、脚本和模块入口
# 都能复用同一个 ``main`` 函数，避免 CLI 逻辑分散到多个地方。

from .interfaces.cli.wiki import main


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main"]
