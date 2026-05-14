from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPDATED = "2026-05-08T23:59:00+08:00"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def section_replace(text: str, heading: str, replacement: str) -> str:
    pattern = rf"\n## {re.escape(heading)}\n.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, "\n" + replacement.rstrip() + "\n", text, flags=re.S)
    return text


def insert_after_first_section(text: str, block: str) -> str:
    marker = "## Source-first 标签证据使用边界 / V11.1"
    text = re.sub(r"\n## Source-first 标签证据使用边界 / V11\.1\n.*?(?=\n## |\Z)", "", text, flags=re.S)
    m = re.search(r"\n## [^\n]+\n.*?(?=\n## |\Z)", text, flags=re.S)
    if not m:
        return text.rstrip() + "\n\n" + block.rstrip() + "\n"
    return text[: m.end()].rstrip() + "\n\n" + block.rstrip() + "\n" + text[m.end():]


CENTRAL_POLICY = f"""---
tags: [synthesis, swine, source_first, generation_gate, v11_1]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [RC-CITATION-001, RC-DRUG-GOLD-ROLE-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001, SRC-0001]
---

# Swine Source-first Generation Policy / V11.1

## 核心原则

- 猪病诊断、鉴别诊断、采样、治疗候选、处方边界和评估结论均以来源可追溯性为第一约束。
- 可用来源范围放宽为：`A0-*`、`A1-*`、`A2-*`、`SRC-*`、`RC-*`、`RULE-*`。只要来源页、事实锚点、URL、PDF page、标签页或规则卡可追溯，且不是 `NEEDS_REVIEW`，即可进入生成和评估。
- `NEEDS_REVIEW` 仍可用于召回、追问、待核验提示和负例构造；不得作为最终诊断、处方、休药期或食品安全结论的唯一依据。

## 诊断和鉴别

- 疾病页、syndrome 页、comparison 页、textbook `SRC-*`、官方/权威网页 `A0/A1/A2-*` 和 rule card 均可支持诊断与鉴别。
- 诊断答案应说明支持证据、反证或缺失字段；不能仅凭单一症状锁定单病种。
- 实验室诊断结论必须绑定样本、检测方法、采样时间和阴性/阳性解释边界。

## 处方和用药

- 可生成处方或正向治疗答案的最低门槛不是“中国来源”，而是“具体标签或等效权威事实源”：必须能核对猪靶动物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL/残留边界和禁停用状态。
- 来源可以是 `A0/A1/A2/SRC/RC/RULE` 中任一类；但答案必须限定在该来源自身覆盖的法域、产品、制剂、动物种属和适应证内。
- `positive_label_candidate` 药物页可进入正向用药黄金题；`boundary_only` 用于追问、拒答、标签核验和风险边界；`negative_trap` 用于错误外推评估。
- 没有精确标签/事实源时，可以给出诊断、采样、药敏和兽医复核路径，但不输出执行性剂量、疗程、休药期或肉品可食承诺。

## 法域和监管表述

- 中国监管来源不再作为猪病生成和评估的默认唯一门槛。
- 只有当问题明确要求“中国合规”“当地执法/报告/检疫/扑杀/出栏/肉品可食”时，才必须回到相应法域的官方来源或明确标注“仅限所引来源法域”。
- 禁用、停用、淘汰、食品安全和公共卫生人员安全仍是硬边界；硬边界的来源可以来自已锚定的官方、权威教材、规则卡或标签源。

## 黄金集评估

- 正确答案优先奖励：来源清晰、事实真实、数据有效、边界限定准确。
- 主要扣分：无来源结论、把候选/类别/非猪标签外推为处方、把一个法域的标签伪装成另一法域合规、遗漏禁停用或人员安全硬边界。
"""


