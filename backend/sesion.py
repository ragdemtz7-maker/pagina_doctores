from datetime import date, datetime, timedelta

import pymysql

from backend.bd import get_connection


def get_nombre_completo_usuario(id_persona):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT nombre, apellido FROM Persona WHERE id_persona = %s"
        cursor.execute(query, (id_persona,))
        resultado = cursor.fetchone()

        if resultado:
            nombre, apellido = resultado
            return f"{nombre} {apellido}"
        else:
            return None
    except pymysql.MySQLError as err:
        print(f"Error al obtener nombre de usuario: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_medicos():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()       
        query = """
        SELECT
            m.id_medico,
            p.nombre,
            p.apellido
        FROM
            Medico m
        JOIN
            Persona p ON m.id_persona = p.id_persona
        JOIN
            Usuario u ON p.id_persona = u.id_persona
        WHERE
            u.rol = 'medico';
        """
        cursor.execute(query)
        raw_medicos = cursor.fetchall()

        medicos_formateados = []
        for medico_tuple in raw_medicos:
            medicos_formateados.append({
                'id': medico_tuple[0],
                'nombre': medico_tuple[1],
                'apellido': medico_tuple[2],
                'nombre_completo': f"{medico_tuple[1]} {medico_tuple[2]}"
            })
        return medicos_formateados
    except pymysql.MySQLError as err:
        print(f"Error al obtener médicos: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def generate_all_time_slots():
    slots = []
    start_time = datetime.strptime("08:00", "%H:%M").time()
    end_time = datetime.strptime("17:00", "%H:%M").time()
    interval = timedelta(minutes=30)

    current_time = start_time
    while current_time < end_time:
        slot_start = current_time
        slot_end = (datetime.combine(date.min, current_time) + interval).time()
        slots.append(f"{slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}")
        current_time = slot_end
    return slots

def get_disponibilidad_medico_mes(id_medico):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        today = date.today()
        fechas_a_consultar = [today + timedelta(days=i) for i in range(30)]
        fechas_str = [f.strftime('%Y-%m-%d') for f in fechas_a_consultar]

        query_citas_ocupadas = """
        SELECT
            P.fecha,
            TIME_FORMAT(P.hora_inicio, '%H:%i') AS hora_inicio,
            TIME_FORMAT(P.hora_fin, '%H:%i') AS hora_fin
        FROM
            CitaMedica CM
        JOIN
            Programacion P ON CM.id_programacion = P.id_programacion
        WHERE
            P.id_medico = %s
            AND P.fecha BETWEEN %s AND %s
            AND CM.estado = 'programada';
        """
        cursor.execute(query_citas_ocupadas, (id_medico, fechas_str[0], fechas_str[-1]))
        citas_ocupadas_raw = cursor.fetchall()

        ocupadas_por_fecha = {}
        for fecha, hora_inicio, hora_fin in citas_ocupadas_raw:
            fecha_key = fecha.strftime('%Y-%m-%d')
            if fecha_key not in ocupadas_por_fecha:
                ocupadas_por_fecha[fecha_key] = []
            ocupadas_por_fecha[fecha_key].append(f"{hora_inicio}-{hora_fin}")

        disponibilidad_completa = {}
        all_possible_slots = generate_all_time_slots()

        for d_date in fechas_a_consultar:
            fecha_key = d_date.strftime('%Y-%m-%d')
            slots_del_dia = []
            for slot_time_range in all_possible_slots:
                is_occupied = fecha_key in ocupadas_por_fecha and slot_time_range in ocupadas_por_fecha[fecha_key]
                slots_del_dia.append({
                    'time_range': slot_time_range,
                    'ocupado': is_occupied,
                    'id_programacion': None
                })
            disponibilidad_completa[fecha_key] = slots_del_dia
            
        return disponibilidad_completa

    except pymysql.MySQLError as err:
        print(f"Error al obtener disponibilidad para médico {id_medico}: {err}")
        return {}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
