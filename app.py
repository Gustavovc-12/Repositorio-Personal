from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

APP_TOKEN = "APP_TOKEN_ABC123"
DEVICE_TOKEN = "ESP32_TOKEN_ABC123"

servo_state = {
    "group": "arm",
    "mode": "manual",
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

def check_app_token(req):
    return req.headers.get("Authorization") == f"Bearer {APP_TOKEN}"

def check_device_token(req):
    return req.headers.get("X-Device-Token") == DEVICE_TOKEN

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/servo", methods=["POST"])
def set_servo():
    if not check_app_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "expected JSON"}), 400

    servo_state.update({
        "group": data["group"],
        "mode": data["mode"],
        "pos": int(data.get("pos", 0)),
        "max_pos": int(data.get("max_pos", 90)),
        "periodic": bool(data.get("periodic", False)),
        "duration_s": int(data.get("duration_s", 0)),
        "last_update": "app"
    })

    return jsonify({"ok": True})

@app.route("/servo/state")
def get_servo():
    if not check_device_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(servo_state)

@app.route("/esp32/battery", methods=["POST"])
def set_battery():
    if not check_device_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json()
    battery_state["percentage"] = int(data["percentage"])
    battery_state["voltage"] = float(data["voltage"])
    battery_state["last_update"] = "esp32"

    return jsonify({"ok": True})

@app.route("/battery/state")
def get_battery():
    return jsonify(battery_state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
