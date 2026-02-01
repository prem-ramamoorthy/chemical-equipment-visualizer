# Desktop Frontend – PyQt5

This is the **desktop application** version of the Chemical Equipment Parameter Visualizer.

---

## 🧠 Responsibilities

- Desktop UI for analytics
- API communication with Django backend
- Dataset visualization using Matplotlib
- Cross-platform execution

---

## 🛠 Tech Stack

- Python 3.12+
- PyQt5
- Requests
- Matplotlib

---

## 📦 Setup

```bash
cd Frontend/DesktopFrontend
python -m venv venv
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
pip install -r requirements.txt
```

### ▶ Run Application

```bash
python main.py
```

### 🔗 Backend Configuration

Ensure the backend is running at:

```
http://localhost:8000
```

API base URL can be changed inside:

```
api/client.py
```

---

## 🧩 UI Components

- Navbar
- File Upload
- Summary Cards
- Charts (Matplotlib)
- Data Table
- History List
