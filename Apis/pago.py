"""
API de Pagos - Endpoints para gestión de pagos
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.pagoCRUD import PagoCRUD
from database.config import get_db
from models import PagoCreate, PagoUpdate, PagoResponse, RespuestaAPI

router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("/", response_model=List[PagoResponse])
async def obtener_pagos(
    skip: int = 0,
    limit: int = 100,
    contrato_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
):
    """Obtener todos los pagos con paginación y filtro por contrato."""
    try:
        pago_crud = PagoCRUD(db)
        pagos = pago_crud.obtener_pagos(skip=skip, limit=limit, contrato_id=contrato_id)
        return pagos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los pagos: {str(e)}",
        )


@router.get("/{pago_id}", response_model=PagoResponse)
async def obtener_pago(pago_id: UUID, db: Session = Depends(get_db)):
    """Obtener un pago por su ID."""
    try:
        pago_crud = PagoCRUD(db)
        pago = pago_crud.obtener_pago(pago_id)
        if not pago:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado",
            )
        return pago
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el pago: {str(e)}",
        )


@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
async def crear_pago(pago_data: PagoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo pago."""
    try:
        pago_crud = PagoCRUD(db)
        pago = pago_crud.crear_pago(
            contrato_id=pago_data.contrato_id,
            monto=pago_data.monto,
            id_usuario_creacion=pago_data.id_usuario_creacion,
            fecha_pago=pago_data.fecha_pago,
        )
        return pago
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el pago: {str(e)}",
        )


@router.put("/{pago_id}", response_model=PagoResponse)
async def actualizar_pago(
    pago_id: UUID, pago_data: PagoUpdate, db: Session = Depends(get_db)
):
    """Actualizar un pago existente."""
    try:
        pago_crud = PagoCRUD(db)
        pago_existente = pago_crud.obtener_pago(pago_id)

        if not pago_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in pago_data.model_dump().items() if v is not None
        }

        if not campos_actualizacion:
            return pago_existente

        pago_actualizado = pago_crud.actualizar_pago(
            pago_id,
            id_usuario_edicion=pago_data.id_usuario_edicion,
            **campos_actualizacion,
        )
        return pago_actualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el pago: {str(e)}",
        )


@router.delete("/{pago_id}", response_model=RespuestaAPI)
async def eliminar_pago(pago_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un pago por ID."""
    try:
        pago_crud = PagoCRUD(db)
        pago_existente = pago_crud.obtener_pago(pago_id)

        if not pago_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado",
            )

        eliminado = pago_crud.eliminar_pago(pago_id)
        if eliminado:
            return RespuestaAPI(mensaje="Pago eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el pago",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el pago: {str(e)}",
        )
