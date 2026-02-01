# Chemical Equipment Visualizer

Visual analytics for chemical equipment datasets across two frontends (web and desktop) backed by a Django REST API. Upload equipment data, explore summaries, correlations, distributions, and performance rankings.

## Project structure

```
Backend/
  config/                 Django project (REST API)
Frontend/
  WebFrontend/            React + Vite web app
  DesktopFrontend/        PyQt5 desktop app
```

## Features

- Upload equipment datasets and compute analytics
- Summary cards (averages, counts, distributions)
- Charts: scatter, histogram, box plot, correlations
- Dataset history (last 1–5 uploads)
- Auth endpoints (register/login/logout/me)

## Tech stack

- Backend: Django, Django REST Framework, django-cors-headers, SQLite
- Web frontend: React, TypeScript, Vite, Tailwind, Chart.js/Recharts
- Desktop frontend: PyQt5, requests

## Quick start

### 1) Backend API

```powershell
cd Backend\config
# create/activate a virtualenv, then install deps
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install django djangorestframework django-cors-headers

python manage.py migrate
python manage.py runserver 8000
```

API runs at `http://localhost:8000`.

### 2) Web frontend

```powershell
cd Frontend\WebFrontend
npm install
npm run dev
```

The web app expects the API base URL from `Frontend/WebFrontend/.env`:

```
VITE_API_BASE_URL="http://localhost:8000/api"
```

### 3) Desktop frontend

```powershell
cd Frontend\DesktopFrontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pyqt5 requests

python main.py
```

## API endpoints

Base: `http://localhost:8000/api`

- `POST /datasets/upload/`
  - Body: JSON array of equipment records
  - Required keys per record:
    - `Equipment Name`
    - `Type`
    - `Flowrate`
    - `Pressure`
    - `Temperature`
- `GET /datasets/history/?limit=5` (limit clamped 1–5)
- `POST /auth/register/`
- `POST /auth/login/`
- `POST /auth/logout/`
- `GET /auth/me/`

## CSV format (web upload)

The web client converts CSV rows into JSON and posts to `/datasets/upload/`.
Ensure your CSV header includes:

```
Equipment Name,Type,Flowrate,Pressure,Temperature
```

## Notes

- Backend uses SQLite by default (`Backend/config/db.sqlite3`).
- CORS is configured for `http://localhost:5173`.
- The desktop app calls the same auth endpoints as the web app.
