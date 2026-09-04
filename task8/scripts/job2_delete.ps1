[CmdletBinding()]
param(
    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$WorkDirectory = "C:/Users/Dmitry/JenkinsWork/task8-project"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$gitExecutable = (Get-Command git -CommandType Application -ErrorAction Stop).Source
$projectPath = [System.IO.Path]::GetFullPath($WorkDirectory)
$gitDirectory = Join-Path $projectPath ".git"

if (-not (Test-Path -LiteralPath $gitDirectory -PathType Container)) {
    throw "Job_1 must prepare the Git repository before Job_2 runs: $projectPath"
}

$relativeFiles = @(
    "task8/demo/delete_me_1.txt",
    "task8/demo/delete_me_2.txt"
)

$trimCharacters = [char[]]@(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
)
$projectPrefix = $projectPath.TrimEnd($trimCharacters) + [System.IO.Path]::DirectorySeparatorChar

foreach ($relativeFile in $relativeFiles) {
    $targetPath = [System.IO.Path]::GetFullPath((Join-Path $projectPath $relativeFile))

    if (-not $targetPath.StartsWith(
        $projectPrefix,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw "Refusing to delete a path outside the Jenkins project: $targetPath"
    }

    if (-not (Test-Path -LiteralPath $targetPath -PathType Leaf)) {
        throw "Expected demonstration file does not exist: $targetPath"
    }

    Remove-Item -LiteralPath $targetPath -Force
    Write-Host "[Job_2] Removed $relativeFile"
}

$keepFile = Join-Path $projectPath "task8/demo/keep.txt"

if (-not (Test-Path -LiteralPath $keepFile -PathType Leaf)) {
    throw "The safety file must not be removed: task8/demo/keep.txt"
}

$diffArguments = @(
    "-C", $projectPath,
    "diff", "--name-only", "--diff-filter=D", "--"
) + $relativeFiles
$deletedFiles = @(& $gitExecutable @diffArguments)

if ($LASTEXITCODE -ne 0) {
    throw "Cannot verify the deleted files with Git."
}

foreach ($relativeFile in $relativeFiles) {
    if ($deletedFiles -notcontains $relativeFile) {
        throw "Git does not report the expected file as deleted: $relativeFile"
    }
}

Write-Host "[Job_2] Verified: exactly the two demonstration files are absent."
