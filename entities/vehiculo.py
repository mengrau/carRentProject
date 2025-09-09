"""
Entidad Vehiculo
================
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

from ..database.database import Base

class Vehiculo(Base):
    __tablename__ = 'vehiculos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_id = Column(Integer, ForeignKey("tipos_vehiculo.id"), nullable=False)  # Relación con TipoVehiculo
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    placa = Column(String(20), unique=True, nullable=True, index=True)
    disponible = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    tipo_vehiculo = relationship("TipoVehiculo", back_populates="vehiculos")
    contratos = relationship("Contrato", back_populates="vehiculo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Vehiculo(id={self.id}, marca='{self.marca}', modelo='{self.modelo}', disponible={self.disponible})>"


# ====== Pydantic Schemas ======

class VehiculoBase(BaseModel):
    marca: str
    modelo: str
    placa: Optional[str] = None
    disponible: bool = True
    categoria_id: int
    tipo_id: int   # <--- ahora también forma parte del esquema

    @validator('marca', 'modelo')
    def no_vacios(cls, v):
        if not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip().title()


class VehiculoCreate(VehiculoBase):
    """Esquema para crear un vehículo"""
    pass


class VehiculoUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    placa: Optional[str] = None
    disponible: Optional[bool] = None
    categoria_id: Optional[int] = None
    tipo_id: Optional[int] = None   # se permite actualizar también el tipo


class VehiculoResponse(VehiculoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}
