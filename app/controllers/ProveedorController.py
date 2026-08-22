from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.Session import get_db
from app.middleware.Authentication import get_current_user
from app.middleware.Authorizacion import require_provider
from app.schemas.proveedor.SectorCreate import SectorCreate
from app.schemas.proveedor.EspacioProveedorCreate import EspacioProveedorCreate

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

@router.get("/mapa")
def mapa_publico(db: Session = Depends(get_db)):
    sectores = db.execute(text("SELECT idSector,nombreSector,descripcion,latitud,longitud,precioHora FROM Sector WHERE estado='ACTIVO' AND latitud IS NOT NULL AND longitud IS NOT NULL" )).mappings().all()
    espacios = db.execute(text("SELECT e.idEspacio,e.idSector,e.codigoEspacio,e.tipoEspacio,e.estado,e.latitud,e.longitud,s.nombreSector,s.precioHora FROM Espacio e JOIN Sector s ON s.idSector=e.idSector WHERE e.estado IN ('DISPONIBLE','RESERVADO') AND e.latitud IS NOT NULL AND e.longitud IS NOT NULL" )).mappings().all()
    return {"sectores":[dict(x) for x in sectores],"espacios":[dict(x) for x in espacios]}

@router.post("/sectores", status_code=status.HTTP_201_CREATED)
def crear_sector(datos: SectorCreate, usuario=Depends(require_provider), db: Session=Depends(get_db)):
    try:
        proveedor = db.execute(text("SELECT idProveedor FROM Proveedor WHERE idUsuario=:uid AND estado='ACTIVO'"), {"uid":usuario.idUsuario}).scalar()
        if not proveedor: raise HTTPException(403, "El proveedor no está habilitado.")
        existente = db.execute(text("SELECT idSector FROM Sector WHERE nombreSector=:n"), {"n":datos.nombreSector.strip()}).scalar()
        if existente: raise HTTPException(409, "Ya existe un sector con ese nombre.")
        result = db.execute(text("INSERT INTO Sector (idProveedor,nombreSector,descripcion,ubicacion,latitud,longitud,precioHora,estado) VALUES (:p,:n,:d,:u,:lat,:lng,:price,'ACTIVO')"), {"p":proveedor,"n":datos.nombreSector.strip(),"d":datos.descripcion,"u":f"{datos.latitud},{datos.longitud}","lat":datos.latitud,"lng":datos.longitud,"price":datos.precioHora})
        db.commit()
        return {"idSector": result.lastrowid, **datos.model_dump()}
    except HTTPException: raise
    except Exception as e:
        db.rollback(); raise HTTPException(400, f"No se pudo crear el sector: {e}")

@router.get("/sectores/mis-sectores")
def mis_sectores(usuario=Depends(require_provider), db: Session=Depends(get_db)):
    rows=db.execute(text("SELECT s.* FROM Sector s JOIN Proveedor p ON p.idProveedor=s.idProveedor WHERE p.idUsuario=:uid ORDER BY s.idSector DESC"),{"uid":usuario.idUsuario}).mappings().all()
    return [dict(r) for r in rows]

@router.post("/espacios", status_code=status.HTTP_201_CREATED)
def crear_espacio(datos: EspacioProveedorCreate, usuario=Depends(require_provider), db: Session=Depends(get_db)):
    proveedor=db.execute(text("SELECT idProveedor FROM Proveedor WHERE idUsuario=:uid AND estado='ACTIVO'"),{"uid":usuario.idUsuario}).scalar()
    if not proveedor: raise HTTPException(403,"Proveedor no habilitado.")
    owner=db.execute(text("SELECT idSector FROM Sector WHERE idSector=:sid AND idProveedor=:pid"),{"sid":datos.idSector,"pid":proveedor}).scalar()
    if not owner: raise HTTPException(403,"El sector no pertenece a este proveedor.")
    dup=db.execute(text("SELECT idEspacio FROM Espacio WHERE codigoEspacio=:c"),{"c":datos.codigoEspacio.strip()}).scalar()
    if dup: raise HTTPException(409,"El código del espacio ya existe.")
    try:
        result=db.execute(text("INSERT INTO Espacio (idSector,codigoEspacio,tipoEspacio,estado,descripcion,latitud,longitud) VALUES (:s,:c,:t,'DISPONIBLE',:d,:lat,:lng)"),datos.model_dump() | {"s":datos.idSector,"c":datos.codigoEspacio.strip(),"t":datos.tipoEspacio,"d":datos.descripcion,"lat":datos.latitud,"lng":datos.longitud})
        db.commit(); return {"idEspacio":result.lastrowid,**datos.model_dump(),"estado":"DISPONIBLE"}
    except Exception as e:
        db.rollback(); raise HTTPException(400,f"No se pudo crear el espacio: {e}")

@router.get("/reservas")
def reservas_proveedor(usuario=Depends(require_provider), db: Session=Depends(get_db)):
    rows=db.execute(text("""SELECT r.idReserva,r.codigoReserva,r.fechaInicioReserva,r.fechaFinReserva,r.estado,
        c.idCliente,c.nombre,c.primerApellido,e.idEspacio,e.codigoEspacio,s.idSector,s.nombreSector
        FROM Reserva r JOIN Cliente c ON c.idCliente=r.idCliente JOIN Espacio e ON e.idEspacio=r.idEspacio
        JOIN Sector s ON s.idSector=e.idSector JOIN Proveedor p ON p.idProveedor=s.idProveedor
        WHERE p.idUsuario=:uid ORDER BY r.fechaInicioReserva DESC"""),{"uid":usuario.idUsuario}).mappings().all()
    return [dict(r) for r in rows]
