from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from backend.paciente.routes import router as paciente_router
from backend.usuario.routes import router as usuario_router
from backend.medico.routes import router as medico_router
from backend.cita_medica.routes import router as cita_medica_router
from backend.persona.routes import router as persona_router
from backend.programacion.routes import router as programacion_router

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

# Routers
app.include_router(paciente_router, prefix="/api", tags=["Paciente"])
app.include_router(usuario_router, prefix="/api", tags=["Usuario"])
app.include_router(medico_router, prefix="/api", tags=["Medico"])
app.include_router(cita_medica_router, prefix="/api", tags=["CitaMedica"])
app.include_router(persona_router, prefix="/api", tags=["Persona"])
app.include_router(programacion_router, prefix="/api", tags=["Programacion"])

@app.get("/")
def home():
    return {"message": "API modularizada funcionando"}

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
