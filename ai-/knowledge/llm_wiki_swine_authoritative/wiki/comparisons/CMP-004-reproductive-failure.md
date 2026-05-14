---
tags: [comparison, swine, reproductive_failure, phase2, v8]
comparison_id: CMP-004
updated: 2026-05-08T13:10:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, differential_support, gold_candidate, differential_comparison]
sources: [SYN-003, DIS-015, DIS-023, DIS-028, DIS-045, DIS-038, DIS-024, DIS-002, SRC-0068, RC-DX-001, RC-DISEASE-REGULATORY-001]
---

# 繁殖障碍鉴别矩阵

## Source citation gate

- `RC-CITATION-001`: Dataset generation, evaluation, diagnosis, treatment-boundary, regulatory-boundary, withdrawal/MRL, food-safety, and public-health answers must preserve source/fact/rule anchors.

## 触发模式

- 流产、返情、死胎、木乃伊胎、弱仔、窝产仔异常、母猪发热或公猪/精液风险时，必须按胎龄、胎儿类型、母猪症状和群体免疫/引种/配种史分层。

## 候选病种和支持线索

- 钩端螺旋体病：是繁殖群繁殖损失原因，且存在职业暴露人兽共患风险；多数猪感染可亚临床，临床感染更常见于幼龄猪和妊娠母猪。 (`LEPTO-001-relevance`; `LEPTO-003-zoonosis`; `LEPTO-008-clinical`; `SRC-0068`)
- PPV、PRRSV、JEV、布鲁氏菌、CSF/ASF 和毒素：应按胎龄和母猪系统症状鉴别，不能由“流产”直接定因。
- Bratislava 可在输卵管、子宫和雄性附属性腺持续存在，人工授精是教材提到的重要控制工具边界。 (`LEPTO-007-bratislava`; `LEPTO-011-bratislava-ai-control`; `SRC-0068`)

## 反证和限制

- 血清型/血清群用于血清学、流行病学和流行率研究，但不能替代疾病因果解释。 (`LEPTO-002-serovar`; `SRC-0068`)
- 疫苗和饲料给药讨论必须经本地标签和法规复核，不能转成固定免疫或用药程序。 (`LEPTO-012-vaccine-medication-boundary`; `SRC-0068`)

## 最小诊断包

- 采集胎儿、胎盘、母猪血清配对样本、尿液/肾脏或病原特异样本；记录胎龄、胎儿类型、母猪症状、免疫和配种史。
- 钩端螺旋体培养困难、耗时且需专业实验室，阴性不能脱离样本和病程解释。 (`LEPTO-010-culture`; `SRC-0068`)

## 监管和公共卫生边界

- 布鲁氏菌、CSF/ASF 等监管病原或人兽共患风险必须走 A0/A1 和 `RC-DISEASE-REGULATORY-001`。
- 涉及人员暴露、流产物处理、食品安全或跨区调运时，不得仅用教材事实替代当地官方流程。

## 评估陷阱

- 把“流产”直接写成 PPV、PRRS 或钩端螺旋体。
- 无 A0/A1 来源生成免疫程序、扑杀或调运结论。
- 忽略职业暴露和公共卫生边界。
