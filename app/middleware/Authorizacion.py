from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.Session import get_db
from app.middleware.Authentication import get_current_user
from app.repositories.RolRepository import RolRepository

def _require_role(allowed, usuario, db):
    rol = RolRepository(db).obtener_por_id(usuario.idRol)
    if rol is None or rol.nombreRol not in allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para realizar esta operación.")
    return usuario

def require_admin(usuario=Depends(get_current_user), db: Session = Depends(get_db)):
    return _require_role({"ADMINISTRADOR"}, usuario, db)

def require_provider(usuario=Depends(get_current_user), db: Session = Depends(get_db)):
    return _require_role({"PROVEEDOR"}, usuario, db)
