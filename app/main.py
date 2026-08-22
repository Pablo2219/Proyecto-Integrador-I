from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.ClienteController import router as cliente_router
from app.controllers.VehiculoController import router as vehiculo_router
from app.controllers.EspacioController import router as espacio_router
from app.controllers.ReservaController import router as reserva_router
from app.controllers.QrController import router as qr_router
from app.controllers.OcupacionController import router as ocupacion_router
from app.controllers.PagoController import router as pago_router
from app.controllers.DeudaController import router as deuda_router
from app.controllers.NotificacionController import router as notificacion_router
from app.controllers.AuthController import router as auth_router
from app.controllers.UsuarioController import router as usuario_router
from app.controllers.ProveedorController import router as proveedor_router
app=FastAPI(title='ParkSmart API',version='2.1.0',description='API REST ParkSmart con cuentas, proveedores, mapa y reservas por rol')
app.add_middleware(CORSMiddleware,allow_origins=['http://127.0.0.1:5500','http://localhost:5500','http://127.0.0.1:8000','http://localhost:8000'],allow_origin_regex=r'http://(localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+):\d+',allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(auth_router);app.include_router(usuario_router);app.include_router(cliente_router);app.include_router(vehiculo_router);app.include_router(espacio_router);app.include_router(reserva_router);app.include_router(qr_router);app.include_router(ocupacion_router);app.include_router(pago_router);app.include_router(deuda_router);app.include_router(notificacion_router);app.include_router(proveedor_router)
@app.get('/')
def inicio():return {'mensaje':'ParkSmart API en línea','version':'2.1.0','documentacion':'/docs'}
