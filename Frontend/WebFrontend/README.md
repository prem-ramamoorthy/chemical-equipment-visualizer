# Web Frontend (React + Vite)

Web UI for the Chemical Equipment Visualizer. Upload CSV datasets, explore analytics, and review dataset history.

## Requirements

- Node.js 18+ (recommended)
- npm (or your preferred package manager)

## Setup

```powershell
cd Frontend\WebFrontend
npm install
npm run dev
```

The app runs at `http://localhost:5173` by default.

## Configuration

Set the API base URL in `Frontend/WebFrontend/.env`:

```
VITE_API_BASE_URL="http://localhost:8000/api"
```

## Notes

- The backend must be running for API calls.
- CSV headers should include:
  - `Equipment Name`
  - `Type`
  - `Flowrate`
  - `Pressure`
  - `Temperature`
