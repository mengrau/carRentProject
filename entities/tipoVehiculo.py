"""
Entidad TipoVehiculo
====================

Modelo de TipoVehiculo con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class TipoVehiculo(Base):
    """
    Modelo de TipoVehiculo que representa la tabla 'tipos_vehiculo'
    
    Atributos:
        id: Identificador único del tipo de vehículo
        nombre: Nombre del tipo de vehículo (ej. Auto, Moto, Bici)
        descripcion: Descripción del tipo de vehículo
        activo: Estado del tipo de vehículo
        fecha_creacion: Fecha y hora de creación
        fecha_actualizacion: Fecha y hora de última actualización
    """
    
    __tablename__ = 'tipos_vehiculo'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    vehiculos = relationship("Vehiculo", back_populates="tipo_vehiculo", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<TipoVehiculo(id={self.id}, nombre='{self.nombre}', activo={self.activo})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

# ===== Pydantic Schemas =====

class TipoVehiculoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del tipo de vehículo")
    descripcion: Optional[str] = Field(None, description="Descripción del tipo de vehículo")
    activo: bool = Field(True, description="Estado del tipo de vehículo")
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip().title()

class TipoVehiculoCreate(TipoVehiculoBase):
    pass

class TipoVehiculoUpdate(BaseModel):
    nombre: Optional[str]()
