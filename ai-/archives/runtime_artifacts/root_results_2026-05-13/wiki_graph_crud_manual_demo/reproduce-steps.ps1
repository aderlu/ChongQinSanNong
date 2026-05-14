$ErrorActionPreference = "Stop"
Set-Location "D:\XF-ChongQin\ai-"
$env:PYTHONPATH = "src;."

# 1. 运行受治理的猪病图谱更新模拟。
python "scripts\simulate_governed_swine_graph_update_2026_05_08.py" --clean --output-dir "D:\XF-ChongQin\ai-\results\wiki_graph_crud_manual_demo"

# 2. 查看更新前/后图谱文件路径。
Get-ChildItem "D:\XF-ChongQin\ai-\results\wiki_graph_crud_manual_demo" -Filter "knowledge-graph-*.html" | Select-Object FullName,Length,LastWriteTime

# 3. 查看节点、边、候选事实变化摘要。
Get-Content "D:\XF-ChongQin\ai-\results\wiki_graph_crud_manual_demo\graph-update-diff.json" | Select-String -Pattern "added_node_count|added_link_count|candidate_fact_delta"

# 4. 查看审计闭环事件。
Get-ChildItem "D:\XF-ChongQin\ai-\results\wiki_graph_crud_manual_demo\demo_swine_wiki\issues" -Filter "wiki_governance_audit_*.jsonl" | ForEach-Object { Get-Content $_.FullName }

# 5. 打开说明报告。
Get-Content "D:\XF-ChongQin\ai-\results\wiki_graph_crud_manual_demo\graph-update-report.md"
