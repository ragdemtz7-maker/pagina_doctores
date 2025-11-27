from fastapi import HTTPException
from backend.bd import get_connection
from backend.persona.logic import crear_persona_si_no_existe

def crear_usuario(data):
    try:
        id_persona = crear_persona_si_no_existe(data.dict())
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Usuario (id_persona, id_cognito, rol)
                VALUES (%s, %s, %s)
            """, (id_persona, data.id_cognito, data.rol))
            conn.commit()
            return {"status": "ok", "id_usuario": cursor.lastrowid, "id_persona": id_persona}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def listar_usuarios():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.id_usuario, u.id_cognito, u.rol,
                       p.id_persona, p.nombre, p.apellido, p.num_documento, p.correo, p.telefono, p.direccion
                FROM Usuario u
                JOIN Persona p ON u.id_persona = p.id_persona
            """)
            rows = cursor.fetchall()
            return [dict(zip([d[0] for d in cursor.description], r)) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def obtener_usuario(id_usuario):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.id_usuario, u.id_cognito, u.rol,
                       p.id_persona, p.nombre, p.apellido, p.num_documento, p.correo, p.telefono, p.direccion
                FROM Usuario u
                JOIN Persona p ON u.id_persona = p.id_persona
                WHERE u.id_usuario = %s
            """, (id_usuario,))
            row = cursor.fetchone()
            if row:
                return dict(zip([d[0] for d in cursor.description], row))
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def actualizar_usuario(id_usuario, data):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_persona FROM Usuario WHERE id_usuario = %s", (id_usuario,))
            r = cursor.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            id_persona = r[0]

            cursor.execute("""
                UPDATE Persona SET nombre=%s, apellido=%s, num_documento=%s,
                correo=%s, telefono=%s, direccion=%s
                WHERE id_persona = %s
            """, (
                data.nombre, data.apellido, data.num_documento,
                data.correo, data.telefono, data.direccion, id_persona
            ))

            cursor.execute("""
                UPDATE Usuario SET id_cognito=%s, rol=%s WHERE id_usuario=%s
            """, (data.id_cognito, data.rol, id_usuario))

            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def eliminar_usuario(id_usuario):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_persona FROM Usuario WHERE id_usuario = %s", (id_usuario,))
            r = cursor.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            id_persona = r[0]

            cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id_usuario,))
            cursor.execute("DELETE FROM Persona WHERE id_persona = %s", (id_persona,))
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
