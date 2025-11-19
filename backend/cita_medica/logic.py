from fastapi import HTTPException
from backend.bd import get_connection

def crear_cita_medica(data):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO CitaMedica (id_programacion, estado)
                VALUES (%s, %s)
            """, (data.id_programacion, data.estado))
            conn.commit()
            return {"status": "ok", "id_cita": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def listar_citas_medicas():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_cita, id_programacion, estado
                FROM CitaMedica
            """)
            rows = cursor.fetchall()
            return [dict(zip([d[0] for d in cursor.description], r)) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def obtener_cita_medica(id_cita):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_cita, id_programacion, estado
                FROM CitaMedica WHERE id_cita = %s
            """, (id_cita,))
            row = cursor.fetchone()
            if row:
                return dict(zip([d[0] for d in cursor.description], row))
            else:
                raise HTTPException(status_code=404, detail="Cita médica no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def actualizar_cita_medica(id_cita, data):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE CitaMedica
                SET id_programacion=%s, estado=%s
                WHERE id_cita=%s
            """, (data.id_programacion, data.estado, id_cita))
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def eliminar_cita_medica(id_cita):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM CitaMedica WHERE id_cita=%s", (id_cita,))
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
