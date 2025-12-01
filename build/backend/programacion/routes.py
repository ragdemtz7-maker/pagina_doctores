from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.programacion.models import ProgramacionCreate, ProgramacionUpdate
from backend.programacion.logic import (
    crear_programacion,
    listar_programaciones,
    actualizar_programacion,
    eliminar_programacion,
)

router = APIRouter(prefix="/programacion", tags=["Programacion"])

@router.post("/crear", summary="Crear programación")
def api_crear_programacion(data: ProgramacionCreate):
    resultado = crear_programacion(data.dict())
    if resultado.get("status") == "error":
        return JSONResponse(content=resultado, status_code=500)
    return resultado

@router.get("/listar", summary="Listar programaciones")
def api_listar_programaciones():
    resultado = listar_programaciones()
    return resultado

@router.put("/actualizar/{id_programacion}", summary="Actualizar programación")
def api_actualizar_programacion(id_programacion: int, data: ProgramacionUpdate):
    resultado = actualizar_programacion(id_programacion, data.dict())
    if resultado.get("status") == "error":
        return JSONResponse(content=resultado, status_code=500)
    return resultado

@router.delete("/eliminar/{id_programacion}", summary="Eliminar programación")
def api_eliminar_programacion(id_programacion: int):
    resultado = eliminar_programacion(id_programacion)
    if resultado.get("status") == "error":
        return JSONResponse(content=resultado, status_code=500)
    return resultado
