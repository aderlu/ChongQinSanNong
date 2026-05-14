param(
    [string]$TaskName = "SwineDiseaseLLMWikiWeeklyMaintenance",
    [string]$ProjectRoot = "D:\XF-ChongQin\ai-",
    [string]$WikiDir = "D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative",
    [string]$ProtocolFile = "D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\swine_wiki_diseases_drugs_deep_gap_review_2026-05-08.md",
    [ValidateSet("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")]
    [string]$DayOfWeek = "Monday",
    [string]$At = "03:00"
)

$ErrorActionPreference = "Stop"

$runner = Join-Path $ProjectRoot "scripts\run_llm_wiki_weekly_maintenance.ps1"
if (-not (Test-Path $runner)) {
    throw "Weekly maintenance runner was not found: $runner"
}

if (-not $env:NONELINEAR_API_KEY) {
    $env:NONELINEAR_API_KEY = [Environment]::GetEnvironmentVariable("NONELINEAR_API_KEY", "User")
}

if (-not $env:NONELINEAR_API_KEY) {
    Write-Warning "NONELINEAR_API_KEY is not available in this session. The task can be registered, but the user or system environment variable must exist before the task runs."
}

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$runner`" -ProjectRoot `"$ProjectRoot`" -WikiDir `"$WikiDir`" -ProtocolFile `"$ProtocolFile`""

# Use a weekly trigger. The CLI command executes one maintenance pass;
# the Windows scheduled task controls how often that pass is run.
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $DayOfWeek -At $At
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Description "Weekly Nonelinear gpt-5.4-mini-medium maintenance for the swine disease LLM Wiki, gap-review-first." `
    -Force | Out-Null

Write-Host "Registered weekly maintenance task: $TaskName"
Write-Host "Schedule: every $DayOfWeek at $At"
Write-Host "Runner: $runner"
Write-Host "WikiDir: $WikiDir"
Write-Host "ProtocolFile: $ProtocolFile"
