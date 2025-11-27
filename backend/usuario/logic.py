from fastapi import HTTPException
from backend.bd import get_connection
from backend.persona.logic import crear_persona_si_no_existe
import boto3

# Configuración Cognito
COGNITO_USER_POOL_ID = "us-east-2_sbXYObV2q"
COGNITO_CLIENT_ID = "5eiror37ph4chhlm1a85sqk0cg"
cognito_client = boto3.client("cognito-idp", region_name="us-east-2")

def crear_usuario(data):
    try:
        # 1) Crear usuario en Cognito
        try:
            response = cognito_client.admin_create_user(
                UserPoolId=COGNITO_USER_POOL_ID,
                Username=data.correo,
                UserAttributes=[
                    {"Name": "email", "Value": data.correo},
                    {"Name": "name", "Value": data.nombre},
                    {"Name": "family_name", "Value": data.apellido},
                ]
            )
            attributes = {attr["Name"]: attr["Value"] for attr in response["User"]["Attributes"]}
            id_cognito = attributes.get("sub")
            if not id_cognito:
                raise HTTPException(status_code=500, detail="No se pudo obtener id_cognito de Cognito")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creando usuario en Cognito: {str(e)}")

        # 2) Crear Persona en tu BD
        id_persona = crear_persona_si_no_existe(data.dict())
        if not id_persona:
            raise HTTPException(status_code=400, detail="La persona ya existe o no se pudo crear")

        # 3) Insertar Usuario vinculado a esa persona
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Usuario (id_persona, id_cognito, rol)
                VALUES (%s, %s, %s)
            """, (id_persona, id_cognito, data.rol))
            conn.commit()
            id_usuario = cursor.lastrowid if cursor.lastrowid else None

        return {
            "status": "ok",
            "id_usuario": id_usuario,
            "id_persona": id_persona,
            "id_cognito": id_cognito
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def listar_usuarios():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.id_usuario, u.id_cognito, u.rol,
                       p.id_persona, p.nombre, p.apellido, p.num_documento,
                       p.correo, p.telefono, p.direccion
                FROM Usuario u
                JOIN Persona p ON u.id_persona = p.id_persona
            """)
            rows = cursor.fetchall()
            return [dict(zip([d[0] for d in cursor.description], r)) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def obtener_usuario(id_usuario: int):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.id_usuario, u.id_cognito, u.rol,
                       p.id_persona, p.nombre, p.apellido, p.num_documento,
                       p.correo, p.telefono, p.direccion
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


def actualizar_usuario(id_usuario: int, data):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_persona FROM Usuario WHERE id_usuario=%s", (id_usuario,))
            r = cursor.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            id_persona = r[0]

            # Actualizar Persona vinculada
            cursor.execute("""
                UPDATE Persona
                SET nombre=%s, apellido=%s, num_documento=%s,
                    correo=%s, telefono=%s, direccion=%s
                WHERE id_persona=%s
            """, (
                data.nombre, data.apellido, data.num_documento,
                data.correo, data.telefono, data.direccion, id_persona
            ))

            # Actualizar Usuario
            cursor.execute("""
                UPDATE Usuario
                SET id_cognito=%s, rol=%s
                WHERE id_usuario=%s
            """, (data.id_cognito, data.rol, id_usuario))

            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def eliminar_usuario(id_usuario: int):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_persona FROM Usuario WHERE id_usuario=%s", (id_usuario,))
            r = cursor.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            id_persona = r[0]

            # Eliminar Usuario y Persona vinculada
            cursor.execute("DELETE FROM Usuario WHERE id_usuario=%s", (id_usuario,))
            cursor.execute("DELETE FROM Persona WHERE id_persona=%s", (id_persona,))
            conn.commit()
            return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
