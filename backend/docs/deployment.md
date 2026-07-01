# EduTrack Pro Deployment

## Backend

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/alembic upgrade head
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Required environment variables:

- `DATABASE_URL`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `CORS_ORIGINS`

## Frontend

```bash
cd frontend
npm install
npm run build
```

Set `VITE_API_BASE_URL` to the deployed backend `/api/v1` URL.

For local demo data:

```bash
cd backend
.venv/bin/python -m app.database.seed
```
