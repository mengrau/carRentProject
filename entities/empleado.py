"""
Entidad Empleado
================
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    rol = Column(String(50), nullable=False, default="Asesor")
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
        "Contrato", back_populates="empleado", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Empleado(nombre='{self.nombre}', email='{self.email} rol={self.rol})>"


class EmpleadoBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: str = "Asesor"
    activo: bool = True


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class EmpleadoResponse(EmpleadoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True
