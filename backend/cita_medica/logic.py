from fastapi import HTTPException
from backend.bd import get_connection

def crear_cita_medica(data):
    """
    Crea una cita médica vinculando programación y paciente.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO CitaMedica (id_programacion, id_paciente, estado)
                VALUES (%s, %s, %s)
            """, (data.id_programacion, data.id_paciente, data.estado))
            conn.commit()
            return {"status": "ok", "id_cita": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


def listar_citas_medicas():
    """
    Lista todas las citas médicas con datos de programación y paciente.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.id_cita, c.id_programacion, c.id_paciente, c.estado,
                       p.fecha, p.hora_inicio, p.hora_fin,
                       pa.nombre AS paciente_nombre, pa.apellido AS paciente_apellido
                FROM CitaMedica c
                JOIN Programacion p ON c.id_programacion = p.id_programacion
                JOIN Paciente pa ON c.id_paciente = pa.id_paciente
                ORDER BY p.fecha, p.hora_inicio
            """)
            rows = cursor.fetchall()
            return [dict(zip([d[0] for d in cursor.description], r)) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


def obtener_cita_medica(id_cita: int):
    """
    Obtiene una cita médica por su ID.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.id_cita, c.id_programacion, c.id_paciente, c.estado,
                       p.fecha, p.hora_inicio, p.hora_fin,
                       pa.nombre AS paciente_nombre, pa.apellido AS paciente_apellido
                FROM CitaMedica c
                JOIN Programacion p ON c.id_programacion = p.id_programacion
                JOIN Paciente pa ON c.id_paciente = pa.id_paciente
                WHERE c.id_cita = %s
            """, (id_cita,))
            row = cursor.fetchone()
            if row:
                return dict(zip([d[0] for d in cursor.description], row))
            else:
                raise HTTPException(status_code=404, detail="Cita médica no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


def actualizar_cita_medica(id_cita: int, data):
    """
    Actualiza una cita médica (programación, paciente o estado).
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE CitaMedica
                SET id_programacion=%s, id_paciente=%s, estado=%s
                WHERE id_cita=%s
            """, (data.id_programacion, data.id_paciente, data.estado, id_cita))
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


def eliminar_cita_medica(id_cita: int):
    """
    Elimina una cita médica por su ID.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM CitaMedica WHERE id_cita=%s", (id_cita,))
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
