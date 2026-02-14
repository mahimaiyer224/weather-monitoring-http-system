import requests
import random
import time

EDGE_URL = "http://localhost:5001/receive"

def generate_data():
    return{
        "station": "east",
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 90), 2),
        "rainfall": round(random.uniform(0, 5), 2),
        "wind_speed": round(random.uniform(1, 10), 2)
    }
while True:
    data = generate_data()
    try:
        res = requests.post(EDGE_URL, json=data)
        print("Sent:", data, "| Status:", res.status_code)
    except Exception as e:
        print("Error: ", e)
    time.sleep(5)