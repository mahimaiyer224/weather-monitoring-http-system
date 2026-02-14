from flask import Flask, request, jsonify
import time

app = Flask(__name__)

sensor_data = []

@app.route("/receive", methods=["POST"])

def receive_data():
    data = request.json

    if not data:
        return jsonify({"error": "No data"}), 400

    data["received_at"] = time.time()
    sensor_data.append(data)

    if len(sensor_data) > 100:
        sensor_data.pop(0)

    print("Received: ", data)
    return jsonify({"status": "OK"}), 200

@app.route("/stats", methods=["GET"])

def get_stats():
    if not sensor_data:
        return jsonify({"message": "No data yet"})
    
    temps = [d["temperature"] for d in sensor_data]
    rain = [d["rainfall"] for d in sensor_data]
    avg_temp = sum(temps)/len(temps)
    total_rain = sum(rain)

    return jsonify({
        "samples": len(sensor_data),
        "avg_temperature": round(avg_temp, 2),
        "total_rainfall": round(total_rain, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)