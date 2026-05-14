# 2026-05-13 Phase13 Phase14 Race Guard And Mojibake Hardening

## 之前存在的问题

- `Phase13` 和 `Phase14` 对上游产物缺少就绪校验。
- 当上游文件尚未稳定落盘、内容为空或读取到空列表时，脚本会继续执行，并生成“0 skeleton”或“0 sample”这类静默假阴性结果。
- `Phase13` 和 `Phase14` 的部分模板文本中存在明显乱码/坏编码字符串，会直接污染生成样本。
- 当前流程里缺少对 mojibake 的硬阻断，导致脏文本可能继续进入 `Phase15/18/16`。

## 修改前代码情况

- `phase13_build_answer_skeletons.py`
  - 直接读取 plan 文件，即使上游计划文件为空也不会阻断。
  - 生成 0 条 skeleton 时，脚本仍会正常写文件并输出 `passed: false`，但不会抛出运行错误。
  - 模板边界文本中存在坏编码中文。

- `phase14_generate_two_stage_samples.py`
  - 直接读取 skeleton 和 plan 文件，没有“最近生成、非空、可用”的校验。
  - 即使 0 样本也可能继续输出，缺少强阻断。
  - 问题模板、边界模板、fallback 文本中存在坏编码中文。
  - 没有样本级乱码检测。

## 本次修改

- 在 `Phase13` 中新增：
  - 上游 plan 文件存在、非空、最近生成的校验。
  - 0 skeleton 强阻断。
  - mojibake 检测，坏编码 boundary/claim 不再进入 skeleton。

- 在 `Phase14` 中新增：
  - 上游 skeleton/plan 文件存在、非空、最近生成的校验。
  - 0 sample 强阻断。
  - 样本级 mojibake 检测。
  - 将硬编码坏中文模板改成干净中文模板。

## 解决了什么

- 防止 `Phase13`/`Phase14` 在上游未完成时读到空文件还继续执行。
- 防止“看起来跑完了，实际上产物是 0 条”的静默失败。
- 防止脚本自身硬编码模板继续制造乱码样本。
- 在样本进入评估和导出前，增加了第一层编码质量硬闸门。

## 更新文件

- [phase13_build_answer_skeletons.py](/D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase13_build_answer_skeletons.py)
- [phase14_generate_two_stage_samples.py](/D:/XF-ChongQin/ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py)
- [2026-05-13-phase13-phase14-race-guard-and-mojibake-hardening.md](/D:/XF-ChongQin/knowledge_change_records/2026-05-13-phase13-phase14-race-guard-and-mojibake-hardening.md)

## 预计效果

- 运行时稳定性更高，跨阶段竞态更容易被第一时间发现。
- 空产物会从“软失败”变成“显式失败”，便于排查和汇报。
- 明显乱码文本不再轻易进入后续 `Phase15/18/16`。
- 为后续继续做全链路 UTF-8 清洗和高质量数据生成提供更干净的入口。
