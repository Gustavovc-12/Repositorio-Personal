from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ====== ESTADO GLOBAL ======
servo_state = {
    "pos": 90,
    "last_update": "nunca"
}

battery_state = {
    "percentage": None,
    "voltage": None,
    "time_real_h": None,
    "time_remaining_h": None,
    "efficiency": None,
    "last_update": "nunca"
}

# ====== WEB ======
@app.route("/")
def index():
    return render_template("index.html")

# ====== APP → SERVIDOR (SERVO) ======
# Espera: pos=123 (form-urlencoded)
@app.route("/servo", methods=["POST"])
def set_servo():

    if "pos" not in request.form:
        return jsonify({"error": "missing pos"}), 400

    try:
        servo_state["pos"] = int(request.form["pos"])
    except ValueError:
        return jsonify({"error": "invalid pos"}), 400

    servo_state["last_update"] = "app"

    return jsonify({
        "ok": True,
        "pos": servo_state["pos"]
    })

# ====== ESP32 / WEB → LEER SERVO ======
@app.route("/servo/state", methods=["GET"])
def get_servo():
    return jsonify(servo_state)

# ====== ESP32 → SERVIDOR (BATERIA) ======
@app.route("/esp32/battery", methods=["POST"])
def set_battery():

    if not request.is_json:
        return jsonify({"error": "expected JSON"}), 400

    data = request.get_json()

    try:
        battery_state["percentage"] = int(data["percentage"])
        battery_state["voltage"] = float(data["voltage"])
        battery_state["time_real_h"] = float(data["time_real_h"])
        battery_state["time_remaining_h"] = float(data["time_remaining_h"])
        battery_state["efficiency"] = float(data["efficiency"])
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "invalid battery data"}), 400

    battery_state["last_update"] = "esp32"

    return jsonify({
        "ok": True,
        "battery": battery_state
    })

# ====== LEER ESTADO DE BATERIA ======
@app.route("/battery/state", methods=["GET"])
def get_battery():
    return jsonify(battery_state)

# ====== RENDER ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
