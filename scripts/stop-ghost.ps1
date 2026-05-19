$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$ghostDir = Join-Path $root "ghost-local"
$shimDir = Join-Path $root ".ghost-bin"
$pythonDir = "C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python"
$pythonScriptsDir = Join-Path $pythonDir "Scripts"

$env:PATH = "$shimDir;$pythonDir;$pythonScriptsDir;" + $env:PATH

Set-Location -LiteralPath $ghostDir
npm exec --yes --package node@22 --package ghost-cli -- ghost stop
