from fastapi import APIRouter
from backend.especialidad.models import EspecialidadCreate, MedicoEspecialidadCreate
from backend.especialidad.logic import (
    agregar_especialidad,
    asignar_especialidad_a_medico,
    obtener_especialidades,
    obtener_especialidad_por_id,
    obtener_especialidades_por_medico
)

router = APIRouter(prefix="/especialidad", tags=["Especialidad"])

# Crear especialidad
@router.post("/agregar")
def crear_especialidad(data: EspecialidadCreate):
    return agregar_especialidad(data)

# Asignar especialidad a médico
@router.post("/asignar")
def asignar_especialidad(data: MedicoEspecialidadCreate):
    return asignar_especialidad_a_medico(data)

# Listar todas las especialidades
@router.get("/todas")
def listar_especialidades():
    return obtener_especialidades()

# Obtener especialidad por ID
@router.get("/{id_especialidad}")
def get_especialidad(id_especialidad: int):
    return obtener_especialidad_por_id(id_especialidad)

# Obtener especialidades por médico
@router.get("/medico/{id_medico}")
def get_especialidades_medico(id_medico: int):
    return obtener_especialidades_por_medico(id_medico)
