[CmdletBinding()]
param(
  [string] $CommitMessage = '',
  [string] $ReleaseTag = '',
  [switch] $DryRun,
  [switch] $NonInteractive,
  [switch] $VerboseReport
)

$ErrorActionPreference = 'Stop'
try {
  Import-Module (Join-Path $PSScriptRoot 'Release.Workflow.psm1') -Force -DisableNameChecking
  $parameters = @{
    ScriptPath = $PSCommandPath
    CommitMessage = $CommitMessage
    ReleaseTag = $ReleaseTag
    DryRun = [bool]$DryRun
    NonInteractive = [bool]$NonInteractive
  }
  $result = Invoke-TradingBotRelease -Parameters $parameters
  if ($VerboseReport) { $result | ConvertTo-Json -Depth 8 }
  else { $result | Format-List Mode, LocalMain, LocalProduction, Tag, TagStatus, GitHubRelease, TemporaryWorktree, Publication, Error }
  if ($result.Mode -notin @('DRY_RUN', 'PUBLISHED')) { exit 1 }
  exit 0
} catch {
  Write-Host ("[FAIL] {0}" -f $_.Exception.Message) -ForegroundColor Red
  exit 1
}
