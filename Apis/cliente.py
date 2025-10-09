"""
API de Categorías - Endpoints para gestión de categorías
"""

from typing import List
from uuid import UUID

from crud.clienteCRUD import ClienteCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import ClienteCreate, ClienteResponse, ClienteUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/Clientes", tags=["Clientes"])


@router.get("/", response_model=List[ClienteResponse])
async def obtener_clientes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los clientes"""
    try:
        Cliente_CRUD = ClienteCRUD(db)
        clientes = Cliente_CRUD.obtener_clientes(skip=skip, limit=limit)
        return clientes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los clientes: {str(e)}",
        )


@router.get("/{clientes_id}", response_model=ClienteResponse)
async def obtener_cliente(clientes_id: UUID, db: Session = Depends(get_db)):
    """Obtener un cliente por ID."""
    try:
        Cliente_CRUD = ClienteCRUD(db)
        cliente = Cliente_CRUD.obtener_cliente(clientes_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.get("/email/{email}", response_model=ClienteResponse)
async def obtener_cliente_por_email(email: str, db: Session = Depends(get_db)):
    """Obtener un cliente por email."""
    try:
        Cliente_CRUD = ClienteCRUD(db)
        cliente = Cliente_CRUD.obtener_cliente_por_email(email)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cliente."""
    try:
        Cliente_CRUD = ClienteCRUD(db)
        cliente = Cliente_CRUD.crear_cliente(
            nombre=cliente_data.nombre,
            email=cliente_data.email,
            telefono=cliente_data.telefono,
            id_usuario_creacion=cliente_data.id_usuario_creacion,
        )
        return cliente
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el cliente: {str(e)}",
        )


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(
    cliente_id: UUID, cliente_data: ClienteUpdate, db: Session = Depends(get_db)
):
    """Actualizar un cliente existente."""
    try:
        Cliente_CRUD = ClienteCRUD(db)

        # Verificar que la categoría existe
        cliente_existente = Cliente_CRUD.obtener_cliente(cliente_id)
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in cliente_data.model_dump().items() if v is not None
        }

        if not campos_actualizacion:
            return cliente_existente

        cliente_actualizado = Cliente_CRUD.actualizar_cliente(
            cliente_id, **campos_actualizacion
        )
        return cliente_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}",
        )


@router.delete("/{cliente_id}", response_model=RespuestaAPI)
async def eliminar_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un cliente."""
    try:
        Cliente_CRUD = ClienteCRUD(db)

        # Verificar que el cliente existe
        cliente_existente = Cliente_CRUD.obtener_cliente(cliente_id)
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        eliminado = Cliente_CRUD.eliminar_cliente(cliente_id)
        if eliminado:
            return RespuestaAPI(mensaje="Cliente eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el cliente",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}",
        )
