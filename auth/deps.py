from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from uuid import UUID
from .utils import decode_token
from database.config import get_db
from crud.usuarioCRUD import UsuarioCRUD
from fastapi import Header


def get_current_user(
    authorization: str = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
):

    try:

        if not authorization:
            raise Exception()

        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise Exception()

        payload = decode_token(token)
        sub = payload.get("sub")
        if not sub:
            raise Exception()

        user_id = UUID(sub)

        crud = UsuarioCRUD(db)
        usuario = crud.obtener_usuario_por_id(user_id)
        if not usuario:
            raise Exception()

        return usuario

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado"
        )
