"""
Entidad Contrato
================
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class Contrato(Base):
    __tablename__ = 'contratos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    cliente = relationship("Cliente", back_populates="contratos")
    vehiculo = relationship("Vehiculo", back_populates="contratos")
    empleado = relationship("Empleado", back_populates="contratos")
    pagos = relationship("Pago", back_populates="contrato", cascade="all, delete-orphan")

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
