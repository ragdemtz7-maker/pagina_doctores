# backend/medico/routes.py
from fastapi import APIRouter, Path
from backend.medico.models import MedicoCreate, MedicoUpdate
from backend.medico.logic import (
    crear_medico, listar_medicos,
    obtener_medico, actualizar_medico, eliminar_medico
)

router = APIRouter()

@router.post("/medico", summary="Crear médico")
def crear(data: MedicoCreate):
    return crear_medico(data)

@router.get("/medico", summary="Listar médicos")
def listar():
    return listar_medicos()

@router.get("/medico/{id_medico}", summary="Obtener médico por ID")
def obtener(id_medico: int = Path(...)):
    return obtener_medico(id_medico)

@router.put("/medico/{id_medico}", summary="Actualizar médico")
def actualizar(id_medico: int, data: MedicoUpdate):
    return actualizar_medico(id_medico, data)

@router.delete("/medico/{id_medico}", summary="Eliminar médico")
def eliminar(id_medico: int = Path(...)):
    return eliminar_medico(id_medico)
