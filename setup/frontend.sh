#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

ok() {
  printf '✔ %s\n' "$1"
}

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

command -v npm >/dev/null 2>&1 || fail "npm is required. Please install Node.js and npm."

cd "$FRONTEND_DIR"

echo "Installing frontend dependencies..."
npm install
ok "Frontend dependencies installed"

if [ "${RUN_NPM_AUDIT_FIX:-0}" = "1" ]; then
  echo "Running npm audit fix..."
  npm audit fix
  ok "npm audit fix complete"
else
  ok "Skipping npm audit fix"
fi

cat <<'EOF'
=================================
EduTrack Pro Frontend Ready 🚀
Run:
npm run dev
=================================
EOF

if [ "${SKIP_FRONTEND_DEV:-0}" != "1" ]; then
  npm run dev
fi
