from __future__ import annotations

"""猪病 LLM Wiki 真实更新的固定入口。

所有会写入 source、fact、runtime page、evidence expansion、rule card、
export、graph 或 gold dataset 的脚本，都应该通过本脚本执行，而不是直接运行。

总体调用链：

1. 维护者先用 `create_crud_decision.py` 生成绑定式 CRUD 决策文件；
2. 本脚本读取 `--decision` 和 `--` 后的真实更新命令；
3. 先运行 `audit_governance_compliance.py`，确认治理体系仍完整；
4. 再运行 `audit_crud_decision.py`，确认决策文件授权了这条真实命令；
5. 通过后注入 guarded 环境变量，执行真实更新脚本；
6. 更新成功后运行 `run_swine_wiki_maintenance_checks.py` 做完整验收；
7. 每次运行都会写入 `issues/guarded_wiki_update_last_run.json` 和 jsonl 日志。

这样可以同时防止三类问题：

- 绕过治理规则直接改库；
- 决策文件批准 A 脚本但实际执行 B 脚本；
- 更新后不重建 manifest/graph/readiness 或不跑风险/编码/测试验收。
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


WIKI_ROOT = Path(__file__).resolve().parents[2]
AI_ROOT = WIKI_ROOT.parents[1]
ISSUES = WIKI_ROOT / "issues"
TZ = timezone(timedelta(hours=8))
RUN_LOG = ISSUES / "guarded_wiki_update_runs.jsonl"

# 固定入口调用的三个阶段脚本。
# 路径以 AI_ROOT 为 cwd，因此这里使用 `knowledge/...` 相对路径。
GOVERNANCE_PREFLIGHT = "knowledge/llm_wiki_swine_authoritative/tools/audit_governance_compliance.py"
CRUD_PREFLIGHT = "knowledge/llm_wiki_swine_authoritative/tools/audit_crud_decision.py"
POSTCHECK = "knowledge/llm_wiki_swine_authoritative/tools/run_swine_wiki_maintenance_checks.py"


def command_string(command: list[str]) -> str:
    """把命令列表渲染成审计报告里的可读字符串。"""
    return " ".join(shlex.quote(part) for part in command)


def utf8_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    """构造子进程环境，强制 Python 以 UTF-8 输出，降低中文乱码风险。"""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    if extra:
        env.update(extra)
    return env


def resolve_decision(path_text: str) -> Path:
    """解析 `--decision`。

    支持绝对路径、普通相对路径，以及以 `issues/` 开头的 Wiki 内部路径。
    """
    path = Path(path_text)
    if not path.is_absolute():
        path = (WIKI_ROOT / path).resolve() if path_text.startswith("issues/") else path.resolve()
    return path


def rel(path: Path) -> str:
    """把路径尽量转换成相对 Wiki 根目录的形式，便于 JSON 报告阅读。"""
    try:
        return path.relative_to(WIKI_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def run_command(command: list[str], cwd: Path = AI_ROOT, env_extra: dict[str, str] | None = None) -> dict[str, object]:
    """运行一个阶段命令，并把退出码、通过状态和日志尾部收集为结构化结果。"""
    result = subprocess.run(
        command,
        cwd=cwd,
        env=utf8_env(env_extra),
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command_string(command),
        "cwd": cwd.as_posix(),
        "returncode": result.returncode,
        "passed": result.returncode == 0,
        "stdout_tail": result.stdout[-6000:],
        "stderr_tail": result.stderr[-6000:],
    }


def write_report(payload: dict[str, object]) -> Path:
    """写入本次固定入口运行报告。

    `guarded_wiki_update_last_run.json` 便于人工快速查看最近一次结果；
    `guarded_wiki_update_runs.jsonl` 保留历史流水，便于后续审计。
    """
    ISSUES.mkdir(parents=True, exist_ok=True)
    report = ISSUES / "guarded_wiki_update_last_run.json"
    report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return report


def parse_args() -> argparse.Namespace:
    """解析固定入口参数。

    `command` 使用 REMAINDER 接收 `--` 后面的真实更新命令。这样更新脚本
    可以拥有自己的参数，而不会被固定入口提前解析。
    """
    parser = argparse.ArgumentParser(
        description=(
            "Guarded entrypoint for swine LLM Wiki updates. Requires a bound CRUD decision file, "
            "runs governance and CRUD preflight, executes the update command, then runs full checks."
        )
    )
    parser.add_argument("--decision", required=True, help="Bound CRUD decision file created by create_crud_decision.py.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run preflight and show the intended command without executing the update or postchecks.",
    )
    parser.add_argument(
        "--skip-postcheck",
        action="store_true",
        help="Emergency diagnostics only. Executes preflight and command, but skips full post-update checks.",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Update command after '--'.")
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    return args


def finish(payload: dict[str, object], code: int) -> int:
    """统一收尾：写报告、打印 JSON、返回退出码。"""
    report = write_report(payload)
    payload["report"] = rel(report)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return code


def main() -> int:
    """按 preflight -> update -> postcheck 的顺序执行完整受控更新。"""
    args = parse_args()
    generated_at = datetime.now(TZ).isoformat(timespec="seconds")
    decision = resolve_decision(args.decision)
    steps: list[dict[str, object]] = []

    if not args.command:
        # 没有真实更新命令时不能继续。决策文件本身只授权，不执行任何写库动作。
        return finish(
            {
                "generated_at": generated_at,
                "passed": False,
                "reason": "missing_update_command",
                "decision_file": decision.as_posix(),
                "usage": (
                    "python knowledge/llm_wiki_swine_authoritative/tools/run_guarded_wiki_update.py "
                    "--decision issues/crud_decisions/<file>.md -- python <update_script.py>"
                ),
                "steps": steps,
            },
            2,
        )

    # 第一关：治理体系检查。
    # 如果治理文档、入口文档、工具链或最新留痕不完整，后续更新不应继续。
    governance = run_command([sys.executable, GOVERNANCE_PREFLIGHT])
    steps.append({"name": "preflight_governance_compliance", **governance})
    if not governance["passed"]:
        return finish(
            {
                "generated_at": generated_at,
                "passed": False,
                "reason": "preflight_governance_compliance_failed",
                "decision_file": decision.as_posix(),
                "steps": steps,
            },
            1,
        )

    # 第二关：本次 CRUD 决策检查。
    # 这里把真实命令传给 audit_crud_decision.py，与决策文件中的 planned command 对比。
    crud = run_command([sys.executable, CRUD_PREFLIGHT, "--decision", decision.as_posix(), "--", *args.command])
    steps.append({"name": "preflight_crud_decision", **crud})
    if not crud["passed"]:
        return finish(
            {
                "generated_at": generated_at,
                "passed": False,
                "reason": "preflight_crud_decision_failed",
                "decision_file": decision.as_posix(),
                "steps": steps,
            },
            1,
        )

    if args.dry_run:
        # dry-run 只验证两道门禁和 planned command，不执行写库脚本和后验收。
        return finish(
            {
                "generated_at": generated_at,
                "passed": True,
                "dry_run": True,
                "decision_file": decision.as_posix(),
                "intended_update_command": command_string(args.command),
                "steps": steps,
            },
            0,
        )

    # 只有两道门禁都通过后，才给真实更新脚本注入 guarded 环境变量。
    # 写库脚本可通过 guarded_update_context.require_guarded_update()
    # 验证自己确实由本入口启动。
    update_env = {
        "SWINE_WIKI_GUARDED_UPDATE": "1",
        "SWINE_WIKI_CRUD_DECISION": decision.as_posix(),
    }
    update = run_command(args.command, cwd=AI_ROOT, env_extra=update_env)
    steps.append({"name": "update_command", **update})
    if not update["passed"]:
        return finish(
            {
                "generated_at": generated_at,
                "passed": False,
                "reason": "update_command_failed",
                "decision_file": decision.as_posix(),
                "steps": steps,
            },
            1,
        )

    if args.skip_postcheck:
        # 仅用于紧急诊断。正常维护不应跳过后验收。
        return finish(
            {
                "generated_at": generated_at,
                "passed": True,
                "warning": "postcheck_skipped",
                "decision_file": decision.as_posix(),
                "steps": steps,
            },
            0,
        )

    # 更新成功后，必须跑完整维护检查，确保 manifest、图谱、风险、readiness、
    # 编码和 runtime 测试都没有被破坏。
    postcheck = run_command([sys.executable, POSTCHECK])
    steps.append({"name": "post_update_full_checks", **postcheck})
    return finish(
        {
            "generated_at": generated_at,
            "passed": postcheck["passed"],
            "reason": "" if postcheck["passed"] else "post_update_checks_failed",
            "decision_file": decision.as_posix(),
            "steps": steps,
        },
        0 if postcheck["passed"] else 1,
    )


if __name__ == "__main__":
    raise SystemExit(main())
