from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from models import Token, LoginRequest
from auth.utils import create_access_token, decode_token
from database.config import get_db  # ajusta si tu módulo de db está en otra ruta
from crud.usuarioCRUD import UsuarioCRUD  # ruta según tu proyecto
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    usuario = crud.autenticar_usuario(login_data.username, login_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # payload mínimo: sub = id del usuario
    access_token = create_access_token({"sub": str(usuario.id)})
    logger.debug("Usuario autenticado: %s", usuario.id)
    return {
    "access_token": access_token,
    "token_type": "bearer",
    "user_id": str(usuario.id)  # 👈 agregas el ID del usuario autenticado
}