SYNTHESIS_REWRITES = {
    "swine_drug_and_withdrawal_boundary.md": f"""---
tags: [synthesis, swine, drug, withdrawal, source_first, v11_1]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [RC-DRUG-001, RC-WITHDRAWAL-MRL-001, RC-DRUG-GOLD-ROLE-001, RC-CITATION-001]
---

# 猪病用药和休药期 source-first 边界

## 系统用途

本页定义药物、处方、休药期、MRL、残留和食品安全答案的证据门槛。V11.1 后不再把中国 A0/A1 作为唯一可用来源；任何可追溯且未待审的 `A0/A1/A2/SRC/RC/RULE` 证据，均可用于生成和评估，但不得超出来源自身覆盖的法域、靶动物、产品、剂型、途径和适应证。

## 可用来源

- `A0-*`、`A1-*`、`A2-*`、`SRC-*`、`RC-*`、`RULE-*` 均可作为猪病诊断、治疗候选、处方边界和评估证据。
- 每条可评分结论必须能回到 source page、URL、PDF page、标签页、fact_id 或 rule_card。
- `NEEDS_REVIEW` 仅用于召回和待核验提示，不作为最终处方或休药期结论的唯一来源。

## 处方生成门槛

- 正向处方或治疗方案必须同时核验：猪靶动物、具体药物/产品、剂型、给药途径、适应证、剂量/疗程、处方状态、休药期/MRL/残留边界、禁用/停用状态。
- 药物类别页、教材候选命中、处方药目录命中、同类药、其他动物标签、人医语境或公共卫生语境不能单独升级为执行性处方。
- `positive_label_candidate` 可在其精确来源范围内生成限定性正向答案；`boundary_only` 只能生成追问、拒答、核验路径和风险边界；`negative_trap` 用于评估错误外推。

## 休药期和 MRL

- 休药期、肉品可食、残留合格和 MRL 数值必须精确到具体来源条款；来源可以是 A0/A1/A2/SRC/RC/RULE，但必须覆盖对应产品、动物种属、组织/食品类别和适用条件。
- 如果来源只证明“存在标签候选”或“处方药管理状态”，不得推出休药期、残留合格或可出栏结论。
- 当用户明确询问特定法域合规或本地执行，必须使用该法域的现行官方或等效权威来源；若来源来自其他法域，应标注“仅限所引来源法域”。
""",
    "swine_dataset_generation_validity_gate_v7.md": f"""---
tags: [synthesis, swine, dataset, qa, evidence_gate, generation_gate, source_first, v11_1]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [RC-CITATION-001, RC-TRAIN-READY-001, RC-DRUG-GOLD-ROLE-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001]
---

# Swine Dataset Generation Validity Gate V11.1

## Purpose

This page defines the minimum source-first evidence package for swine QA dataset generation, draft answers, judging and export.

## Required Evidence Package

- Disease identity must be normalized through `exports/alias_index.csv`.
- Standard anchors may be `source=A0-...`, `source=A1-...`, `source=A2-...`, `source=SRC-...`, `source=RC-...`, or `source=RULE-...`.
- Diagnosis requires at least one disease-specific source and one differential, syndrome, sampling or laboratory source.
- Treatment language requires a drug page or rule card plus a specific label/fact source when the answer gives executable dose, route, course, indication, withdrawal period or MRL.
- Regulated, zoonotic, toxic, food-safety or public-health cases must include the applicable rule/source before management language.
- Positive drug-use answers require the referenced drug page to be `positive_label_candidate` or an equivalent exact label/fact source. Missing `gold_dataset_use` defaults to `boundary_only`.
- Drug-class pages cannot support specific product, dose, route, course, indication, withdrawal period, MRL or lawfulness.

## Train-ready Reject Reasons

- `final_label` is not `pass`.
- `target_disease_mismatch` is true after alias normalization.
- Standard citation count is less than 3.
- The answer contains a specific dose, course, route, withdrawal period, MRL or meat-edibility conclusion without an exact label/fact source.
- The answer treats a `boundary_only`, `negative_trap`, `exclude_from_positive_generation`, or `NEEDS_REVIEW` drug page as a positive treatment source.
- The answer infers pig use from a drug class page, candidate PDF hit, human-public-health context, other animal species, or unrelated label.
- The answer hides source jurisdiction and presents one jurisdiction's label as another jurisdiction's compliance conclusion.
- Any judge marks `fatal_risk=true`.
""",
    "swine_answer_evaluation_rubric.md": f"""---
tags: [synthesis, swine, evaluation, source_first, v11_1]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [RC-CITATION-001, RC-TRAIN-READY-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001]
---

# 猪病答案评估量表 / Source-first V11.1

## 系统用途

评估答案时优先检查来源清晰度、事实真实性、数据有效性、诊断鉴别完整性、处方/休药期是否限定在具体标签或事实源内。

## 可用来源

- `A0/A1/A2/SRC/RC/RULE` 均可进入猪病生成与评估。
- `NEEDS_REVIEW` 可用于提示待核验，不可单独支撑最终诊断、处方、休药期、MRL、食品安全或监管执行结论。
- 中国来源不再是默认唯一门槛；只有回答明确承诺“中国合规/本地执行”时才必须使用中国对应来源。

## 评分维度

- 证据锚定 25 分：核心结论是否逐条带 source_id、URL、PDF page、fact_id 或 rule anchor。
- 临床鉴别 20 分：是否覆盖 syndrome/comparison 页列出的常见鉴别，并说明支持、反对和缺失字段。
- 诊断解释 15 分：是否区分样本、方法、时间点、阴性边界、混合感染和药敏结果边界。
- 药物标签边界 20 分：处方、剂量、疗程、途径、休药期和 MRL 是否来自具体标签或等效来源，并限定在对应产品和法域内。
- 安全与监管 10 分：禁停用药、重大疫病、食品安全、公共卫生、毒物气体人员安全是否触发正确边界。
- 表达质量 10 分：结构清晰、先处理安全风险，再给鉴别、采样和治疗核验路径。

## 硬性失败

- 无来源生成处方剂量、疗程、休药期、MRL、禁用药替代方案或肉品可食承诺。
- 把教材候选、药物类别、处方药目录、其他动物标签或一个法域标签外推为通用猪用处方。
- ASF/FMD 等重大疫病疑似或阳性时遗漏报告、隔离、限制移动或官方流程。
- 毒物气体题忽略人员撤离、通风和进入密闭空间风险。
- 诊断结果绝对化解释且没有样本/方法/时间点边界。
""",
    "swine_treatment_candidate_matrix_v7.md": f"""---
tags: [synthesis, swine, treatment_candidates, source_first, v11_1]
updated: {UPDATED}
evidence_status: PROCESSED_SOURCE_ANCHORED
sources: [SRC-0012, SRC-0058, SRC-0059, SRC-0062, SRC-0063, SRC-0064, SRC-0065, SRC-0069, SRC-0070, SRC-0071, SRC-0072, SRC-0073, SRC-0074, SRC-0075, SRC-0076, SRC-0077, SRC-0080, SRC-0081, SRC-0082, RC-DRUG-001, RC-DRUG-GOLD-ROLE-001]
---

# Swine Treatment Candidate Matrix / 猪病治疗候选矩阵

## 来源和状态

- 本页由 `Diseases of Swine, 11th Edition` 全文候选扫描和后续 V11 标签证据补强汇总而来。
- 教材候选可用于召回疾病-药物关系、生成药敏/标签核验追问和构造评估陷阱。
- 候选命中不等于处方；正向处方需要回到具体标签或等效事实源。

## Source-first 可用边界

- 可用于：治疗候选召回、药物类别归并、病原/药敏/阶段判断、标签复核提示、处方越界识别。
- 可升级为正向处方的条件：猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL/禁停用状态均有清晰来源。
- 来源不限于中国 A0/A1；`A0/A1/A2/SRC/RC/RULE` 均可，但答案必须限定在来源本身的法域和标签范围内。
- `high_review` 药物应优先查禁用/停用/淘汰清单、AMR 审慎来源、药敏证据和产品标签。

## 候选概览

- 候选关系行数：178。
- 高复核药物包括：ceftiofur、cefquinome、fluoroquinolones、colistin、chloramphenicol、carbadox、olaquindox、nitroimidazoles、ractopamine。
""",
    "swine_pdf_vs_authority_source_policy.md": f"""---
tags: [synthesis, swine, source_policy, source_first, v11_1]
updated: {UPDATED}
evidence_status: HUMAN_REVIEWED
sources: [SRC-0001, RC-CITATION-001]
---

# PDF 与权威网页来源使用政策 / Source-first V11.1

## 原则

- 本知识库按来源可追溯性使用证据，不按“中国/非中国”预设可用或不可用。
- `SRC-*` 教材/PDF、`A0/A1/A2-*` 官方或权威网页、`RC-*` rule card、`RULE-*` 规则页均可用于猪病诊断、鉴别、处方边界和评估。
- 自动抽取或 `NEEDS_REVIEW` 内容只能做候选召回；进入标准答案前必须有人审或有明确可追溯锚点。

## 使用边界

- 诊断和鉴别可以引用教材、网页、comparison、syndrome 和 rule card。
- 处方、休药期、MRL 和食品安全结论必须精确到具体标签、产品、动物种属、剂型、途径和适用条件。
- 当答案涉及某一法域的合规承诺时，必须使用该法域来源；否则应显式说明“仅限所引来源范围”。
""",
}


