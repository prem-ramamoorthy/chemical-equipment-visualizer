# Web Frontend – React + TypeScript

This is the **web interface** of the Chemical Equipment Parameter Visualizer.

---

## 🧠 Responsibilities

- User authentication
- Dataset upload
- Visualization of analytics
- Dataset history navigation
- Interactive charts & tables

---

## 🛠 Tech Stack

- React
- TypeScript (TSX)
- Tailwind CSS
- Chart.js
- Vite

---

## 📦 Setup

```bash
cd frontend/webfrontend
npm install
```

### ▶ Run Development Server

```bash
npm run dev
```

App runs at:  
[http://localhost:5173](http://localhost:5173)

---

### 🔗 Environment Variables

Create a `.env` file:

```env
VITE_API_BASE_URL="https://fosseebackend-production.up.railway.app/api"

# For local backend:
 VITE_API_BASE_URL="http://localhost:8000/api"
```

---

## 📊 Components

- AdvancedChartsGrid
- DistributionAnalysis
- StatisticalSummary
- CorrelationInsights
- ConditionalAnalysis
- EquipmentPerformanceRanking
- GroupedEquipmentAnalytics
- DataTable
- HistoryList

---

## 🔄 Data Flow

1. User uploads dataset
2. Frontend sends JSON to backend
3. Backend returns ChartsGridSummary
4. Frontend renders analytics dynamically

---

## 🚀 Production Build

```bash
npm run build
```

Deployable to Vercel or any static host.

