# Chemical Equipment Visualizer

End-to-end analytics for chemical equipment datasets with a Django REST API and two clients: a React web app and a PyQt5 desktop app. Upload equipment data, generate summaries and charts, and review recent dataset history.

## What is included

- Backend API for dataset upload, analytics, history, and auth
- Web frontend (React + Vite) for CSV upload and dashboards
- Desktop frontend (PyQt5) for dashboards and auth

## Repo structure

```
Backend/
  README.md
  config/                 Django project + API
Frontend/
  WebFrontend/            React + Vite web app
  DesktopFrontend/        PyQt5 desktop app
```

Each subfolder contains its own README with additional details:
- `Backend/README.md`
- `Frontend/WebFrontend/README.md`
- `Frontend/DesktopFrontend/README.md`

## Requirements

- Python 3.10+ (recommended)
- Node.js 18+ and npm (for the web frontend)

## Quick start (local dev)

### 1) Backend API

```powershell
cd Backend\config
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver 8000
```

API base URL: `http://localhost:8000/api`

### 2) Web frontend

```powershell
cd Frontend\WebFrontend
npm install
npm run dev
```

Web app URL: `http://localhost:5173`

Environment config: `Frontend/WebFrontend/.env`
```
VITE_API_BASE_URL="http://localhost:8000/api"
```

### 3) Desktop frontend

```powershell
cd Frontend\DesktopFrontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python main.py
```

Environment config: `Frontend/DesktopFrontend/.env`
```
API_BASE_URL=http://localhost:8000/api
```

## API overview

Base URL: `http://localhost:8000/api`

- `POST /datasets/upload/`
  - Body: JSON array of equipment records
  - Required keys per record:
    - `Equipment Name`
    - `Type`
    - `Flowrate`
    - `Pressure`
    - `Temperature`
- `GET /datasets/history/?limit=5` (limit clamped 1-5)
- `POST /auth/register/`
- `POST /auth/login/`
- `POST /auth/logout/`
- `GET /auth/me/`

## CSV format (web upload)

The web client parses CSV rows and sends JSON to `/datasets/upload/`.
Ensure the CSV header includes:

```
Equipment Name,Type,Flowrate,Pressure,Temperature
```

## Data storage and limits

- Default database: SQLite at `Backend/config/db.sqlite3`
- History endpoint returns up to the last 5 datasets
- CORS allows `http://localhost:5173`

## Troubleshooting

- Backend not reachable: ensure `python manage.py runserver 8000` is running.
- CORS errors in the web app: confirm the frontend URL matches `CORS_ALLOWED_ORIGINS` in `Backend/config/config/settings.py`.
- Desktop app cannot log in: verify `API_BASE_URL` in `Frontend/DesktopFrontend/.env`.

## License

Add your license information here.