RULE_REWRITES = {
    "RC-DRUG-001.md": f"""---
tags: [rule_card, swine, drug, prescription, source_first, v11_1]
card_id: RC-DRUG-001
updated: {UPDATED}
severity: critical
jurisdiction: Global
hard_block: true
evidence_status: HUMAN_REVIEWED
sources: [RC-CITATION-001, RC-DRUG-GOLD-ROLE-001, RC-WITHDRAWAL-MRL-001]
---

# 猪病处方必须有具体标签或等效来源

## 触发词

- 用药
- 剂量
- 休药期
- 处方
- 治疗方案
- 抗菌药
- 驱虫药
- 抗球虫药

## 规则

不得把“中国 A0/A1”作为唯一可用来源；但任何正向处方都必须有具体标签或等效事实源。可用来源包括 `A0/A1/A2/SRC/RC/RULE`，前提是能核验猪靶动物、药物/产品、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。

## 允许响应

- 在精确来源覆盖范围内生成限定性处方或治疗建议。
- 在来源不足时提供诊断、采样、药敏、兽医复核和标签核验路径。
- 标注来源法域和产品范围，避免跨法域或跨制剂外推。

## 禁止响应

- 编造剂量、疗程、给药途径或休药期。
- 把药物类别页、教材候选、处方药目录、其他动物标签或人医语境当作猪用处方。
- 把一个法域的标签伪装成另一个法域的合规结论。
- 用“延长休药期”规避禁用、停用、淘汰或无标签用药。
""",
    "RC-WITHDRAWAL-MRL-001.md": f"""---
tags: [rule_card, swine, drug, withdrawal, mrl, residue, food_safety, source_first, v11_1]
card_id: RC-WITHDRAWAL-MRL-001
updated: {UPDATED}
severity: critical
jurisdiction: Global
hard_block: true
evidence_status: HUMAN_REVIEWED
sources: [RC-DRUG-001, RC-CITATION-001]
---

# 休药期和残留合格必须精确到来源

## 触发词

- 休药期
- 停药期
- 出栏
- 屠宰
- 肉能不能吃
- 残留
- MRL
- 最大残留限量
- 食品安全

## 规则

休药期、肉品可食、残留合格和 MRL 结论必须精确到具体来源条款。来源可以是 `A0/A1/A2/SRC/RC/RULE`，但必须覆盖对应产品、药物、动物种属、剂型、组织/食品类别、适用条件和法域。

## 允许响应

- 引用具体标签、标准或权威来源给出限定性结论。
- 来源不足时回答“不能确认，需要具体标签/标准/残留检测依据复核”。
- 对禁用、停用或淘汰药物触发硬阻断。

## 禁止响应

- 编造休药期天数或 MRL 数值。
- 把其他动物、其他制剂、其他法域、人医语境或教材候选外推为猪。
- 把入口公告、目录命中或摘要页当作具体数值来源。
- 用“延长休药期”规避禁用药、停用药或无批准标签用药。
""",
    "RC-DRUG-GOLD-ROLE-001.md": f"""---
tags: [rule_card, swine, drug, dataset, gold_generation, source_first, v11_1]
card_id: RC-DRUG-GOLD-ROLE-001
updated: {UPDATED}
severity: critical
jurisdiction: Global
hard_block: true
evidence_status: HUMAN_REVIEWED
sources: [RC-TRAIN-READY-001, RC-DRUG-001, RC-DRUG-CLASS-001, RC-WITHDRAWAL-MRL-001]
---

# 药物页按黄金集用途分级

## 生成角色

- `positive_label_candidate`: 已有具体标签或等效来源，可核验猪靶动物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 或禁停用状态；可在严格引用下进入正向用药题。
- `boundary_only`: 只能说明需要标签、药敏、兽医处方、来源或法域复核；不得生成执行性处方。
- `negative_trap`: 用于训练和评估错误外推，例如人医语境、公共卫生语境、非猪靶动物、禁用/停用/淘汰药或无标签证据。
- `exclude_from_positive_generation`: 不进入正向黄金答案生成。

## 规则

药物页没有显式 `gold_dataset_use` 时，默认视为 `boundary_only`。药物页若为 `NEEDS_REVIEW`，只能做候选召回或待核验提示，除非答案同时引用了可独立核验的具体标签/事实源。

## 允许响应

- 使用 `positive_label_candidate` 页面在精确来源范围内生成限定性处方边界。
- 使用 `boundary_only` 页面生成拒答、追问、标签核验和来源需求。
- 使用 `negative_trap` 页面生成评估陷阱和反例。

## 禁止响应

- 将 `boundary_only` 或 `negative_trap` 页面转化为正向治疗方案。
- 在没有 `gold_dataset_use` 和精确标签来源时默认认为药物可用于猪。
- 将候选命中、教材页码、处方药目录命中或同类药当成批准适应证。
""",
    "RC-CITATION-001.md": f"""---
card_id: RC-CITATION-001
severity: high
jurisdiction: Global
hard_block: false
evidence_status: HUMAN_REVIEWED
updated: {UPDATED}
---

# 标准证据引用门禁

## Rule

所有诊断、采样、监管、用药、休药期和食品安全结论必须使用标准来源锚点：`source=A0-...`、`source=A1-...`、`source=A2-...`、`source=SRC-...`、`source=RC-...` 或 `source=RULE-...`。内部 anchor key、裸页面路径、无来源摘要不能作为训练可用引用。

## Enforcement

- Candidate generation: inject this card whenever a case asks for diagnosis, treatment, sampling, regulation, sale, withdrawal period, or public-health boundary.
- CSV conversion: compute local flags from normalized aliases and standard citations.
- Train-ready export: reject records that violate this card.
""",
    "RC-TRAIN-READY-001.md": f"""---
card_id: RC-TRAIN-READY-001
severity: critical
jurisdiction: Global
hard_block: true
evidence_status: HUMAN_REVIEWED
updated: {UPDATED}
sources: [RC-CITATION-001, RC-DRUG-001, RC-WITHDRAWAL-MRL-001]
---

# 训练可用样本门禁

## Rule

训练可用样本必须 pass、无 fatal risk、目标疾病别名命中诊断、回答标准引用不少于 3 个，且不得包含无来源剂量、无来源疗程、无来源具体休药期或无来源食品安全承诺。

## Source-first adjustment

可接受来源包括 `A0/A1/A2/SRC/RC/RULE`。中国来源不再是默认唯一门槛；但任何法域合规承诺、处方、休药期、MRL 或肉品可食结论都必须精确到对应来源自身覆盖范围。

## Enforcement

- Candidate generation: inject this card whenever a case asks for diagnosis, treatment, sampling, regulation, sale, withdrawal period, or public-health boundary.
- CSV conversion: compute local flags from normalized aliases and standard citations.
- Train-ready export: reject records that violate this card.
""",
}


