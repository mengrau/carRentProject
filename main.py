import uvicorn
from Apis import (
    cliente,
    contrato,
    empleado,
    pago,
    tipoVehiculo,
    usuario,
    vehiculo,
    dashboard,
)
from database.config import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router

app = FastAPI(
    title="Sistema de Renta de Vehiculos",
    description="API REST para gestión de usuarios, clientes y vehiculos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(cliente.router)
app.include_router(contrato.router)
app.include_router(empleado.router)
app.include_router(pago.router)
app.include_router(tipoVehiculo.router)
app.include_router(usuario.router)
app.include_router(vehiculo.router)
app.include_router(dashboard.router)


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
            "Auth": "/auth",
            "Clientes": "/cliente",
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
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
