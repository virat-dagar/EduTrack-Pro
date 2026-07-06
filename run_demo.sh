#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

BACKEND_HOST="${BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="${FRONTEND_HOST:-127.0.0.1}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"
SKIP_SETUP="${SKIP_SETUP:-0}"

BACKEND_PID=""
FRONTEND_PID=""
BACKEND_PYTHON=""

info() {
  printf '\n%s\n' "$1"
}

ok() {
  printf 'OK: %s\n' "$1"
}

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

find_backend_python() {
  if [ -x "$BACKEND_DIR/.venv/bin/python" ]; then
    printf '%s\n' "$BACKEND_DIR/.venv/bin/python"
    return 0
  fi

  if [ -x "$BACKEND_DIR/venv/bin/python" ]; then
    printf '%s\n' "$BACKEND_DIR/venv/bin/python"
    return 0
  fi

  return 1
}

cleanup() {
  local exit_code=$?
  trap - INT TERM EXIT

  if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" >/dev/null 2>&1; then
    printf '\nStopping frontend...\n'
    kill "$FRONTEND_PID" >/dev/null 2>&1 || true
  fi

  if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
    printf 'Stopping backend...\n'
    kill "$BACKEND_PID" >/dev/null 2>&1 || true
  fi

  wait "$FRONTEND_PID" >/dev/null 2>&1 || true
  wait "$BACKEND_PID" >/dev/null 2>&1 || true
  exit "$exit_code"
}

ensure_backend() {
  info "Preparing backend..."

  if [ "$SKIP_SETUP" != "1" ] && ! find_backend_python >/dev/null 2>&1; then
    "$ROOT_DIR/setup/backend.sh"
  fi

  BACKEND_PYTHON="$(find_backend_python)" || fail "Backend virtual environment was not found. Run ./setup.sh or allow run_demo.sh to create it."

  if [ "$SKIP_SETUP" != "1" ]; then
    if ! "$BACKEND_PYTHON" -c 'import fastapi, sqlalchemy, uvicorn' >/dev/null 2>&1; then
      (cd "$BACKEND_DIR" && "$BACKEND_PYTHON" -m pip install -r requirements.txt)
    fi

    if [ ! -f "$BACKEND_DIR/.env" ] && [ -f "$BACKEND_DIR/.env.example" ]; then
      cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
    fi
  fi

  (cd "$BACKEND_DIR" && "$BACKEND_PYTHON" -m app.database.seed)
  ok "Backend ready with demo data"
}

ensure_frontend() {
  info "Preparing frontend..."

  command -v npm >/dev/null 2>&1 || fail "npm was not found. Install Node.js and npm first."

  if [ "$SKIP_SETUP" != "1" ] && [ ! -x "$FRONTEND_DIR/node_modules/.bin/vite" ]; then
    (cd "$FRONTEND_DIR" && npm install)
  fi

  ok "Frontend ready"
}

wait_for_backend() {
  local health_url="http://$BACKEND_HOST:$BACKEND_PORT/health"
  local attempts=40
  local count=1

  if ! command -v curl >/dev/null 2>&1; then
    sleep 3
    return 0
  fi

  while [ "$count" -le "$attempts" ]; do
    if curl -fsS "$health_url" >/dev/null 2>&1; then
      ok "Backend is responding at $health_url"
      return 0
    fi
    sleep 1
    count=$((count + 1))
  done

  fail "Backend did not start at $health_url"
}

start_backend() {
  info "Starting backend..."
  (
    cd "$BACKEND_DIR"
    "$BACKEND_PYTHON" -m uvicorn app.main:app --host "$BACKEND_HOST" --port "$BACKEND_PORT"
  ) &
  BACKEND_PID=$!
}

start_frontend() {
  info "Starting frontend..."
  (
    cd "$FRONTEND_DIR"
    VITE_API_BASE_URL="http://$BACKEND_HOST:$BACKEND_PORT/api/v1" \
      npm run dev -- --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" --strictPort
  ) &
  FRONTEND_PID=$!
}

monitor_servers() {
  while true; do
    if ! kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
      wait "$BACKEND_PID"
      exit $?
    fi

    if ! kill -0 "$FRONTEND_PID" >/dev/null 2>&1; then
      wait "$FRONTEND_PID"
      exit $?
    fi

    sleep 2
  done
}

main() {
  trap cleanup INT TERM EXIT

  info "EduTrack Pro demo runner"
  ensure_backend
  ensure_frontend
  start_backend
  wait_for_backend
  start_frontend

  cat <<EOF

EduTrack Pro is running.

Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT
Backend:  http://$BACKEND_HOST:$BACKEND_PORT/docs

Demo accounts:
teacher@example.com / Password123
student@example.com / Password123

Press Ctrl+C to stop both servers.
EOF

  monitor_servers
}

main "$@"
