from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum

from backend.paciente import guardar_paciente
from backend.sesion import (
    get_disponibilidad_medico_mes,
    get_medicos,
    get_nombre_completo_usuario,
)

app = FastAPI(
    title="API Citas Médicas",
    description="CRUD modularizado por entidad con ejemplos JSON listos para probar",
    version="1.0.0",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend de Citas Médicas funcionando"}

@app.post("/api/guardar_paciente")
async def api_guardar_paciente(request: Request):
    data = await request.json()
    resultado = guardar_paciente(data)
    if resultado.get("status") == "error":
        return JSONResponse(content=resultado, status_code=500)
    return JSONResponse(content=resultado)

@app.get("/api/nombre_usuario/{id_persona}")
def api_nombre_usuario(id_persona: int):
    nombre = get_nombre_completo_usuario(id_persona)
    if nombre:
        return {"nombre_completo": nombre}
    return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)

@app.get("/api/medicos")
def api_get_medicos():
    medicos = get_medicos()
    if medicos:
        return medicos
    return JSONResponse(content={"message": "No se encontraron médicos"}, status_code=404)

@app.get("/api/medicos/{id_medico}/disponibilidad")
def api_get_disponibilidad_medico(id_medico: int):
    disponibilidad = get_disponibilidad_medico_mes(id_medico)
    if disponibilidad:
        return disponibilidad
    return JSONResponse(
        content={"message": "No se pudo obtener la disponibilidad para este médico."},
        status_code=404,
    )

# Handler para Lambda
handler = Mangum(app)

# Bloque para ejecución local con python -m
if __name__ == "__main__":
    import asyncio
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5001"]

    asyncio.run(serve(app, config))
