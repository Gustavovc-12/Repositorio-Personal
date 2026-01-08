from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ========= ESTADO SERVO =========
servo_state = {
    "group": "arm",          # arm | hand
    "mode": "manual",        # manual | auto
    "pos": 90,               # manual
    "max_pos": 120,          # auto
    "periodic": False,       # auto
    "duration_s": 0,         # auto
    "last_update": "nunca"
}

# ========= ESTADO BATERÍA =========
battery_state = {
    "percentage": None,
    "voltage": None,
    "last_update": "nunca"
}

# ========= WEB =========
@app.route("/")
def index():
    return render_template("index.html")

# ========= APP → SERVIDOR =========
@app.route("/servo", methods=["POST"])
def set_servo():
    if not request.is_json:
        return jsonify({"error": "expected JSON"}), 400

    data = request.get_json()

    servo_state["group"] = data.get("group", servo_state["group"])
    servo_state["mode"] = data.get("mode", servo_state["mode"])
    servo_state["pos"] = int(data.get("pos", servo_state["pos"]))
    servo_state["max_pos"] = int(data.get("max_pos", servo_state["max_pos"]))
    servo_state["periodic"] = bool(data.get("periodic", servo_state["periodic"]))
    servo_state["duration_s"] = int(data.get("duration_s", servo_state["duration_s"]))
    servo_state["last_update"] = "app"

    return jsonify({"ok": True, "state": servo_state})

# ========= ESP32 / WEB =========
@app.route("/servo/state", methods=["GET"])
def get_servo():
    return jsonify(servo_state)

# ========= ESP32 → SERVIDOR =========
@app.route("/esp32/battery", methods=["POST"])
def set_battery():
    if not request.is_json:
        return jsonify({"error": "expected JSON"}), 400

    data = request.get_json()

    try:
        battery_state["percentage"] = int(data["percentage"])
        battery_state["voltage"] = float(data["voltage"])
        battery_state["last_update"] = "esp32"
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "invalid battery data"}), 400

    return jsonify({"ok": True})

# ========= WEB =========
@app.route("/battery/state", methods=["GET"])
def get_battery():
    return jsonify(battery_state)

# ========= RENDER =========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)