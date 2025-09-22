"""
CRUD de Usuario
===============
"""

from sqlalchemy.orm import Session
from uuid import UUID
from entities.usuario import Usuario, RolEnum
from typing import Optional


class UsuarioCRUD:
    """Operaciones CRUD para Usuario"""

    def __init__(self, db: Session):
        self.db = db

    def crear_usuario(
        self,
        username: str,
        password: str,
        id_usuario_creacion: UUID,
        rol: RolEnum = RolEnum.admin,
        estado: bool = True,
    ) -> Usuario:
        """Crear un nuevo usuario"""
        usuario = Usuario(
            username=username,
            id_usuario_creacion=id_usuario_creacion,
            rol=rol,
            estado=estado,
        )
        usuario.set_password(password)
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario_por_id(self, usuario_id: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_por_username(self, username: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def obtener_usuarios(self) -> list[Usuario]:
        return self.db.query(Usuario).all()

    def actualizar_usuario(
        self, usuario_id: str, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Usuario]:
        """Actualizar campos de un usuario"""
        usuario = self.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return None

        if "password" in kwargs and kwargs["password"]:
            usuario.set_password(kwargs.pop("password"))

        for key, value in kwargs.items():
            if hasattr(usuario, key) and value is not None:
                setattr(usuario, key, value)

        usuario.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: str) -> bool:
        """Eliminar un usuario por ID"""
        usuario = self.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return False
        self.db.delete(usuario)
        self.db.commit()
        return True

    def autenticar_usuario(self, username: str, password: str) -> Optional[Usuario]:
        """Autenticar credenciales de usuario"""
        usuario = self.obtener_usuario_por_username(username)
        if usuario and usuario.check_password(password) and usuario.estado:
            return usuario
        return None

    def obtener_admin_por_defecto(self) -> Optional[Usuario]:
        """Verificar si ya existe un admin"""
        return self.db.query(Usuario).filter(Usuario.username == "admin").first()

    def cambiar_contrasena(
        self, usuario_id: str, password_actual: str, password_nueva: str
    ) -> bool:
        """Cambiar contraseña de un usuario"""
        usuario = self.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return False

        if not usuario.check_password(password_actual):
            return False

        usuario.set_password(password_nueva)
        self.db.commit()
        return True
