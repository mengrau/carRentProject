"""
Entidad Vehiculo
================
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class Vehiculo(Base):
    """
    Modelo de la tabla vehiculos

    Representa un vehiculo registrado en el sistema, con informacion basica de
    identificacion, disponibilidad y trazabilidad de creacion y edicion.

    Atributos:
        id (UUID): Identificador unico del vehiculo.
        tipo_id (UUID): Referencia al tipo de vehiculo asociado.
        marca (str): Marca del vehiculo.
        modelo (str): Modelo del vehiculo.
        placa (str): Placa unica del vehiculo.
        disponible (bool): Indica si el vehiculo esta disponible.

        id_usuario_creacion (UUID): Usuario que realizo la creacion del registro.
        id_usuario_edicion (UUID, opcional): Usuario que realizo la ultima edicion.
        fecha_creacion (datetime): Fecha en que fue creado el registro.
        fecha_actualizacion (datetime): Fecha en que se actualizo por ultima vez.

    Relaciones:
        usuario_creador (Usuario): Usuario que realizo la creacion.
        usuario_editor (Usuario): Usuario que realizo la edicion.
        tipo_vehiculo (TipoVehiculo): Tipo al que pertenece el vehiculo.
        contratos (list[Contrato]): Contratos asociados al vehiculo.
    """

    __tablename__ = "vehiculos"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    tipo_id = Column(
        UUID(as_uuid=True), ForeignKey("tipos_vehiculo.id"), nullable=False
    )
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    placa = Column(String(20), unique=True, nullable=False, index=True)
    disponible = Column(Boolean, default=True, nullable=False)

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
    tipo_vehiculo = relationship("TipoVehiculo", back_populates="vehiculos")
    contratos = relationship(
        "Contrato", back_populates="vehiculo", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Vehiculo(marca='{self.marca}', modelo='{self.modelo}', placa='{self.placa}, disponible={self.disponible})>"


class VehiculoBase(BaseModel):
    marca: str
    modelo: str
    placa: Optional[str] = None
    disponible: bool = True
    categoria_id: int
    tipo_id: int

    @validator("marca", "modelo")
    def no_vacios(cls, v):
        if not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip().title()


class VehiculoUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    placa: Optional[str] = None
    disponible: Optional[bool] = None
    categoria_id: Optional[int] = None
    tipo_id: Optional[int] = None


class VehiculoResponse(VehiculoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}
