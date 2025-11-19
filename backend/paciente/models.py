from pydantic import BaseModel, EmailStr

class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    num_documento: str
    correo: EmailStr
    telefono: str
    direccion: str

class PacienteCreate(PersonaBase):
    fecha_nacimiento: str  # YYYY-MM-DD

class PacienteUpdate(PersonaBase):
    fecha_nacimiento: str  # YYYY-MM-DD
