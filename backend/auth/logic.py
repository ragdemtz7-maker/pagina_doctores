from fastapi import HTTPException
import boto3

COGNITO_CLIENT_ID = "5eiror37ph4chhlm1a85sqk0cg"
COGNITO_REGION = "us-east-2"

client = boto3.client("cognito-idp", region_name=COGNITO_REGION)

def login_user(username: str, password: str, new_password: str = None):
    """
    Inicia sesión en Cognito. Si el usuario tiene contraseña temporal,
    Cognito devuelve el challenge NEW_PASSWORD_REQUIRED y se responde con la nueva contraseña.
    """
    try:
        resp = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password
            },
            ClientId=COGNITO_CLIENT_ID
        )

        # Caso: Cognito exige cambio de contraseña
        if resp.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
            if not new_password:
                raise HTTPException(
                    status_code=400,
                    detail="Nueva contraseña requerida"
                )
            resp2 = client.respond_to_auth_challenge(
                ClientId=COGNITO_CLIENT_ID,
                ChallengeName="NEW_PASSWORD_REQUIRED",
                Session=resp["Session"],
                ChallengeResponses={
                    "USERNAME": username,
                    "NEW_PASSWORD": new_password
                }
            )
            return resp2["AuthenticationResult"]

        # Login normal
        return resp["AuthenticationResult"]

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error en login: {str(e)}")


def logout():
    """
    El logout real se hace en frontend (revocar tokens en Cognito).
    Aquí devolvemos un estado simple.
    """
    return {"status": "ok", "message": "Sesión cerrada"}
