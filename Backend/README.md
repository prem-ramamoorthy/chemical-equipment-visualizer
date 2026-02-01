# Backend – Django REST API

This backend provides all analytics, authentication, and dataset storage for the Chemical Equipment Visualizer.

---

## 🧠 Responsibilities

- Accept dataset uploads (JSON)
- Perform statistical analytics using Pandas
- Store datasets in SQLite
- Expose REST APIs for Web & Desktop clients
- Manage dataset history (last 5 uploads)

---

## 🛠 Tech Stack

- Python 3.12+
- Django
- Django REST Framework
- Pandas
- NumPy
- SQLite (persistent on Railway)

---

## 📦 Setup (Local)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 🗄 Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### ▶ Run Server

```bash
python manage.py runserver
```

Server runs at:  
http://localhost:8000

---

## 🔐 Authentication APIs

| Method | Endpoint                |
|--------|-------------------------|
| POST   | /api/auth/register/     |
| POST   | /api/auth/login/        |
| POST   | /api/auth/logout/       |
| GET    | /api/auth/me/           |

Authentication is session-based; cookies are required.

---

## 📊 Dataset APIs

| Method | Endpoint                  |
|--------|---------------------------|
| POST   | /api/datasets/upload/     |
| GET    | /api/datasets/history/    |

**Upload format:**

```json
[
  {
    "Equipment Name": "Pump-1",
    "Type": "Pump",
    "Flowrate": "120",
    "Pressure": "5.2",
    "Temperature": "110"
  }
]
```
