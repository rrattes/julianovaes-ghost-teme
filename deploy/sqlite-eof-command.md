# Criar o instalador SQLite no servidor usando EOF

Cole no servidor Ubuntu:

```bash
cat > install-julianovaes-sqlite.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${DOMAIN:-www.julianovaes.com.br}"
ALT_DOMAIN="${ALT_DOMAIN:-julianovaes.com.br}"
SITE_URL="${SITE_URL:-https://${DOMAIN}}"
SITE_DIR="${SITE_DIR:-/var/www/julianovaes}"
GHOST_USER="${GHOST_USER:-ghost-julianovaes}"
GHOST_PORT="${GHOST_PORT:-2369}"
SERVICE_NAME="${SERVICE_NAME:-ghost-julianovaes}"
REPO_URL="${REPO_URL:-https://github.com/rrattes/julianovaes-ghost-teme.git}"
REPO_BRANCH="${REPO_BRANCH:-main}"
REPO_DIR="${REPO_DIR:-/opt/julianovaes-ghost-theme}"
SQLITE_DB_PATH="${SQLITE_DB_PATH:-${SITE_DIR}/content/data/ghost-local.db}"
CERTBOT_EMAIL="${CERTBOT_EMAIL:-}"
SKIP_SSL="${SKIP_SSL:-0}"

if [[ "${EUID}" -ne 0 ]]; then
  echo "ERROR: run this script with sudo/root."
  exit 1
fi

apt-get update
apt-get install -y nginx curl git rsync ca-certificates certbot python3-certbot-nginx python3 sqlite3

if ! command -v node >/dev/null 2>&1 || ! node -v | grep -Eq '^v22\.'; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi

npm install -g ghost-cli@latest

if ! id "$GHOST_USER" >/dev/null 2>&1; then
  adduser --disabled-password --gecos "" "$GHOST_USER"
fi

mkdir -p "$SITE_DIR" "$REPO_DIR"
chown -R "$GHOST_USER:$GHOST_USER" "$SITE_DIR"

if [[ -d "${REPO_DIR}/.git" ]]; then
  git -C "$REPO_DIR" fetch origin "$REPO_BRANCH"
  git -C "$REPO_DIR" checkout "$REPO_BRANCH"
  git -C "$REPO_DIR" reset --hard "origin/${REPO_BRANCH}"
else
  rm -rf "$REPO_DIR"
  git clone --branch "$REPO_BRANCH" "$REPO_URL" "$REPO_DIR"
fi

if [[ ! -d "${SITE_DIR}/current" ]]; then
  chown -R "$GHOST_USER:$GHOST_USER" "$SITE_DIR"
  sudo -H -u "$GHOST_USER" bash -lc "cd '$SITE_DIR' && ghost install local --no-start --no-prompt"
fi

cat > "${SITE_DIR}/config.production.json" <<CONFIG
{
  "url": "${SITE_URL}",
  "server": {
    "port": ${GHOST_PORT},
    "host": "127.0.0.1"
  },
  "database": {
    "client": "sqlite3",
    "connection": {
      "filename": "${SQLITE_DB_PATH}"
    },
    "useNullAsDefault": true,
    "debug": false
  },
  "mail": {
    "transport": "Direct"
  },
  "logging": {
    "transports": [
      "file",
      "stdout"
    ]
  },
  "process": "systemd",
  "paths": {
    "contentPath": "${SITE_DIR}/content"
  },
  "security": {
    "staffDeviceVerification": false
  }
}
CONFIG

chown "$GHOST_USER:$GHOST_USER" "${SITE_DIR}/config.production.json"
mkdir -p "${SITE_DIR}/content/themes" "${SITE_DIR}/content/data" "${SITE_DIR}/content/images/2026/05"
rsync -a --delete "${REPO_DIR}/ghost-theme/julia-novaes/" "${SITE_DIR}/content/themes/julia-novaes/"
cp "${REPO_DIR}/redirects.yaml" "${SITE_DIR}/content/data/redirects.yaml"
chown -R "$GHOST_USER:$GHOST_USER" "${SITE_DIR}/content"

sudo -H -u "$GHOST_USER" bash -lc "PROJECT_ROOT='$REPO_DIR' GHOST_DB_PATH='$SQLITE_DB_PATH' GHOST_IMAGES_TARGET='${SITE_DIR}/content/images/2026/05' python3 '$REPO_DIR/scripts/seed-ghost-articles.py'"
sudo -H -u "$GHOST_USER" bash -lc "PROJECT_ROOT='$REPO_DIR' GHOST_DB_PATH='$SQLITE_DB_PATH' python3 '$REPO_DIR/scripts/seed-ghost-pages.py'"

sudo -H -u "$GHOST_USER" sqlite3 "$SQLITE_DB_PATH" <<SQL
UPDATE settings SET value = 'julia-novaes', updated_at = datetime('now') WHERE key = 'active_theme';
UPDATE settings SET value = 'Julia Novaes Psicóloga', updated_at = datetime('now') WHERE key = 'title';
UPDATE settings SET value = 'Psicologia com escuta, ética e presença.', updated_at = datetime('now') WHERE key = 'description';
SQL

cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<SERVICE
[Unit]
Description=Ghost site ${DOMAIN}
After=network.target

[Service]
Type=simple
WorkingDirectory=${SITE_DIR}
User=${GHOST_USER}
Group=${GHOST_USER}
Environment=NODE_ENV=production
ExecStart=/usr/bin/node ${SITE_DIR}/current/index.js
Restart=always
RestartSec=10
SyslogIdentifier=${SERVICE_NAME}

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"

NGINX_CONF="/etc/nginx/sites-available/${DOMAIN}.conf"
cat > "$NGINX_CONF" <<NGINX
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN} ${ALT_DOMAIN};

    client_max_body_size 50m;

    location / {
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header Host \$host;
        proxy_pass http://127.0.0.1:${GHOST_PORT};
    }
}
NGINX

ln -sfn "$NGINX_CONF" "/etc/nginx/sites-enabled/${DOMAIN}.conf"
nginx -t
systemctl reload nginx

systemctl restart "$SERVICE_NAME"
sleep 4
curl -fsSI "http://127.0.0.1:${GHOST_PORT}/" >/dev/null
curl -fsSI "http://127.0.0.1:${GHOST_PORT}/sobre/" >/dev/null
curl -fsSI "http://127.0.0.1:${GHOST_PORT}/contato/" >/dev/null

if [[ "$SKIP_SSL" != "1" && -n "$CERTBOT_EMAIL" ]]; then
  certbot --nginx \
    -d "$DOMAIN" \
    -d "$ALT_DOMAIN" \
    --non-interactive \
    --agree-tos \
    -m "$CERTBOT_EMAIL" \
    --redirect
fi

echo "Done: ${SITE_URL}"
echo "Admin: ${SITE_URL}/ghost/"
echo "SQLite DB: ${SQLITE_DB_PATH}"
EOF

chmod +x install-julianovaes-sqlite.sh
```

Executar:

```bash
sudo DOMAIN=www.julianovaes.com.br \
  ALT_DOMAIN=julianovaes.com.br \
  CERTBOT_EMAIL='seu-email@dominio.com' \
  ./install-julianovaes-sqlite.sh
```

Sem SSL enquanto DNS nao aponta:

```bash
sudo DOMAIN=www.julianovaes.com.br \
  ALT_DOMAIN=julianovaes.com.br \
  SKIP_SSL=1 \
  ./install-julianovaes-sqlite.sh
```
