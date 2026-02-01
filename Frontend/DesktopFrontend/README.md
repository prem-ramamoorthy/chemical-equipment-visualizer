# Desktop Frontend (PyQt5)

PyQt5 desktop application for the Chemical Equipment Visualizer. Connects to the Django API for auth and dataset history.

## Requirements

- Python 3.10+ (recommended)
- See `Frontend/DesktopFrontend/requirements.txt`

## Setup

```powershell
cd Frontend\DesktopFrontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python main.py
```

## Configuration

Set the API base URL in `Frontend/DesktopFrontend/.env`:

```
API_BASE_URL=http://localhost:8000/api
```

## Notes

- Login, signup, and logout call the API endpoints under `/api/auth/`.
- Dataset history and analytics depend on the backend being running.
