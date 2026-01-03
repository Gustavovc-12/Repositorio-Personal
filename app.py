from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# -------------------------------
# PÁGINA WEB PRINCIPAL
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# RUTA DE PRUEBA (PING)
# -------------------------------
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "ok",
        "message": "Conexión App-Web-ESP32 activa"
    })


# -------------------------------
# ESTADO GENERAL DEL SISTEMA
# -------------------------------
@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "conexion": "activa",
        "servidores": "operativos",
        "recomendacion": "Sistema funcionando correctamente"
    })


# -------------------------------
# CONTROL DE SERVOMOTORES
# -------------------------------
@app.route("/servo", methods=["POST"])
def control_servo():
    data = request.json

    return jsonify({
        "resultado": "comando recibido",
        "servo": data.get("servo"),
        "velocidad": data.get("velocidad"),
        "tiempo": data.get("tiempo"),
        "modo": data.get("modo")
    })


# -------------------------------
# DATOS DE BATERÍA
# -------------------------------
@app.route("/battery", methods=["GET"])
def battery():
    return jsonify({
        "porcentaje": 78,
        "estado": "normal",
        "autonomia_estimada": "2h 30min",
        "eficiencia": "alta"
    })


# -------------------------------
# DATOS PARA GRÁFICOS
# -------------------------------
@app.route("/graphs", methods=["GET"])
def graphs():
    return jsonify({
        "bateria": [100, 95, 90, 85, 80, 78],
        "tiempo": [0, 10, 20, 30, 40, 50]
    })


# -------------------------------
# ARRANQUE DEL SERVIDOR
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)