# normalize_wiki_entity_status.py 注释补充说明

时间：2026-05-12

## 一、修改前存在的问题

`tools/normalize_wiki_entity_status.py` 已经承担实体页状态规范化工作，但代码注释较少。后续维护者不容易直接看出：

1. 为什么只处理 diseases、drugs、comparisons、syndromes、synthesis。
2. `source_trust/evidence_coverage/usage_scope` 三字段各自含义是什么。
3. 为什么旧状态会被折叠为 `authoritative`、`complete`、`partial`。
4. 哪些正文内容可以删除，哪些医学安全边界必须保留。
5. `positive_drug_candidate`、`gold_candidate` 等页面级用途不等于边级 verified。

## 二、本次修改内容

修改文件：

- `tools/normalize_wiki_entity_status.py`

新增内容：

1. 增加目标目录说明，避免误清洗 source/rule 类页面。
2. 为每个函数补充 docstring，解释输入、输出和设计原因。
3. 在 `infer_status` 中补充页面类型、旧状态映射、usage_scope 推断逻辑说明。
4. 明确 `retrieval`、`diagnosis_support`、`differential_support`、`control_support`、`drug_boundary`、`positive_drug_candidate`、`gold_candidate` 的页面级含义。
5. 说明脚本不会判断具体医学关系是否成立，关系边仍需 edge validator/source alignment/medical entailment。
6. 说明正文清理只删除历史模板噪声，不删除 source_id/fact_id/anchor、药物禁用、剂量、休药期、MRL 和监管限制。

## 三、修改后解决的问题

- 提高脚本可读性，方便后续维护和汇报。
- 降低误用脚本导致医学安全边界被删除的风险。
- 让后续 GPT 或开发者能理解页面级 usage_scope 与边级 verified 的区别。

## 四、验证结果

已执行：

```powershell
py -m py_compile tools/normalize_wiki_entity_status.py
py tools/normalize_wiki_entity_status.py
py tools/audit_encoding_integrity.py
```

结果：

- Python 编译通过。
- 脚本重复运行结果为 `normalized_files=0`，说明本次只补充注释，没有改变实体页清洗结果。
- 编码审计通过，未引入乱码。

## 五、预计效果

后续维护者可以直接从代码注释理解状态简化规则，减少重复解释成本，并能更安全地扩展 usage_scope 判断逻辑。
