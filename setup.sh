#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cat <<'EOF'
====================================
EduTrack Pro Setup
1. Backend
2. Frontend
3. Complete Project
Choose:
====================================
EOF

read -r choice

case "$choice" in
  1)
    "$ROOT_DIR/setup/backend.sh"
    ;;
  2)
    "$ROOT_DIR/setup/frontend.sh"
    ;;
  3)
    "$ROOT_DIR/setup/backend.sh"
    SKIP_FRONTEND_DEV=1 "$ROOT_DIR/setup/frontend.sh"
    cat <<'EOF'
====================================
EduTrack Pro Setup Complete 🚀
Run backend:
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

Run frontend:
cd frontend && npm run dev
====================================
EOF
    ;;
  *)
    echo "Invalid choice. Please choose 1, 2, or 3."
    exit 1
    ;;
esac
