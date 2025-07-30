import requests
import time
import random

API_URL = "http://localhost:5001/sensor-data"

def generate_sensor_data():
    return {
        "device_id": "sensor-001",
        "temperature": round(random.uniform(20, 100), 2),
        "smoke_level": round(random.uniform(10, 120), 2)
    }

while True:
    data = generate_sensor_data()
    print(f"Sending: {data}")
    try:
        requests.post(API_URL, json=data)
    except Exception as e:
        print(f"Failed to send: {e}")
    time.sleep(3)
