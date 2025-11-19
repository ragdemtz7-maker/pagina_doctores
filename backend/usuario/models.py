from pydantic import BaseModel, EmailStr

class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    num_documento: str
    correo: EmailStr
    telefono: str
    direccion: str

class UsuarioCreate(PersonaBase):
    id_cognito: str
    rol: str

class UsuarioUpdate(UsuarioCreate):
    pass
