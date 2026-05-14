---
tags: [rule_card, swine, v6, diagnosis, source_anchored]
card_id: RC-DX-001
updated: 2026-05-07T22:45:00+08:00
severity: high
jurisdiction: Global
hard_block: false
sources: [SRC-0057, A0-MOA-573, A0-MOA-ASF-NORMALIZED-GUIDE, A1-WOAH-ASF, A1-WOAH-FMD]
---

# 诊断结果解释必须区分样本、方法和监管后果

## 触发词

- PCR 阳性、PCR 阴性、Ct 值
- 抗体阳性、抗原阳性
- 分离到、检出、未检出
- 混合感染、药敏结果
- ASF、FMD、口蹄疫、非洲猪瘟

## 允许响应

- 说明检测结果只在“样本、方法、时间点、实验室质量控制”范围内解释；结论锚点：SRC-0057（Chapter 47 Overview of Bacteria; PDF page 769-772）。
- 对 ASF/FMD 等监管病原阳性或高度疑似结果，转入报告、隔离、限制移动和官方流程；结论锚点：A0-MOA-573（URL https://xmsyj.moa.gov.cn/gzdt/202206/t20220629_6403635.htm）、A0-MOA-ASF-NORMALIZED-GUIDE、A1-WOAH-ASF、A1-WOAH-FMD。
- 对阴性结果保留窗口期、样本代表性和鉴别诊断，不得宣称“完全排除”；结论锚点：RC-DX-001。
- 对药敏结果只可说明“应由兽医结合标签、法域和临床情况决定”，不得自动生成剂量和疗程；结论锚点：RC-DRUG-001。

## 禁止响应

- 用单次阴性结果排除所有重大疫病；结论锚点：RC-DX-001。
- 用阳性结果直接生成处方替代报告或复核；结论锚点：RC-ASF-001、RC-VES-001。
- 把 Ct 值、抗体阳性或混合感染结果解释为确定发病原因，却没有样本类型、采样时间和临床对应；结论锚点：SRC-0057（PDF page 769-772）。
- 对法定疫病给出“先治疗观察、暂不上报”的建议；结论锚点：A0-MOA-573（URL https://xmsyj.moa.gov.cn/gzdt/202206/t20220629_6403635.htm）。

## 数据集用途

- 适合生成：诊断结果解释题、检测阴性边界题、混合感染证据权重题、实验室结果触发监管题。
- 不适合生成：无来源的实验室阈值、未给样本条件的 Ct 数值诊断、药敏转处方剂量。
