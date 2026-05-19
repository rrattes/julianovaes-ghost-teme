$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$source = Join-Path $root "ghost-theme\julia-novaes"
$target = Join-Path $root "ghost-local\content\themes\julia-novaes"

if (!(Test-Path -LiteralPath $source)) {
  throw "Theme source not found: $source"
}

if (Test-Path -LiteralPath $target) {
  Remove-Item -LiteralPath $target -Recurse -Force
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
Copy-Item -LiteralPath $source -Destination $target -Recurse -Force

Write-Host "Ghost theme synced to $target"
