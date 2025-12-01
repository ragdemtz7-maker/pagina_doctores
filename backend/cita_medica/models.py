from pydantic import BaseModel

class CitaMedicaBase(BaseModel):
    id_programacion: int
    id_paciente: int          # ✅ nuevo campo
    estado: str               # valores: programada, cancelada, completada

class CitaMedicaCreate(CitaMedicaBase):
    pass

class CitaMedicaUpdate(CitaMedicaBase):
    pass