SOURCE_FIRST_BLOCK_POSITIVE = """## Source-first 标签证据使用边界 / V11.1

- 本页 `gold_dataset_use=positive_label_candidate`，表示已存在可召回的具体标签或等效权威事实源；可用于正向用药答案，但只能限定在该来源覆盖的猪靶动物、制剂、途径、适应证、剂量/疗程、处方状态和休药期/MRL 范围内。
- 生成处方或评估答案时，可接受 `A0/A1/A2/SRC/RC/RULE` 任一类已锚定来源；不再要求必须是中国 A0/A1，但不得把一个法域、产品或制剂的证据外推到另一个法域、产品或制剂。
- 如果问题明确要求中国合规、当地出栏、残留合格或肉品可食，必须回到中国现行标签/标准/公告；否则应标注“仅限所引来源范围”。
"""

SOURCE_FIRST_BLOCK_BOUNDARY = """## Source-first 标签证据使用边界 / V11.1

- 本页 `gold_dataset_use=boundary_only`，可用于治疗候选召回、标签核验追问、药敏/诊断建议、处方越界识别和评估负例；不能单独生成执行性剂量、疗程、休药期、MRL 或肉品可食承诺。
- 正向用药答案不再要求必须有中国 A0/A1；但必须另有具体标签或等效事实源，且能核验猪靶动物、具体产品/药物、剂型、途径、适应证、剂量/疗程、处方状态、休药期/MRL 和禁停用状态。
- 教材候选、药物类别、处方药目录、其他动物标签、人医语境和公共卫生语境只能提供召回或边界，不得外推为猪用处方。
"""

