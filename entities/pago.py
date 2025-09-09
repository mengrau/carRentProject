"""
Entidad Pago
============
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from ..database.database import Base

class Pago(Base):
    __tablename__ = 'pagos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_pago = Column(DateTime, default=datetime.now, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    contrato = relationship("Contrato", back_populates="pagos")

class PagoBase(BaseModel):
    contrato_id: int
    monto: float
    fecha_pago: Optional[datetime] = None

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    monto: Optional[float] = None
    fecha_pago: Optional[datetime] = None

class PagoResponse(PagoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True
