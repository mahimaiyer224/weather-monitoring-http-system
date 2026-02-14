from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import time
import threading

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://cautious-memory-r4r967rrv95jc56q9-7000.app.github.dev"
        ]
    }
})
NE_EDGE = "http://localhost:5001/stats"
SW_EDGE = "http://localhost:5002/stats"

latest_data = {
    "ne": {},
    "sw": {},
    "last_updated": None
}

def poll_edges():
    while True:
        try:
            ne_res = requests.get(NE_EDGE, timeout=3)
            sw_res = requests.get(SW_EDGE, timeout=3)

            if ne_res.status_code == 200:
                latest_data["ne"] = ne_res.json()
            if sw_res.status_code == 200:
                latest_data["sw"] = sw_res.json()
            latest_data["last_updated"] = time.time()

            print("Cloud Updated from Edges")

        except Exception as e:
            print("Cloud Polling Error: ", e)

        time.sleep(30)
@app.route("/global_stats", methods=["GET"])

def global_stats():
    ne = latest_data.get("ne", {})
    sw = latest_data.get("sw", {})

    if not ne or not sw:
        return jsonify({"message": "Waiting for edge data"})
    
    total_samples = ne["samples"] + sw["samples"]

    avg_temp = (
        ne["avg_temperature"] * ne["samples"] + 
        sw["avg_temperature"] * sw["samples"]
    ) / total_samples

    total_rain = ne["total_rainfall"] + sw["total_rainfall"]

    return jsonify({
        "total_samples": total_samples,
        "city_avg_temperature": round(avg_temp, 2),
        "city_total_rainfall": round(total_rain, 2),
        "last_updated": latest_data["last_updated"]
    })
if __name__ == "__main__":
    t = threading.Thread(target=poll_edges)
    t.daemon = True
    t.start()

    app.run(host="0.0.0.0", port=8000, debug=False)