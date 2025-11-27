"""
API de Empleados - Endpoints para gestión de empleados
"""

from typing import List
from uuid import UUID

from crud.empleadoCRUD import EmpleadoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import (
    EmpleadoCreate,
    EmpleadoUpdate,
    EmpleadoResponse,
    RespuestaAPI,
)
from auth.deps import get_current_user

router = APIRouter(
    prefix="/Empleados", tags=["Empleados"], dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=List[EmpleadoResponse])
async def obtener_empleados(
    skip: int = 0,
    limit: int = 100,
    solo_activos: bool = False,
    db: Session = Depends(get_db),
):
    """Obtener todos los empleados"""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleados = empleado_crud.obtener_empleados(
            skip=skip, limit=limit, solo_activos=solo_activos
        )
        return empleados
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los empleados: {str(e)}",
        )


@router.get("/{empleado_id}", response_model=EmpleadoResponse)
async def obtener_empleado(empleado_id: UUID, db: Session = Depends(get_db)):
    """Obtener un empleado por su ID."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.obtener_empleado(empleado_id)
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )
        return empleado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleado: {str(e)}",
        )


@router.post("/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
async def crear_empleado(empleado_data: EmpleadoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo empleado."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado = empleado_crud.crear_empleado(
            nombre=empleado_data.nombre,
            email=empleado_data.email,
            rol=empleado_data.rol,
            activo=empleado_data.activo,
            id_usuario_creacion=empleado_data.id_usuario_creacion,
        )
        return empleado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el empleado: {str(e)}",
        )


@router.put("/{empleado_id}", response_model=EmpleadoResponse)
async def actualizar_empleado(
    empleado_id: UUID, empleado_data: EmpleadoUpdate, db: Session = Depends(get_db)
):
    """Actualizar un empleado existente."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado_existente = empleado_crud.obtener_empleado(empleado_id)

        if not empleado_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )

        campos_actualizacion = {
            k: v for k, v in empleado_data.model_dump().items() if v is not None
        }

        if not campos_actualizacion:
            return empleado_existente

        empleado_actualizado = empleado_crud.actualizar_empleado(
            empleado_id,
            **campos_actualizacion,
        )
        return empleado_actualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar empleado: {str(e)}",
        )


@router.delete("/{empleado_id}", response_model=RespuestaAPI)
async def eliminar_empleado(empleado_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un empleado por ID."""
    try:
        empleado_crud = EmpleadoCRUD(db)
        empleado_existente = empleado_crud.obtener_empleado(empleado_id)

        if not empleado_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado",
            )

        eliminado = empleado_crud.eliminar_empleado(empleado_id)
        if eliminado:
            return RespuestaAPI(mensaje="Empleado eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el empleado",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar empleado: {str(e)}",
        )
