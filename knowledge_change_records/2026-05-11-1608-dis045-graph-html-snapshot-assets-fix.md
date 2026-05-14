# DIS-045 图谱 HTML 快照无节点连线问题修复说明

## 1. 本次修改目标

本次修改目标是修复 `DIS-045-before-knowledge-graph.html` 打开后只显示背景和统计信息，但不显示图谱节点、连线的问题，并将修复方式固化到演示文档中，避免后续再次生成不可独立渲染的 HTML 快照。

问题文件：

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/DIS-045-graph-html-snapshots/DIS-045-before-knowledge-graph.html`

## 2. 修改前存在的问题

用户打开 `DIS-045-before-knowledge-graph.html` 后，页面顶部能显示：

- 已生成 2569 个索引点
- 关系 3151 条

但中间图谱区域只显示底图背景，没有实际节点和连线。

经检查，HTML 文件内部包含图谱数据和统计信息，也包含以下相对路径脚本引用：

- `d3.min.js`
- `rough.min.js`
- `marked.min.js`
- `purify.min.js`
- `graph-wash-helpers.js`
- `graph-wash.js`

但是 `issues/DIS-045-graph-html-snapshots` 目录下原来只有：

- `DIS-045-before-knowledge-graph.html`

缺少同级 JS 渲染依赖。浏览器从快照目录打开 HTML 时无法加载这些脚本，因此图谱渲染逻辑没有执行，表现为“有统计数字、无节点连线”。

## 3. 本次修复内容

### 3.1 补齐当前快照目录依赖

已从正式图谱目录：

- `ai-/knowledge/llm_wiki_swine_authoritative/wiki`

复制以下文件到：

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/DIS-045-graph-html-snapshots`

补齐文件包括：

- `d3.min.js`
- `rough.min.js`
- `marked.min.js`
- `purify.min.js`
- `graph-wash-helpers.js`
- `graph-wash.js`

这样 `DIS-045-before-knowledge-graph.html` 作为快照单独打开时，可以加载同级依赖并渲染节点和连线。

### 3.2 固化到演示文档

修改文档：

- `ai-/knowledge/llm_wiki_swine_authoritative/WIKI_UPDATE_POWERSHELL_DEMO.md`

新增 PowerShell 变量：

- `$script:GraphHtmlAssets`

新增 PowerShell 函数：

- `Copy-Dis045GraphHtmlAssets`

该函数会把正式 `wiki` 目录中的 6 个图谱渲染依赖复制到 `DIS-045-graph-html-snapshots` 目录。

同时更新：

- `Invoke-Dis045GraphBefore`
- `Invoke-Dis045GraphAfterUpdate`

让 before/after HTML 快照生成时自动同步复制 JS 依赖，并在输出中返回 `html_assets` 字段。

## 4. 解决的问题

本次修复解决了以下问题：

- 快照 HTML 不再是孤立文件。
- 打开 `DIS-045-before-knowledge-graph.html` 时可以加载图谱渲染脚本。
- 图谱节点和连线能够正常显示。
- 后续生成 DIS-045 before/after 图谱快照时，会自动带上同级依赖，避免再次出现只有背景没有图谱的情况。
- 现场演示时，可以直接打开快照目录下的 HTML 进行前后对比。

## 5. 本次未修改的内容

本次没有修改图谱数据本身，没有修改 `graph-data.json`、事实库、来源索引、疾病页或药品页。

本次问题是 HTML 快照资产缺失，不是知识图谱数据为空，也不是 DIS-045 入库失败。正式图谱目录中的 `knowledge-graph.html` 和渲染依赖原本是存在的。

## 6. 验证结果

已完成以下验证：

- 检查 `DIS-045-before-knowledge-graph.html`，确认其引用了 6 个相对路径 JS 依赖。
- 检查正式 `wiki` 目录，确认 6 个依赖文件存在。
- 将 6 个依赖复制到 `DIS-045-graph-html-snapshots` 目录。
- 检查快照目录，确认 6 个依赖文件均存在且文件长度正常。
- 检查 `WIKI_UPDATE_POWERSHELL_DEMO.md`，确认新增 `Copy-Dis045GraphHtmlAssets` 函数，并已在 before/after 快照流程中调用。
- 检查常见乱码信号，未发现异常标记。

## 7. 预计效果

后续打开以下文件时，应能看到图谱节点和连线，而不是仅显示背景图：

- `ai-/knowledge/llm_wiki_swine_authoritative/issues/DIS-045-graph-html-snapshots/DIS-045-before-knowledge-graph.html`

后续按演示文档重新生成 before/after HTML 快照时，会同时复制渲染依赖，使快照目录具备独立展示能力。

## 8. 防乱码措施

本次检查和文档修改均使用 UTF-8 读取和写入。演示文档中仍保留 PowerShell UTF-8 设置，避免中文标题、日志和图谱说明在 Windows 终端中发生乱码。
