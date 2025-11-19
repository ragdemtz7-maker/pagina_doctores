# Lógica CRUD para persona
from flask import request, jsonify
from backend.bd import get_connection

def crear_persona_si_no_existe(data):
    """
    Crea una persona si no existe por num_documento o correo.
    Retorna el id_persona existente o recién creado.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_persona FROM Persona
                WHERE num_documento = %s OR correo = %s
            """, (data.get("num_documento"), data.get("correo")))
            row = cursor.fetchone()
            if row:
                return row[0]  # persona ya existe

            cursor.execute("""
                INSERT INTO Persona (nombre, apellido, num_documento, correo, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data.get("nombre"), data.get("apellido"), data.get("num_documento"),
                data.get("correo"), data.get("telefono"), data.get("direccion")
            ))
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        raise Exception(f"Error al crear persona: {str(e)}")
    finally:
        conn.close()
