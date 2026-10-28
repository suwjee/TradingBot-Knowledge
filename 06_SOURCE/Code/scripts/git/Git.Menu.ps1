[CmdletBinding()]
param([switch] $LoadFunctionsOnly)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ModulePath = Join-Path $PSScriptRoot 'Release.Workflow.psm1'
if (-not (Test-Path -LiteralPath $ModulePath -PathType Leaf)) {
  Write-Host '[FAIL] Release.Workflow.psm1 was not found.' -ForegroundColor Red
  exit 2
}
Import-Module $ModulePath -Force -DisableNameChecking

$script:Root = ''
$script:RepoName = ''
$script:StageNumber = 0
$script:StageTotal = 0
$script:HadOperationFailure = $false

function Write-ColorLine {
  param([string] $Text, [ConsoleColor] $Color = [ConsoleColor]::Gray)
  Write-Host $Text -ForegroundColor $Color
}

function Write-Run {
  param([string] $Text)
  if ($script:StageTotal -gt 0) {
    $script:StageNumber++
    Write-ColorLine ("[{0}/{1}] {2}" -f $script:StageNumber, $script:StageTotal, $Text) Cyan
  } else {
    Write-ColorLine ("[...] {0}" -f $Text) Cyan
  }
}

function Write-SubRun { param([string] $Text); Write-ColorLine ("[...] {0}" -f $Text) Cyan }
function Write-Ok     { param([string] $Text); Write-ColorLine ("[OK] {0}" -f $Text) Green }
function Write-Warn   { param([string] $Text); Write-ColorLine ("[WARN] {0}" -f $Text) Yellow }
function Write-Skip   { param([string] $Text); Write-ColorLine ("[SKIP] {0}" -f $Text) Yellow }
function Write-Fail   { param([string] $Text); Write-ColorLine ("[FAIL] {0}" -f $Text) Red }
function Write-Info   { param([string] $Text); Write-ColorLine $Text Gray }

function Clear-MenuScreen {
  try { Clear-Host } catch { }
}

function Pause-Menu {
  Write-Host ''
  [void](Read-Host 'Press Enter to return to menu')
}

function Invoke-GitSafe {
  param([Parameter(Mandatory)] [string[]] $Arguments, [string] $WorkingDirectory = $script:Root)
  return Invoke-ReleaseGit -Root $script:Root -Arguments $Arguments -WorkingDirectory $WorkingDirectory
}

function Assert-GitOk {
  param($Result, [string] $Message)
  if ($Result.ExitCode -ne 0) {
    $detail = if (-not [string]::IsNullOrWhiteSpace($Result.StdErr)) { $Result.StdErr.Trim() } else { $Result.StdOut.Trim() }
    if ([string]::IsNullOrWhiteSpace($detail)) { throw $Message }
    throw "$Message $detail"
  }
}

function Get-OriginRepositoryName {
  $remote = Invoke-GitSafe @('remote', 'get-url', 'origin')
  Assert-GitOk $remote 'The origin remote is unavailable.'
  $match = [regex]::Match($remote.StdOut.Trim(), '(?i)github\.com[:/](?<owner>[^/]+)/(?<repository>[^/]+?)(?:\.git)?/?$')
  if (-not $match.Success) { return '' }
  return "$($match.Groups['owner'].Value)/$($match.Groups['repository'].Value)"
}

function Invoke-GhBound {
  param([Parameter(Mandatory)] [string[]] $Arguments)
  if ([string]::IsNullOrWhiteSpace($script:RepoName)) { throw 'GitHub repository identity could not be derived from origin.' }
  $gh = Get-Command gh -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($null -eq $gh) {
    return [pscustomobject]@{ ExitCode = 127; StdOut = ''; StdErr = 'GitHub CLI (gh) is not installed.' }
  }
  $effectiveArguments = @()
  if ($Arguments.Count -ge 2 -and $Arguments[0] -eq 'repo' -and $Arguments[1] -eq 'view') {
    $effectiveArguments = @('repo', 'view', $script:RepoName)
    if ($Arguments.Count -gt 2) { $effectiveArguments += @($Arguments[2..($Arguments.Count - 1)]) }
  } else {
    $effectiveArguments = @($Arguments) + @('--repo', $script:RepoName)
  }
  return Invoke-ReleaseGh -Root $script:Root -Arguments $effectiveArguments
}

function Get-RemoteOid {
  param([Parameter(Mandatory)] [string] $Ref)
  $result = Invoke-GitSafe @('ls-remote', 'origin', $Ref)
  Assert-GitOk $result "Could not read remote ref: $Ref"
  if ([string]::IsNullOrWhiteSpace($result.StdOut)) { return $null }
  return (($result.StdOut -split '\s+' | Select-Object -First 1).Trim())
}

function Get-LocalCommitOid {
  param([Parameter(Mandatory)] [string] $Ref)
  $result = Invoke-GitSafe @('rev-parse', '--verify', '--quiet', "$Ref^{commit}")
  if ($result.ExitCode -ne 0) { return $null }
  return (($result.StdOut -split '\s+' | Select-Object -First 1).Trim())
}

function Get-ObjectOid {
  param([Parameter(Mandatory)] [string] $Ref)
  $result = Invoke-GitSafe @('rev-parse', '--verify', '--quiet', $Ref)
  if ($result.ExitCode -ne 0) { return $null }
  return (($result.StdOut -split '\s+' | Select-Object -First 1).Trim())
}

function Get-TreeOid {
  param([Parameter(Mandatory)] [string] $Commit)
  $result = Invoke-GitSafe @('rev-parse', '--verify', "$Commit^{tree}")
  Assert-GitOk $result "Could not resolve tree for commit $Commit."
  return $result.StdOut.Trim()
}

function Test-OidEqual {
  param($A, $B)
  if ($null -eq $A -and $null -eq $B) { return $true }
  if ($null -eq $A -or $null -eq $B) { return $false }
  return [string]::Equals([string]$A, [string]$B, [StringComparison]::OrdinalIgnoreCase)
}

function Test-CommitContains {
  param([string] $Ancestor, [string] $Descendant)
  if ([string]::IsNullOrWhiteSpace($Ancestor) -or [string]::IsNullOrWhiteSpace($Descendant)) { return $false }
  $r = Invoke-GitSafe @('merge-base', '--is-ancestor', $Ancestor, $Descendant)
  if ($r.ExitCode -gt 1) { throw "Could not compare Git commits: $Ancestor and $Descendant" }
  return ($r.ExitCode -eq 0)
}

function Get-AheadBehind {
  param([string] $RemoteSha, [string] $LocalSha)
  if ([string]::IsNullOrWhiteSpace($RemoteSha) -or [string]::IsNullOrWhiteSpace($LocalSha)) {
    return [pscustomobject]@{ Ahead = 0; Behind = 0 }
  }
  $r = Invoke-GitSafe @('rev-list', '--left-right', '--count', "$RemoteSha...$LocalSha")
  Assert-GitOk $r 'Could not compare local and remote branch history.'
  $parts = @($r.StdOut.Trim() -split '\s+')
  if ($parts.Count -ne 2 -or $parts[0] -notmatch '^\d+$' -or $parts[1] -notmatch '^\d+$') { throw 'Git returned an invalid ahead/behind count.' }
  return [pscustomobject]@{ Behind = [int]$parts[0]; Ahead = [int]$parts[1] }
}

function Get-ActiveBranch {
  $r = Invoke-GitSafe @('symbolic-ref', '--quiet', '--short', 'HEAD')
  if ($r.ExitCode -ne 0) { return '<detached>' }
  return $r.StdOut.Trim()
}

