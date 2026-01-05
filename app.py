from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ====== ESTADO GLOBAL ======
servo_state = {
    "pos": 90,
    "last_update": "nunca"
}

# ====== WEB ======
@app.route("/")
def index():
    return render_template("index.html")

# ====== APP → SERVIDOR ======
@app.route("/servo", methods=["POST"])
def set_servo():
    data = request.json
    if not data or "pos" not in data:
        return jsonify({"error": "missing pos"}), 400

    servo_state["pos"] = int(data["pos"])
    servo_state["last_update"] = "app"

    return jsonify({
        "ok": True,
        "pos": servo_state["pos"]
    })

# ====== ESP32 / WEB → LEER ESTADO ======
@app.route("/servo/state", methods=["GET"])
def get_servo():
    return jsonify(servo_state)

# ====== RENDER ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
