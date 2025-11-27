from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.auth.logic import login_user, logout

router = APIRouter(prefix="/api", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str
    new_password: str | None = None

@router.post("/login")
def login_route(data: LoginRequest):
    try:
        result = login_user(data.username, data.password, data.new_password)
        return {
            "access_token": result["AccessToken"],
            "id_token": result["IdToken"],
            "refresh_token": result["RefreshToken"],
            "token_type": result["TokenType"],
            "expires_in": result["ExpiresIn"]
        }
    except HTTPException as e:
        raise e

@router.post("/logout")
def logout_route():
    return logout()
