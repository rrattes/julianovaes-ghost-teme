# Julia Novaes Ghost Theme

Tema Ghost e arquivos auxiliares do site da psicologa Julia Novaes.

## Estrutura

- `ghost-theme/julia-novaes/`: tema Ghost versionado.
- `scripts/`: automacoes locais para subir Ghost, sincronizar tema e semear conteudo.
- `PROJECT_BRIEF.md`: briefing de direcao visual, conteudo e criterios do projeto.
- `mockups-home.html`: mockup inicial usado na fase de exploracao.

## Ambiente local

O Ghost local fica em `ghost-local/`, que nao e versionado.

Com o Ghost ja instalado localmente:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-ghost.ps1
```

Para parar:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\stop-ghost.ps1
```

Para sincronizar alteracoes do tema versionado para a instalacao local:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-ghost-theme.ps1
```

Para sincronizar redirects legados:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-ghost-redirects.ps1
```

Para recriar artigos e paginas locais:

```powershell
C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\scripts\seed-ghost-articles.py
C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\scripts\seed-ghost-pages.py
```

## URLs locais

- Site: `http://127.0.0.1:2368/`
- Admin: `http://127.0.0.1:2368/ghost/`

## Observacoes

As imagens oficiais de logo e posts estao versionadas dentro do tema, em `ghost-theme/julia-novaes/assets/images/`.

## Trocar foto definitiva do hero

Hoje o hero usa temporariamente:

```txt
ghost-theme/julia-novaes/assets/images/posts/post-psicoterapia.png
```

Para colocar a foto definitiva:

1. Salve a imagem em `ghost-theme/julia-novaes/assets/images/hero-definitivo.png`.
2. Abra `ghost-theme/julia-novaes/index.hbs`.
3. Troque o caminho dentro do bloco `.hero-image` para:

```hbs
<img src="{{asset "images/hero-definitivo.png"}}" alt="Descricao da imagem">
```

4. Rode `scripts/sync-ghost-theme.ps1` no ambiente local ou copie o tema para o servidor.