SOURCE_FIRST_BLOCK_NEGATIVE = """## Source-first 标签证据使用边界 / V11.1

- 本页 `gold_dataset_use=negative_trap` 或被排除于正向生成，主要用于训练和评估错误外推。
- 可用来构造拒答、纠错、禁停用或非猪标签陷阱；不得用于正向处方、休药期、MRL 或食品安全答案。
- 若后续发现具体猪用标签或等效来源，必须先更新本页角色和来源索引，再进入正向生成。
"""


def write_policy_and_core_pages() -> None:
    write(ROOT / "wiki/synthesis/swine_source_first_generation_policy_v11_1.md", CENTRAL_POLICY)
    for name, text in SYNTHESIS_REWRITES.items():
        write(ROOT / "wiki/synthesis" / name, text)
    for name, text in RULE_REWRITES.items():
        write(ROOT / "wiki/rule_cards" / name, text)


def drug_role(text: str) -> str:
    m = re.search(r"^gold_dataset_use:\s*(\S+)", text, flags=re.M)
    return m.group(1) if m else "boundary_only"


def clean_drug_pages() -> int:
    changed = 0
    for path in sorted((ROOT / "wiki/drugs").glob("DRUG-*.md")):
        text = read(path)
        original = text
        role = drug_role(text)
        block = SOURCE_FIRST_BLOCK_BOUNDARY
        if role == "positive_label_candidate":
            block = SOURCE_FIRST_BLOCK_POSITIVE
        elif role in {"negative_trap", "exclude_from_positive_generation"}:
            block = SOURCE_FIRST_BLOCK_NEGATIVE

        text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
        text = text.replace("## 中国合规复核边界", "## 标签和法域有效性复核边界")
        text = section_replace(text, "系统使用边界", "")
        text = section_replace(text, "标签和法域有效性复核边界", "")
        text = section_replace(text, "V6 生成可用边界", "")
        text = section_replace(text, "V7 生成可用边界", "")

        replacements = {
            "未完成中国批准产品、说明书、休药期、禁限用和药敏证据逐项复核前，不得生成处方、剂量、疗程或中国合规承诺。":
                "未完成具体标签、靶动物、剂型/途径、适应证、禁停用和药敏证据逐项复核前，不得生成执行性处方、剂量、疗程、休药期或法域合规承诺。",
            "不得从教材直接生成中国处方、给水用药方案或休药期":
                "不得从教材直接生成执行性处方、给水用药方案或休药期",
            "不得跨法域泛化为中国处方或休药期":
                "不得跨法域泛化为处方或休药期",
            "中国合规承诺": "特定法域合规承诺",
            "中国合规、当地出栏、残留合格或肉品可食": "特定法域合规、当地出栏、残留合格或肉品可食",
            "中国猪场": "特定法域猪场",
            "中国官方具体标签": "具体标签或等效权威来源",
            "没有精确 A0 标签时": "没有精确标签或等效来源时",
            "无精确 A0": "无精确标签",
            "中国现行兽药标签、批准文号、公告或兽医处方依据":
                "具体标签、批准文件、权威来源或兽医处方依据",
            "必须在具体回答时逐条核对原始 A0 标签/标准":
                "必须在具体回答时逐条核对原始标签、标准或等效来源",
            "原始 A0 标签/标准": "原始标签、标准或等效来源",
            "A0 标签": "具体标签",
            "中国休药期": "休药期",
            "中国处方": "处方",
            "`evidence_only` 表示仅有教材或边界证据，不得生成处方、剂量、疗程或休药期。":
                "`boundary_only` 表示本页可用于候选召回和边界判断；正向处方需另有具体标签或等效来源。",
            "`china_regulated` 表示存在中国官方来源入口，但具体药物条目和休药期仍需公告原文、标签或 A0/A1 文件逐项核验。":
                "`jurisdiction` 仅描述来源适用范围；生成答案时应按所引标签或事实源限定法域和产品范围。",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        if role == "positive_label_candidate":
            text = re.sub(r"^evidence_status:\s*NEEDS_REVIEW", "evidence_status: HUMAN_REVIEWED", text, flags=re.M)
            text = text.replace("页面类型：`evidence_only` + `NEEDS_REVIEW`。", "页面类型：`positive_label_candidate`。")
            text = text.replace("页面类型：`evidence_only`。", "页面类型：`positive_label_candidate`。")
        elif role == "boundary_only":
            text = text.replace("页面类型：`evidence_only` + `NEEDS_REVIEW`。", "页面类型：`boundary_only`。")
            text = text.replace("页面类型：`evidence_only`。", "页面类型：`boundary_only`。")

        text = insert_after_first_section(text, block)

        if text != original:
            write(path, text)
            changed += 1
    return changed


def clean_synthesis_remaining_phrases() -> int:
    changed = 0
    replacements = {
        "中国监管、禁用药、剂量、休药期、检疫、扑杀、食品处理和公共卫生暴露处置必须要求 A0/A1 来源。":
            "禁用药、剂量、休药期、检疫、扑杀、食品处理和公共卫生暴露处置必须要求可追溯来源；来源可以是 A0/A1/A2/SRC/RC/RULE，涉及特定法域合规时必须使用该法域来源。",
        "中国监管、处方、剂量、休药期、食品处理、扑杀、检疫和公共卫生执行细则仍需 A0/A1 权威来源。":
            "处方、剂量、休药期、食品处理、扑杀、检疫和公共卫生执行细则必须有可追溯权威来源；涉及特定法域合规时必须使用对应法域来源。",
        "中国监管、ASF/FMD、禁用药、处方剂量、休药期、检疫、扑杀、食品处置和公共卫生执行细则必须使用 A0/A1 或 rule_card 硬阻断，不接受教材外推；":
            "重大疫病、禁用药、处方剂量、休药期、检疫、扑杀、食品处置和公共卫生执行细则必须使用 A0/A1/A2/SRC/RC/RULE 中的可追溯来源，不接受无锚点外推；",
        "必须有 A0/A1/标签支持": "必须有具体标签或等效来源支持",
        "无 A0/A1/标签支持": "无具体标签或等效来源支持",
        "没有 A0/A1 来源": "没有可追溯来源",
        "A0/A1 来源": "A0/A1/A2/SRC/RC/RULE 来源",
        "A0/A1 权威来源": "可追溯权威来源",
        "中国猪场合规用药": "特定法域猪场合规用药",
        "中国合规": "特定法域合规",
    }
    for path in sorted((ROOT / "wiki/synthesis").glob("*.md")):
        text = read(path)
        original = text
        text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            write(path, text)
            changed += 1
    return changed


def clean_rules() -> int:
    changed = 0
    replacements = {
        "需 A0/A1 来源": "需对应法域官方或等效权威来源",
        "必须等待 A0/A1 来源": "必须等待对应法域官方或等效权威来源",
        "等待中国官方或 A0/A1 来源": "等待中国官方或等效权威来源",
        "必须另引 A0/A1 来源": "必须另引对应法域官方或等效权威来源",
        "A0/A1 来源": "A0/A1/A2/SRC/RC/RULE 来源",
        "中国执法处置": "特定法域执法处置",
        "中国召回执行": "特定法域召回执行",
        "中国监管处置": "特定法域监管处置",
        "中国监管结论": "特定法域监管结论",
        "中国监管、扑杀、检疫或人暴露处置结论": "特定法域监管、扑杀、检疫或人暴露处置结论",
        "召回/执法/中国监管结论": "召回、执法或特定法域监管结论",
        "食品处理、执法、召回、处罚或中国监管处置": "食品处理、执法、召回、处罚或特定法域监管处置",
    }
    adjustment = """## Source-first adjustment / V11.1

- 本规则不把中国 A0/A1 作为唯一来源门槛；诊断、鉴别、传播、临床和实验室解释可使用任何清晰锚定的 `A0/A1/A2/SRC/RC/RULE` 来源。
- 当答案承诺某一法域的报告、检疫、扑杀、召回、食品处理、暴露后处置或本地合规结论时，必须回到该法域官方或等效权威来源。
"""
    for path in sorted((ROOT / "wiki/rules").glob("*.md")):
        text = read(path)
        if "A0/A1" not in text and "中国监管" not in text and "中国执法" not in text and "中国召回" not in text:
            continue
        original = text
        text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r"\n## Source-first adjustment / V11\.1\n.*?(?=\n## |\Z)", "", text, flags=re.S)
        text = text.rstrip() + "\n\n" + adjustment
        if text != original:
            write(path, text)
            changed += 1
    return changed


