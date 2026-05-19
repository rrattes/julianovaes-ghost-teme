# Deploy em Ubuntu 22.04

Este diretorio contem um instalador para publicar o site Ghost da Julia Novaes em um servidor Ubuntu 22.04 que ja pode ter Nginx com outros sites.

O script cria um server block separado para este dominio e nao remove configuracoes existentes do Nginx.

## Uso basico

No servidor:

```bash
git clone https://github.com/rrattes/julianovaes-ghost-teme.git
cd julianovaes-ghost-teme
```

Execute:

```bash
sudo DOMAIN=www.julianovaes.com.br \
  ALT_DOMAIN=julianovaes.com.br \
  MYSQL_PASSWORD='troque-esta-senha' \
  CERTBOT_EMAIL='seu-email@dominio.com' \
  bash deploy/install-ubuntu-22-ghost.sh
```

## Sem SSL no primeiro teste

Use isto quando o DNS ainda nao aponta para o servidor:

```bash
sudo DOMAIN=www.julianovaes.com.br \
  ALT_DOMAIN=julianovaes.com.br \
  MYSQL_PASSWORD='troque-esta-senha' \
  SKIP_SSL=1 \
  bash deploy/install-ubuntu-22-ghost.sh
```

## Porta do Ghost

Por padrao o Ghost sera configurado na porta `2369`, para evitar conflito com outro Ghost/site que ja use `2368`.

Para alterar:

```bash
sudo GHOST_PORT=2370 MYSQL_PASSWORD='troque-esta-senha' bash deploy/install-ubuntu-22-ghost.sh
```

## Importar um .sql

Se voce tiver um dump MySQL compativel com a mesma versao do Ghost:

```bash
sudo DOMAIN=www.julianovaes.com.br \
  ALT_DOMAIN=julianovaes.com.br \
  MYSQL_PASSWORD='troque-esta-senha' \
  IMPORT_SQL_PATH=/tmp/julianovaes.sql \
  CERTBOT_EMAIL='seu-email@dominio.com' \
  bash deploy/install-ubuntu-22-ghost.sh
```

O script faz um backup antes de importar:

```txt
/root/julianovaes_prod-before-import-YYYYMMDD-HHMMSS.sql
```

Importante: o banco local deste projeto e SQLite (`ghost-local.db`). Ele nao pode ser importado diretamente no MySQL. Para conteudo de producao, prefira uma exportacao/importacao oficial do Ghost Admin, ou gere um dump MySQL a partir de outra instalacao Ghost MySQL.

## Depois do deploy

Verifique:

```bash
curl -I http://www.julianovaes.com.br/
curl -I http://www.julianovaes.com.br/about-me
curl -I http://www.julianovaes.com.br/marcar-consulta
```

As URLs antigas devem responder com `301`.

Admin:

```txt
https://www.julianovaes.com.br/ghost/
```
