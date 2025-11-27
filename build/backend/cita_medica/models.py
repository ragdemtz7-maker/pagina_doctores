from pydantic import BaseModel

class CitaMedicaBase(BaseModel):
    id_programacion: int
    estado: str  # valores: activa, cancelada, pasada

class CitaMedicaCreate(CitaMedicaBase):
    pass

class CitaMedicaUpdate(CitaMedicaBase):
    pass
