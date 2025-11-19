# Lógica CRUD para programacion
from flask import request, jsonify
from backend.bd import get_connection

def crear_programacion():
    data = request.json or {}
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Programacion (id_medico, fecha, hora_inicio, hora_fin)
                VALUES (%s, %s, %s, %s)
            """, (data.get("id_medico"), data.get("fecha"), data.get("hora_inicio"), data.get("hora_fin")))
            conn.commit()
            return jsonify({"status": "ok", "id_programacion": cursor.lastrowid})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
    finally:
        conn.close()

def listar_programaciones():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Programacion ORDER BY fecha, hora_inicio")
            rows = cursor.fetchall()
            programaciones = [dict(zip([d[0] for d in cursor.description], r)) for r in rows]
            return jsonify(programaciones)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def actualizar_programacion(id_programacion):
    data = request.json or {}
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Programacion
                SET fecha = %s, hora_inicio = %s, hora_fin = %s
                WHERE id_programacion = %s
            """, (data.get("fecha"), data.get("hora_inicio"), data.get("hora_fin"), id_programacion))
            conn.commit()
            return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
    finally:
        conn.close()

def eliminar_programacion(id_programacion):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Programacion WHERE id_programacion = %s", (id_programacion,))
            conn.commit()
            return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
    finally:
        conn.close()
