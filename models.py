from pydantic import BaseModel, EmailStr
from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime


# =========================
# MODELOS: CLIENTE
# =========================
class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None


class ClienteCreate(ClienteBase):
    """Modelo para crear cliente (el router actual solo envía nombre/email/telefono)."""

    id_usuario_creacion: UUID


class ClienteUpdate(BaseModel):
    """Modelo para actualizar cliente. id_usuario_edicion se incluye para auditoría."""

    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    id_usuario_edicion: UUID


class ClienteResponse(ClienteBase):
    id: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    activo: Optional[bool] = True

    # Pydantic v2: permitir construcciones desde objetos ORM (SQLAlchemy)
    model_config = {"from_attributes": True}


# =========================
# MODELOS: CONTRATO
# =========================
class ContratoBase(BaseModel):
    cliente_id: UUID
    vehiculo_id: UUID
    empleado_id: UUID
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    activo: Optional[bool] = True


class ContratoCreate(ContratoBase):
    id_usuario_creacion: UUID


class ContratoUpdate(BaseModel):
    cliente_id: Optional[UUID] = None
    vehiculo_id: Optional[UUID] = None
    empleado_id: Optional[UUID] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    activo: Optional[bool] = None
    id_usuario_edicion: UUID


class ContratoResponse(ContratoBase):
    id: UUID
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    model_config = {"from_attributes": True}


# =========================
# MODELOS: EMPLEADO
# =========================
class EmpleadoBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: Optional[str] = "Asesor"
    activo: Optional[bool] = True


class EmpleadoCreate(EmpleadoBase):
    id_usuario_creacion: UUID


class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None
    id_usuario_edicion: UUID


class EmpleadoResponse(EmpleadoBase):
    id: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    model_config = {"from_attributes": True}


# =========================
# MODELOS: PAGO
# =========================
class PagoBase(BaseModel):
    contrato_id: UUID
    monto: float
    fecha_pago: Optional[datetime] = None


class PagoCreate(PagoBase):
    id_usuario_creacion: UUID
    fecha_pago: Optional[datetime] = None


class PagoUpdate(BaseModel):
    monto: Optional[float] = None
    fecha_pago: Optional[datetime] = None
    id_usuario_edicion: UUID


class PagoResponse(PagoBase):
    id: UUID
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    model_config = {"from_attributes": True}


# =========================
# MODELOS: TIPO VEHICULO
# =========================
class TipoVehiculoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: Optional[bool] = True


class TipoVehiculoCreate(TipoVehiculoBase):
    id_usuario_creacion: UUID


class TipoVehiculoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
    id_usuario_edicion: UUID


class TipoVehiculoResponse(TipoVehiculoBase):
    id: UUID
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    model_config = {"from_attributes": True}


# =========================
# MODELOS: USUARIO
# =========================
class UsuarioBase(BaseModel):
    username: str
    rol: Optional[str] = "admin"
    estado: Optional[bool] = True


class UsuarioCreate(UsuarioBase):
    password: str
    id_usuario_creacion: UUID


class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[bool] = None
    id_usuario_edicion: UUID


class UsuarioResponse(UsuarioBase):
    id: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UsuarioLogin(BaseModel):
    username: str
    password: str


# =========================
# MODELOS: VEHICULO
# =========================
class VehiculoBase(BaseModel):
    marca: str
    modelo: str
    tipo_id: UUID
    placa: Optional[str] = None
    disponible: Optional[bool] = True


class VehiculoCreate(VehiculoBase):
    id_usuario_creacion: UUID


class VehiculoUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    tipo_id: Optional[UUID] = None
    placa: Optional[str] = None
    disponible: Optional[bool] = None
    id_usuario_edicion: UUID


class VehiculoResponse(VehiculoBase):
    id: UUID
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    model_config = {"from_attributes": True}


# =========================
# RESPUESTAS GENERALES
# =========================
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[Dict[str, Any]] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: Optional[str] = None
    codigo: Optional[int] = None
