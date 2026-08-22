from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.middleware.Authentication import get_current_user
from app.schemas.auth.AuthResponse import AuthResponse
from app.schemas.auth.LoginRequest import LoginRequest
from app.schemas.auth.PasswordChangeRequest import PasswordChangeRequest
from app.schemas.auth.PasswordRecoveryRequest import PasswordRecoveryRequest
from app.schemas.auth.PasswordRecoveryResponse import PasswordRecoveryResponse
from app.schemas.auth.PasswordResetRequest import PasswordResetRequest
from app.schemas.usuario.UsuarioResponse import UsuarioResponse
from app.services.AuthService import AuthService


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=AuthResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    try:
        return AuthService(db).login(datos.usuario, datos.contrasena)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))


@router.get("/me", response_model=UsuarioResponse)
def mi_cuenta(usuario=Depends(get_current_user), db: Session = Depends(get_db)):
    return AuthService(db).usuario_response(usuario)


@router.post("/solicitar-restablecimiento", response_model=PasswordRecoveryResponse)
def solicitar_restablecimiento(datos: PasswordRecoveryRequest, db: Session = Depends(get_db)):
    try:
        return AuthService(db).solicitar_restauracion(datos)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/restablecer-contrasena")
def restablecer_contrasena(datos: PasswordResetRequest, db: Session = Depends(get_db)):
    try:
        return AuthService(db).restablecer(datos)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.put("/cambiar-contrasena")
def cambiar_contrasena(
    datos: PasswordChangeRequest,
    usuario=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return AuthService(db).cambiar_contrasena(usuario, datos)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/logout")
def logout():
    return {"mensaje": "Sesión cerrada. El token debe eliminarse del cliente."}
