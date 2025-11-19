from fastapi import APIRouter, Path
from backend.paciente.models import PacienteCreate, PacienteUpdate
from backend.paciente.logic import (
    crear_paciente, listar_pacientes,
    obtener_paciente, actualizar_paciente, eliminar_paciente
)

router = APIRouter()

@router.post("/paciente", summary="Crear paciente")
def crear(data: PacienteCreate):
    return crear_paciente(data)

@router.get("/paciente", summary="Listar pacientes")
def listar():
    return listar_pacientes()

@router.get("/paciente/{id_paciente}", summary="Obtener paciente por ID")
def obtener(id_paciente: int = Path(...)):
    return obtener_paciente(id_paciente)

@router.put("/paciente/{id_paciente}", summary="Actualizar paciente")
def actualizar(id_paciente: int, data: PacienteUpdate):
    return actualizar_paciente(id_paciente, data)

@router.delete("/paciente/{id_paciente}", summary="Eliminar paciente")
def eliminar(id_paciente: int = Path(...)):
    return eliminar_paciente(id_paciente)