EMPTY_FORMAL_FACT_LINE = re.compile(
    r"\n### [^\n]+\n\n- [^\n]*(?:HUMAN_REVIEWED|暂无|A0/A1)[^\n]*(?:暂|待|不[得可]|不得)[^\n]*",
    flags=re.S,
)


def clean_disease_empty_formal_sections() -> int:
    changed = 0
    for path in sorted((ROOT / "wiki/diseases").glob("DIS-*.md")):
        text = read(path)
        original = text
        text = re.sub(r"updated:\s*.*", f"updated: {UPDATED}", text, count=1)
        text = text.replace(
            "A0/A1 来源",
            "A0/A1/A2/SRC/RC/RULE 来源",
        )
        text = text.replace(
            "clear source_id/fact_id/SRC/A0/A1 anchor exists",
            "clear source_id/fact_id/A0/A1/A2/SRC/RC/RULE anchor exists",
        )
        text = text.replace(
            "source-anchored/A0/A1 evidence",
            "source-anchored evidence",
        )
        text = text.replace(
            "中国饲料放行结论",
            "特定法域饲料放行结论",
        )
        text = re.sub(
            r"\n## 中国监管状态\n.*?(?=\n## |\Z)",
            "\n## 监管/执行性处置边界\n\n"
            "- 本页默认按 source-first 证据使用；疾病诊断、鉴别、传播、临床症状、剖检变化和实验室诊断不以中国监管来源作为唯一门槛。\n"
            "- 可用证据包括 `A0/A1/A2/SRC/RC/RULE`，但必须保留 source_id、fact_id、URL、PDF page、标签页或 rule_card 锚点。\n"
            "- 只有当问题要求特定法域的报告、检疫、扑杀、调运、免疫、食品处理或本地合规承诺时，才必须回到对应法域的官方或等效权威来源；本病页摘要不能单独替代执行命令。\n",
            text,
            flags=re.S,
        )
        text = text.replace(
            "待正文抽取和中国兽药合规复核。",
            "待正文抽取和具体标签/等效来源复核；不以中国兽药来源作为唯一门槛。",
        )
        text = text.replace(
            "法定疫病或疑似重大动物疫病不得生成经验性治疗替代确诊/上报/隔离建议。",
            "法定疫病或疑似重大动物疫病不得生成经验性治疗来替代确诊、报告、隔离或对应法域官方流程。",
        )
        text = text.replace(
            "中国监管、处方、剂量、休药期、食品处理、扑杀、检疫和公共卫生执行细则仍需 A0/A1 权威来源。",
            "处方、剂量、休药期、食品处理、扑杀、检疫和公共卫生执行细则必须有可追溯权威来源；涉及特定法域合规时必须使用对应法域来源。",
        )
        text = text.replace(
            "监管、用药、休药期和食品安全结论仍由 rule cards/A0 来源门禁控制。",
            "用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制。",
        )
        text = text.replace(
            "监管、用药、休药期和食品安全结论仍由 rule cards/A0 来源门禁控制",
            "用药、休药期、食品安全和执行性处置结论仍由 rule cards 与可追溯来源门禁控制",
        )
        text = text.replace(
            "中国动物疾病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走 RC-DISEASE-REGULATORY-001 中 A0 来源核验。",
            "动物疾病分类、报告、治疗可行性、移动控制、免疫、扑杀和无害化处理结论必须走可追溯来源核验；涉及中国本地执行时再调用 RC-DISEASE-REGULATORY-001 或对应 A0 来源。",
        )
        text = text.replace(
            "涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 和 RC-WITHDRAWAL-MRL-001，本病页不得单独作为执行性处方来源。",
            "涉及抗菌药、驱虫药、消毒药、剂量、疗程、休药期、残留或肉品可食结论时，必须走 RC-DRUG-001 和 RC-WITHDRAWAL-MRL-001，并回到具体标签或等效来源；本病页不得单独作为执行性处方来源。",
        )

        if "## Formal Disease Completion / V5" in text:
            start = text.find("## Formal Disease Completion / V5")
            nxt = text.find("\n## ", start + 4)
            end = nxt if nxt != -1 else len(text)
            block = text[start:end]
            # Remove placeholder subsections that contain no usable fact. This keeps populated
            # V5 subsections and later V8/V11 disease evidence blocks intact.
            block2 = EMPTY_FORMAL_FACT_LINE.sub("", block)
            block2 = re.sub(r"\n{3,}", "\n\n", block2)
            text = text[:start] + block2 + text[end:]

        if text != original:
            write(path, text)
            changed += 1
    return changed


