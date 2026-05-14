param(
    [string]$ProjectRoot = "D:\XF-ChongQin\ai-",
    [string]$Python = "python",
    [string]$WikiDir = "D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative",
    [string]$ProtocolFile = "D:\XF-ChongQin\ai-\knowledge\llm_wiki_swine_authoritative\issues\swine_wiki_diseases_drugs_deep_gap_review_2026-05-08.md"
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot
$env:PYTHONPATH = "src;."

if (-not $env:NONELINEAR_API_KEY) {
    $env:NONELINEAR_API_KEY = [Environment]::GetEnvironmentVariable("NONELINEAR_API_KEY", "User")
}

if (-not $env:NONELINEAR_API_KEY) {
    throw "Missing NONELINEAR_API_KEY. Set the third-party LLM API key as a user or system environment variable first."
}

$logDir = Join-Path $ProjectRoot "results\llm_wiki_maintenance"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logPath = Join-Path $logDir "weekly-maintain-$stamp.json"

# The CLI subcommand is named daily-maintain because it executes one
# maintenance pass. This scheduled runner makes that pass run weekly.
& $Python -m chicken_data_synthesis.wiki_cli --json --wiki-dir "$WikiDir" daily-maintain `
    --base-url "https://api.nonelinear.com/v1" `
    --model "gpt-5.4-mini-medium" `
    --protocol-file "$ProtocolFile" `
    *> $logPath

if ($LASTEXITCODE -ne 0) {
    throw "LLM Wiki weekly maintenance failed. See $logPath"
}

Write-Host "Swine LLM Wiki weekly maintenance completed: $logPath"
Write-Host "WikiDir: $WikiDir"
Write-Host "ProtocolFile: $ProtocolFile"