function Get-RepositoryBlockers {
  $blockers = [System.Collections.Generic.List[string]]::new()
  $unmerged = Invoke-GitSafe @('diff', '--name-only', '--diff-filter=U')
  Assert-GitOk $unmerged 'Could not inspect unresolved Git conflicts.'
  $paths = @($unmerged.StdOut -split "`r?`n" | Where-Object { $_ })
  if ($paths.Count) {
    $blockers.Add(("Unresolved conflicts in {0} file(s). Inspect with git status; resolve them before a release. Examples: {1}" -f $paths.Count, (($paths | Select-Object -First 5) -join ', ')))
  }
  foreach ($marker in @('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-apply', 'rebase-merge', 'sequencer')) {
    $path = Invoke-GitSafe @('rev-parse', '--git-path', $marker)
    Assert-GitOk $path "Could not locate Git operation marker: $marker"
    $markerPath = $path.StdOut.Trim()
    if (-not [IO.Path]::IsPathRooted($markerPath)) { $markerPath = Join-Path $script:Root $markerPath }
    if (Test-Path -LiteralPath $markerPath) { $blockers.Add("Git operation in progress: $marker. Finish that operation before a release.") }
  }
  $branch = Get-ActiveBranch
  if ($branch -ne 'main') { $blockers.Add("Release operations require main. Current branch: $branch. Resolve pending Git work before switching to main.") }
  return $blockers.ToArray()
}

function Assert-ActiveMain {
  $blockers = @(Get-RepositoryBlockers)
  if ($blockers.Count) { throw ($blockers -join [Environment]::NewLine) }
}

function Sync-MainFastForwardIfNeeded {
  param($State)
  if ($State.MainBehind -gt 0) {
    throw ("Local main is behind or diverged from origin/main by {0} commit(s). Reconcile main manually before continuing; no local changes were stashed or merged." -f $State.MainBehind)
  }
}

function Update-RemoteState {
  param([ValidateSet('main','production','both')] [string] $Target = 'both')
  Write-SubRun 'Fetching selected branch objects into temporary refs'
  $id = [guid]::NewGuid().ToString('N')
  $mainRef = "refs/release-tmp/$id/main"
  $productionRef = "refs/release-tmp/$id/production"
  try {
    $arguments = @('fetch', '--no-tags', '--quiet', 'origin', "+refs/heads/main:$mainRef")
    if ($Target -in @('production','both')) { $arguments += "+refs/heads/production:$productionRef" }
    $fetch = Invoke-GitSafe $arguments
    Assert-GitOk $fetch 'Could not fetch the required origin branches.'
  } finally {
    $null = Invoke-GitSafe @('update-ref', '-d', $mainRef)
    $null = Invoke-GitSafe @('update-ref', '-d', $productionRef)
  }
  Write-Ok 'Remote objects refreshed without advancing permanent local branches'
}

function Get-BranchState {
  param([ValidateSet('main','production','both')] [string] $Target = 'both')
  $remoteMain = Get-RemoteOid 'refs/heads/main'
  $remoteProduction = if ($Target -in @('production','both')) { Get-RemoteOid 'refs/heads/production' } else { $null }
  if ([string]::IsNullOrWhiteSpace($remoteMain)) { throw 'origin/main is missing.' }
  if ($Target -in @('production','both') -and [string]::IsNullOrWhiteSpace($remoteProduction)) { throw 'origin/production is missing.' }
  $localMain = Get-LocalCommitOid 'refs/heads/main'
  if ($null -eq $localMain) { throw 'Local main has no commit.' }
  $localProduction = Get-LocalCommitOid 'refs/heads/production'
  $mainRelation = Get-AheadBehind -RemoteSha $remoteMain -LocalSha $localMain
  $prodRelation = if ($null -ne $remoteProduction -and $null -ne $localProduction) { Get-AheadBehind -RemoteSha $remoteProduction -LocalSha $localProduction } else { [pscustomobject]@{ Ahead = 0; Behind = 0 } }
  return [pscustomobject]@{
    RemoteMain = $remoteMain
    RemoteProduction = $remoteProduction
    LocalMain = $localMain
    LocalProduction = $localProduction
    MainAhead = $mainRelation.Ahead
    MainBehind = $mainRelation.Behind
    ProductionAhead = $prodRelation.Ahead
    ProductionBehind = $prodRelation.Behind
  }
}

function Show-RepositoryStatus {
  param($State)
  Write-Host ''
  Write-ColorLine 'MAIN' White
  Write-Info ("Local  : {0}" -f $State.LocalMain)
  Write-Info ("Remote : {0}" -f $State.RemoteMain)
  Write-Info ("Ahead  : {0}" -f $State.MainAhead)
  Write-Info ("Behind : {0}" -f $State.MainBehind)
  if ($null -eq $State.RemoteProduction) { return }
  Write-Host ''
  Write-ColorLine 'PRODUCTION' White
  Write-Info ("Local  : {0}" -f $(if ($State.LocalProduction) { $State.LocalProduction } else { '<none>' }))
  Write-Info ("Remote : {0}" -f $State.RemoteProduction)
  Write-Info ("Ahead  : {0}" -f $State.ProductionAhead)
  Write-Info ("Behind : {0}" -f $State.ProductionBehind)
}

function Test-GitAuthentication {
  param([ValidateSet('main','production','both')] [string] $Target = 'main', $State)
  Write-SubRun 'Checking Git push authorization (dry-run only)'
  $specs = @()
  if ($Target -in @('main','both')) {
    $main = if ($null -eq $State) { 'HEAD' } else { $State.LocalMain }
    $specs += "${main}:refs/heads/main"
  }
  if ($Target -in @('production','both')) {
    if ($null -eq $State -or [string]::IsNullOrWhiteSpace($State.RemoteProduction)) { throw 'Production authorization requires the fetched origin/production state.' }
    $specs += "$($State.RemoteProduction):refs/heads/production"
  }
  $probe = Invoke-GitSafe (@('push', '--dry-run', 'origin') + $specs)
  Assert-GitOk $probe 'Git push authentication/authorization check failed.'
  Write-Ok 'Git push authorization verified'
}

function Test-GitHubAuthentication {
  Write-SubRun 'Checking GitHub CLI authentication'
  $auth = Invoke-GhBound @('repo', 'view', '--json', 'nameWithOwner')
  if ($auth.ExitCode -ne 0) { throw 'GitHub CLI authentication/repository access check failed.' }
  $actual = ''
  try { $actual = ($auth.StdOut | ConvertFrom-Json).nameWithOwner } catch { }
  if (-not [string]::Equals($actual, $script:RepoName, [StringComparison]::OrdinalIgnoreCase)) {
    throw "GitHub CLI repository mismatch. Expected $($script:RepoName), got $actual"
  }
  Write-Ok ("GitHub CLI: {0}" -f $actual)
}

function Read-YesNo {
  param([Parameter(Mandatory)] [string] $Prompt)
  $value = Read-Host "$Prompt [y/N]"
  return ($value -match '^(?i:y|yes)$')
}

function Read-TargetChoice {
  param([switch] $AllowBack)
  while ($true) {
    Write-Host ''
    Write-ColorLine '1. Main' White
    Write-ColorLine '2. Production' White
    Write-ColorLine '3. Both' White
    if ($AllowBack) { Write-ColorLine '0. Back' DarkGray }
    $choice = (Read-Host 'Select target').Trim()
    switch ($choice) {
      '1' { return 'main' }
      '2' { return 'production' }
      '3' { return 'both' }
      '0' { if ($AllowBack) { return 'back' } }
      default { Write-Warn 'Invalid selection.' }
    }
  }
}

