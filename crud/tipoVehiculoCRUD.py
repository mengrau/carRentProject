"""
Operaciones CRUD para TipoVehiculo
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.tipoVehiculo import TipoVehiculo


class TipoVehiculoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_tipo_vehiculo(
        self, nombre: str, descripcion: str = None, activo: bool = True
    ) -> TipoVehiculo:
        """
        Crear un nuevo tipo de vehículo con validaciones

        Args:
            nombre: Nombre del tipo de vehículo (único, máx. 100 caracteres)
            descripcion: Descripción opcional
            activo: Estado del tipo de vehículo

        Returns:
            TipoVehiculo creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del tipo de vehículo es obligatorio")

        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if self.obtener_tipo_vehiculo_por_nombre(nombre):
            raise ValueError("Ya existe un tipo de vehículo con ese nombre")

        tipo = TipoVehiculo(
            nombre=nombre.strip().title(),
            descripcion=descripcion.strip() if descripcion else None,
            activo=activo,
        )

        self.db.add(tipo)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def obtener_tipo_vehiculo(self, tipo_id: UUID) -> Optional[TipoVehiculo]:
        """
        Obtener un tipo de vehículo por ID
        """
        return self.db.query(TipoVehiculo).filter(TipoVehiculo.id == tipo_id).first()

    def obtener_tipo_vehiculo_por_nombre(self, nombre: str) -> Optional[TipoVehiculo]:
        """
        Obtener un tipo de vehículo por nombre
        """
        return (
            self.db.query(TipoVehiculo)
            .filter(TipoVehiculo.nombre == nombre.strip().title())
            .first()
        )

    def obtener_tipos_vehiculo(
        self, skip: int = 0, limit: int = 100
    ) -> List[TipoVehiculo]:
        """
        Obtener lista de tipos de vehículo con paginación
        """
        return self.db.query(TipoVehiculo).offset(skip).limit(limit).all()

    def actualizar_tipo_vehiculo(
        self, tipo_id: UUID, **kwargs
    ) -> Optional[TipoVehiculo]:
        """
        Actualizar un tipo de vehículo con validaciones
        """
        tipo = self.obtener_tipo_vehiculo(tipo_id)
        if not tipo:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre del tipo de vehículo es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            if (
                self.obtener_tipo_vehiculo_por_nombre(nombre)
                and self.obtener_tipo_vehiculo_por_nombre(nombre).id != tipo_id
            ):
                raise ValueError("Ya existe un tipo de vehículo con ese nombre")
            kwargs["nombre"] = nombre.strip().title()

        if "descripcion" in kwargs and kwargs["descripcion"]:
            kwargs["descripcion"] = kwargs["descripcion"].strip()

        for key, value in kwargs.items():
            if hasattr(tipo, key):
                setattr(tipo, key, value)

        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def eliminar_tipo_vehiculo(self, tipo_id: UUID) -> bool:
        """
        Eliminar un tipo de vehículo
        """
        tipo = self.obtener_tipo_vehiculo(tipo_id)
        if tipo:
            self.db.delete(tipo)
            self.db.commit()
            return True
        return False
