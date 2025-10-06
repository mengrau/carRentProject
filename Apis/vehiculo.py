"""
API de Vehículos - Endpoints para la gestión de vehículos
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.vehiculoCRUD import VehiculoCRUD
from database.config import get_db
from models import VehiculoCreate, VehiculoUpdate, VehiculoResponse, RespuestaAPI

router = APIRouter(prefix="/vehiculos", tags=["vehiculos"])


@router.get("/", response_model=List[VehiculoResponse])
async def obtener_vehiculos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los vehículos con paginación
    """
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculos = vehiculo_crud.obtener_vehiculos(skip=skip, limit=limit)
        return vehiculos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los vehículos: {str(e)}",
        )


@router.get("/{vehiculo_id}", response_model=VehiculoResponse)
async def obtener_vehiculo(vehiculo_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un vehículo por su ID
    """
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculo = vehiculo_crud.obtener_vehiculo(vehiculo_id)
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return vehiculo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el vehículo: {str(e)}"
        )


@router.post("/", response_model=VehiculoResponse, status_code=status.HTTP_201_CREATED)
async def crear_vehiculo(vehiculo_data: VehiculoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo vehículo con validaciones
    """
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculo = vehiculo_crud.crear_vehiculo(
            marca=vehiculo_data.marca,
            modelo=vehiculo_data.modelo,
            tipo_id=vehiculo_data.tipo_id,
            id_usuario_creacion=vehiculo_data.id_usuario_creacion,
            placa=vehiculo_data.placa,
            disponible=vehiculo_data.disponible,
        )
        return vehiculo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear el vehículo: {str(e)}"
        )


@router.put("/{vehiculo_id}", response_model=VehiculoResponse)
async def actualizar_vehiculo(
    vehiculo_id: UUID, vehiculo_data: VehiculoUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar los datos de un vehículo existente
    """
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculo_existente = vehiculo_crud.obtener_vehiculo(vehiculo_id)

        if not vehiculo_existente:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        campos_actualizacion = {
            k: v for k, v in vehiculo_data.model_dump().items() if v is not None
        }

        if not campos_actualizacion:
            return vehiculo_existente

        vehiculo_actualizado = vehiculo_crud.actualizar_vehiculo(
            vehiculo_id,
            id_usuario_edicion=vehiculo_data.id_usuario_edicion,
            **campos_actualizacion,
        )
        return vehiculo_actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar vehículo: {str(e)}"
        )


@router.delete("/{vehiculo_id}", response_model=RespuestaAPI)
async def eliminar_vehiculo(vehiculo_id: UUID, db: Session = Depends(get_db)):
    """
    Eliminar un vehículo por su ID
    """
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculo = vehiculo_crud.obtener_vehiculo(vehiculo_id)
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        eliminado = vehiculo_crud.eliminar_vehiculo(vehiculo_id)
        if eliminado:
            return RespuestaAPI(mensaje="Vehículo eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=500, detail="No se pudo eliminar el vehículo"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar el vehículo: {str(e)}"
        )
