from fastapi import HTTPException
from backend.bd import get_connection
from backend.persona.logic import crear_persona_si_no_existe

def crear_paciente(data):
    try:
        # 1) Crear/reciclar Persona
        id_persona = crear_persona_si_no_existe(data.dict())

        # 2) Insertar Paciente con id_persona
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Paciente (id_persona, fecha_nacimiento)
                VALUES (%s, %s)
            """, (id_persona, data.fecha_nacimiento))
            conn.commit()
            return {"status": "ok", "id_paciente": cursor.lastrowid, "id_persona": id_persona}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def listar_pacientes():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    pa.id_paciente, pa.fecha_nacimiento,
                    p.id_persona, p.nombre, p.apellido, p.num_documento, p.correo, p.telefono, p.direccion
                FROM Paciente pa
                JOIN Persona p ON pa.id_persona = p.id_persona
            """)
            rows = cursor.fetchall()
            return [dict(zip([d[0] for d in cursor.description], r)) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def obtener_paciente(id_paciente):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    pa.id_paciente, pa.fecha_nacimiento,
                    p.id_persona, p.nombre, p.apellido, p.num_documento, p.correo, p.telefono, p.direccion
                FROM Paciente pa
                JOIN Persona p ON pa.id_persona = p.id_persona
                WHERE pa.id_paciente = %s
            """, (id_paciente,))
            row = cursor.fetchone()
            if row:
                return dict(zip([d[0] for d in cursor.description], row))
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def actualizar_paciente(id_paciente, data):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # Obtener id_persona asociado
            cursor.execute("SELECT id_persona FROM Paciente WHERE id_paciente=%s", (id_paciente,))
            r = cursor.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Paciente no encontrado")
            id_persona = r[0]

            # Actualizar Persona
            cursor.execute("""
                UPDATE Persona
                SET nombre=%s, apellido=%s, num_documento=%s, correo=%s, telefono=%s, direccion=%s
                WHERE id_persona=%s
            """, (data.nombre, data.apellido, data.num_documento, data.correo, data.telefono, data.direccion, id_persona))

            # Actualizar Paciente
            cursor.execute("""
                UPDATE Paciente
                SET fecha_nacimiento=%s
                WHERE id_paciente=%s
            """, (data.fecha_nacimiento, id_paciente))

            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def eliminar_paciente(id_paciente):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # Obtener id_persona asociado
            cursor.execute("SELECT id_persona FROM Paciente WHERE id_paciente=%s", (id_paciente,))
            r = cursor.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Paciente no encontrado")
            id_persona = r[0]

            # Eliminar Paciente y su Persona
            cursor.execute("DELETE FROM Paciente WHERE id_paciente=%s", (id_paciente,))
            cursor.execute("DELETE FROM Persona WHERE id_persona=%s", (id_persona,))
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
