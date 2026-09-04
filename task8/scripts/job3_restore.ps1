[CmdletBinding()]
param(
    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$Branch = "master",

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$WorkDirectory = "C:/Users/Dmitry/JenkinsWork/task8-project"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$gitExecutable = (Get-Command git -CommandType Application -ErrorAction Stop).Source

function Invoke-Git {
    param(
        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    & $script:gitExecutable @Arguments

    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed with exit code ${LASTEXITCODE}: git $($Arguments -join ' ')"
    }
}

$projectPath = [System.IO.Path]::GetFullPath($WorkDirectory)
$gitDirectory = Join-Path $projectPath ".git"

if (-not (Test-Path -LiteralPath $gitDirectory -PathType Container)) {
    throw "Job_1 must prepare the Git repository before Job_3 runs: $projectPath"
}

$relativeFiles = @(
    "task8/demo/delete_me_1.txt",
    "task8/demo/delete_me_2.txt"
)

Write-Host "[Job_3] Fetching origin/$Branch"
Invoke-Git -Arguments @("-C", $projectPath, "fetch", "--prune", "origin", $Branch)

$restoreArguments = @(
    "-C", $projectPath,
    "restore", "--source", "origin/$Branch", "--staged", "--worktree", "--"
) + $relativeFiles
Invoke-Git -Arguments $restoreArguments

foreach ($relativeFile in $relativeFiles) {
    $fullPath = Join-Path $projectPath $relativeFile

    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        throw "Git did not restore the expected file: $relativeFile"
    }

    Write-Host "[Job_3] Restored $relativeFile"
}

$verifyArguments = @(
    "-C", $projectPath,
    "diff", "--exit-code", "origin/$Branch", "--"
) + $relativeFiles
Invoke-Git -Arguments $verifyArguments

$keepFile = Join-Path $projectPath "task8/demo/keep.txt"

if (-not (Test-Path -LiteralPath $keepFile -PathType Leaf)) {
    throw "The safety file is missing: task8/demo/keep.txt"
}

Write-Host "[Job_3] Verified: the demonstration files match origin/$Branch."
