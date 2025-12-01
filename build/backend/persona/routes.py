from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from backend.persona.logic import crear_persona_si_no_existe

router = APIRouter(prefix="/persona", tags=["Persona"])

@router.post("/crear")
async def crear_persona(request: Request):
    data = await request.json()
    try:
        id_persona = crear_persona_si_no_existe(data)
        return {"id_persona": id_persona}
    except Exception as e:
        return JSONResponse(
            content={"error": f"Error al crear persona: {str(e)}"},
            status_code=500,
        )
