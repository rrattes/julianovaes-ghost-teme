$ErrorActionPreference = "Stop"

Set-Location -LiteralPath "C:\Users\Admin\OneDrive\Documentos\Site-JuliaNovaes"
& "C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m http.server 4173 --bind 127.0.0.1
