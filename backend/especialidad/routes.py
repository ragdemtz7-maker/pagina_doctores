from fastapi import APIRouter
from backend.especialidad.models import EspecialidadCreate, MedicoEspecialidadCreate
from backend.especialidad.logic import agregar_especialidad, asignar_especialidad_a_medico

router = APIRouter(prefix="/especialidad", tags=["Especialidad"])

@router.post("/agregar")
def crear_especialidad(data: EspecialidadCreate):
    return agregar_especialidad(data)

@router.post("/asignar")
def asignar_especialidad(data: MedicoEspecialidadCreate):
    return asignar_especialidad_a_medico(data)
