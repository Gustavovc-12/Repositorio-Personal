from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ================== TOKENS ==================
APP_TOKEN = "APP_TOKEN_ABC123"
DEVICE_TOKEN = "ESP32_TOKEN_ABC123"

# ================== ESTADO GLOBAL ==================
servo_state = {
    "group": "arm",          # arm | hand
    "mode": "manual",        # manual | auto
    "pos": 0,
    "max_pos": 90,
    "periodic": False,
    "duration_s": 0,
    "last_update": "nunca"
}

battery_state = {
    "percentage": None,
    "voltage": None,
    "last_update": "nunca"
}

# ================== HELPERS ==================
def check_app_token(req):
    auth = req.headers.get("Authorization")
    return auth == f"Bearer {APP_TOKEN}"

def check_device_token(req):
    token = req.headers.get("X-Device-Token")
    return token == DEVICE_TOKEN

# ================== WEB ==================
@app.route("/")
def index():
    return render_template("index.html")

# ================== APP → SERVIDOR (SERVO) ==================
@app.route("/servo", methods=["POST"])
def set_servo():

    if not check_app_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "expected JSON"}), 400

    try:
        servo_state["group"] = data["group"]      # arm / hand
        servo_state["mode"] = data["mode"]        # manual / auto
        servo_state["pos"] = int(data.get("pos", 0))
        servo_state["max_pos"] = int(data.get("max_pos", 90))
        servo_state["periodic"] = bool(data.get("periodic", False))
        servo_state["duration_s"] = int(data.get("duration_s", 0))
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "invalid servo data"}), 400

    servo_state["last_update"] = "app"

    return jsonify({"ok": True, "servo": servo_state})

# ================== ESP32 → LEER SERVO ==================
@app.route("/servo/state", methods=["GET"])
def get_servo():

    if not check_device_token(request):
        return jsonify({"error": "unauthorized"}), 401

    return jsonify(servo_state)

# ================== ESP32 → SERVIDOR (BATERÍA) ==================
@app.route("/esp32/battery", methods=["POST"])
def set_battery():

    if not check_device_token(request):
        return jsonify({"error": "unauthorized"}), 401

    if not request.is_json:
        return jsonify({"error": "expected JSON"}), 400

    data = request.get_json()

    try:
        battery_state["percentage"] = int(data["percentage"])
        battery_state["voltage"] = float(data["voltage"])
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "invalid battery data"}), 400

    battery_state["last_update"] = "esp32"

    return jsonify({"ok": True})

# ================== APP / WEB → LEER BATERÍA ==================
@app.route("/battery/state", methods=["GET"])
def get_battery():
    return jsonify(battery_state)

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
