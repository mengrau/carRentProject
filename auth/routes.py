from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from models import Token, LoginRequest
from auth.utils import create_access_token, decode_token
from database.config import get_db
from crud.usuarioCRUD import UsuarioCRUD 
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])


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

    access_token = create_access_token({"sub": str(usuario.id)})
    logger.debug("Usuario autenticado: %s", usuario.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(usuario.id), 
    }
