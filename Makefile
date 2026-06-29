.PHONY: setup backend frontend run-backend run-frontend test test-backend test-frontend lint

setup:
	./setup.sh

backend:
	./setup/backend.sh

frontend:
	SKIP_FRONTEND_DEV=1 ./setup/frontend.sh

run-backend:
	cd backend && venv/bin/python -m uvicorn app.main:app --reload

run-frontend:
	cd frontend && npm run dev

test: test-backend test-frontend

test-backend:
	cd backend && venv/bin/python -m pytest

test-frontend:
	cd frontend && npm run lint

lint:
	cd backend && venv/bin/python -m ruff check app tests
	cd frontend && npm run lint
