"""
Modelo de Usuario
"""

from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime
from auth.security import hash_password, verify_password
import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID


class RolEnum(enum.Enum):
    admin = "admin"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), default=RolEnum.admin, nullable=False)
    estado = Column(Boolean, default=True)

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True
    )
    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    usuario_creador = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_editor = relationship("Usuario", foreign_keys=[id_usuario_edicion])

    def set_password(self, password: str):
        """Convierte la clave en hash y la guarda"""
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        """Verifica la clave contra el hash almacenado"""
        return verify_password(password, self.password_hash)

    def __repr__(self):
        return f"<Usuario(username={self.username})>"
