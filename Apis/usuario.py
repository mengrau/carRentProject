"""
API de Usuarios - Endpoints para gestión de usuarios (usa modelos Pydantic)
"""

from typing import List
from uuid import UUID

from crud.usuarioCRUD import UsuarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
    UsuarioLogin,  # opcional para login si tienes ese modelo
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/Usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
async def obtener_usuarios(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    """Obtener todos los usuarios (sin paginar por ahora, pero con skip/limit)."""
    try:
        crud = UsuarioCRUD(db)
        usuarios = crud.obtener_usuarios()
        # Si quisieras aplicar skip/limit en DB: cambiaría por query con offset/limit
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los usuarios: {str(e)}",
        )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Obtener un usuario por su ID."""
    try:
        crud = UsuarioCRUD(db)
        usuario = crud.obtener_usuario_por_id(str(usuario_id))
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el usuario: {str(e)}",
        )


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario (la contraseña se encripta en el CRUD)."""
    try:
        crud = UsuarioCRUD(db)
        # Validar que no exista username
        if crud.obtener_usuario_por_username(usuario_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya existe",
            )

        usuario = crud.crear_usuario(
            username=usuario_data.username,
            password=usuario_data.password,
            id_usuario_creacion=usuario_data.id_usuario_creacion,
            rol=usuario_data.rol,
            estado=usuario_data.estado,
        )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}",
        )


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: UUID, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)
):
    """Actualizar un usuario existente."""
    try:
        crud = UsuarioCRUD(db)
        usuario_existente = crud.obtener_usuario_por_id(str(usuario_id))
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        # Obtener diccionario y filtrar None (Pydantic v2 -> model_dump)
        campos = {k: v for k, v in usuario_data.model_dump().items() if v is not None}

        # Se espera que usuario_data incluya id_usuario_edicion (igual que en otros routers)
        id_usuario_edicion = campos.pop("id_usuario_edicion", None)
        if id_usuario_edicion is None:
            # Si prefieres exigirlo, lanza un 400; aquí lo dejamos como required por convención
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id_usuario_edicion es requerido para la actualización",
            )

        if not campos:
            return usuario_existente

        usuario_actualizado = crud.actualizar_usuario(
            str(usuario_id),
            id_usuario_edicion=id_usuario_edicion,
            **campos,
        )
        return usuario_actualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el usuario: {str(e)}",
        )


@router.delete("/{usuario_id}", response_model=RespuestaAPI)
async def eliminar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un usuario por su ID."""
    try:
        crud = UsuarioCRUD(db)
        eliminado = crud.eliminar_usuario(str(usuario_id))
        if eliminado:
            return RespuestaAPI(mensaje="Usuario eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el usuario: {str(e)}",
        )


@router.post("/login", response_model=UsuarioResponse)
async def autenticar_usuario(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    """
    Autenticar usuario.
    """
    try:
        crud = UsuarioCRUD(db)
        usuario = crud.autenticar_usuario(login_data.username, login_data.password)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas o usuario inactivo",
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al autenticar: {str(e)}",
        )


@router.put(
    "/{usuario_id}/cambiar-password",
    status_code=status.HTTP_200_OK,
    response_model=RespuestaAPI,
)
async def cambiar_contrasena(
    usuario_id: UUID,
    current_password: str,
    new_password: str,
    db: Session = Depends(get_db),
):
    """Cambiar contraseña de un usuario."""
    try:
        crud = UsuarioCRUD(db)
        cambiado = crud.cambiar_contrasena(
            str(usuario_id), current_password, new_password
        )
        if not cambiado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta o usuario no encontrado",
            )
        return RespuestaAPI(mensaje="Contraseña actualizada correctamente", exito=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cambiar la contraseña: {str(e)}",
        )
