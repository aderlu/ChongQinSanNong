from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import PROJECT_CONFIG_PATH, load_project_config
from .evaluator import evaluate_case_with_deepeval


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="使用 DeepEval 对单条鸡病样本进行标准化评测。")
    parser.add_argument("--case-file", required=True, help="待评测样本 JSON 文件路径。")
    parser.add_argument(
        "--judge-key",
        default="judge_a",
        help="config.json 中 api.models 的裁判 key，例如 judge_a / judge_b / arbiter。",
    )
    parser.add_argument(
        "--config",
        default=str(PROJECT_CONFIG_PATH),
        help="项目配置文件路径，默认使用鸡病数据合成系统/config.json。",
    )
    parser.add_argument(
        "--judge-label",
        default="deepeval_judge",
        help="输出结果中的 judge_label。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_project_config(Path(args.config))
    case_data = json.loads(Path(args.case_file).read_text(encoding="utf-8"))
    judge_config = config["api"]["models"][args.judge_key]
    result = evaluate_case_with_deepeval(
        case_data=case_data,
        judge_config=judge_config,
        judge_label=args.judge_label,
        project_config=config,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
