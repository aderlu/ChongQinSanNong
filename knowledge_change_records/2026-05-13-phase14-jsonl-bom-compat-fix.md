# Phase14 JSONL BOM 兼容修复记录

- 日期：2026-05-13
- 目标：解决 Phase14 在读取计划或骨架 JSONL 时，因 UTF-8 BOM 导致的首行解析失败问题。

## 之前存在的问题

- `phase14_generate_two_stage_samples.py` 的 `read_jsonl()` 只按 `utf-8` 读取。
- 某些通过 PowerShell 或外部工具写出的 JSONL 文件带有 BOM，导致 `json.loads()` 在第一行报错：
  `Unexpected UTF-8 BOM (decode using utf-8-sig)`
- 这会直接中断 real-api 生成流程，影响四路并行重跑。

## 本次修改

修改文件：
- `D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\tools\phase14_generate_two_stage_samples.py`

更新内容：
- 将 JSONL 读取编码改为 `utf-8-sig`
- 对单行内容增加 `lstrip("\ufeff")`，提高兼容性

## 修改后解决了什么

- 计划和骨架文件即使带 BOM，也能正常读取。
- 四路并行 real-api 生成不再被首行编码头阻断。

## 预计效果

- 降低 Windows 环境下的脚本失败率。
- 提高批量生成与重跑稳定性。
