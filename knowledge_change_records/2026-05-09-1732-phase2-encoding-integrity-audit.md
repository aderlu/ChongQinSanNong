# Phase 2 Encoding Integrity Audit

Date: 2026-05-09

## 修改目标和范围

执行猪病 LLM Wiki 清洗整理的 Phase 2：建立可重复运行的编码完整性审计，识别 UTF-8 解码错误、replacement character 和 mojibake-like 内容，防止后续清洗过程把中文实体名、疾病名、药物名、来源标题和证据锚点写成乱码。

新增文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/tools/audit_encoding_integrity.py`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/encoding_integrity_audit_2026-05-09.json`
- `ai-/knowledge/llm_wiki_swine_authoritative/issues/encoding_integrity_audit_2026-05-09.md`

## 修改前存在的问题

执行文档已要求防乱码，但知识库内没有专门的、可重复运行的编码完整性审计脚本。此前只能依赖临时命令扫描，难以稳定回答：

- runtime manifest 内是否存在编码损坏文件。
- 损坏是在 production runtime，还是只在 raw/issues 历史材料中。
- 哪些文件含有 `�` 替换字符。
- 哪些文件含有高频 mojibake-like 模式。

## 修改前代码和文件状态

修改前 `tools/` 中已有 readiness、manifest、hallucination risk 等维护工具，但没有独立的 `audit_encoding_integrity.py`。

Phase 1 修改根文件时已采取 UTF-8 读写；Phase 2 需要把这个检查固化成脚本。

## 本次更新或新增了什么代码

新增 `tools/audit_encoding_integrity.py`。

脚本特性：

- 显式用 UTF-8 读取和写入。
- 扫描 `.md`、`.txt`、`.json`、`.csv`、`.yaml`、`.yml`、`.py`、`.ps1`、`.toml`。
- 加载 `exports/runtime_core_manifest.json`，标记损坏文件是否属于默认 runtime。
- 检查 UTF-8 解码错误。
- 检查 replacement character `�`。
- 检查常见 mojibake-like 模式。
- 输出 JSON 和 Markdown 报告。
- JSON 输出使用 `ensure_ascii=False`。
- 报告中的损坏行预览使用 `unicode_escape` 转义，避免审计报告自身写入 replacement character 后在下一轮扫描中产生自举噪声。
- 跳过当前编码审计报告自身，避免工具输出被工具再次计入损坏输入。

## 本次进行了什么整理工作

运行：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
```

生成：

- `issues/encoding_integrity_audit_2026-05-09.json`
- `issues/encoding_integrity_audit_2026-05-09.md`

首次审计结果：

- text_files_scanned: 1668。
- runtime_manifest_paths_loaded: 198。
- encoding_ok: 1657。
- decode_or_replacement_damage: 3。
- mojibake_like_content: 0。
- minor_mojibake_signal: 8。
- runtime_damaged_count: 0。

修复报告自举噪声后复跑结果：

- text_files_scanned: 1670。
- runtime_manifest_paths_loaded: 198。
- encoding_ok: 1659。
- decode_or_replacement_damage: 3。
- mojibake_like_content: 0。
- minor_mojibake_signal: 8。
- runtime_damaged_count: 0。

发现的高风险损坏文件：

- `issues/phase2_encoding_quarantine_2026-05-09.json`
- `issues/wiki_diseases_comparisons_drugs_mojibake_audit_2026-05-08.md`
- `raw/md/猪场兽药使用与猪病防治技术200-363页.md`

这些文件均不属于 runtime manifest 默认加载路径。

## 修改后解决了什么

- Phase 2 有了可重复运行的编码检查工具。
- 可以明确说明默认生产/评估 runtime 当前没有编码损坏文件。
- 可以把 raw/issues 中的损坏文件隔离为后续重处理对象，而不是让它们影响本轮运行时清洗。
- 后续每轮实体页整理前后都可以运行同一脚本做回归检查。

## 预计更新效果

- 降低 Windows/PowerShell 环境下中文被误写成乱码的风险。
- 降低损坏 raw/md 被重新抽取为事实的风险。
- 提高后续清洗过程的可审计性和可汇报性。

## 验证

已运行：

```powershell
python knowledge\llm_wiki_swine_authoritative\tools\audit_encoding_integrity.py
python knowledge\llm_wiki_swine_authoritative\tools\build_runtime_core_manifest.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_runtime_hallucination_risk.py
python knowledge\llm_wiki_swine_authoritative\tools\audit_swine_llm_wiki_readiness.py
```

结果：

- runtime_damaged_count: 0。
- runtime manifest entries: 198。
- runtime manifest missing_paths: 0。
- hallucination risk high: 0。
- hallucination risk medium: 0。
- readiness_score: 99。
- missing_paths: 0。
- bad_fact_tables: []。

## 残余风险和下一步

本阶段没有修复 raw/issues 中已损坏文件，只完成识别和隔离判断。

下一步：

- 对损坏 raw/md 文件从原始 PDF 或备份重新转换。
- 对历史 issue 中的 replacement 字符保留为历史问题记录，不进入 runtime。
- 后续 Phase 4 整理 disease/drug 实体页前后都运行该脚本，确保 runtime_damaged_count 保持 0。
