"""
API de Contratos - Endpoints para gestión de contratos
"""

from typing import List
from uuid import UUID
from datetime import datetime

from crud.contratoCRUD import ContratoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import (
    ContratoCreate,
    ContratoResponse,
    ContratoUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/Contratos", tags=["Contratos"])


@router.get("/", response_model=List[ContratoResponse])
async def obtener_contratos(
    skip: int = 0,
    limit: int = 100,
    solo_activos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todos los contratos"""
    try:
        contrato_crud = ContratoCRUD(db)
        contratos = contrato_crud.obtener_contratos(
            skip=skip, limit=limit, solo_activos=solo_activos
        )
        return contratos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los contratos: {str(e)}",
        )


@router.get("/{contrato_id}", response_model=ContratoResponse)
async def obtener_contrato(contrato_id: UUID, db: Session = Depends(get_db)):
    """Obtener un contrato por ID."""
    try:
        contrato_crud = ContratoCRUD(db)
        contrato = contrato_crud.obtener_contrato(contrato_id)
        if not contrato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contrato no encontrado",
            )
        return contrato
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener contrato: {str(e)}",
        )


@router.post("/", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
async def crear_contrato(contrato_data: ContratoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo contrato."""
    try:
        contrato_crud = ContratoCRUD(db)
        contrato = contrato_crud.crear_contrato(
            cliente_id=contrato_data.cliente_id,
            vehiculo_id=contrato_data.vehiculo_id,
            empleado_id=contrato_data.empleado_id,
            id_usuario_creacion=contrato_data.id_usuario_creacion,
            fecha_inicio=contrato_data.fecha_inicio,
            fecha_fin=contrato_data.fecha_fin,
        )
        return contrato
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el contrato: {str(e)}",
        )


@router.put("/{contrato_id}", response_model=ContratoResponse)
async def actualizar_contrato(
    contrato_id: UUID, contrato_data: ContratoUpdate, db: Session = Depends(get_db)
):
    """Actualizar un contrato existente."""
    try:
        contrato_crud = ContratoCRUD(db)

        contrato_existente = contrato_crud.obtener_contrato(contrato_id)
        if not contrato_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contrato no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in contrato_data.model_dump().items() if v is not None
        }

        if not campos_actualizacion:
            return contrato_existente

        contrato_actualizado = contrato_crud.actualizar_contrato(
            contrato_id,
            id_usuario_edicion=contrato_data.id_usuario_edicion,
            **campos_actualizacion,
        )
        return contrato_actualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar contrato: {str(e)}",
        )


@router.delete("/{contrato_id}", response_model=RespuestaAPI)
async def eliminar_contrato(contrato_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un contrato y marcar el vehículo como disponible."""
    try:
        contrato_crud = ContratoCRUD(db)

        contrato_existente = contrato_crud.obtener_contrato(contrato_id)
        if not contrato_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contrato no encontrado",
            )

        eliminado = contrato_crud.eliminar_contrato(contrato_id)
        if eliminado:
            return RespuestaAPI(mensaje="Contrato eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el contrato",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar contrato: {str(e)}",
        )
