[CmdletBinding()]
param(
    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$RepositoryUrl = "https://github.com/DmitryBat9/test_for_devops.git",

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
$parentDirectory = [System.IO.Directory]::GetParent($projectPath)

if ($null -eq $parentDirectory) {
    throw "Cannot determine the parent directory for: $projectPath"
}

New-Item -ItemType Directory -Path $parentDirectory.FullName -Force | Out-Null

$gitDirectory = Join-Path $projectPath ".git"

if (Test-Path -LiteralPath $gitDirectory -PathType Container) {
    $actualOrigin = (& $gitExecutable -C $projectPath remote get-url origin).Trim()

    if ($LASTEXITCODE -ne 0) {
        throw "Cannot read the origin URL from: $projectPath"
    }

    if ($actualOrigin -ne $RepositoryUrl) {
        throw "The existing directory belongs to another repository. Expected '$RepositoryUrl', found '$actualOrigin'."
    }

    Write-Host "[Job_1] Updating the existing repository in $projectPath"
    Invoke-Git -Arguments @("-C", $projectPath, "fetch", "--prune", "origin", $Branch)
    Invoke-Git -Arguments @("-C", $projectPath, "checkout", $Branch)

    $demoFiles = @(
        "task8/demo/delete_me_1.txt",
        "task8/demo/delete_me_2.txt"
    )
    $restoreArguments = @(
        "-C", $projectPath,
        "restore", "--source", "origin/$Branch", "--staged", "--worktree", "--"
    ) + $demoFiles

    Invoke-Git -Arguments $restoreArguments
    Invoke-Git -Arguments @("-C", $projectPath, "merge", "--ff-only", "origin/$Branch")
}
else {
    if (Test-Path -LiteralPath $projectPath -PathType Container) {
        $existingItems = @(Get-ChildItem -LiteralPath $projectPath -Force)

        if ($existingItems.Count -gt 0) {
            throw "The target directory exists, is not empty, and is not a Git repository: $projectPath"
        }
    }

    Write-Host "[Job_1] Cloning branch '$Branch' into $projectPath"
    Invoke-Git -Arguments @(
        "clone", "--branch", $Branch, "--single-branch",
        $RepositoryUrl, $projectPath
    )
}

$requiredFiles = @(
    "task8/demo/keep.txt",
    "task8/demo/delete_me_1.txt",
    "task8/demo/delete_me_2.txt"
)

foreach ($relativeFile in $requiredFiles) {
    $fullPath = Join-Path $projectPath $relativeFile

    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        throw "Required file was not checked out: $relativeFile"
    }
}

$headCommit = (& $gitExecutable -C $projectPath rev-parse --short HEAD).Trim()

if ($LASTEXITCODE -ne 0) {
    throw "Cannot determine the checked-out commit."
}

Write-Host "[Job_1] Branch '$Branch' is ready at commit $headCommit"
