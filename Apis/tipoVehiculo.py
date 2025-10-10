"""
API - Gestión de Tipos de Vehículo
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database.config import get_db
from crud.tipoVehiculoCRUD import TipoVehiculoCRUD
from models import (
    TipoVehiculoCreate,
    TipoVehiculoUpdate,
    TipoVehiculoResponse,
    RespuestaAPI,
)

router = APIRouter(prefix="/Tipos-de-Vehiculos", tags=["Tipos de Vehiculos"])


@router.post(
    "/", response_model=TipoVehiculoResponse, status_code=status.HTTP_201_CREATED
)
def crear_tipo_vehiculo(tipo_data: TipoVehiculoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo tipo de vehículo
    """
    crud = TipoVehiculoCRUD(db)
    try:
        nuevo_tipo = crud.crear_tipo_vehiculo(
            nombre=tipo_data.nombre,
            id_usuario_creacion=tipo_data.id_usuario_creacion,
            descripcion=tipo_data.descripcion,
            activo=tipo_data.activo,
        )
        return nuevo_tipo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear tipo de vehículo: {str(e)}"
        )


@router.get("/", response_model=List[TipoVehiculoResponse])
def listar_tipos_vehiculo(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener lista de tipos de vehículo con paginación
    """
    crud = TipoVehiculoCRUD(db)
    try:
        return crud.obtener_tipos_vehiculo(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al listar tipos de vehículo: {str(e)}"
        )


@router.get("/{tipo_id}", response_model=TipoVehiculoResponse)
def obtener_tipo_vehiculo(tipo_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un tipo de vehículo por su ID
    """
    crud = TipoVehiculoCRUD(db)
    try:
        tipo = crud.obtener_tipo_vehiculo(tipo_id)
        if not tipo:
            raise HTTPException(
                status_code=404, detail="Tipo de vehículo no encontrado"
            )
        return tipo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener tipo de vehículo: {str(e)}"
        )


@router.put("/{tipo_id}", response_model=TipoVehiculoResponse)
def actualizar_tipo_vehiculo(
    tipo_id: UUID, tipo_data: TipoVehiculoUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar un tipo de vehículo existente
    """
    crud = TipoVehiculoCRUD(db)
    try:

        tipo_existente = crud.obtener_tipo_vehiculo(tipo_id)
        if not tipo_existente:
            raise HTTPException(
                status_code=404, detail="Tipo de vehículo no encontrado"
            )

        campos_actualizados = {
            k: v for k, v in tipo_data.model_dump().items() if v is not None
        }

        tipo_actualizado = crud.actualizar_tipo_vehiculo(
            tipo_id,
            **campos_actualizados,
        )

        return tipo_actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar tipo de vehículo: {str(e)}"
        )


@router.delete("/{tipo_id}", response_model=RespuestaAPI)
def eliminar_tipo_vehiculo(tipo_id: UUID, db: Session = Depends(get_db)):
    """
    Eliminar un tipo de vehículo
    """
    crud = TipoVehiculoCRUD(db)
    try:
        eliminado = crud.eliminar_tipo_vehiculo(tipo_id)
        if not eliminado:
            raise HTTPException(
                status_code=404, detail="Tipo de vehículo no encontrado"
            )

        return RespuestaAPI(
            mensaje="Tipo de vehículo eliminado exitosamente", exito=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar tipo de vehículo: {str(e)}"
        )
