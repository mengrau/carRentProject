"""
Operaciones CRUD para Contrato
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from entities.contrato import Contrato
from sqlalchemy.orm import Session


class ContratoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_contrato(
        self,
        cliente_id: UUID,
        vehiculo_id: UUID,
        empleado_id: UUID,
        fecha_inicio: datetime,
        fecha_fin: Optional[datetime] = None,
    ) -> Contrato:
        """
        Crear un nuevo contrato con validaciones

        Args:
            cliente_id: UUID del cliente
            vehiculo_id: UUID del vehículo
            empleado_id: UUID del empleado
            fecha_inicio: Fecha de inicio del contrato
            fecha_fin: Fecha opcional de fin del contrato

        Returns:
            Contrato creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if fecha_fin and fecha_fin < fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio")

        contrato = Contrato(
            cliente_id=cliente_id,
            vehiculo_id=vehiculo_id,
            empleado_id=empleado_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            activo=True,
        )
        self.db.add(contrato)
        self.db.commit()
        self.db.refresh(contrato)
        return contrato

    def obtener_contrato(self, contrato_id: UUID) -> Optional[Contrato]:
        """
        Obtener un contrato por ID
        """
        return self.db.query(Contrato).filter(Contrato.id == contrato_id).first()

    def obtener_contratos(
        self, skip: int = 0, limit: int = 100, solo_activos: bool = False
    ) -> List[Contrato]:
        """
        Obtener lista de contratos con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
            solo_activos: Si True, solo devuelve contratos activos
        """
        query = self.db.query(Contrato)
        if solo_activos:
            query = query.filter(Contrato.activo == True)
        return query.offset(skip).limit(limit).all()

    def actualizar_contrato(
        self, contrato_id: UUID, **kwargs
    ) -> Optional[Contrato]:
        """
        Actualizar un contrato con validaciones

        Args:
            contrato_id: UUID del contrato
            kwargs: Campos a actualizar

        Returns:
            Contrato actualizado o None
        """
        contrato = self.obtener_contrato(contrato_id)
        if not contrato:
            return None

        if "fecha_inicio" in kwargs and kwargs["fecha_inicio"]:
            if contrato.fecha_fin and kwargs["fecha_inicio"] > contrato.fecha_fin:
                raise ValueError("La fecha de inicio no puede ser mayor a la de fin")

        if "fecha_fin" in kwargs and kwargs["fecha_fin"]:
            if kwargs["fecha_fin"] < contrato.fecha_inicio:
                raise ValueError("La fecha de fin no puede ser anterior a la de inicio")

        for key, value in kwargs.items():
            if hasattr(contrato, key) and value is not None:
                setattr(contrato, key, value)

        self.db.commit()
        self.db.refresh(contrato)
        return contrato

    def eliminar_contrato(self, contrato_id: UUID) -> bool:
        """
        Eliminar un contrato

        Returns:
            True si se eliminó, False si no existe
        """
        contrato = self.obtener_contrato(contrato_id)
        if contrato:
            self.db.delete(contrato)
            self.db.commit()
            return True
        return False
