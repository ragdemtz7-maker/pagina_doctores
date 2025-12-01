from backend.bd import get_connection
from fastapi import HTTPException

def crear_programacion(data: dict) -> dict:
    """
    Crea una programación y retorna el id generado.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Programacion (id_medico, fecha, hora_inicio, hora_fin)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    data.get("id_medico"),
                    data.get("fecha"),
                    data.get("hora_inicio"),
                    data.get("hora_fin"),
                ),
            )
            conn.commit()
            return {"status": "ok", "id_programacion": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


def listar_programaciones() -> list:
    """
    Lista todas las programaciones ordenadas por fecha y hora.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Programacion ORDER BY fecha, hora_inicio")
            rows = cursor.fetchall()
            return [dict(zip([d[0] for d in cursor.description], r)) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


def actualizar_programacion(id_programacion: int, data: dict) -> dict:
    """
    Actualiza una programación existente.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Programacion
                SET fecha = %s, hora_inicio = %s, hora_fin = %s
                WHERE id_programacion = %s
                """,
                (
                    data.get("fecha"),
                    data.get("hora_inicio"),
                    data.get("hora_fin"),
                    id_programacion,
                ),
            )
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


def eliminar_programacion(id_programacion: int) -> dict:
    """
    Elimina una programación por id.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Programacion WHERE id_programacion = %s",
                (id_programacion,),
            )
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
