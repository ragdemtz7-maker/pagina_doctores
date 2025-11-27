from fastapi import HTTPException
from jose import jwt
import requests

COGNITO_POOL_URL = "https://cognito-idp.us-east-2.amazonaws.com/us-east-2_sbXYObV2q"
COGNITO_CLIENT_ID = "5eiror37ph4chhlm1a85sqk0cg"

def verify_token(token: str):
    try:
        # Obtener JWKS de Cognito
        jwks_url = f"{COGNITO_POOL_URL}/.well-known/jwks.json"
        jwks = requests.get(jwks_url).json()

        # Decodificar JWT
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            audience=COGNITO_CLIENT_ID
        )
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

def login(token: str):
    # Validar token y devolver info del usuario
    payload = verify_token(token)
    return {
        "status": "ok",
        "id_cognito": payload.get("sub"),
        "email": payload.get("email"),
        "claims": payload
    }

def logout():
    # En Cognito el logout real se hace en frontend (revocar tokens).
    # Aquí devolvemos un estado simple.
    return {"status": "ok", "message": "Sesión cerrada"}
