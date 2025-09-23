"""
Entidad Cliente
===============
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class Cliente(Base):
    """
    Modelo de la tabla clientes

    Representa a un cliente dentro del sistema, incluyendo sus datos de
    identificación y de contacto, ademas de la trazabilidad de su
    creacion y edicion.

    Atributos:
        id (UUID): Identificador unico del cliente.
        nombre (str): Nombre completo del cliente.
        email (str): Correo electronico unico del cliente.
        telefono (str, opcional): Numero de telefono de contacto.
        activo (bool): Estado del cliente (activo o inactivo).

        id_usuario_creacion (UUID): Usuario que creó el registro.
        id_usuario_edicion (UUID, opcional): Ultimo usuario que editó el registro.
        fecha_creacion (datetime): Fecha de creación del registro.
        fecha_actualizacion (datetime): Ultima fecha de actualización del registro.

    Relaciones:
        usuario_creador (Usuario): Relación con el usuario que creó el cliente.
        usuario_editor (Usuario): Relación con el usuario que lo editó.
        contratos (list[Contrato]): Lista de contratos asociados al cliente.
    """

    __tablename__ = "clientes"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False
    )
    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    usuario_creador = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_editor = relationship("Usuario", foreign_keys=[id_usuario_edicion])
    contratos = relationship(
        "Contrato", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Cliente(nombre='{self.nombre}', email='{self.email} activo={self.activo})>"


class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    activo: bool = True

    @validator("nombre")
    def validar_nombre(cls, v):
        return v.strip().title()


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None


class ClienteResponse(ClienteBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True
