import uvicorn
from Apis import cliente, contrato, empleado, pago, tipoVehiculo, usuario, vehiculo
from database.config import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI(
    title="Sistema de Renta de Vehiculos",
    description="API REST para gestión de usuarios, clientes y vehiculos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers de las APIs
app.include_router(cliente.router)
app.include_router(contrato.router)
app.include_router(empleado.router)
app.include_router(pago.router)
app.include_router(tipoVehiculo.router)
app.include_router(usuario.router)
app.include_router(vehiculo.router)


@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print("Iniciando Sistema de renta de vehiculos...")
    print("Configurando base de datos...")
    create_tables()
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:8000/docs")


@app.get("/", tags=["raíz"])
async def root():
    """Endpoint raíz que devuelve información básica de la API."""
    return {
        "mensaje": "Bienvenido al Sistema de Gestión de Productos",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "clientes": "/cliente",
            "contratos": "/contrato",
            "empleado": "/empleados",
            "pago": "/pago",
            "tipoVehiculo": "/tipo de vehiculos",
            "usuario": "/usuarios",
            "vehiculo": "/vehiculos",
        },
    }


def main():
    """Función principal para ejecutar el servidor"""
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Recargar automáticamente en desarrollo
        log_level="info",
    )


if __name__ == "__main__":
    main()
