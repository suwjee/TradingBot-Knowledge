[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$ChartRoot = Join-Path $Root 'apps\chart'
$LocalStateRoot = $null
$env:PYTHONDONTWRITEBYTECODE = '1'

# Runtime dependencies used by the maintained Python engine.
$PythonPackages = @('orjson', 'tzdata')

# Authoritative production layout after the engine refactor.
$EngineFiles = @(
  'engine\bridge\trading_pipeline.py',
  'engine\pipeline\reaction_engine.py',
  'engine\pipeline\blue_line_detector.py',
  'engine\pipeline\a_zone_detector.py',
  'engine\pipeline\s_zone_detector.py',
  'engine\pipeline\e_zone_detector.py',
  'engine\pipeline\lifecycle_engine.py'
)

$PythonPackageFiles = @(
  'engine\__init__.py',
  'engine\pipeline\__init__.py'
)

$ChartFiles = @(
  'apps\chart\package.json',
  'apps\chart\vite.config.js',
  'apps\chart\scripts\dev-server.mjs'
)

function Write-Step([string]$Text, [ConsoleColor]$Color = 'Gray') {
  Write-Host ("[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $Text) -ForegroundColor $Color
}

function Find-Command([string[]]$Names) {
  foreach ($name in $Names) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
  }
  return $null
}

function Refresh-Path {
  $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
    [Environment]::GetEnvironmentVariable('Path', 'User')
}

function Install-Winget([string]$Id, [string]$Label) {
  $winget = Find-Command @('winget.exe', 'winget')
  if (-not $winget) {
    throw "winget is required to install $Label automatically. Install App Installer and retry."
  }

  Write-Step "Installing/updating $Label..." Yellow
  & $winget install --id $Id --exact --silent --accept-package-agreements --accept-source-agreements
  if ($LASTEXITCODE -ne 0) {
    throw "Unable to install/update $Label (winget exit code $LASTEXITCODE)."
  }
  Refresh-Path
}

function Ensure-Path([string]$Path, [string]$Label) {
  if (-not (Test-Path -LiteralPath $Path)) {
    throw "Required $Label was not found: $Path"
  }
}

function Ensure-ProjectFiles {
  $required = @($ChartFiles + $PythonPackageFiles + $EngineFiles)
  foreach ($relative in $required) {
    Ensure-Path (Join-Path $Root $relative) $relative
  }

  $manifestPath = Join-Path $ChartRoot 'package.json'
  try {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
  } catch {
    throw "Invalid apps\\chart\\package.json: $($_.Exception.Message)"
  }

  if (-not $manifest.scripts -or -not $manifest.scripts.dev) {
    throw 'apps\\chart\\package.json must define scripts.dev.'
  }

  Write-Step 'Project structure matches the refactored TradingBot layout.' Green
}

function Ensure-Directories {
  $directories = @(
    'data\raw',
    'cache\drawings',
    'cache\indicator-calculations',
    'cache\indicator-templates',
    'secret',
    'tmp\faraz-candle-exports'
  )

  foreach ($relative in $directories) {
    New-Item -ItemType Directory -Force -Path (Join-Path $LocalStateRoot $relative) | Out-Null
  }
}

function Resolve-LocalState([string]$Node) {
  # Use the application's resolver so launcher and server enforce one path policy.
  $resolver = Join-Path $ChartRoot 'server\local-state-paths.js'
  $program = 'import { pathToFileURL } from ''node:url''; const { resolveLocalStatePaths } = await import(pathToFileURL(process.argv[1])); process.stdout.write(resolveLocalStatePaths(process.argv[2]).root);'
  $resolved = & $Node --input-type=module -e $program $resolver $Root
  if ($LASTEXITCODE -ne 0) { throw 'Unable to resolve the dedicated chart state directory.' }
  $script:LocalStateRoot = $resolved
  $env:TRADINGBOT_LOCAL_STATE_ROOT = $script:LocalStateRoot
}

function Ensure-Runtimes {
  $node = Find-Command @('node.exe', 'node')
  if (-not $node) {
    Install-Winget 'OpenJS.NodeJS.LTS' 'Node.js LTS'
    $node = Find-Command @('node.exe', 'node')
  }
  if (-not $node) { throw 'Node.js is unavailable after installation.' }

  $nodeVersion = [version]((& $node --version).Trim().TrimStart('v'))
  if ($nodeVersion -lt [version]'20.19.0') {
    Install-Winget 'OpenJS.NodeJS.LTS' 'Node.js LTS'
    $node = Find-Command @('node.exe', 'node')
    if (-not $node) { throw 'Node.js is unavailable after update.' }
    $nodeVersion = [version]((& $node --version).Trim().TrimStart('v'))
    if ($nodeVersion -lt [version]'20.19.0') {
      throw "Node.js 20.19.0 or newer is required; found $nodeVersion."
    }
  }

  $npm = Find-Command @('npm.cmd', 'npm')
  if (-not $npm) { throw 'npm was not found alongside Node.js.' }

  $python = Find-Command @('python.exe', 'python', 'py.exe', 'py')
  if (-not $python) {
    Install-Winget 'Python.Python.3.12' 'Python 3.12'
    $python = Find-Command @('python.exe', 'python', 'py.exe', 'py')
  }
  if (-not $python) { throw 'Python is unavailable after installation.' }

  $pythonVersionText = (& $python --version 2>&1).ToString().Trim()
  if ($pythonVersionText -notmatch 'Python\s+(\d+)\.(\d+)') {
    throw "Unable to determine Python version: $pythonVersionText"
  }
  $pythonVersion = [version]("{0}.{1}" -f $Matches[1], $Matches[2])
  if ($pythonVersion -lt [version]'3.12') {
    throw "Python 3.12 or newer is required; found $pythonVersionText."
  }

  foreach ($package in $PythonPackages) {
    & $python -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('$package') else 1)" 2>$null
    if ($LASTEXITCODE -ne 0) {
      Write-Step "Installing Python package $package..." Yellow
      & $python -m pip install --disable-pip-version-check --quiet $package
      if ($LASTEXITCODE -ne 0) { throw "Failed to install Python package $package." }
    }
  }

  foreach ($relative in @($PythonPackageFiles + $EngineFiles)) {
    $path = Join-Path $Root $relative
    & $python -B -c "import ast,pathlib,sys; ast.parse(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8-sig'))" $path
    if ($LASTEXITCODE -ne 0) { throw "Python syntax validation failed: $relative" }
  }

  Write-Step (
    "Node {0}; npm {1}; {2}" -f
    (& $node --version).Trim(),
    (& $npm --version).Trim(),
    $pythonVersionText
  ) Green

  return [pscustomobject]@{
    Node = $node
    Npm = $npm
    Python = $python
  }
}

