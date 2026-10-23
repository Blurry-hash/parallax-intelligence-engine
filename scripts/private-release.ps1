# PARALLAX v10.0 | Windows PowerShell 5.1+ | ZIP auto-discovery + preserve repository visibility.
# This script makes GitHub file changes ONLY with -Apply. It NEVER changes repository visibility.
# Dry-run: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\private-release.ps1
# Apply:   powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\private-release.ps1 -Apply
# Custom:  ... -ZipPath "C:\path\parallax-intelligence-engine-v10.0-private.zip" -Apply
# -SkipPush confirms repo access without pushing; it never edits any repository settings.
[CmdletBinding()]
param(
  [switch]$Apply,
  [switch]$SkipPush,
  [string]$ProjectRoot,
  [string]$ZipPath
)
$ErrorActionPreference = 'Stop'
$owner = 'Blurry-hash'
$oldRepo = "$owner/aiontrix-universal-intelligence" # Historical GitHub remote slug only.
$newRepo = "$owner/parallax-intelligence-engine"
$script:GhExecutable = $null
$script:GitExecutable = $null
$tempRoot = $null

function Get-Executable {
  param([Parameter(Mandatory=$true)][string]$Name)
  $result = Get-Command -Name "$Name.exe" -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
  if (-not $result) { throw "$Name.exe was not found in PATH. Install $Name and open a new terminal." }
  return $result.Source
}
function Invoke-GhCli {
  param([Parameter(Mandatory=$true)][string[]]$Arguments)
  $result = & $script:GhExecutable @Arguments
  if ($LASTEXITCODE -ne 0) { throw "GitHub CLI failed (exit $LASTEXITCODE): gh $($Arguments -join ' ')" }
  return $result
}
function Invoke-GitCli {
  param([Parameter(Mandatory=$true)][string[]]$Arguments)
  $result = & $script:GitExecutable @Arguments
  if ($LASTEXITCODE -ne 0) { throw "Git failed (exit $LASTEXITCODE): git $($Arguments -join ' ')" }
  return $result
}
function Assert-ProjectRoot {
  param([Parameter(Mandatory=$true)][string]$Path)
  $resolved = (Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
  foreach ($required in @('README.md','MASTER_PROMPT.md','AGENTS.md','skills','docs/execution-backends.md','skills/browser-compute-bridge/SKILL.md','skills/video-temporal-consistency/SKILL.md','docs/video-v10.md','tools/video_qc.py')) {
    if (-not (Test-Path -LiteralPath (Join-Path $resolved $required))) {
      throw "Incomplete or outdated PARALLAX project: missing $required in $resolved. Download the latest v10 ZIP. No GitHub changes made."
    }
  }
  return $resolved
}
function Find-ReleaseZip {
  param([string]$Requested)
  if ($Requested) {
    if (-not (Test-Path -LiteralPath $Requested -PathType Leaf)) { throw "ZIP does not exist: $Requested" }
    return (Resolve-Path -LiteralPath $Requested).Path
  }
  $bases = @($PSScriptRoot, (Split-Path -Parent $PSScriptRoot), (Get-Location).Path,
    (Join-Path $env:USERPROFILE 'Downloads'), (Join-Path $env:USERPROFILE 'Desktop'))
  $archives = @()
  foreach ($base in ($bases | Where-Object { $_ } | Select-Object -Unique)) {
    if (Test-Path -LiteralPath $base -PathType Container) {
      $archives += @(Get-ChildItem -LiteralPath $base -Filter 'parallax-intelligence-engine*.zip' -File -ErrorAction SilentlyContinue)
    }
  }
  if ($archives.Count -eq 0) {
    throw 'PARALLAX ZIP not found. Download the v10 ZIP to Downloads, or specify -ZipPath. No GitHub changes made.'
  }
  # Prefer highest release version, then newest timestamp. Avoid choosing an older renamed ZIP merely because it was copied recently.
  $ranked = @($archives | Sort-Object -Property @{Expression={
    if ($_.Name -match '-v(\d+(?:\.\d+){0,2})') {
      $bits = @($Matches[1].Split('.')); while ($bits.Count -lt 3) { $bits += '0' }
      [version]::new([int]$bits[0],[int]$bits[1],[int]$bits[2])
    } else { [version]::new(0,0,0) }
  };Descending=$true}, @{Expression={$_.LastWriteTimeUtc};Descending=$true})
  return $ranked[0].FullName
}
function Expand-VerifiedRelease {
  param([Parameter(Mandatory=$true)][string]$Path)
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $archive = [System.IO.Compression.ZipFile]::OpenRead($Path)
  try {
    foreach ($entry in $archive.Entries) {
      $name = $entry.FullName.Replace('\','/')
      if ($name.StartsWith('/') -or $name -match '^[a-zA-Z]:' -or $name -match '(^|/)\.\.(/|$)' -or $name.Contains(':')) {
        throw "Unsafe ZIP entry: $name. No GitHub changes made."
      }
    }
  } finally { $archive.Dispose() }
  $script:tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("parallax-release-" + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $script:tempRoot -Force | Out-Null
  Expand-Archive -LiteralPath $Path -DestinationPath $script:tempRoot -Force
  $root = Join-Path $script:tempRoot 'parallax-intelligence-engine'
  if (-not (Test-Path -LiteralPath $root -PathType Container)) { $root = $script:tempRoot }
  return Assert-ProjectRoot -Path $root
}
function Get-OwnedRepositories {
  # For this personal account, the owner-scoped repo list is the intended set; cap is explicit.
  $raw = (Invoke-GhCli -Arguments @('repo','list',$owner,'--limit','1000','--json','nameWithOwner,isPrivate')) | Out-String
  $repos = @($raw | ConvertFrom-Json)
  if ($repos.Count -ge 1000) { throw 'Repository list truncated at 1000. Stop; handle pagination before changes.' }
  return @($repos | Where-Object { $_.nameWithOwner -like "$owner/*" })
}

try {
  $script:GhExecutable = Get-Executable 'gh'
  $script:GitExecutable = Get-Executable 'git'
  $project = $null
  if (-not $SkipPush) {
    if ($ProjectRoot) { $project = Assert-ProjectRoot -Path $ProjectRoot }
    else {
      $chosenZip = Find-ReleaseZip -Requested $ZipPath
      Write-Host "ZIP selected: $chosenZip"
      $project = Expand-VerifiedRelease -Path $chosenZip
    }
    Write-Host "Validated project: $project"
  }
  Invoke-GhCli -Arguments @('auth','status') | Out-Null
  $login = ((Invoke-GhCli -Arguments @('api','user','--jq','.login')) | Out-String).Trim()
  if ($login -ne $owner) { throw "Logged in as '$login'; expected '$owner'. No GitHub changes made." }
  $repos = @(Get-OwnedRepositories)
  $names = @($repos | ForEach-Object { $_.nameWithOwner })
  if (($names -contains $oldRepo) -and ($names -contains $newRepo)) { throw 'Both old and new repo names exist. Stop to avoid overwriting.' }
  if (($names -notcontains $oldRepo) -and ($names -notcontains $newRepo)) { throw 'Target repo does not exist. No GitHub changes made.' }
  $targetRepo = if ($names -contains $newRepo) { $newRepo } else { $oldRepo }
  $isPrivate = ((Invoke-GhCli -Arguments @('repo','view',$targetRepo,'--json','isPrivate','--jq','.isPrivate')) | Out-String).Trim()
  Write-Host "Target: $targetRepo | Current visibility: $(if ($isPrivate -eq 'true') { 'PRIVATE' } else { 'PUBLIC' })"
  Write-Host 'Repository visibility will NOT be changed.'
  if (-not $Apply) {
    Write-Host 'DRY RUN ONLY: No GitHub settings or files changed. Add -Apply after reviewing output.'
    return
  }
  if ($targetRepo -ne $newRepo) {
    throw "The target repository is still named $oldRepo. Rename it separately and retry; no remote changes made."
  }
  if (-not $SkipPush) {
    Invoke-GhCli -Arguments @('auth','setup-git') | Out-Null
    $cloneDir = Join-Path $script:tempRoot 'checkout'
    if (-not $script:tempRoot) {
      $script:tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("parallax-release-" + [guid]::NewGuid().ToString('N'))
      New-Item -ItemType Directory -Path $script:tempRoot -Force | Out-Null
      $cloneDir = Join-Path $script:tempRoot 'checkout'
    }
    Invoke-GitCli -Arguments @('clone',"https://github.com/$newRepo.git",$cloneDir) | Out-Null
    # Clone first: this retains any pre-existing history and avoids destructive force pushes.
    $branch = ((Invoke-GhCli -Arguments @('repo','view',$newRepo,'--json','defaultBranchRef','--jq','.defaultBranchRef.name')) | Out-String).Trim()
    if (-not $branch -or $branch -eq 'null') { $branch = 'main' }
    $ignored = @('.git','__pycache__','.pytest_cache','.venv','node_modules')
    foreach ($item in (Get-ChildItem -LiteralPath $project -Force)) {
      if ($ignored -contains $item.Name) { continue }
      Copy-Item -LiteralPath $item.FullName -Destination $cloneDir -Recurse -Force
    }
    Invoke-GitCli -Arguments @('-C',$cloneDir,'add','-A') | Out-Null
    $staged = (& $script:GitExecutable -C $cloneDir diff --cached --name-only | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Git diff failed' }
    # Use existing user identity, or owner-linked GitHub noreply identity in this temporary checkout.
    $configuredName = (& $script:GitExecutable -C $cloneDir config user.name | Out-String).Trim()
    if (-not $configuredName) { Invoke-GitCli -Arguments @('-C',$cloneDir,'config','user.name',$login) | Out-Null }
    $configuredEmail = (& $script:GitExecutable -C $cloneDir config user.email | Out-String).Trim()
    if (-not $configuredEmail) {
      $accountId = ((Invoke-GhCli -Arguments @('api','user','--jq','.id')) | Out-String).Trim()
      if ($accountId -notmatch '^\d+$') { throw 'Could not resolve account ID for git commit identity.' }
      Invoke-GitCli -Arguments @('-C',$cloneDir,'config','user.email',"$accountId+$login@users.noreply.github.com") | Out-Null
    }
    if ($staged) {
      Write-Host "Publishing project files to $newRepo..."
      Invoke-GitCli -Arguments @('-C',$cloneDir,'commit','-m','Release PARALLAX Intelligence Engine') | Out-Null
      Invoke-GitCli -Arguments @('-C',$cloneDir,'push','origin',"HEAD:refs/heads/$branch") | Out-Null
    } else { Write-Host 'Remote already matches release content.' }
    $localSha = ((Invoke-GitCli -Arguments @('-C',$cloneDir,'rev-parse','HEAD')) | Out-String).Trim()
    $remoteRefs = (Invoke-GitCli -Arguments @('-C',$cloneDir,'ls-remote','origin',"refs/heads/$branch") | Out-String).Trim()
    if (-not $remoteRefs.StartsWith($localSha)) { throw 'Remote commit SHA verification failed.' }
    Write-Host "VERIFIED PUSH: $localSha ($branch)"
  }
  $finalIsPrivate = ((Invoke-GhCli -Arguments @('repo','view',$newRepo,'--json','isPrivate','--jq','.isPrivate')) | Out-String).Trim()
  if ($finalIsPrivate -ne $isPrivate) { throw 'Repository visibility unexpectedly changed. Investigate immediately.' }
  Write-Host "SUCCESS: $newRepo updated; repository visibility preserved."
} finally {
  if ($tempRoot -and (Test-Path -LiteralPath $tempRoot)) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
  }
}
