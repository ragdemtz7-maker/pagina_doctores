from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.paciente import guardar_paciente
from backend.sesion import (get_disponibilidad_medico_mes, get_medicos,
                            get_nombre_completo_usuario)

app = Flask(__name__)

# CORS config
CORS(app, resources={r"/api/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})

@app.route("/")
def home():
    return "Backend de Citas Médicas funcionando"

@app.route('/api/guardar_paciente', methods=['POST'])
def api_guardar_paciente():
    data = request.json or {}
    resultado = guardar_paciente(data)
    if resultado.get("status") == "error":
        return jsonify(resultado), 500 
    return jsonify(resultado)

@app.route('/api/nombre_usuario/<int:id_persona>', methods=['GET'])
def api_nombre_usuario(id_persona):
    nombre = get_nombre_completo_usuario(id_persona)
    if nombre:
        return jsonify({"nombre_completo": nombre})
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/api/medicos', methods=['GET'])
def api_get_medicos():
    medicos = get_medicos()
    if medicos:
        return jsonify(medicos)
    else:
        return jsonify({"message": "No se encontraron médicos"}), 404

@app.route('/api/medicos/<int:id_medico>/disponibilidad', methods=['GET'])
def api_get_disponibilidad_medico(id_medico):
    disponibilidad = get_disponibilidad_medico_mes(id_medico)
    if disponibilidad:
        return jsonify(disponibilidad)
    else:
        return jsonify({"message": "No se pudo obtener la disponibilidad para este médico."}), 404
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
