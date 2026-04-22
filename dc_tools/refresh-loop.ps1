$ErrorActionPreference = 'Stop'

$configPath = Join-Path $PSScriptRoot 'runtime-config.json'
if (-not (Test-Path $configPath)) {
    throw "Missing runtime config: $configPath"
}

$config = Get-Content $configPath -Raw | ConvertFrom-Json
$interval = [int]$config.snapshotIntervalSeconds
if ($interval -lt 1) {
    throw "snapshotIntervalSeconds must be >= 1"
}

Write-Output "[refresh-loop] interval=${interval}s"
Write-Output "[refresh-loop] press Ctrl+C to stop"

while ($true) {
    $start = Get-Date
    Write-Output "[refresh-loop] refresh started: $start"

    # Demo refresh command. Replace with your actual ETL pipeline command.
    python (Join-Path $PSScriptRoot 'create_sample_dbs.py')

    $done = Get-Date
    Write-Output "[refresh-loop] refresh finished: $done"
    Start-Sleep -Seconds $interval
}
