from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
import uuid
from datetime import datetime
import enum


# ================= CLIENTE =================
class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    activo: bool = True

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
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


# ================= CONTRATO =================
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


# ================= EMPLEADO =================
class EmpleadoBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: str = "Asesor"
    activo: bool = True


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class EmpleadoResponse(EmpleadoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True


# ================= PAGO =================
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


# ================= TIPO VEHICULO =================
class TipoVehiculoBase(BaseModel):
    nombre: str = Field(
        ..., min_length=2, max_length=100, description="Nombre del tipo de vehículo"
    )
    descripcion: Optional[str] = Field(
        None, description="Descripción del tipo de vehículo"
    )
    activo: bool = Field(True, description="Estado del tipo de vehículo")

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
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

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío si se envía")
        return v.strip().title() if v else v


class RolEnum(str, enum.Enum):
    admin = "admin"


# ------------------------
# MODELOS DE ENTRADA
# ------------------------


class UsuarioCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nombre de usuario único utilizado para autenticación",
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Contraseña en texto plano (mínimo 6 caracteres)",
    )
    rol: RolEnum = Field(
        default=RolEnum.admin,
        description="Rol asignado al usuario",
    )


class UsuarioUpdate(BaseModel):
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Nombre de usuario"
    )
    password: Optional[str] = Field(
        None, min_length=6, max_length=128, description="Nueva contraseña"
    )
    rol: Optional[RolEnum] = Field(None, description="Rol del usuario")
    estado: Optional[bool] = Field(
        None, description="Estado del usuario (activo/inactivo)"
    )


# ------------------------
# MODELOS DE RESPUESTA
# ------------------------


class UsuarioRead(BaseModel):
    id: uuid.UUID
    username: str
    rol: RolEnum
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permite convertir desde SQLAlchemy ORM
