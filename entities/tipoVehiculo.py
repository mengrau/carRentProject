"""
Entidad TipoVehiculo
====================
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class TipoVehiculo(Base):
    """
    Modelo de la tabla tipos_vehiculo

    Representa una categoria de vehiculo dentro del sistema. Define el
    nombre y una descripcion opcional, ademas de la trazabilidad de su
    creacion y edicion.

    Atributos:
        id (UUID): Identificador unico del tipo de vehiculo.
        nombre (str): Nombre unico del tipo de vehiculo.
        descripcion (str, opcional): Texto descriptivo sobre el tipo de vehiculo.
        activo (bool): Estado del registro (activo o inactivo).

        id_usuario_creacion (UUID): Usuario que realizo la creacion del registro.
        id_usuario_edicion (UUID, opcional): Usuario que realizo la ultima edicion.
        fecha_creacion (datetime): Fecha en que fue creado el registro.
        fecha_actualizacion (datetime): Fecha en que se actualizo por ultima vez.

    Relaciones:
        usuario_creador (Usuario): Usuario que realizo la creacion.
        usuario_editor (Usuario): Usuario que realizo la edicion.
        vehiculos (list[Vehiculo]): Vehiculos asociados a este tipo.
    """

    __tablename__ = "tipos_vehiculo"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
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
    vehiculos = relationship(
        "Vehiculo", back_populates="tipo_vehiculo", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<TipoVehiculo(nombre='{self.nombre}', descripcion='{self.descripcion} activo={self.activo})>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "activo": self.activo,
            "fecha_creacion": (
                self.fecha_creacion.isoformat() if self.fecha_creacion else None
            ),
            "fecha_actualizacion": (
                self.fecha_actualizacion.isoformat()
                if self.fecha_actualizacion
                else None
            ),
        }


class TipoVehiculoBase(BaseModel):
    nombre: str = Field(
        ..., min_length=2, max_length=100, description="Nombre del tipo de vehículo"
    )
    descripcion: Optional[str] = Field(
        None, description="Descripción del tipo de vehículo"
    )
    activo: bool = Field(True, description="Estado del tipo de vehículo")

    @validator("nombre")
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip().title()


class TipoVehiculoCreate(TipoVehiculoBase):
    pass


class TipoVehiculoUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str] = Field(
        None, description="Nueva descripción del tipo de vehículo"
    )
    activo: Optional[bool] = Field(
        None, description="Nuevo estado del tipo de vehículo"
    )

    @validator("nombre")
    def validar_nombre(cls, v):
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío si se envía")
        return v.strip().title() if v else v
