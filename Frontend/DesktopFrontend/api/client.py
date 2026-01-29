import time
import random
import requests

def mockLogin(username, password):
    if not username.strip() or not password.strip():
        return {"success": False, "error": "Please enter both username and password"}
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code == 200 and "username" in response.json():
            return {"success": True, "username": response.json()["username"]}
        else:
            return {"success": False, "error": "Invalid credentials. Please try again."}
    except requests.RequestException as err:
        try:
            error_data = err.response.json().get("error")
            if isinstance(error_data, str):
                return {"success": False, "error": error_data}
            elif isinstance(error_data, dict):
                first_error = next(iter(error_data.values()))
                return {"success": False, "error": first_error[0] if isinstance(first_error, list) else str(first_error)}
            else:
                return {"success": False, "error": "Invalid credentials. Please try again."}
        except Exception:
            return {"success": False, "error": "An unexpected error occurred. Please try again."}


    time.sleep(1)
    return True

def mockUploadCSV(filename):
    time.sleep(2)

    equipment = [
        {
            "name": f"Pump {i}",
            "type": random.choice(["Pump", "Reactor", "Heat Exchanger"]),
            "flowrate": random.uniform(20, 80),
            "pressure": random.uniform(1, 10),
            "temperature": random.uniform(30, 120),
        }
        for i in range(12)
    ]

    return {
        "id": random.randint(1000, 9999),
        "total_count": len(equipment),
        "avg_flowrate": round(sum(e["flowrate"] for e in equipment) / len(equipment), 1),
        "avg_pressure": round(sum(e["pressure"] for e in equipment) / len(equipment), 1),
        "avg_temperature": round(sum(e["temperature"] for e in equipment) / len(equipment), 1),
        "type_distribution": {
            "Pump": 5,
            "Reactor": 4,
            "Heat Exchanger": 3
        },
        "data": equipment
    }

def signup_user(username, email, password, confirm_password):
    if not username.strip() or not email.strip() or not password.strip() or not confirm_password.strip():
        return {"success": False, "error": "All fields are required"}

    if password != confirm_password:
        return {"success": False, "error": "Passwords do not match"}

    try:
        response = requests.post(
            "http://localhost:8000/api/auth/register/",
            json={
                "username": username,
                "email": email,
                "password": password,
                "password2": confirm_password,
            },
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        data = response.json()
        if response.ok:
            return {"success": True}
        else:
            if "error" in data:
                return {"success": False, "error": data["error"]}
            elif "errors" in data:
                return {"success": False, "error": "Validation errors: " + str(data["errors"])}
            else:
                return {"success": False, "error": "Signup failed. Try again."}
    except Exception:
        return {"success": False, "error": "An unexpected error occurred. Try again."}
    
def logout_user():
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/logout/",
            headers={"Content-Type": "application/json"},
        )
        return response.ok
    except Exception:
        return False