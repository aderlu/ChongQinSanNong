# 2026-05-14 Phase14 运行时导入路径修复记录

## 修改背景

执行真实全链路时，Phase14 通过根目录兼容脚本 `tools/phase14_generate_two_stage_samples.py` 加载 `tools/pipeline/phase14_generate_two_stage_samples.py`。pipeline 文件内部需要导入同目录的 `consultation_case_variables.py`。

实际运行 `--help` 时触发错误：

```text
ModuleNotFoundError: No module named 'consultation_case_variables'
```

## 修改前代码行为

目标文件：

`ai-/knowledge/llm_wiki_swine_authoritative/tools/pipeline/phase14_generate_two_stage_samples.py`

修改前行为：

- 根兼容脚本只把 `tools` 目录加入 `sys.path`。
- pipeline 文件直接执行 `from consultation_case_variables import ...`。
- 当通过兼容加载器加载 pipeline 文件时，`tools/pipeline` 不一定在 `sys.path` 中，导致真实运行链路中断。

## 本次修改内容

在 Phase14 pipeline 文件顶部新增：

```python
PIPELINE_DIR = Path(__file__).resolve().parent
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))
```

## 解决的问题

- 修复 Phase14 真实执行时无法导入同目录辅助模块的问题。
- 保持根兼容脚本和 pipeline 新主链路都可运行。
- 不改变生成逻辑，只修复运行时阻塞。

## 预期效果

- Phase14 `--help` 和真实 API 生成命令可以正常启动。
- 后续 8 并发 40 条真实生成链路不再被导入错误阻断。

## 编码与清理

- 文件保持 UTF-8。
- 未新增临时脚本。
- 此修复是最小运行时修复，未改动业务生成规则。
