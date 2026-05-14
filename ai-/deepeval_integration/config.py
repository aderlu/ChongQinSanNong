from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent
PROJECT_CONFIG_PATH = PROJECT_ROOT / "config.json"


@dataclass(frozen=True)
class MetricDefinition:
    key: str
    display_name: str
    max_score: int
    weight: float
    criteria: str
    evaluation_steps: List[str]


def load_project_config(path: Path | None = None) -> Dict[str, Any]:
    target_path = path or PROJECT_CONFIG_PATH
    with target_path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def build_metric_definitions(config: Dict[str, Any]) -> List[MetricDefinition]:
    dimensions = config["scoring"]["dimensions"]
    return [
        MetricDefinition(
            key="diagnosis_accuracy",
            display_name=str(dimensions["diagnosis_accuracy"]["name"]),
            max_score=int(dimensions["diagnosis_accuracy"]["max_score"]),
            weight=float(dimensions["diagnosis_accuracy"]["weight"]),
            criteria=(
                "判断诊断是否与病例描述和 metadata 中的疾病信息一致，"
                "是否给出了可信的主要诊断、必要的鉴别判断，以及是否符合常见鸡病诊疗常识。"
            ),
            evaluation_steps=[
                "阅读病例描述、诊断和 metadata，确认核心症状与疾病名称是否匹配。",
                "判断诊断结论是否明确，是否包含必要的鉴别诊断或排除逻辑。",
                "若诊断与症状明显不符、结论模糊或存在严重医学常识错误，则降低分数。",
            ],
        ),
        MetricDefinition(
            key="pathology_logic",
            display_name=str(dimensions["pathology_logic"]["name"]),
            max_score=int(dimensions["pathology_logic"]["max_score"]),
            weight=float(dimensions["pathology_logic"]["weight"]),
            criteria=(
                "判断诊断分析中的病理推理是否闭环，是否能从症状、病程、环境和流行病学信息"
                "合理推导到结论，是否存在明显跳步或自相矛盾。"
            ),
            evaluation_steps=[
                "检查症状、环境背景和诊断之间的推理链是否连贯。",
                "判断是否说明了关键病理机制、诱因或流行病学依据。",
                "如果存在明显逻辑断裂、遗漏关键判断依据或前后矛盾，则降低分数。",
            ],
        ),
        MetricDefinition(
            key="prescription_safety",
            display_name=str(dimensions["prescription_safety"]["name"]),
            max_score=int(dimensions["prescription_safety"]["max_score"]),
            weight=float(dimensions["prescription_safety"]["weight"]),
            criteria=(
                "判断处方是否安全、合规、可执行。重点关注药物选择、给药途径、剂量、频次、疗程、"
                "休药期和禁药风险，尤其要识别可能造成严重后果的安全问题。"
            ),
            evaluation_steps=[
                "检查处方中的药物、剂量、频次、疗程和给药方式是否完整且合理。",
                "核对是否存在禁药、明显错误剂量、缺失休药期或安全风险提示不足等问题。",
                "如果存在可能导致严重后果的用药风险，给出显著低分并在理由中指出。",
            ],
        ),
        MetricDefinition(
            key="data_quality",
            display_name=str(dimensions["data_quality"]["name"]),
            max_score=int(dimensions["data_quality"]["max_score"]),
            weight=float(dimensions["data_quality"]["weight"]),
            criteria=(
                "判断样本是否真实、完整、结构清晰且适合进入黄金数据集。需要同时关注字段完整性、"
                "表述质量、可执行性，以及是否满足结构化要求。"
            ),
            evaluation_steps=[
                "检查 user_query、diagnosis、prescription、withdrawal_period 和 metadata 是否完整。",
                "判断描述是否自然真实，是否便于后续作为训练或评测样本使用。",
                "如果结构缺失、字段空洞、内容模板化严重或难以执行，则降低分数。",
            ],
        ),
    ]
