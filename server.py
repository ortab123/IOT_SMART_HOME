from flask import Flask, request, jsonify
from db_handler import init_db, insert_sensor_data

app = Flask(__name__)

# מצב גלובלי של המערכת
ac_on = False
auto_mode = True
current_temperature = None
motion_history = []

def process_auto_logic():
    global ac_on

    if current_temperature is None or len(motion_history) < 2:
        return  # עדיין אין מספיק נתונים

    # התראה – טמפ' גבוהה מדי
    if current_temperature > 30:
        print(f"[WARNING] High temperature detected: {current_temperature}°C")

    # תנאי להדלקת מזגן
    if current_temperature > 26 and any(motion_history):
        if not ac_on:
            print("[AUTO] Turning AC ON (Hot + Motion)")
            ac_on = True

    # תנאי לכיבוי מזגן
    elif current_temperature < 23 or not any(motion_history):
        if ac_on:
            print("[AUTO] Turning AC OFF (Cold or No Motion)")
            ac_on = False

@app.route("/sensor", methods=["POST"])
def receive_sensor_data():
    global current_temperature, motion_history

    data = request.get_json()
    sensor = data.get("sensor")
    value = data.get("value")

    print(f"[SERVER] Received from {sensor}: {value}")

    insert_sensor_data(sensor, value)

    # עיבוד חיישנים
    if auto_mode:
        if sensor == "temperature":
            current_temperature = float(value)
        elif sensor == "motion":
            motion_history.append(bool(value))
            if len(motion_history) > 2:
                motion_history.pop(0)

        process_auto_logic()

    return jsonify({"status": "received", "sensor": sensor, "value": value})

@app.route("/manual", methods=["POST"])
def manual_command():
    global ac_on, auto_mode

    data = request.get_json()
    value = data.get("value")

    if isinstance(value, bool):
        auto_mode = False
        ac_on = value
        print(f"[SERVER] Manual command received: AC set to {'ON' if ac_on else 'OFF'}")
        return jsonify({"status": "manual override", "ac_on": ac_on})
    else:
        return jsonify({"error": "Invalid manual value"}), 400

@app.route("/ac_status", methods=["GET"])
def get_ac_status():
    return jsonify({"ac_on": ac_on, "mode": "auto" if auto_mode else "manual"})

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5050, debug=False)



