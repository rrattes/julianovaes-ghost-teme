#!/usr/bin/env bash
set -euo pipefail

# Update an existing Julia Novaes Ghost SQLite install without reinstalling Ghost.
#
# Usage on the server:
#
#   cd /opt/julianovaes-ghost-teme
#   sudo bash deploy/update-ubuntu-22-ghost-sqlite.sh

SITE_DIR="${SITE_DIR:-/var/www/julianovaes}"
GHOST_USER="${GHOST_USER:-ghost-julianovaes}"
SERVICE_NAME="${SERVICE_NAME:-ghost-julianovaes}"
REPO_BRANCH="${REPO_BRANCH:-main}"
REPO_DIR="${REPO_DIR:-/opt/julianovaes-ghost-theme}"
SQLITE_DB_PATH="${SQLITE_DB_PATH:-${SITE_DIR}/content/data/ghost-local.db}"

if [[ "${EUID}" -ne 0 ]]; then
  echo "ERROR: run this script with sudo/root."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_REPO="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "==> Updating working repository"
git -C "$CURRENT_REPO" fetch origin "$REPO_BRANCH"
git -C "$CURRENT_REPO" checkout "$REPO_BRANCH"
git -C "$CURRENT_REPO" pull --ff-only origin "$REPO_BRANCH"

echo "==> Updating deployment repository mirror at ${REPO_DIR}"
if [[ "$CURRENT_REPO" != "$REPO_DIR" ]]; then
  mkdir -p "$REPO_DIR"
  rsync -a --delete \
    --exclude ".git" \
    --exclude "ghost-local" \
    --exclude "node_modules" \
    --exclude ".next" \
    "${CURRENT_REPO}/" "${REPO_DIR}/"
else
  REPO_DIR="$CURRENT_REPO"
fi

if [[ ! -f "$SQLITE_DB_PATH" ]]; then
  echo "ERROR: SQLite DB not found at ${SQLITE_DB_PATH}"
  exit 1
fi

echo "==> Stopping Ghost"
systemctl stop "$SERVICE_NAME" || true

echo "==> Syncing theme and redirects"
mkdir -p "${SITE_DIR}/content/themes" "${SITE_DIR}/content/data" "${SITE_DIR}/content/images/2026/05"
rsync -a --delete "${REPO_DIR}/ghost-theme/julia-novaes/" "${SITE_DIR}/content/themes/julia-novaes/"
cp "${REPO_DIR}/redirects.yaml" "${SITE_DIR}/content/data/redirects.yaml"
chown -R "$GHOST_USER:$GHOST_USER" "${SITE_DIR}/content"

echo "==> Updating posts and pages in SQLite"
sudo -H -u "$GHOST_USER" bash -lc "PROJECT_ROOT='$REPO_DIR' GHOST_DB_PATH='$SQLITE_DB_PATH' GHOST_IMAGES_TARGET='${SITE_DIR}/content/images/2026/05' python3 '$REPO_DIR/scripts/seed-ghost-articles.py'"
sudo -H -u "$GHOST_USER" bash -lc "PROJECT_ROOT='$REPO_DIR' GHOST_DB_PATH='$SQLITE_DB_PATH' python3 '$REPO_DIR/scripts/seed-ghost-pages.py'"

echo "==> Ensuring theme is active"
sudo -H -u "$GHOST_USER" sqlite3 "$SQLITE_DB_PATH" <<SQL
UPDATE settings SET value = 'julia-novaes', updated_at = datetime('now') WHERE key = 'active_theme';
SQL

echo "==> Starting Ghost"
systemctl start "$SERVICE_NAME"

echo "==> Done"
echo "Check:"
echo "  curl -IL https://www.julianovaes.com.br/"
echo "  curl -IL https://www.julianovaes.com.br/psicoterapia-individual/"
