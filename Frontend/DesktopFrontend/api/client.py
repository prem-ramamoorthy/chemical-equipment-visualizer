import time
import random

def mockLogin(username, password):
    time.sleep(1)
    return True

def mockSignup(username, email, password):
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

def signup_user(name, email, password):
    payload = {
        "name": name,
        "email": email,
        "password": password
    }
    return True