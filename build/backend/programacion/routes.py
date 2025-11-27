from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from backend.programacion.logic import (
    crear_programacion,
    listar_programaciones,
    actualizar_programacion,
    eliminar_programacion,
)

router = APIRouter(prefix="/api/programacion", tags=["Programacion"])

@router.post("/crear")
async def api_crear_programacion(request: Request):
    data = await request.json()
    resultado = crear_programacion(data)
    if resultado.get("status") == "error":
        return JSONResponse(content=resultado, status_code=500)
    return resultado

@router.get("/listar")
def api_listar_programaciones():
    resultado = listar_programaciones()
    if isinstance(resultado, dict) and "error" in resultado:
        return JSONResponse(content=resultado, status_code=500)
    return resultado

@router.put("/actualizar/{id_programacion}")
async def api_actualizar_programacion(id_programacion: int, request: Request):
    data = await request.json()
    resultado = actualizar_programacion(id_programacion, data)
    if resultado.get("status") == "error":
        return JSONResponse(content=resultado, status_code=500)
    return resultado

@router.delete("/eliminar/{id_programacion}")
def api_eliminar_programacion(id_programacion: int):
    resultado = eliminar_programacion(id_programacion)
    if resultado.get("status") == "error":
        return JSONResponse(content=resultado, status_code=500)
    return resultado
