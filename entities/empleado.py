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
    """
    Modelo de la tabla empleados

    Representa un empleado dentro del sistema. Contiene informacion basica
    como nombre, email, rol y estado, ademas de la trazabilidad de su
    creacion y edicion.

    Atributos:
        id (UUID): Identificador unico del empleado.
        nombre (str): Nombre completo del empleado (max 150 caracteres).
        email (str): Correo electronico unico del empleado.
        rol (str): Rol asignado al empleado dentro de la organizacion
            (por defecto "Asesor").
        activo (bool): Estado del empleado (activo o inactivo).

        id_usuario_creacion (UUID): Usuario que realizo la creacion del registro.
        id_usuario_edicion (UUID, opcional): Usuario que realizo la ultima edicion.
        fecha_creacion (datetime): Fecha en que fue creado el registro.
        fecha_actualizacion (datetime): Fecha en que se actualizo por ultima vez.

    Relaciones:
        usuario_creador (Usuario): Usuario que realizo la creacion.
        usuario_editor (Usuario): Usuario que realizo la edicion.
        contratos (list[Contrato]): Contratos asociados al empleado.
    """

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
