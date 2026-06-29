#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"

ok() {
  printf '✔ %s\n' "$1"
}

info() {
  printf '%s\n' "$1"
}

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

find_python() {
  local candidate
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
      if "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; then
        printf '%s\n' "$candidate"
        return 0
      fi
    fi
  done
  return 1
}

info "Checking Python..."
PYTHON_CMD="$(find_python)" || fail "Python >= 3.11 is required. Please install Python 3.11 or newer."
PYTHON_VERSION="$("$PYTHON_CMD" -c 'import platform; print(platform.python_version())')"
ok "Python $PYTHON_VERSION found"

cd "$BACKEND_DIR"

info "Creating virtual environment..."
if [ ! -d "venv" ]; then
  "$PYTHON_CMD" -m venv venv
  ok "Virtual environment created"
else
  ok "Virtual environment already exists"
fi

info "Activating virtual environment..."
# shellcheck source=/dev/null
source venv/bin/activate
ok "Activated"

info "Upgrading pip..."
python -m pip install --upgrade pip
ok "pip upgraded"

info "Installing dependencies..."
python -m pip install -r requirements.txt
ok "Production dependencies installed"

info "Installing development dependencies..."
python -m pip install -r requirements-dev.txt
ok "Development dependencies installed"

info "Creating .env..."
if [ ! -f ".env" ]; then
  cp .env.example .env
  ok ".env created"
else
  ok ".env already exists"
fi

info "Alembic initialization will be added later."

cat <<'EOF'
=================================
EduTrack Pro Backend Ready 🚀
Run:
uvicorn app.main:app --reload
=================================
EOF
