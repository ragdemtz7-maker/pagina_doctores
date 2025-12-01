from fastapi import APIRouter, Path
from backend.cita_medica.models import CitaMedicaCreate, CitaMedicaUpdate
from backend.cita_medica.logic import (
    crear_cita_medica,
    listar_citas_medicas,
    obtener_cita_medica,
    actualizar_cita_medica,
    eliminar_cita_medica,
)

router = APIRouter(prefix="/api/cita_medica", tags=["CitaMedica"])

@router.post("/", summary="Crear cita médica")
def crear(data: CitaMedicaCreate):
    """
    Crear una cita médica vinculando programación y paciente.
    """
    return crear_cita_medica(data)

@router.get("/", summary="Listar citas médicas")
def listar():
    """
    Listar todas las citas médicas con datos de programación y paciente.
    """
    return listar_citas_medicas()

@router.get("/{id_cita}", summary="Obtener cita médica por ID")
def obtener(id_cita: int = Path(...)):
    """
    Obtener una cita médica específica por su ID.
    """
    return obtener_cita_medica(id_cita)

@router.put("/{id_cita}", summary="Actualizar cita médica")
def actualizar(id_cita: int, data: CitaMedicaUpdate):
    """
    Actualizar una cita médica (programación, paciente o estado).
    """
    return actualizar_cita_medica(id_cita, data)

@router.delete("/{id_cita}", summary="Eliminar cita médica")
def eliminar(id_cita: int = Path(...)):
    """
    Eliminar una cita médica por su ID.
    """
    return eliminar_cita_medica(id_cita)
