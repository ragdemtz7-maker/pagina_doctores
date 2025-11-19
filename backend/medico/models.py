# backend/medico/models.py
from pydantic import BaseModel, EmailStr

class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    num_documento: str
    correo: EmailStr
    telefono: str
    direccion: str

class MedicoCreate(PersonaBase):
    pass

class MedicoUpdate(PersonaBase):
    pass
