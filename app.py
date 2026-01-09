from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ================= SERVO STATE =================
servo_state = {
    "group": "arm",              # arm | hand
    "mode": "manual",            # manual | auto
    "command": "stop",           # executeUp | executeDown | stop
    "max_pos": 120,
    "periodic": False,
    "duration_s": 0,
    "last_update": "nunca"
}

# ================= BATTERY STATE =================
battery_state = {
    "percentage": None,
    "voltage": None,
    "last_update": "nunca"
}

# ================= WEB =================
@app.route("/")
def index():
    return render_template("index.html")

# ================= APP → SERVER =================
@app.route("/servo", methods=["POST"])
def set_servo():

    data = request.get_json(silent=True)

    # 👉 SI NO ES JSON, LEER FORM DATA
    if data is None:
        data = request.form.to_dict()

    if not data:
        return jsonify({"error": "no data received"}), 400

    servo_state["group"] = data.get("group", servo_state["group"])
    servo_state["mode"] = data.get("mode", servo_state["mode"])

    # -------- MANUAL --------
    if servo_state["mode"] == "manual":
        servo_state["command"] = data.get("command", "stop")

    # -------- AUTO --------
    if servo_state["mode"] == "auto":
        servo_state["max_pos"] = int(data.get("max_pos", servo_state["max_pos"]))
        servo_state["periodic"] = str(data.get("periodic", "false")).lower() == "true"
        servo_state["duration_s"] = int(data.get("duration_s", servo_state["duration_s"]))

    servo_state["last_update"] = f"app @ {now()}"

    return jsonify({"ok": True, "received": data})

# ================= ESP32 → SERVO =================
@app.route("/servo/state", methods=["GET"])
def get_servo_state():
    return jsonify(servo_state)

# ================= ESP32 → BATTERY =================
@app.route("/esp32/battery", methods=["POST"])
def set_battery():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    try:
        battery_state["percentage"] = int(data["percentage"])
        battery_state["voltage"] = float(data["voltage"])
        battery_state["last_update"] = f"esp32 @ {now()}"
    except:
        return jsonify({"error": "datos inválidos"}), 400

    return jsonify({"ok": True})

# ================= STATUS GLOBAL =================
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

# ================= MAIN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)