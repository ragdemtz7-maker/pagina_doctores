# backend/medico/logic.py
from fastapi import HTTPException
from backend.bd import get_connection
from backend.persona.logic import crear_persona_si_no_existe

def crear_medico(data):
    try:
        # Crear/reciclar Persona
        id_persona = crear_persona_si_no_existe(data.dict())
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Medico (id_persona) VALUES (%s)", (id_persona,))
            conn.commit()
            return {"status": "ok", "id_medico": cursor.lastrowid, "id_persona": id_persona}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def listar_medicos():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.id_medico,
                       p.id_persona, p.nombre, p.apellido, p.num_documento, p.correo, p.telefono, p.direccion
                FROM Medico m
                JOIN Persona p ON m.id_persona = p.id_persona
            """)
            rows = cursor.fetchall()
            return [dict(zip([d[0] for d in cursor.description], r)) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def obtener_medico(id_medico: int):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.id_medico,
                       p.id_persona, p.nombre, p.apellido, p.num_documento, p.correo, p.telefono, p.direccion
                FROM Medico m
                JOIN Persona p ON m.id_persona = p.id_persona
                WHERE m.id_medico = %s
            """, (id_medico,))
            row = cursor.fetchone()
            if row:
                return dict(zip([d[0] for d in cursor.description], row))
            raise HTTPException(status_code=404, detail="Medico no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def actualizar_medico(id_medico: int, data):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # Obtener id_persona
            cursor.execute("SELECT id_persona FROM Medico WHERE id_medico=%s", (id_medico,))
            r = cursor.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Medico no encontrado")
            id_persona = r[0]

            # Actualizar Persona
            cursor.execute("""
                UPDATE Persona SET nombre=%s, apellido=%s, num_documento=%s,
                                   correo=%s, telefono=%s, direccion=%s
                WHERE id_persona=%s
            """, (data.nombre, data.apellido, data.num_documento,
                  data.correo, data.telefono, data.direccion, id_persona))
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def eliminar_medico(id_medico: int):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_persona FROM Medico WHERE id_medico=%s", (id_medico,))
            r = cursor.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Medico no encontrado")
            id_persona = r[0]

            cursor.execute("DELETE FROM Medico WHERE id_medico=%s", (id_medico,))
            cursor.execute("DELETE FROM Persona WHERE id_persona=%s", (id_persona,))
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
