from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config.Security import TokenError, decode_token
from app.database.Session import get_db
from app.repositories.UsuarioRepository import UsuarioRepository


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debe iniciar sesión.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(credentials.credentials, "access")
        usuario = UsuarioRepository(db).obtener_por_id(int(payload["sub"]))
    except (TokenError, ValueError, KeyError):
        usuario = None
    if usuario is None or usuario.estado != "ACTIVO":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión no es válida o expiró.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario
