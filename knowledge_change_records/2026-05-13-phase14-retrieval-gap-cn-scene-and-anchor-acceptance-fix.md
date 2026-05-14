# Phase14 检索缺口样本中文场景化与锚点放行修复记录

- 日期：2026-05-13
- 目标：补齐 `retrieval_gap_or_eval` 类样本的真实中文问诊表达，并修复阶段14中事实锚点被过度拦截导致的样本短缺问题。

## 之前存在的问题

1. `L1_retrieval_grounded` 中 `retrieval_gap_or_eval` 计划虽然已经进入计划与骨架，但最终真实生成时会少于 10 条，导致四路并行产出不稳定。
2. 该类样本的问句仍偏内部评估语气，不够像真实的中国猪场兽医问诊。
3. `anchor_from_claim()` 对事实锚点的可用性判断过严，要求事实锚点与 rule card 同时满足，导致部分本可落样本被判为不可用。

## 本次修改

修改文件：
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase14_generate_two_stage_samples.py`

更新内容：
- 为 `L1_retrieval_grounded + retrieval_gap_or_eval` 增加中文现场问诊式问题模板。
- 将事实锚点的可用性判断改为“事实锚点成立即可”，不再强制依赖 rule card。

## 修改后解决了什么

- 让检索缺口/评估类样本也能稳定进入真实生成链路。
- 让问句更贴近中国猪场兽医现场咨询场景。
- 降低因锚点判定过严导致的样本丢失风险。

## 预计效果

- 四路并行生成更接近 40 条完整输出。
- 生成样本的中文场景感更强，适合后续 SFT 与评估数据使用。
- 相关短缺问题会显著减少。
