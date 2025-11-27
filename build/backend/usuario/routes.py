from fastapi import APIRouter, Path
from backend.usuario.models import UsuarioCreate, UsuarioUpdate
from backend.usuario.logic import (
    crear_usuario, listar_usuarios,
    obtener_usuario, actualizar_usuario, eliminar_usuario
)

router = APIRouter()

@router.post("/usuario", summary="Crear usuario")
def crear(data: UsuarioCreate):
    return crear_usuario(data)

@router.get("/usuario", summary="Listar usuarios")
def listar():
    return listar_usuarios()

@router.get("/usuario/{id_usuario}", summary="Obtener usuario por ID")
def obtener(id_usuario: int = Path(...)):
    return obtener_usuario(id_usuario)

@router.put("/usuario/{id_usuario}", summary="Actualizar usuario")
def actualizar(id_usuario: int, data: UsuarioUpdate):
    return actualizar_usuario(id_usuario, data)

@router.delete("/usuario/{id_usuario}", summary="Eliminar usuario")
def eliminar(id_usuario: int = Path(...)):
    return eliminar_usuario(id_usuario)