function Ensure-NpmDependencies([string]$Npm) {
  Push-Location $ChartRoot
  try {
    $requiredNodeModules = @('vite', 'lightweight-charts', 'playwright-core')
    $missing = @(
      $requiredNodeModules | Where-Object {
        -not (Test-Path -LiteralPath (Join-Path $ChartRoot ("node_modules\{0}" -f $_)))
      }
    )

    if ($missing.Count -gt 0) {
      Write-Step ("Installing npm dependencies (missing: {0})..." -f ($missing -join ', ')) Yellow
      if (Test-Path -LiteralPath (Join-Path $ChartRoot 'package-lock.json')) {
        & $Npm ci
      } else {
        & $Npm install
      }
      if ($LASTEXITCODE -ne 0) {
        throw "npm dependency installation failed (exit code $LASTEXITCODE)."
      }
    }

    foreach ($module in $requiredNodeModules) {
      if (-not (Test-Path -LiteralPath (Join-Path $ChartRoot ("node_modules\{0}" -f $module)))) {
        throw "npm dependency is still missing after installation: $module"
      }
    }
  } finally {
    Pop-Location
  }

  Write-Step 'npm dependencies are ready.' Green
}

function Start-DevServer([string]$Npm, [string]$Python) {
  $env:TRADINGBOT_PYTHON = $Python
  $env:TRADINGBOT_PROJECT_ROOT = $Root

  Push-Location $ChartRoot
  try {
    Write-Step 'Starting TradingBot development server...' Cyan
    # Vite's bundled config loader corrupts paths on the VMware shared drive.
    # Native loading keeps the launcher's reported LAN addresses routable.
    & $Npm run dev -- --host 0.0.0.0 --configLoader native
    if ($LASTEXITCODE -ne 0) {
      throw "npm run dev exited with code $LASTEXITCODE."
    }
  } finally {
    Pop-Location
  }
}

try {
  Write-Step "Checking project at $Root" Cyan
  Ensure-ProjectFiles
  $tools = Ensure-Runtimes
  Resolve-LocalState $tools.Node
  Ensure-Directories
  Ensure-NpmDependencies $tools.Npm
  Start-DevServer $tools.Npm $tools.Python
} catch {
  Write-Step $_.Exception.Message Red
  Write-Host "`nStartup failed. Press any key to close." -ForegroundColor Red
  $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
  exit 1
}
