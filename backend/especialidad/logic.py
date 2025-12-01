import pymysql
from fastapi import HTTPException
from backend.db import get_connection  # Asumiendo que tienes esta función

def agregar_especialidad(data):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Especialidades (id_especialidad, especialidad) VALUES (%s, %s)",
                (data.id_especialidad, data.especialidad)
            )
        conn.commit()
        return {"status": "ok", "message": "Especialidad agregada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar especialidad: {str(e)}")

def asignar_especialidad_a_medico(data):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Medico_Especialidad (id_medico, especialidad) VALUES (%s, %s)",
                (data.id_medico, data.especialidad)
            )
        conn.commit()
        return {"status": "ok", "message": "Especialidad asignada al médico"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al asignar especialidad: {str(e)}")
