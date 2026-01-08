from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ========= ESTADO SERVO =========
servo_state = {
    "group": "arm",          # arm | hand
    "mode": "manual",        # manual | auto
    "pos": 90,
    "max_pos": 120,
    "periodic": False,
    "duration_s": 0,
    "last_update": "nunca"
}

# ========= ESTADO BATERÍA =========
battery_state = {
    "percentage": None,
    "voltage": None,
    "low": False,
    "last_update": "nunca"
}

BATTERY_LOW_THRESHOLD = 20  # %

# ========= WEB =========
@app.route("/")
def index():
    return render_template("index.html")

# ========= APP → SERVIDOR (SERVO) =========
@app.route("/servo", methods=["POST"])
def set_servo():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "expected JSON"}), 400

    servo_state["group"] = data.get("group", servo_state["group"])
    servo_state["mode"] = data.get("mode", servo_state["mode"])
    servo_state["pos"] = int(data.get("pos", servo_state["pos"]))
    servo_state["max_pos"] = int(data.get("max_pos", servo_state["max_pos"]))
    servo_state["periodic"] = bool(data.get("periodic", servo_state["periodic"]))
    servo_state["duration_s"] = int(data.get("duration_s", servo_state["duration_s"]))
    servo_state["last_update"] = f"app @ {now()}"

    return jsonify({"ok": True})

# ========= ESP32 → SERVIDOR (BATERÍA) =========
@app.route("/esp32/battery", methods=["POST"])
def set_battery():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "expected JSON"}), 400

    try:
        percentage = int(data["percentage"])
        voltage = float(data["voltage"])

        battery_state["percentage"] = percentage
        battery_state["voltage"] = voltage
        battery_state["low"] = percentage < BATTERY_LOW_THRESHOLD
        battery_state["last_update"] = f"esp32 @ {now()}"

    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "invalid battery data"}), 400

    return jsonify({"ok": True})

# ========= ESTADO GLOBAL =========
@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "server": {
            "alive": True,
            "time": now()
        },
        "servo": servo_state,
        "battery": battery_state
    })

# ========= RUN =========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
