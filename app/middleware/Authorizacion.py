from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.middleware.Authentication import get_current_user
from app.repositories.RolRepository import RolRepository


def require_admin(usuario=Depends(get_current_user), db: Session = Depends(get_db)):
    rol = RolRepository(db).obtener_por_id(usuario.idRol)
    if rol is None or rol.nombreRol != "ADMINISTRADOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta operación requiere el rol ADMINISTRADOR.",
        )
    return usuario
