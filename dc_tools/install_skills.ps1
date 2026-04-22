$ErrorActionPreference = 'Stop'

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = $PSScriptRoot
$targetRoot = Join-Path $workspaceRoot '.roo\skills'

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

$tools = @('tool1','tool2','tool3')

foreach ($tool in $tools) {
    $srcSkill = Join-Path $sourceRoot "$tool\SKILL.md"
    if (-not (Test-Path $srcSkill)) {
        Write-Warning "Missing: $srcSkill"
        continue
    }

    $dstDir = Join-Path $targetRoot $tool
    New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
    Copy-Item -Force $srcSkill (Join-Path $dstDir 'SKILL.md')

    Write-Output "Installed skill: $tool -> $dstDir"
}

Write-Output "Done. Restart Roo chat/session or start a new task so skills are rediscovered."
