from fastapi import APIRouter, Path
from backend.cita_medica.models import CitaMedicaCreate, CitaMedicaUpdate
from backend.cita_medica.logic import (
    crear_cita_medica, listar_citas_medicas,
    obtener_cita_medica, actualizar_cita_medica, eliminar_cita_medica
)

router = APIRouter()

@router.post("/cita_medica", summary="Crear cita médica")
def crear(data: CitaMedicaCreate):
    return crear_cita_medica(data)

@router.get("/cita_medica", summary="Listar citas médicas")
def listar():
    return listar_citas_medicas()

@router.get("/cita_medica/{id_cita}", summary="Obtener cita médica por ID")
def obtener(id_cita: int = Path(...)):
    return obtener_cita_medica(id_cita)

@router.put("/cita_medica/{id_cita}", summary="Actualizar cita médica")
def actualizar(id_cita: int, data: CitaMedicaUpdate):
    return actualizar_cita_medica(id_cita, data)

@router.delete("/cita_medica/{id_cita}", summary="Eliminar cita médica")
def eliminar(id_cita: int = Path(...)):
    return eliminar_cita_medica(id_cita)
