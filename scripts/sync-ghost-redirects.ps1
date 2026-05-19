$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$source = Join-Path $root "redirects.yaml"
$targetDir = Join-Path $root "ghost-local\content\data"
$target = Join-Path $targetDir "redirects.yaml"

if (!(Test-Path -LiteralPath $source)) {
  throw "redirects.yaml not found at $source"
}

if (!(Test-Path -LiteralPath $targetDir)) {
  New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
}

Copy-Item -LiteralPath $source -Destination $target -Force
Write-Host "Ghost redirects synced to $target"
