import pymysql
from fastapi import HTTPException
from backend.bd import get_connection  # ✅ correcto: bd, no db

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

def obtener_especialidades():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_especialidad, especialidad FROM Especialidades")
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener especialidades: {str(e)}")

def obtener_especialidad_por_id(id_especialidad: int):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_especialidad, especialidad FROM Especialidades WHERE id_especialidad = %s",
                (id_especialidad,)
            )
            result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Especialidad no encontrada")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener especialidad: {str(e)}")

def obtener_especialidades_por_medico(id_medico: int):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT e.id_especialidad, e.especialidad
                FROM Medico_Especialidad me
                JOIN Especialidades e ON me.especialidad = e.especialidad
                WHERE me.id_medico = %s
                """,
                (id_medico,)
            )
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener especialidades del médico: {str(e)}")
