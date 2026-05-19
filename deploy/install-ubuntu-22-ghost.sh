#!/usr/bin/env bash
set -euo pipefail

# Ubuntu 22.04 Ghost deploy for julianovaes.com.br.
# Run as root or with sudo:
#
#   sudo DOMAIN=www.julianovaes.com.br \
#     ALT_DOMAIN=julianovaes.com.br \
#     MYSQL_PASSWORD='change-this-password' \
#     CERTBOT_EMAIL='email@example.com' \
#     bash deploy/install-ubuntu-22-ghost.sh
#
# Optional MySQL import:
#
#   sudo IMPORT_SQL_PATH=/tmp/julianovaes.sql MYSQL_PASSWORD='...' bash deploy/install-ubuntu-22-ghost.sh
#
# IMPORTANT: IMPORT_SQL_PATH must be a MySQL dump compatible with the installed
# Ghost version. A local SQLite ghost-local.db cannot be imported directly.

DOMAIN="${DOMAIN:-www.julianovaes.com.br}"
ALT_DOMAIN="${ALT_DOMAIN:-julianovaes.com.br}"
SITE_URL="${SITE_URL:-https://${DOMAIN}}"
SITE_DIR="${SITE_DIR:-/var/www/julianovaes}"
GHOST_USER="${GHOST_USER:-ghost-julianovaes}"
GHOST_PORT="${GHOST_PORT:-2369}"

REPO_URL="${REPO_URL:-https://github.com/rrattes/julianovaes-ghost-teme.git}"
REPO_BRANCH="${REPO_BRANCH:-main}"
REPO_DIR="${REPO_DIR:-/opt/julianovaes-ghost-theme}"

MYSQL_DB="${MYSQL_DB:-julianovaes_prod}"
MYSQL_USER="${MYSQL_USER:-julianovaes}"
MYSQL_PASSWORD="${MYSQL_PASSWORD:-}"
IMPORT_SQL_PATH="${IMPORT_SQL_PATH:-}"

CERTBOT_EMAIL="${CERTBOT_EMAIL:-}"
SKIP_SSL="${SKIP_SSL:-0}"

if [[ -z "$MYSQL_PASSWORD" ]]; then
  echo "ERROR: MYSQL_PASSWORD is required."
  exit 1
fi

if [[ "${EUID}" -ne 0 ]]; then
  echo "ERROR: run this script with sudo/root."
  exit 1
fi

echo "==> Installing system packages"
apt-get update
apt-get install -y nginx mysql-server curl git unzip rsync ca-certificates certbot python3-certbot-nginx

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

echo "==> Creating MySQL database and user"
mysql <<SQL
CREATE DATABASE IF NOT EXISTS \`${MYSQL_DB}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
ALTER USER '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${MYSQL_DB}\`.* TO '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;
SQL

echo "==> Cloning or updating repository"
if [[ -d "${REPO_DIR}/.git" ]]; then
  git -C "$REPO_DIR" fetch origin "$REPO_BRANCH"
  git -C "$REPO_DIR" checkout "$REPO_BRANCH"
  git -C "$REPO_DIR" reset --hard "origin/${REPO_BRANCH}"
else
  rm -rf "$REPO_DIR"
  git clone --branch "$REPO_BRANCH" "$REPO_URL" "$REPO_DIR"
fi

echo "==> Installing Ghost if needed"
if [[ ! -f "${SITE_DIR}/config.production.json" ]]; then
  chown -R "$GHOST_USER:$GHOST_USER" "$SITE_DIR"
  sudo -H -u "$GHOST_USER" bash -lc "cd '$SITE_DIR' && ghost install \
    --url '$SITE_URL' \
    --db mysql \
    --dbhost localhost \
    --dbuser '$MYSQL_USER' \
    --dbpass '$MYSQL_PASSWORD' \
    --dbname '$MYSQL_DB' \
    --no-setup-nginx \
    --no-setup-ssl \
    --no-start \
    --no-prompt"
else
  echo "Ghost already installed at ${SITE_DIR}"
fi

echo "==> Configuring Ghost port and URL"
sudo -H -u "$GHOST_USER" bash -lc "cd '$SITE_DIR' && ghost config url '$SITE_URL'"
sudo -H -u "$GHOST_USER" bash -lc "cd '$SITE_DIR' && ghost config server.port '$GHOST_PORT'"

echo "==> Installing theme and redirects"
rsync -a --delete "${REPO_DIR}/ghost-theme/julia-novaes/" "${SITE_DIR}/content/themes/julia-novaes/"
cp "${REPO_DIR}/redirects.yaml" "${SITE_DIR}/content/data/redirects.yaml"
chown -R "$GHOST_USER:$GHOST_USER" "${SITE_DIR}/content/themes/julia-novaes" "${SITE_DIR}/content/data/redirects.yaml"

if [[ -n "$IMPORT_SQL_PATH" ]]; then
  if [[ ! -f "$IMPORT_SQL_PATH" ]]; then
    echo "ERROR: IMPORT_SQL_PATH not found: $IMPORT_SQL_PATH"
    exit 1
  fi

  echo "==> Backing up current database before SQL import"
  BACKUP_PATH="/root/${MYSQL_DB}-before-import-$(date +%Y%m%d-%H%M%S).sql"
  mysqldump "$MYSQL_DB" > "$BACKUP_PATH"
  echo "Backup saved to $BACKUP_PATH"

  echo "==> Importing SQL into ${MYSQL_DB}"
  mysql "$MYSQL_DB" < "$IMPORT_SQL_PATH"
fi

echo "==> Activating theme in Ghost database"
mysql "$MYSQL_DB" <<SQL
UPDATE settings
SET value = 'julia-novaes', updated_at = UTC_TIMESTAMP()
WHERE \`key\` = 'active_theme';
SQL

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
sudo -H -u "$GHOST_USER" bash -lc "cd '$SITE_DIR' && ghost restart || ghost start"

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
echo "Site:  ${SITE_URL}"
echo "Admin: ${SITE_URL}/ghost/"
echo "Check: curl -I http://${DOMAIN}/about-me"
