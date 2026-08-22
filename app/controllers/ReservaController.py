from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.Session import get_db
from app.middleware.Authentication import get_current_user
from app.middleware.Authorizacion import require_client
from app.repositories.RolRepository import RolRepository
from app.schemas.reserva.ReservaCreate import ReservaCreate
from app.schemas.reserva.ReservaUpdate import ReservaUpdate
from app.schemas.reserva.ReservaResponse import ReservaResponse
from app.services.ReservaService import ReservaService
router=APIRouter(prefix='/reservas',tags=['Reservas'])
@router.get('/',response_model=List[ReservaResponse])
def listar_reservas(db:Session=Depends(get_db)): return ReservaService(db).listar_reservas()
@router.get('/activas',response_model=List[ReservaResponse])
def listar_reservas_activas(db:Session=Depends(get_db)): return ReservaService(db).listar_reservas_activas()
@router.get('/cliente/{idCliente}',response_model=List[ReservaResponse])
def listar_reservas_por_cliente(idCliente:int,usuario=Depends(get_current_user),db:Session=Depends(get_db)):
    rol=RolRepository(db).obtener_por_id(usuario.idRol)
    if rol and rol.nombreRol=='CLIENTE' and usuario.idCliente!=idCliente: raise HTTPException(403,'Solo puede consultar sus propias reservas.')
    try:return ReservaService(db).listar_reservas_por_cliente(idCliente)
    except ValueError as error:raise HTTPException(404,detail=str(error))
@router.get('/{idReserva}',response_model=ReservaResponse)
def obtener_reserva(idReserva:int,db:Session=Depends(get_db)):
    try:return ReservaService(db).obtener_reserva(idReserva)
    except ValueError as error:raise HTTPException(404,detail=str(error))
@router.post('/',response_model=ReservaResponse,status_code=201)
def crear_reserva(datos:ReservaCreate,usuario=Depends(require_client),db:Session=Depends(get_db)):
    if datos.idCliente!=usuario.idCliente: raise HTTPException(403,'La reserva debe pertenecer al cliente autenticado.')
    try:return ReservaService(db).crear_reserva(datos)
    except ValueError as error:raise HTTPException(400,detail=str(error))
@router.put('/{idReserva}',response_model=ReservaResponse)
def actualizar_reserva(idReserva:int,datos:ReservaUpdate,db:Session=Depends(get_db)):
    try:return ReservaService(db).actualizar_reserva(idReserva,datos)
    except ValueError as error:raise HTTPException(400,detail=str(error))
@router.put('/{idReserva}/cancelar',response_model=ReservaResponse)
def cancelar_reserva(idReserva:int,db:Session=Depends(get_db)):
    try:return ReservaService(db).cancelar_reserva(idReserva)
    except ValueError as error:raise HTTPException(400,detail=str(error))
@router.delete('/{idReserva}',response_model=ReservaResponse)
def eliminar_reserva(idReserva:int,db:Session=Depends(get_db)):
    try:return ReservaService(db).cancelar_reserva(idReserva)
    except ValueError as error:raise HTTPException(400,detail=str(error))
