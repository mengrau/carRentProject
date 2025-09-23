"""
Entidad Contrato
================
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class Contrato(Base):
    """
    Modelo de la tabla contratos

    Representa un contrato entre un cliente, un vehiculo y un empleado.
    Define las fechas de inicio y fin, el estado del contrato y la
    informacion de trazabilidad de su creacion y edicion.

    Atributos:
        id (UUID): Identificador unico del contrato.
        cliente_id (UUID): Referencia al cliente asociado.
        vehiculo_id (UUID): Referencia al vehiculo asociado.
        empleado_id (UUID): Referencia al empleado asociado.
        fecha_inicio (datetime): Fecha en que inicia el contrato.
        fecha_fin (datetime, opcional): Fecha en que terminó o finalizará el contrato.
        activo (bool): Estado del contrato (activo o inactivo).

        id_usuario_creacion (UUID): Usuario que realizó la creacion del registro.
        id_usuario_edicion (UUID, opcional): Usuario que realizó la ultima edicion.
        fecha_creacion (datetime): Fecha en que fue creado el registro.
        fecha_actualizacion (datetime): Fecha en que se actualizo por ultima vez.

    Relaciones:
        usuario_creador (Usuario): Usuario que realizo la creacion.
        usuario_editor (Usuario): Usuario que realizo la edicion.
        cliente (Cliente): Cliente asociado al contrato.
        vehiculo (Vehiculo): Vehiculo asociado al contrato.
        empleado (Empleado): Empleado asociado al contrato.
        pagos (list[Pago]): Pagos relacionados con el contrato.
    """

    __tablename__ = "contratos"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    vehiculo_id = Column(UUID(as_uuid=True), ForeignKey("vehiculos.id"), nullable=False)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("empleados.id"), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)
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
    cliente = relationship("Cliente", back_populates="contratos")
    vehiculo = relationship("Vehiculo", back_populates="contratos")
    empleado = relationship("Empleado", back_populates="contratos")
    pagos = relationship(
        "Pago", back_populates="contrato", cascade="all, delete-orphan"
    )


class ContratoBase(BaseModel):
    cliente_id: int
    vehiculo_id: int
    empleado_id: int
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    activo: bool = True


class ContratoCreate(ContratoBase):
    pass


class ContratoUpdate(BaseModel):
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    activo: Optional[bool] = None


class ContratoResponse(ContratoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True
