"""
Entidad Cliente
===============
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    contratos = relationship("Contrato", back_populates="cliente", cascade="all, delete-orphan")

class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    activo: bool = True

    @validator('nombre')
    def validar_nombre(cls, v):
        return v.strip().title()

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None

class ClienteResponse(ClienteBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True