from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from backend.auth.logic import login, logout

router = APIRouter(prefix="/api", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
def login_route(token: str = Depends(oauth2_scheme)):
    try:
        return login(token)
    except HTTPException as e:
        raise e

@router.post("/logout")
def logout_route():
    return logout()
