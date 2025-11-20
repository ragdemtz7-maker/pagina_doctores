from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importar routers
from backend.paciente.routes import router as paciente_router
from backend.usuario.routes import router as usuario_router
from backend.medico.routes import router as medico_router
from backend.cita_medica.routes import router as cita_medica_router
from mangum import Mangum

app = FastAPI(
    title="API Citas Médicas",
    description="CRUD modularizado por entidad con ejemplos JSON listos para probar",
    version="1.0.0"
)

# CORS
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

@app.get("/")
def home():
    return {"message": "API modularizada funcionando"}

# Lambda handler (debe ir al final)
handler = Mangum(app)

# Para ejecución local
if __name__ == "__main__":
    uvicorn.run("backend.app_swagger:app", host="0.0.0.0", port=5001, reload=True)
