# Worker A 疾病实体页状态清洗留痕

## 之前问题
- 疾病实体页中重复堆叠了 Runtime task use、gold dataset role、页面状态、可用边界、运行时层级等状态描述。
- 部分页面把 source/fact/anchor 边界与可用范围说明拆散在多段重复模板里，阅读负担偏高。
- 少量页存在状态字段与边界说明混写，影响后续按简化模型抽取 source_trust / evidence_coverage / usage_scope。

## 修改范围
- 仅处理 `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\diseases` 下疾病实体页。
- 未修改其他目录，也未回退他人改动。
- 保留事实证据、source anchors、fact anchors、rule card 边界和证据扩展索引。

## 修改后解决什么
- 将历史状态描述收敛为 `source_trust / evidence_coverage / usage_scope`。
- 删除或压缩重复的 Runtime task use、gold dataset role、页面状态、可用边界等冗余说明。
- 让页面状态更适合检索、回收和边界校验，同时保持医学事实与监管边界不丢失。

## 修改内容
- 清洗疾病页状态模板与重复说明。
- 保留并压缩 source/fact/page 锚点说明。
- 保留缺失栏目与 source-coverage gap 的边界提示。
- 保留监管、用药、休药期、MRL、食品安全相关的规则卡边界。

## 涉及文件
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\wiki\diseases\*.md`

## 预计效果
- 疾病页默认状态更短、更一致。
- 后续抽取、召回、审校时更容易定位 source_trust、coverage 和可用范围。
- 降低重复模板对医学事实和边界信息的干扰。

## 编码措施
- 全部按 UTF-8 写回。
- 仅做状态层压缩，不改动事实锚点与证据来源。
- 对部分页面保留 partial 语义，对 reviewed 页面保留临床知识页边界。