function Read-TagTarget {
  while ($true) {
    Write-Host ''
    Write-ColorLine 'Tag / Release target' White
    Write-ColorLine '1. Production (recommended)' White
    Write-ColorLine '2. Main' White
    Write-ColorLine '3. Both' White
    $value = (Read-Host 'Select [1]').Trim()
    if ([string]::IsNullOrWhiteSpace($value) -or $value -eq '1') { return 'production' }
    if ($value -eq '2') { return 'main' }
    if ($value -eq '3') { return 'both' }
    Write-Warn 'Invalid selection.'
  }
}

function Get-DiffEntries {
  param([Parameter(Mandatory)] [string] $Base, [Parameter(Mandatory)] [string] $Target)
  if (Test-OidEqual $Base $Target) { return @() }
  $r = Invoke-GitSafe @('diff', '--name-status', '-z', '-M', $Base, $Target, '--')
  Assert-GitOk $r 'Could not calculate branch file preview.'
  $entries = [System.Collections.Generic.List[object]]::new()
  $parts = @($r.StdOut -split "`0")
  for ($i = 0; $i -lt ($parts.Count - 1); $i++) {
    $code = $parts[$i]
    if (-not $code) { continue }
    $kind = 'Modified'
    $oldPath = $null
    $path = $parts[++$i]
    if ($code.StartsWith('A')) { $kind = 'Added' }
    elseif ($code.StartsWith('D')) { $kind = 'Deleted' }
    elseif ($code.StartsWith('R') -or $code.StartsWith('C')) {
      $kind = 'Renamed'
      $oldPath = $path
      $path = $parts[++$i]
    } elseif ($code.StartsWith('M') -or $code.StartsWith('T')) { $kind = 'Modified' }
    $entries.Add([pscustomobject]@{ Kind = $kind; Path = $path.Replace('\','/'); OldPath = if ($oldPath) { $oldPath.Replace('\','/') } else { $null } })
  }
  return $entries.ToArray()
}

function Show-ChangeEntries {
  param([Parameter(Mandatory)] [string] $Title, [object[]] $Entries)
  Write-Host ''
  Write-ColorLine $Title White
  Write-ColorLine ('-' * 70) DarkGray
  if (@($Entries).Count -eq 0) {
    Write-Skip 'No files will change on this branch.'
  } else {
    foreach ($entry in $Entries) {
      switch ($entry.Kind) {
        'Added'    { Write-ColorLine ("+ /{0}" -f $entry.Path) Green }
        'Modified' { Write-ColorLine ("~ /{0}" -f $entry.Path) Yellow }
        'Deleted'  { Write-ColorLine ("- /{0}" -f $entry.Path) Red }
        'Renamed'  { Write-ColorLine ("> /{0}  ->  /{1}" -f $entry.OldPath, $entry.Path) Cyan }
      }
    }
  }
  $added = @($Entries | Where-Object { $_.Kind -eq 'Added' }).Count
  $modified = @($Entries | Where-Object { $_.Kind -eq 'Modified' }).Count
  $deleted = @($Entries | Where-Object { $_.Kind -eq 'Deleted' }).Count
  $renamed = @($Entries | Where-Object { $_.Kind -eq 'Renamed' }).Count
  Write-Host ''
  Write-Info ("Added    : {0}" -f $added)
  Write-Info ("Modified : {0}" -f $modified)
  Write-Info ("Deleted  : {0}" -f $deleted)
  Write-Info ("Renamed  : {0}" -f $renamed)
  Write-Info ("Total    : {0}" -f @($Entries).Count)
}

function Show-PolicyDrift {
  param([string[]] $MainDrift, [string[]] $ProductionDrift)
  $items = @()
  foreach ($item in @($MainDrift)) { if ($item) { $items += "MAIN: $item" } }
  foreach ($item in @($ProductionDrift)) { if ($item) { $items += "PRODUCTION: $item" } }
  if ($items.Count -eq 0) { return }
  Write-Host ''
  Write-ColorLine 'POLICY DRIFT' Magenta
  foreach ($item in $items) { Write-ColorLine ("! {0}" -f $item) Magenta }
}

function Test-MainCandidatePolicy {
  Write-SubRun 'Evaluating main inclusion policy and sensitive content'
  $report = Get-MainPolicyReport -Root $script:Root
  if (@($report.Errors).Count -gt 0) {
    Write-ColorLine 'POLICY DRIFT' Magenta
    foreach ($item in @($report.Drift)) { Write-ColorLine ("! {0}" -f $item) Magenta }
    throw ($report.Errors -join '; ')
  }
  $sensitive = Test-SensitiveCandidate -Root $script:Root -Paths $report.Eligible
  if (@($sensitive.Errors).Count -gt 0) { throw ($sensitive.Errors -join '; ') }
  Write-Ok ("Main policy: {0} eligible, {1} excluded" -f @($report.Eligible).Count, @($report.Excluded).Count)
  return $report
}

function New-MainPreview {
  param([Parameter(Mandatory)] [string] $CommitMessage, [Parameter(Mandatory)] [string] $RemoteMain, [switch] $IncludeWorkingTree)
  if ($IncludeWorkingTree) {
    Write-SubRun 'Building isolated main candidate'
    $candidate = New-MainReleaseSource -Root $script:Root -CommitMessage $CommitMessage -DryRun
    $target = $candidate.MainSha
    Write-Ok 'Main candidate prepared without changing the active index'
  } else {
    $target = Get-LocalCommitOid 'HEAD'
    $candidate = [pscustomobject]@{ MainSha = $target; Changed = $false; DryRun = $true }
  }
  if (-not (Test-CommitContains -Ancestor $RemoteMain -Descendant $target)) {
    throw 'Selected main target does not contain origin/main. Pull/reconcile manually before continuing.'
  }
  return [pscustomobject]@{
    Candidate = $candidate
    TargetSha = $target
    TreeSha = Get-TreeOid $target
    Entries = @(Get-DiffEntries -Base $RemoteMain -Target $target)
  }
}

function Get-ProductionPushTargetWithoutCommit {
  param([Parameter(Mandatory)] $State)
  if ($null -eq $State.LocalProduction) {
    return [pscustomobject]@{ TargetSha = $State.RemoteProduction; HasLocalRef = $false; Ahead = 0 }
  }
  if (-not (Test-CommitContains -Ancestor $State.RemoteProduction -Descendant $State.LocalProduction)) {
    throw 'Local production is not a fast-forward descendant of origin/production. Resolve it manually.'
  }
  $relation = Get-AheadBehind -RemoteSha $State.RemoteProduction -LocalSha $State.LocalProduction
  return [pscustomobject]@{ TargetSha = $State.LocalProduction; HasLocalRef = $true; Ahead = $relation.Ahead }
}

function New-ProductionPreview {
  param(
    [Parameter(Mandatory)] [string] $SourceMainSha,
    [Parameter(Mandatory)] [string] $ProductionBaseSha,
    [Parameter(Mandatory)] [string] $CommitMessage,
    [switch] $RuntimeValidation
  )
  Write-SubRun 'Resolving production runtime dependency closure'
  $policy = Import-ReleasePolicy -Root $script:Root
  $fileSet = Get-ProductionFileSet -Root $script:Root -MainSha $SourceMainSha -Policy $policy
  $fileValidation = Test-ProductionFileSet -FileSet $fileSet -Policy $policy
  if (@($fileSet.Errors).Count -gt 0 -or @($fileValidation.Errors).Count -gt 0) {
    throw (@($fileSet.Errors + $fileValidation.Errors) -join '; ')
  }
  Write-Ok ("Production closure: {0} files" -f @($fileSet.Paths).Count)
  Write-SubRun 'Creating isolated production candidate worktree'
  $snapshot = New-ProductionSnapshot -Root $script:Root -SourceMainSha $SourceMainSha -ProductionBaseSha $ProductionBaseSha -FileSet $fileSet -CommitMessage $CommitMessage -DryRun
  try {
    Write-Ok 'Production candidate created'
    Write-SubRun $(if ($RuntimeValidation) { 'Running full production validation' } else { 'Running structural production validation' })
    $progressCallback = $null
    if ($RuntimeValidation) { $progressCallback = { param($message) Write-Host ("[...] {0}" -f $message) -ForegroundColor Cyan } }
    $validation = Test-ProductionSnapshot -Snapshot $snapshot -RunRuntimeValidation:$RuntimeValidation -ProgressCallback $progressCallback
    if ($RuntimeValidation) { Assert-ReleaseValidationComplete -Validation $validation }
    elseif (@($validation.Errors).Count -gt 0) { throw ($validation.Errors -join '; ') }
    Write-Ok $(if ($RuntimeValidation) { 'Production runtime/build validation passed' } else { 'Production structural validation passed' })
    $treeSha = Get-TreeOid $snapshot.ProductionSha
    $entries = @(Get-DiffEntries -Base $ProductionBaseSha -Target $snapshot.ProductionSha)
    return [pscustomobject]@{
      Snapshot = $snapshot
      FileSet = $fileSet
      Validation = $validation
      TargetSha = $snapshot.ProductionSha
      TreeSha = $treeSha
      Entries = $entries
    }
  } catch {
    Remove-TemporaryReleaseContext -Context $snapshot.Context
    throw
  }
}

function Remove-PreviewProduction {
  param($Preview)
  if ($null -ne $Preview -and $null -ne $Preview.Snapshot -and $null -ne $Preview.Snapshot.Context) {
    Write-SubRun 'Removing temporary production preview worktree'
    Remove-TemporaryReleaseContext -Context $Preview.Snapshot.Context
    Write-Ok 'Temporary production preview removed'
  }
}

function Test-OptionalTag {
  param([string] $Tag, [switch] $CheckGitHubRelease)
  if ([string]::IsNullOrWhiteSpace($Tag)) { return }
  Write-SubRun ("Validating tag: {0}" -f $Tag)
  $syntax = Invoke-GitSafe @('check-ref-format', "refs/tags/$Tag")
  if ($syntax.ExitCode -ne 0) { throw "Invalid Git tag syntax: $Tag" }
  $local = Invoke-GitSafe @('show-ref', '--verify', '--quiet', "refs/tags/$Tag")
  if ($local.ExitCode -eq 0) { throw "Local tag already exists: $Tag" }
  if ($local.ExitCode -ne 1) { throw "Could not determine whether local tag exists: $Tag" }
  $remote = Get-RemoteOid "refs/tags/$Tag"
  if ($null -ne $remote) { throw "Remote tag already exists: $Tag" }
  if ($CheckGitHubRelease) {
    $view = Invoke-GhBound @('release', 'view', $Tag, '--json', 'tagName')
    if ($view.ExitCode -eq 0) { throw "GitHub Release already exists for tag: $Tag" }
    if (($view.StdErr + "`n" + $view.StdOut) -notmatch '(?i)(release not found|HTTP 404: Not Found)') {
      throw "Could not determine whether GitHub Release exists for tag: $Tag"
    }
  }
  Write-Ok 'Tag is valid and unused'
}

function New-MenuTag {
  param(
    [Parameter(Mandatory)] [string] $Tag,
    [Parameter(Mandatory)] [string] $TargetSha,
    [Parameter(Mandatory)] [string] $TargetKind,
    [Parameter(Mandatory)] [string] $MainSourceSha
  )
  $messages = @('-m', "TradingBot $TargetKind tag $Tag")
  if ($TargetKind -in @('production','both')) { $messages += @('-m', "TradingBot-Main-Source: $MainSourceSha") }
  $tagArguments = @('-c', 'user.name=TradingBot Release', '-c', 'user.email=release@tradingbot.invalid', 'tag', '-a') + $messages + @('--', $Tag, $TargetSha)
  $r = Invoke-GitSafe $tagArguments
  Assert-GitOk $r "Could not create local tag: $Tag"
  $tagObject = Get-ObjectOid "refs/tags/$Tag"
  if ([string]::IsNullOrWhiteSpace($tagObject)) { throw "Created tag object could not be resolved: $Tag" }
  return $tagObject
}

function Get-RemoteStatesForRefs {
  param([Parameter(Mandatory)] [object[]] $Refs)
  $state = @{}
  foreach ($item in $Refs) { $state[$item.Name] = Get-RemoteOid $item.RemoteRef }
  return $state
}

function Assert-RemoteBaselinesUnchanged {
  param([Parameter(Mandatory)] [object[]] $Refs)
  foreach ($item in $Refs) {
    $current = Get-RemoteOid $item.RemoteRef
    if (-not (Test-OidEqual $current $item.BaselineOid)) {
      throw "Remote changed after preview: $($item.RemoteRef). Re-run the operation."
    }
  }
}

function Publish-MenuRefs {
  param([Parameter(Mandatory)] [AllowEmptyCollection()] [object[]] $Refs)
  if ($Refs.Count) { Assert-RemoteBaselinesUnchanged -Refs $Refs }
  $toPush = @($Refs | Where-Object { -not (Test-OidEqual $_.DesiredOid $_.BaselineOid) })
  if ($toPush.Count -eq 0) {
    return [pscustomobject]@{ Status = 'SKIPPED'; Method = 'none'; Detail = 'All selected refs already match origin.' }
  }
  foreach ($item in $toPush) {
    $localOid = if ($item.LocalRef -like 'refs/tags/*') { Get-ObjectOid $item.LocalRef } else { Get-LocalCommitOid $item.LocalRef }
    if (-not (Test-OidEqual $localOid $item.DesiredOid)) { throw "Local ref is not prepared as previewed: $($item.LocalRef)" }
  }
  $specs = @($toPush | ForEach-Object { "$($_.DesiredOid):$($_.RemoteRef)" })
  if ($toPush.Count -eq 1) {
    $r = Invoke-GitSafe (@('push', 'origin') + $specs)
    if ($r.ExitCode -ne 0) { throw "Push failed: $($r.StdErr)" }
    $verified = Get-RemoteOid $toPush[0].RemoteRef
    if (-not (Test-OidEqual $verified $toPush[0].DesiredOid)) { throw 'Remote verification failed after push.' }
    return [pscustomobject]@{ Status = 'PASS'; Method = 'single'; Detail = $toPush[0].Name }
  }

  $atomic = Invoke-GitSafe (@('push', '--atomic', 'origin') + $specs)
  $after = Get-RemoteStatesForRefs -Refs $Refs
  $allDesired = $true
  foreach ($item in $Refs) { if (-not (Test-OidEqual $after[$item.Name] $item.DesiredOid)) { $allDesired = $false } }
  if ($atomic.ExitCode -eq 0 -and $allDesired) {
    return [pscustomobject]@{ Status = 'PASS'; Method = 'atomic'; Detail = ($toPush.Name -join ', ') }
  }

  $allUnchanged = $true
  foreach ($item in $Refs) { if (-not (Test-OidEqual $after[$item.Name] $item.BaselineOid)) { $allUnchanged = $false } }
  if (-not $allUnchanged) { throw 'Atomic publication ended in a partial/indeterminate remote state. Stop and inspect origin manually.' }
  $atomicText = ($atomic.StdErr + "`n" + $atomic.StdOut)
  if ($atomicText -notmatch '(?i)(does not support.*atomic|atomic.*not supported|unsupported.*atomic)') {
    throw "Atomic push failed for a reason other than unsupported atomic capability. $($atomic.StdErr)"
  }
  Write-Warn 'Remote does not support atomic push. Using guarded sequential fallback.'
  $expected = @{}
  foreach ($item in $Refs) { $expected[$item.Name] = $item.BaselineOid }
  foreach ($item in $toPush) {
    $current = Get-RemoteStatesForRefs -Refs $Refs
    foreach ($ref in $Refs) {
      if (-not (Test-OidEqual $current[$ref.Name] $expected[$ref.Name])) { throw 'Remote changed during fallback. Stop and inspect remote refs manually.' }
    }
    $r = Invoke-GitSafe @('push', 'origin', "$($item.DesiredOid):$($item.RemoteRef)")
    $expected[$item.Name] = $item.DesiredOid
    $current = Get-RemoteStatesForRefs -Refs $Refs
    $matches = $true
    foreach ($ref in $Refs) { if (-not (Test-OidEqual $current[$ref.Name] $expected[$ref.Name])) { $matches = $false } }
    if ($r.ExitCode -ne 0 -or -not $matches) {
      throw "Partial publication while pushing $($item.Name). Stop and inspect remote refs manually."
    }
  }
  return [pscustomobject]@{ Status = 'PASS'; Method = 'fallback'; Detail = ($toPush.Name -join ', ') }
}

function New-LatestGitHubRelease {
  param(
    [Parameter(Mandatory)] [string] $Tag,
    [Parameter(Mandatory)] [string] $ReleaseName,
    [Parameter(Mandatory)] [string] $TargetKind,
    [Parameter(Mandatory)] [string] $TargetSha,
    [Parameter(Mandatory)] [string] $MainSourceSha
  )
  $notes = @(
    'TradingBot release'
    "Tag: $Tag"
    "Target: $TargetKind"
    "Commit: $TargetSha"
  )
  if ($TargetKind -in @('production','both')) { $notes += "Main Source: $MainSourceSha" }
  $create = Invoke-GhBound @('release', 'create', $Tag, '--verify-tag', '--latest', '--title', $ReleaseName, '--notes', ($notes -join "`n"))
  if ($create.ExitCode -ne 0) { throw "GitHub Release creation failed. $($create.StdErr)" }
  return ($create.StdOut -split "`r?`n" | Select-Object -Last 1).Trim()
}

function Show-FinalSummary {
  param($Context)
  Write-Host ''
  Write-ColorLine ('=' * 72) White
  Write-ColorLine 'FINAL OPERATION' White
  Write-ColorLine ('=' * 72) White
  Write-Info ("Target          : {0}" -f $Context.Target.ToUpperInvariant())
  if ($Context.Target -in @('main','both')) {
    Write-Info ("Main files      : {0}" -f @($Context.MainEntries).Count)
    Write-Info ("Main ahead      : {0}" -f $Context.State.MainAhead)
  }
  if ($Context.Target -in @('production','both')) {
    Write-Info ("Production files: {0}" -f @($Context.ProductionEntries).Count)
    Write-Info ("Production ahead: {0}" -f $Context.State.ProductionAhead)
  }
  Write-Info ("Commit          : {0}" -f $(if ([string]::IsNullOrWhiteSpace($Context.CommitMessage)) { '<skip new commit>' } else { $Context.CommitMessage }))
  Write-Info ("Tag             : {0}" -f $(if ([string]::IsNullOrWhiteSpace($Context.Tag)) { '<skip>' } else { $Context.Tag }))
  if (-not [string]::IsNullOrWhiteSpace($Context.Tag)) { Write-Info ("Tag target      : {0}" -f $Context.TagTarget.ToUpperInvariant()) }
  Write-Info ("Release         : {0}" -f $(if ($Context.CreateRelease) { $Context.ReleaseName } else { '<skip>' }))
  Write-Info ("Latest          : {0}" -f $(if ($Context.CreateRelease) { 'Yes (repository-wide)' } else { 'No' }))
  Write-ColorLine ('=' * 72) White
}

function Show-Results {
  param($Result)
  Write-Host ''
  Write-ColorLine ('=' * 72) White
  Write-ColorLine 'RESULT' White
  Write-ColorLine ('=' * 72) White
  foreach ($row in @(
    @('MAIN COMMIT', $Result.MainCommit),
    @('MAIN PUSH', $Result.MainPush),
    @('PRODUCTION COMMIT', $Result.ProductionCommit),
    @('PRODUCTION PUSH', $Result.ProductionPush),
    @('TAG', $Result.Tag),
    @('GITHUB RELEASE', $Result.Release),
    @('TEMP CLEANUP', $Result.Cleanup)
  )) {
    $color = if ($row[1] -eq 'PASS') { 'Green' } elseif ($row[1] -eq 'FAIL') { 'Red' } else { 'Yellow' }
    Write-ColorLine ("{0,-18}: {1}" -f $row[0], $row[1]) $color
  }
  Write-ColorLine ('=' * 72) White
}

function New-OperationContext {
  param([string] $Target, [switch] $DryRun, [switch] $PreviewOnly)
  return [pscustomobject]@{
    Target = $Target
    DryRun = [bool]$DryRun
    PreviewOnly = [bool]$PreviewOnly
    CommitMessage = ''
    Tag = ''
    TagTarget = if ($Target -eq 'production') { 'production' } else { 'main' }
    CreateRelease = $false
    ReleaseName = ''
    State = $null
    MainReport = $null
    MainPreview = $null
    ProductionPreview = $null
    MainEntries = @()
    ProductionEntries = @()
    ProductionFileSet = $null
    PreviewMainTree = $null
    PreviewProductionTree = $null
  }
}

function Invoke-PreviewOnly {
  param([Parameter(Mandatory)] [string] $Target)
  $ctx = New-OperationContext -Target $Target -PreviewOnly
  $script:StageNumber = 0
  $script:StageTotal = 5
  $prodPreview = $null
  try {
    Write-Run 'Repository validation'
    Assert-ActiveMain
    Write-Ok ("Repository: {0}" -f $script:Root)
    Write-Run 'Remote refresh'
    Update-RemoteState -Target $Target
    $ctx.State = Get-BranchState -Target $Target
    Show-RepositoryStatus $ctx.State
    Write-Run 'Main policy analysis'
    $ctx.MainReport = Test-MainCandidatePolicy
    Write-Run 'Calculating preview candidates'
    $ctx.MainPreview = New-MainPreview -CommitMessage 'TradingBot preview only' -RemoteMain $ctx.State.RemoteMain -IncludeWorkingTree
    $ctx.MainEntries = $ctx.MainPreview.Entries
    $sourceMain = $ctx.MainPreview.TargetSha
    if ($Target -in @('production','both')) {
      $prodPreview = New-ProductionPreview -SourceMainSha $sourceMain -ProductionBaseSha $ctx.State.RemoteProduction -CommitMessage 'TradingBot preview only'
      $ctx.ProductionPreview = $prodPreview
      $ctx.ProductionEntries = $prodPreview.Entries
    }
    Write-Run 'Displaying exact candidate paths'
    if ($Target -in @('main','both')) { Show-ChangeEntries -Title 'MAIN CHANGES' -Entries $ctx.MainEntries }
    elseif (@($ctx.MainEntries).Count) { Show-ChangeEntries -Title 'MAIN SOURCE CHANGES (candidate source for production)' -Entries $ctx.MainEntries }
    if ($Target -in @('production','both')) { Show-ChangeEntries -Title 'PRODUCTION CHANGES' -Entries $ctx.ProductionEntries }
    Show-PolicyDrift -MainDrift $ctx.MainReport.Drift -ProductionDrift $(if ($prodPreview) { $prodPreview.FileSet.Drift } else { @() })
    Write-Ok 'Preview only complete. No commit, tag, push, or release occurred.'
  } finally {
    if ($null -ne $prodPreview) { Remove-PreviewProduction $prodPreview }
  }
}

function Invoke-InteractiveOperation {
  param([Parameter(Mandatory)] [string] $Target, [switch] $DryRun)
  $ctx = New-OperationContext -Target $Target -DryRun:$DryRun
  $result = [pscustomobject]@{ MainCommit='SKIPPED'; MainPush='SKIPPED'; ProductionCommit='SKIPPED'; ProductionPush='SKIPPED'; Tag='SKIPPED'; Release='SKIPPED'; Cleanup='PASS' }
  $previewProd = $null
  $actualProd = $null
  $localTagCreated = $false
  $script:StageNumber = 0
  $script:StageTotal = if ($DryRun) { 9 } else { 14 }

  try {
    Write-Run 'Repository validation'
    Assert-ActiveMain
    Write-Ok ("Repository: {0}" -f $script:Root)

    Write-Run 'Fetching remote refs'
    Update-RemoteState -Target $Target
    $ctx.State = Get-BranchState -Target $Target
    Show-RepositoryStatus $ctx.State
    Sync-MainFastForwardIfNeeded -State $ctx.State

    Write-Run 'Authentication validation'
    Test-GitAuthentication -Target $Target -State $ctx.State

    Write-Run 'Main policy and secret validation'
    $ctx.MainReport = Test-MainCandidatePolicy

    Write-Host ''
    $ctx.CommitMessage = (Read-Host 'Commit message (leave empty for automatic message)').Trim()
    if ([string]::IsNullOrWhiteSpace($ctx.CommitMessage)) { $ctx.CommitMessage = 'Update TradingBot project files' }
    $ctx.Tag = (Read-Host 'Tag (leave empty to skip tag)').Trim()
    if (-not [string]::IsNullOrWhiteSpace($ctx.Tag)) {
      if ($Target -eq 'both') { $ctx.TagTarget = Read-TagTarget }
      elseif ($Target -eq 'production') { $ctx.TagTarget = 'production' }
      else { $ctx.TagTarget = 'main' }
    }
    $releaseRequested = Read-YesNo 'Create GitHub Release?'
    if ($releaseRequested -and [string]::IsNullOrWhiteSpace($ctx.Tag)) {
      Write-Skip 'GitHub Release requires a tag.'
      $ctx.CreateRelease = $false
    } elseif ($releaseRequested) {
      $ctx.ReleaseName = (Read-Host 'Release name (leave empty to skip Release)').Trim()
      if ([string]::IsNullOrWhiteSpace($ctx.ReleaseName)) {
        Write-Skip 'Release name is empty.'
        $ctx.CreateRelease = $false
      } else { $ctx.CreateRelease = $true }
    }

    if (-not [string]::IsNullOrWhiteSpace($ctx.Tag)) {
      if ($ctx.CreateRelease) { Test-GitHubAuthentication }
      Test-OptionalTag -Tag $ctx.Tag -CheckGitHubRelease:$ctx.CreateRelease
    }

    Write-Run 'Calculating branch candidates'
    $includeNewCommit = -not [string]::IsNullOrWhiteSpace($ctx.CommitMessage)
    $sourceMainPreview = $ctx.State.LocalMain
    $ctx.MainPreview = New-MainPreview -CommitMessage $ctx.CommitMessage -RemoteMain $ctx.State.RemoteMain -IncludeWorkingTree
    $ctx.MainEntries = @($ctx.MainPreview.Entries)
    $ctx.PreviewMainTree = $ctx.MainPreview.TreeSha
    $sourceMainPreview = $ctx.MainPreview.TargetSha

    if ($Target -in @('production','both')) {
      $previewProd = New-ProductionPreview -SourceMainSha $sourceMainPreview -ProductionBaseSha $ctx.State.RemoteProduction -CommitMessage $(if ($includeNewCommit) { $ctx.CommitMessage } else { 'TradingBot production validation preview' })
      $ctx.ProductionPreview = $previewProd
      $ctx.ProductionFileSet = $previewProd.FileSet
      $ctx.PreviewProductionTree = $previewProd.TreeSha
      if ($includeNewCommit) {
        $ctx.ProductionEntries = @($previewProd.Entries)
      } else {
        $prodTarget = Get-ProductionPushTargetWithoutCommit -State $ctx.State
        $ctx.ProductionEntries = @(Get-DiffEntries -Base $ctx.State.RemoteProduction -Target $prodTarget.TargetSha)
        if (-not (Test-OidEqual $previewProd.TreeSha (Get-TreeOid $prodTarget.TargetSha))) {
          throw 'Production runtime snapshot differs from the current production commit, but commit message is empty. Enter a commit message to prepare the matching production snapshot.'
        }
      }
    }
    Write-Ok 'Branch candidates calculated'

    Write-Run 'Displaying pre-push file tree'
    if ($Target -in @('main','both')) { Show-ChangeEntries -Title 'MAIN CHANGES' -Entries $ctx.MainEntries }
    elseif (@($ctx.MainEntries).Count) { Show-ChangeEntries -Title 'MAIN SOURCE CHANGES (local commit; main will not be pushed)' -Entries $ctx.MainEntries }
    if ($Target -in @('production','both')) { Show-ChangeEntries -Title 'PRODUCTION CHANGES' -Entries $ctx.ProductionEntries }
    Show-PolicyDrift -MainDrift $ctx.MainReport.Drift -ProductionDrift $(if ($ctx.ProductionFileSet) { $ctx.ProductionFileSet.Drift } else { @() })
    if ($Target -in @('main','both') -and [string]::IsNullOrWhiteSpace($ctx.CommitMessage)) {
      $workingStatus = Invoke-GitSafe @('status', '--porcelain=v1', '--untracked-files=all')
      if (-not [string]::IsNullOrWhiteSpace($workingStatus.StdOut)) { Write-Warn 'Commit message is empty: current uncommitted main changes are not part of this push.' }
      if ($ctx.State.MainAhead -gt 0) { Write-Warn ("Existing main commits waiting to push: {0}" -f $ctx.State.MainAhead) }
    }
    if ($Target -in @('production','both') -and [string]::IsNullOrWhiteSpace($ctx.CommitMessage)) {
      Write-Warn 'Commit message is empty: no new production snapshot will be committed.'
      if ($ctx.State.ProductionAhead -gt 0) { Write-Warn ("Existing production commits waiting to push: {0}" -f $ctx.State.ProductionAhead) }
    }

    Show-FinalSummary $ctx
    if ($null -ne $previewProd) {
      Write-SubRun 'Validating the exact production candidate before confirmation'
      $fullValidation = Test-ProductionSnapshot -Snapshot $previewProd.Snapshot -RunRuntimeValidation -ProgressCallback { param($message) Write-SubRun $message }
      Assert-ReleaseValidationComplete -Validation $fullValidation
      Write-Ok 'Production runtime/build validation passed'
    }
    if ($DryRun) {
      Write-Run 'Running full dry-run production validation'
      if ($Target -in @('production','both')) { Write-Ok 'Confirmed production validation completed above' }
      else { Write-Skip 'Production validation not required for main-only Dry Run.' }
      Write-Run 'Verifying non-publication state'
      Test-OptionalTag -Tag $ctx.Tag -CheckGitHubRelease:$ctx.CreateRelease
      Write-Ok 'No permanent commit, tag, push, or GitHub Release was created'
      Write-Run 'Dry Run result'
      Write-Host ''
      Write-ColorLine ('=' * 72) Green
      Write-ColorLine 'DRY RUN PASSED' Green
      Write-ColorLine 'No commit, push, tag or release occurred.' Green
      Write-ColorLine ('=' * 72) Green
      return
    }

    Write-Run 'Final confirmation'
    if (-not (Read-YesNo 'Continue?')) {
      Write-Skip 'Operation cancelled. Nothing was published.'
      return
    }

    Write-Run 'Re-checking preview state and remote refs'
    $currentRemoteMain = Get-RemoteOid 'refs/heads/main'
    $currentRemoteProduction = if ($Target -in @('production','both')) { Get-RemoteOid 'refs/heads/production' } else { $null }
    if (-not (Test-OidEqual $currentRemoteMain $ctx.State.RemoteMain) -or -not (Test-OidEqual $currentRemoteProduction $ctx.State.RemoteProduction)) {
      throw 'Remote repository changed after preview. Re-run the operation.'
    }
    if (-not [string]::IsNullOrWhiteSpace($ctx.Tag) -and $null -ne (Get-RemoteOid "refs/tags/$($ctx.Tag)")) {
      throw 'Tag appeared on remote after preview. Re-run the operation.'
    }

    $actualMainSha = $ctx.State.LocalMain
    Assert-ActiveMain
    if (-not (Test-OidEqual (Get-LocalCommitOid 'HEAD') $ctx.State.LocalMain)) { throw 'Main HEAD changed after preview.' }
    if ($includeNewCommit) {
      $verifyMain = New-MainPreview -CommitMessage $ctx.CommitMessage -RemoteMain $ctx.State.RemoteMain -IncludeWorkingTree
      if (-not (Test-OidEqual $verifyMain.TreeSha $ctx.PreviewMainTree)) { throw 'Main candidate changed after preview. Re-run the operation.' }
      Write-SubRun 'Creating main commit'
      $result.MainCommit = 'FAIL'
      $actualMain = New-MainReleaseSource -Root $script:Root -CommitMessage $ctx.CommitMessage
      $actualMainSha = $actualMain.MainSha
      if (-not (Test-OidEqual (Get-TreeOid $actualMainSha) $ctx.PreviewMainTree)) { throw 'Created main tree differs from the confirmed preview. Nothing has been pushed.' }
      if ($actualMain.Changed) { $result.MainCommit = 'PASS'; Write-Ok ("Main commit: {0}" -f $actualMainSha) }
      else { $result.MainCommit = 'SKIPPED'; Write-Skip 'Main tree unchanged; no empty commit created.' }
    } elseif ($Target -in @('main','both')) {
      if (-not (Test-OidEqual (Get-LocalCommitOid 'HEAD') $ctx.State.LocalMain)) { throw 'Main HEAD changed after preview.' }
      Write-Skip 'Main commit message is empty; no new main commit created.'
    }

    if ($null -ne $previewProd) {
      Remove-PreviewProduction $previewProd
      $previewProd = $null
    }

    $actualProductionSha = $ctx.State.RemoteProduction
    if ($Target -in @('production','both')) {
      if ($includeNewCommit) {
        Write-SubRun 'Preparing exact production snapshot from committed main SHA'
        $policy = Import-ReleasePolicy -Root $script:Root
        $actualFileSet = Get-ProductionFileSet -Root $script:Root -MainSha $actualMainSha -Policy $policy
        $actualFileValidation = Test-ProductionFileSet -FileSet $actualFileSet -Policy $policy
        if (@($actualFileSet.Errors + $actualFileValidation.Errors).Count -gt 0) { throw (@($actualFileSet.Errors + $actualFileValidation.Errors) -join '; ') }
        $result.ProductionCommit = 'FAIL'
        $actualProd = New-ProductionSnapshot -Root $script:Root -SourceMainSha $actualMainSha -ProductionBaseSha $ctx.State.RemoteProduction -FileSet $actualFileSet -CommitMessage $ctx.CommitMessage
        if ($null -ne $ctx.PreviewProductionTree -and -not (Test-OidEqual (Get-TreeOid $actualProd.ProductionSha) $ctx.PreviewProductionTree)) {
          throw 'Production candidate changed after preview. Re-run the operation.'
        }
        Write-SubRun 'Running production runtime/build validation'
        $prodValidation = Test-ProductionSnapshot -Snapshot $actualProd -RunRuntimeValidation -ProgressCallback { param($message) Write-SubRun $message }
        Assert-ReleaseValidationComplete -Validation $prodValidation
        Write-Ok 'Production validation passed'
        Write-SubRun 'Advancing local production after validation'
        $branch = Finalize-ProductionBranch -Root $script:Root -Snapshot $actualProd
        $actualProductionSha = $branch.ProductionSha
        if ($actualProd.ProductionChanged) { $result.ProductionCommit = 'PASS'; Write-Ok ("Production commit: {0}" -f $actualProductionSha) }
        else { $result.ProductionCommit = 'SKIPPED'; Write-Skip 'Production tree unchanged; no empty production commit created.' }
      } else {
        $prodTarget = Get-ProductionPushTargetWithoutCommit -State $ctx.State
        $actualProductionSha = $prodTarget.TargetSha
        Write-Skip 'Production commit message is empty; no new production commit created.'
      }
    }

    Write-Run 'Preparing optional tag'
    $tagObject = $null
    $tagTargetSha = $null
    if (-not [string]::IsNullOrWhiteSpace($ctx.Tag)) {
      $result.Tag = 'FAIL'
      if ($ctx.TagTarget -eq 'both') {
        if ($Target -notin @('both')) { throw 'Both tag target requires Both operation.' }
        $tagTargetSha = $actualProductionSha
        $tagObject = New-MenuTag -Tag $ctx.Tag -TargetSha $tagTargetSha -TargetKind 'both' -MainSourceSha $actualMainSha
      } elseif ($ctx.TagTarget -eq 'production') {
        if ($Target -notin @('production','both')) { throw 'Production tag target was selected but production is not part of this operation.' }
        $tagTargetSha = $actualProductionSha
        $tagObject = New-MenuTag -Tag $ctx.Tag -TargetSha $tagTargetSha -TargetKind $ctx.TagTarget -MainSourceSha $actualMainSha
      } else {
        if ($Target -notin @('main','both')) { throw 'Main tag target was selected but main is not part of this operation.' }
        $tagTargetSha = $actualMainSha
        $tagObject = New-MenuTag -Tag $ctx.Tag -TargetSha $tagTargetSha -TargetKind $ctx.TagTarget -MainSourceSha $actualMainSha
      }
      $localTagCreated = $true
      $result.Tag = 'LOCAL_ONLY'
      Write-Ok ("Local tag prepared: {0}" -f $ctx.Tag)
    } else { Write-Skip 'No tag requested.' }

    Write-Run 'Remote race protection'
    $remoteProductionNow = if ($Target -in @('production','both')) { Get-RemoteOid 'refs/heads/production' } else { $null }
    if (-not (Test-OidEqual (Get-RemoteOid 'refs/heads/main') $ctx.State.RemoteMain) -or -not (Test-OidEqual $remoteProductionNow $ctx.State.RemoteProduction)) {
      throw 'Remote repository changed during local preparation. Nothing has been pushed; re-run the operation.'
    }
    if (-not [string]::IsNullOrWhiteSpace($ctx.Tag) -and $null -ne (Get-RemoteOid "refs/tags/$($ctx.Tag)")) {
      throw 'Remote tag appeared during preparation. Nothing has been pushed; re-run the operation.'
    }
    Write-Ok 'Remote refs still match the preview baseline'

    Write-Run 'Publishing selected refs'
    $refs = [System.Collections.Generic.List[object]]::new()
    if ($Target -in @('main','both')) {
      $refs.Add([pscustomobject]@{ Name='main'; LocalRef='refs/heads/main'; RemoteRef='refs/heads/main'; BaselineOid=$ctx.State.RemoteMain; DesiredOid=$actualMainSha })
    }
    if ($Target -in @('production','both')) {
      $localProductionNow = Get-LocalCommitOid 'refs/heads/production'
      if ($null -ne $localProductionNow) {
        if (-not (Test-OidEqual $localProductionNow $actualProductionSha)) { throw 'Local production changed after validation. Nothing has been pushed.' }
        $refs.Add([pscustomobject]@{ Name='production'; LocalRef='refs/heads/production'; RemoteRef='refs/heads/production'; BaselineOid=$ctx.State.RemoteProduction; DesiredOid=$actualProductionSha })
      } elseif (-not (Test-OidEqual $actualProductionSha $ctx.State.RemoteProduction)) {
        throw 'Production target differs from origin but no local production ref exists.'
      }
    }
    if ($localTagCreated) {
      $refs.Add([pscustomobject]@{ Name='tag'; LocalRef="refs/tags/$($ctx.Tag)"; RemoteRef="refs/tags/$($ctx.Tag)"; BaselineOid=$null; DesiredOid=$tagObject })
    }
    if ($Target -in @('main','both') -and -not (Test-OidEqual $actualMainSha $ctx.State.RemoteMain)) { $result.MainPush = 'FAIL' }
    if ($Target -in @('production','both') -and -not (Test-OidEqual $actualProductionSha $ctx.State.RemoteProduction)) { $result.ProductionPush = 'FAIL' }
    $publication = Publish-MenuRefs -Refs $refs.ToArray()
    if ($publication.Status -eq 'PASS') {
      if ($Target -in @('main','both') -and -not (Test-OidEqual $actualMainSha $ctx.State.RemoteMain)) { $result.MainPush = 'PASS' }
      if ($Target -in @('production','both') -and -not (Test-OidEqual $actualProductionSha $ctx.State.RemoteProduction)) { $result.ProductionPush = 'PASS' }
      Write-Ok ("Publication complete via {0}" -f $publication.Method)
    } else { Write-Skip 'Selected branch refs already matched origin.' }

    Write-Run 'Verifying remote refs'
    if ($Target -in @('main','both') -and -not (Test-OidEqual (Get-RemoteOid 'refs/heads/main') $actualMainSha)) { throw 'Remote main verification failed.' }
    if ($Target -in @('production','both') -and -not (Test-OidEqual (Get-RemoteOid 'refs/heads/production') $actualProductionSha)) { throw 'Remote production verification failed.' }
    if ($localTagCreated -and -not (Test-OidEqual (Get-RemoteOid "refs/tags/$($ctx.Tag)") $tagObject)) { throw 'Remote tag verification failed.' }
    if ($localTagCreated) { $result.Tag = 'PASS' }
    Write-Ok 'Remote refs verified'

    Write-Run 'Optional GitHub Release'
    if ($ctx.CreateRelease) {
      if (-not $localTagCreated) { throw 'Release requested but no tag was prepared.' }
      $result.Release = 'FAIL'
      $url = New-LatestGitHubRelease -Tag $ctx.Tag -ReleaseName $ctx.ReleaseName -TargetKind $ctx.TagTarget -TargetSha $tagTargetSha -MainSourceSha $actualMainSha
      $result.Release = 'PASS'
      Write-Ok ("GitHub Release created and marked Latest: {0}" -f $url)
    } else { Write-Skip 'GitHub Release not requested.' }

    Write-Run 'Final result'
  } catch {
    $script:HadOperationFailure = $true
    Write-Fail $_.Exception.Message
    if ($result.MainCommit -ne 'PASS' -and $Target -in @('main','both')) { $result.MainCommit = if ([string]::IsNullOrWhiteSpace($ctx.CommitMessage)) { 'SKIPPED' } else { $result.MainCommit } }
  } finally {
    if ($null -ne $previewProd) {
      try { Remove-PreviewProduction $previewProd } catch { $result.Cleanup = 'FAIL'; $script:HadOperationFailure = $true; Write-Warn $_.Exception.Message }
    }
    if ($null -ne $actualProd) {
      try {
        Write-SubRun 'Removing temporary production worktree'
        Remove-TemporaryReleaseContext -Context $actualProd.Context
        Write-Ok 'Temporary production worktree removed'
      } catch { $result.Cleanup = 'FAIL'; $script:HadOperationFailure = $true; Write-Warn $_.Exception.Message }
    }
    Show-Results $result
  }
}

function Show-MainMenu {
  while ($true) {
    Clear-MenuScreen
    Write-ColorLine 'TradingBot Git Manager' Cyan
    Write-ColorLine ('=' * 72) DarkGray
    Write-Info ("Repository : {0}" -f $script:Root)
    Write-Info ("GitHub     : {0}" -f $(if ($script:RepoName) { $script:RepoName } else { '<unknown>' }))
    Write-Info ("Branch     : {0}" -f (Get-ActiveBranch))
    foreach ($blocker in @(Get-RepositoryBlockers)) { Write-Warn $blocker }
    $origin = Invoke-GitSafe @('remote', 'get-url', 'origin')
    if ($origin.ExitCode -ne 0) { Write-Warn 'origin is not configured. Configure it before previewing or publishing.' }
    Write-ColorLine ('=' * 72) DarkGray
    Write-Host ''
    Write-ColorLine '1. Main' White
    Write-ColorLine '2. Production' White
    Write-ColorLine '3. Both' White
    Write-ColorLine '4. Preview Only' White
    Write-ColorLine '5. Dry Run' White
    Write-ColorLine '0. Exit' DarkGray
    Write-Host ''
    $choice = (Read-Host 'Select').Trim()
    try {
      switch ($choice) {
        '1' { Invoke-InteractiveOperation -Target 'main'; Pause-Menu }
        '2' { Invoke-InteractiveOperation -Target 'production'; Pause-Menu }
        '3' { Invoke-InteractiveOperation -Target 'both'; Pause-Menu }
        '4' {
          $target = Read-TargetChoice -AllowBack
          if ($target -ne 'back') { Invoke-PreviewOnly -Target $target; Pause-Menu }
        }
        '5' {
          $target = Read-TargetChoice -AllowBack
          if ($target -ne 'back') { Invoke-InteractiveOperation -Target $target -DryRun; Pause-Menu }
        }
        '0' { return }
        default { Write-Warn 'Invalid selection.'; Start-Sleep -Milliseconds 700 }
      }
    } catch {
      $script:HadOperationFailure = $true
      Write-Fail $_.Exception.Message
      Pause-Menu
    }
  }
}

if ($LoadFunctionsOnly) { return }

try {
  $script:Root = Resolve-TradingBotProjectRoot -ScriptPath $PSCommandPath
  try { $script:RepoName = Get-OriginRepositoryName } catch { $script:RepoName = '' }
  Show-MainMenu
  if ($script:HadOperationFailure) { exit 1 }
  exit 0
} catch {
  Write-Fail $_.Exception.Message
  exit 1
}
