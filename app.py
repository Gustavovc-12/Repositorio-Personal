from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor activo"

@app.route("/ping")
def ping():
    return jsonify(status="ok", message="Servidor despierto")