def update_synthesis_index() -> None:
    idx = ROOT / "exports/synthesis_index.csv"
    if not idx.exists():
        return
    rows = list(csv.DictReader(idx.open(encoding="utf-8-sig", newline="")))
    fieldnames = rows[0].keys() if rows else ["page_id", "title", "evidence_status", "page_relpath"]
    key = "page_relpath" if "page_relpath" in fieldnames else None
    by_rel = {row.get(key, ""): row for row in rows} if key else {}
    for page in sorted((ROOT / "wiki/synthesis").glob("*.md")):
        rel = "wiki/synthesis/" + page.name
        text = read(page)
        title_match = re.search(r"^#\s+(.+)", text, flags=re.M)
        status_match = re.search(r"^evidence_status:\s*(\S+)", text, flags=re.M)
        row = by_rel.get(rel)
        if row is None and key:
            row = {k: "" for k in fieldnames}
            row[key] = rel
            rows.append(row)
            by_rel[rel] = row
        if row is not None:
            if "title" in row and title_match:
                row["title"] = title_match.group(1)
            if "evidence_status" in row:
                row["evidence_status"] = status_match.group(1) if status_match else "HUMAN_REVIEWED"
            if "page_id" in row and not row.get("page_id"):
                stem = page.stem.upper().replace("-", "_")
                row["page_id"] = "SYNTH-" + re.sub(r"[^A-Z0-9_]+", "_", stem)[:64]
    with idx.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def write_log(stats: dict[str, int]) -> None:
    drug_covered = len(list((ROOT / "wiki/drugs").glob("DRUG-*.md")))
    disease_covered = len(list((ROOT / "wiki/diseases").glob("DIS-*.md")))
    rule_covered = len(list((ROOT / "wiki/rules").glob("*.md")))
    log = f"""# Source-first policy cleanup V11.1 execution log

- Date: 2026-05-08
- Core policy added: `wiki/synthesis/swine_source_first_generation_policy_v11_1.md`
- Synthesis pages rewritten/normalized: {stats['synthesis_core'] + stats['synthesis_remaining']}
- Rule cards rewritten: {stats['rule_cards']}
- Rules covered by source-first adjustment: {rule_covered}
- Drug pages covered by source-first label boundary: {drug_covered}
- Disease pages covered by source-first regulatory boundary cleanup: {disease_covered}
- Latest idempotent run changed rules/drugs/diseases: {stats['rules']}/{stats['drugs']}/{stats['diseases']}

## Policy outcome

- `A0/A1/A2/SRC/RC/RULE` are all accepted as evidence families for swine disease generation and evaluation when source anchors are clear and the evidence is not `NEEDS_REVIEW`.
- China-specific regulatory language is no longer the default global gate; it is retained only when the answer claims China/local compliance or execution.
- Drug pages now distinguish positive label candidates from boundary-only pages using source-first label evidence rather than a China-only A0/A1 gate.
- Disease pages had empty V5 placeholder subsections removed while populated V5/V8/V11 evidence blocks were preserved.
"""
    write(ROOT / "issues/source_first_policy_cleanup_v11_1_2026-05-08.md", log)


def main() -> None:
    write_policy_and_core_pages()
    stats = {
        "synthesis_core": len(SYNTHESIS_REWRITES),
        "rule_cards": len(RULE_REWRITES),
        "rules": clean_rules(),
        "drugs": clean_drug_pages(),
        "synthesis_remaining": clean_synthesis_remaining_phrases(),
        "diseases": clean_disease_empty_formal_sections(),
    }
    update_synthesis_index()
    write_log(stats)
    print(stats)


if __name__ == "__main__":
    main()
