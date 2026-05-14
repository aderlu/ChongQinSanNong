from __future__ import annotations

"""猪病 LLM Wiki 更新后完整验收入口。

本脚本由 run_guarded_wiki_update.py 在更新命令成功后调用。
它按 CHECKS 列表顺序执行治理、manifest、图谱、diff、风险、readiness、
编码和 pytest 检查，并输出机器可读的汇总 JSON。

注意：本脚本不负责授权更新。授权发生在固定入口的两个 preflight：
`audit_governance_compliance.py` 和 `audit_crud_decision.py`。
本脚本只回答“更新已经发生后，知识库派生产物和风险指标是否仍然健康”。
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


WIKI_ROOT = Path(__file__).resolve().parents[2]
AI_ROOT = WIKI_ROOT.parents[1]
WORKSPACE_ROOT = WIKI_ROOT.parents[2]
TZ = timezone(timedelta(hours=8))


# 完整验收链路。
# 顺序不能随意调整：先做治理合规，再重建 runtime 派生产物，
# 再审计图谱、风险、readiness、编码，最后跑 runtime 回归测试。
CHECKS = [
    # 确认治理文档、入口、工具和最新留痕仍完整。
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_governance_compliance.py"],
    # 重建 runtime_core_manifest，确保默认检索入口与页面状态一致。
    ["knowledge/llm_wiki_swine_authoritative/tools/build_runtime_core_manifest.py"],
    # 重建 source/disease/drug/rule 等索引、图谱数据和图谱 HTML，并做检索 smoke test。
    ["knowledge/llm_wiki_swine_authoritative/tools/phase9_rebuild_indexes_graph_smoke.py"],
    # 重建 wiki-native 主图谱、build report 和自动化 native diff，避免手工补写最近一次更新日志。
    ["knowledge/llm_wiki_swine_authoritative/tools/build_wiki_native_graph_mvp.py"],
    ["knowledge/llm_wiki_swine_authoritative/tools/render_wiki_native_graph.py"],
    # 比较本次图谱与上一快照，生成 graph_change_diff_last 和 CRUD 图谱日志。
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_graph_change_diff.py"],
    # 检查 runtime 页面是否新增无来源或高风险幻觉信号。
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_runtime_hallucination_risk.py"],
    # 检查生成/评估可用性、路径完整性、rule card 和 synthesis 覆盖情况。
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_swine_llm_wiki_readiness.py"],
    # 检查 UTF-8、乱码、替换字符和 runtime damaged count。
    ["knowledge/llm_wiki_swine_authoritative/tools/audit_encoding_integrity.py"],
    # 跑 runtime 级回归测试，验证关键检索和规则边界没有被破坏。
    ["-m", "pytest", "tests/test_swine_llm_wiki_runtime.py", "-q"],
]


def run_check(args: list[str]) -> dict[str, object]:
    """执行一个验收子流程，并保留退出码、通过状态和日志尾部。"""
    command = [sys.executable, *args]
    # 每个检查项独立执行并保留 stdout/stderr 尾部，
    # 这样最终 JSON 能准确定位失败阶段，便于排查。
    result = subprocess.run(
        command,
        cwd=AI_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": " ".join(command),
        "returncode": result.returncode,
        "passed": result.returncode == 0,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
    }


def main() -> int:
    """按 CHECKS 顺序运行全部验收子流程，并汇总总通过状态。"""
    results = [run_check(args) for args in CHECKS]
    # 输出一个机器可读的总结果，同时保留每个检查项的结果和日志尾部。
    # run_guarded_wiki_update.py 会根据这里的退出码决定整次更新是否最终通过。
    payload = {
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "workspace_root": WORKSPACE_ROOT.as_posix(),
        "ai_root": AI_ROOT.as_posix(),
        "passed": all(item["passed"] for item in results),
        "checks": results,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
