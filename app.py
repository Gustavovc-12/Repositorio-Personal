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
# Espera: pos=123 (form-urlencoded)
@app.route("/servo", methods=["POST"])
def set_servo():
    # MIT App Inventor envía datos como FORM, no JSON
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

# ====== ESP32 / WEB → LEER ESTADO ======
@app.route("/servo/state", methods=["GET"])
def get_servo():
    return jsonify(servo_state)

# ====== RENDER ======
if __name__ == "__main__":
    # Render usa el puerto 10000
    app.run(host="0.0.0.0", port=10000)
