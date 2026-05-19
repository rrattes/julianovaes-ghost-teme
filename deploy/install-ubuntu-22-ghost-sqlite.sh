#!/usr/bin/env bash
set -euo pipefail

# Ubuntu 22.04 Ghost deploy with SQLite.
# This is simpler than the MySQL deploy and is intended for small sites.
#
# One-line usage after cloning the repo:
#
#   sudo DOMAIN=www.julianovaes.com.br \
#     ALT_DOMAIN=julianovaes.com.br \
#     CERTBOT_EMAIL='email@example.com' \
#     bash deploy/install-ubuntu-22-ghost-sqlite.sh
#
# Without SSL while DNS is not ready:
#
#   sudo DOMAIN=www.julianovaes.com.br ALT_DOMAIN=julianovaes.com.br SKIP_SSL=1 \
#     bash deploy/install-ubuntu-22-ghost-sqlite.sh

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

echo "==> Installing system packages"
apt-get update
apt-get install -y nginx curl git rsync ca-certificates certbot python3-certbot-nginx python3 sqlite3

if ! command -v node >/dev/null 2>&1 || ! node -v | grep -Eq '^v22\.'; then
  echo "==> Installing Node.js 22"
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi

echo "==> Installing Ghost CLI"
npm install -g ghost-cli@latest

echo "==> Creating Ghost user and directories"
if ! id "$GHOST_USER" >/dev/null 2>&1; then
  adduser --disabled-password --gecos "" "$GHOST_USER"
fi

mkdir -p "$SITE_DIR" "$REPO_DIR"
chown -R "$GHOST_USER:$GHOST_USER" "$SITE_DIR"

echo "==> Cloning or updating repository"
if [[ -d "${REPO_DIR}/.git" ]]; then
  git -C "$REPO_DIR" fetch origin "$REPO_BRANCH"
  git -C "$REPO_DIR" checkout "$REPO_BRANCH"
  git -C "$REPO_DIR" reset --hard "origin/${REPO_BRANCH}"
else
  rm -rf "$REPO_DIR"
  git clone --branch "$REPO_BRANCH" "$REPO_URL" "$REPO_DIR"
fi

echo "==> Installing Ghost locally with SQLite if needed"
if [[ ! -d "${SITE_DIR}/current" ]]; then
  chown -R "$GHOST_USER:$GHOST_USER" "$SITE_DIR"
  sudo -H -u "$GHOST_USER" bash -lc "cd '$SITE_DIR' && ghost install local --no-start --no-prompt"
else
  echo "Ghost files already exist at ${SITE_DIR}"
fi

echo "==> Writing production SQLite config"
cat > "${SITE_DIR}/config.production.json" <<EOF
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
EOF

chown "$GHOST_USER:$GHOST_USER" "${SITE_DIR}/config.production.json"

echo "==> Installing theme, redirects, and seed content"
mkdir -p "${SITE_DIR}/content/themes" "${SITE_DIR}/content/data" "${SITE_DIR}/content/images/2026/05"
rsync -a --delete "${REPO_DIR}/ghost-theme/julia-novaes/" "${SITE_DIR}/content/themes/julia-novaes/"
cp "${REPO_DIR}/redirects.yaml" "${SITE_DIR}/content/data/redirects.yaml"
chown -R "$GHOST_USER:$GHOST_USER" "${SITE_DIR}/content"

echo "==> Seeding SQLite database with pages and posts"
sudo -H -u "$GHOST_USER" bash -lc "PROJECT_ROOT='$REPO_DIR' GHOST_DB_PATH='$SQLITE_DB_PATH' GHOST_IMAGES_TARGET='${SITE_DIR}/content/images/2026/05' python3 '$REPO_DIR/scripts/seed-ghost-articles.py'"
sudo -H -u "$GHOST_USER" bash -lc "PROJECT_ROOT='$REPO_DIR' GHOST_DB_PATH='$SQLITE_DB_PATH' python3 '$REPO_DIR/scripts/seed-ghost-pages.py'"

echo "==> Activating theme and site metadata in SQLite"
sudo -H -u "$GHOST_USER" sqlite3 "$SQLITE_DB_PATH" <<SQL
UPDATE settings SET value = 'julia-novaes', updated_at = datetime('now') WHERE key = 'active_theme';
UPDATE settings SET value = 'Julia Novaes Psicóloga', updated_at = datetime('now') WHERE key = 'title';
UPDATE settings SET value = 'Psicologia com escuta, ética e presença.', updated_at = datetime('now') WHERE key = 'description';
SQL

echo "==> Creating systemd service"
cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
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
EOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"

echo "==> Creating Nginx server block without touching existing sites"
NGINX_CONF="/etc/nginx/sites-available/${DOMAIN}.conf"
cat > "$NGINX_CONF" <<EOF
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
EOF

ln -sfn "$NGINX_CONF" "/etc/nginx/sites-enabled/${DOMAIN}.conf"
nginx -t
systemctl reload nginx

echo "==> Starting Ghost"
systemctl restart "$SERVICE_NAME"
sleep 4
systemctl --no-pager --full status "$SERVICE_NAME" || true

echo "==> Local health check"
curl -fsSI "http://127.0.0.1:${GHOST_PORT}/" >/dev/null
curl -fsSI "http://127.0.0.1:${GHOST_PORT}/sobre/" >/dev/null
curl -fsSI "http://127.0.0.1:${GHOST_PORT}/contato/" >/dev/null

if [[ "$SKIP_SSL" != "1" ]]; then
  if [[ -z "$CERTBOT_EMAIL" ]]; then
    echo "==> SSL skipped: set CERTBOT_EMAIL to enable Let's Encrypt."
  else
    echo "==> Requesting Let's Encrypt certificate"
    certbot --nginx \
      -d "$DOMAIN" \
      -d "$ALT_DOMAIN" \
      --non-interactive \
      --agree-tos \
      -m "$CERTBOT_EMAIL" \
      --redirect
  fi
fi

echo "==> Done"
echo "Site:       ${SITE_URL}"
echo "Admin:      ${SITE_URL}/ghost/"
echo "SQLite DB:  ${SQLITE_DB_PATH}"
echo "Service:    systemctl status ${SERVICE_NAME}"
echo "Logs:       journalctl -u ${SERVICE_NAME} -f"
echo "Redirects:  curl -I http://${DOMAIN}/about-me"
