"""
Operaciones CRUD para Vehiculo
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from entities.vehiculo import Vehiculo


class VehiculoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_vehiculo(
        self,
        marca: str,
        modelo: str,
        tipo_id: UUID,
        placa: Optional[str] = None,
        disponible: bool = True,
    ) -> Vehiculo:
        """
        Crear un nuevo vehículo con validaciones

        Args:
            marca: Marca del vehículo (obligatoria, máx 100 caracteres)
            modelo: Modelo del vehículo (obligatorio, máx 100 caracteres)
            tipo_id: UUID del tipo de vehículo (obligatorio)
            placa: Placa opcional (única)
            disponible: Estado de disponibilidad (default True)

        Returns:
            Vehículo creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not marca or len(marca.strip()) == 0:
            raise ValueError("La marca del vehículo es obligatoria")
        if not modelo or len(modelo.strip()) == 0:
            raise ValueError("El modelo del vehículo es obligatorio")
        if len(marca) > 100 or len(modelo) > 100:
            raise ValueError("La marca o el modelo no pueden exceder 100 caracteres")

        if placa and self.obtener_vehiculo_por_placa(placa):
            raise ValueError("Ya existe un vehículo con esa placa")

        vehiculo = Vehiculo(
            marca=marca.strip().title(),
            modelo=modelo.strip().title(),
            placa=placa.strip().upper() if placa else None,
            disponible=disponible,
            tipo_id=tipo_id,
        )

        self.db.add(vehiculo)
        self.db.commit()
        self.db.refresh(vehiculo)
        return vehiculo

    def obtener_vehiculo(self, vehiculo_id: UUID) -> Optional[Vehiculo]:
        """
        Obtener un vehículo por ID
        """
        return self.db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()

    def obtener_vehiculo_por_placa(self, placa: str) -> Optional[Vehiculo]:
        """
        Obtener un vehículo por placa
        """
        return (
            self.db.query(Vehiculo)
            .filter(Vehiculo.placa == placa.strip().upper())
            .first()
        )

    def obtener_vehiculos(self, skip: int = 0, limit: int = 100) -> List[Vehiculo]:
        """
        Obtener lista de vehículos con paginación
        """
        return self.db.query(Vehiculo).offset(skip).limit(limit).all()

    def actualizar_vehiculo(self, vehiculo_id: UUID, **kwargs) -> Optional[Vehiculo]:
        """
        Actualizar un vehículo con validaciones
        """
        vehiculo = self.obtener_vehiculo(vehiculo_id)
        if not vehiculo:
            return None

        if "marca" in kwargs:
            marca = kwargs["marca"]
            if not marca or len(marca.strip()) == 0:
                raise ValueError("La marca del vehículo es obligatoria")
            if len(marca) > 100:
                raise ValueError("La marca no puede exceder 100 caracteres")
            kwargs["marca"] = marca.strip().title()

        if "modelo" in kwargs:
            modelo = kwargs["modelo"]
            if not modelo or len(modelo.strip()) == 0:
                raise ValueError("El modelo del vehículo es obligatorio")
            if len(modelo) > 100:
                raise ValueError("El modelo no puede exceder 100 caracteres")
            kwargs["modelo"] = modelo.strip().title()

        if "placa" in kwargs and kwargs["placa"]:
            placa = kwargs["placa"].strip().upper()
            if (
                self.obtener_vehiculo_por_placa(placa)
                and self.obtener_vehiculo_por_placa(placa).id != vehiculo_id
            ):
                raise ValueError("Ya existe un vehículo con esa placa")
            kwargs["placa"] = placa

        for key, value in kwargs.items():
            if hasattr(vehiculo, key):
                setattr(vehiculo, key, value)

        self.db.commit()
        self.db.refresh(vehiculo)
        return vehiculo

    def eliminar_vehiculo(self, vehiculo_id: UUID) -> bool:
        """
        Eliminar un vehículo
        """
        vehiculo = self.obtener_vehiculo(vehiculo_id)
        if vehiculo:
            self.db.delete(vehiculo)
            self.db.commit()
            return True
        return False
