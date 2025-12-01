from pydantic import BaseModel

class ProgramacionBase(BaseModel):
    id_medico: int
    fecha: str        # YYYY-MM-DD
    hora_inicio: str  # HH:MM:SS
    hora_fin: str     # HH:MM:SS

class ProgramacionCreate(ProgramacionBase):
    pass

class ProgramacionUpdate(ProgramacionBase):
    pass
