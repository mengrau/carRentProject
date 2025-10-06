"""
Entidad Pago
============
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class Pago(Base):
    """
    Modelo de la tabla pagos

    Representa un pago asociado a un contrato. Contiene el monto del pago,
    la fecha en que se realizo y la trazabilidad de su creacion y edicion.

    Atributos:
        id (UUID): Identificador unico del pago.
        contrato_id (UUID): Referencia al contrato al que pertenece el pago.
        monto (float): Valor monetario del pago.
        fecha_pago (datetime): Fecha en que se realizo el pago.

        id_usuario_creacion (UUID): Usuario que realizo la creacion del registro.
        id_usuario_edicion (UUID, opcional): Usuario que realizo la ultima edicion.
        fecha_creacion (datetime): Fecha en que fue creado el registro.
        fecha_actualizacion (datetime): Fecha en que se actualizo por ultima vez.

    Relaciones:
        usuario_creador (Usuario): Usuario que realizo la creacion.
        usuario_editor (Usuario): Usuario que realizo la edicion.
        contrato (Contrato): Contrato al que pertenece el pago.
    """

    __tablename__ = "pagos"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    contrato_id = Column(UUID(as_uuid=True), ForeignKey("contratos.id"), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_pago = Column(DateTime, default=datetime.now, nullable=False)

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
    contrato = relationship("Contrato", back_populates="pagos")
