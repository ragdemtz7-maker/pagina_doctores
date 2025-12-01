from pydantic import BaseModel

class EspecialidadCreate(BaseModel):
    id_especialidad: int
    especialidad: str

class MedicoEspecialidadCreate(BaseModel):
    id_medico: int
    id_especialidad: int 