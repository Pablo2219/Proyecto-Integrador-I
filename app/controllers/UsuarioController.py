from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.middleware.Authorizacion import require_admin
from app.schemas.usuario.UsuarioCreate import UsuarioCreate
from app.schemas.usuario.UsuarioResponse import UsuarioResponse
from app.schemas.usuario.UsuarioUpdate import UsuarioUpdate
from app.services.UsuarioService import UsuarioService


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios y roles"],
    dependencies=[Depends(require_admin)],
)


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return UsuarioService(db).listar_usuarios()


@router.get("/{idUsuario}", response_model=UsuarioResponse)
def obtener_usuario(idUsuario: int, db: Session = Depends(get_db)):
    try:
        return UsuarioService(db).obtener_usuario(idUsuario)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return UsuarioService(db).crear_usuario(datos)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.put("/{idUsuario}", response_model=UsuarioResponse)
def actualizar_usuario(idUsuario: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        return UsuarioService(db).actualizar_usuario(idUsuario, datos)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.delete("/{idUsuario}", response_model=UsuarioResponse)
def eliminar_usuario(idUsuario: int, db: Session = Depends(get_db)):
    try:
        return UsuarioService(db).eliminar_usuario(idUsuario)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
