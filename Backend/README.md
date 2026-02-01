# Backend (Django REST API)

This service powers dataset ingestion, analytics, and authentication for the Chemical Equipment Visualizer.

## Requirements

- Python 3.10+ (recommended)
- See `Backend/config/requirements.txt`

## Setup

```powershell
cd Backend\config
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver 8000
```

API base URL: `http://localhost:8000/api`

## Endpoints

- `POST /api/datasets/upload/`
  - Body: JSON array of equipment records
  - Required keys per record:
    - `Equipment Name`
    - `Type`
    - `Flowrate`
    - `Pressure`
    - `Temperature`
- `GET /api/datasets/history/?limit=5` (limit clamped 1–5)
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`

## Notes

- Default database is SQLite at `Backend/config/db.sqlite3`.
- CORS is configured for `http://localhost:5173`.
