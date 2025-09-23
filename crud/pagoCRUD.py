"""
Operaciones CRUD para Pago
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from entities.pago import Pago
from sqlalchemy.orm import Session


class PagoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_pago(
        self,
        contrato_id: UUID,
        monto: float,
        id_usuario_creacion: UUID,
        fecha_pago: Optional[datetime] = None,
    ) -> Pago:
        """
        Crear un nuevo pago con validaciones

        Args:
            contrato_id: UUID del contrato asociado
            monto: Valor del pago (debe ser positivo)
            fecha_pago: Fecha del pago (por defecto ahora)

        Returns:
            Pago creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if monto <= 0:
            raise ValueError("El monto del pago debe ser mayor que 0")

        pago = Pago(
            contrato_id=contrato_id,
            monto=monto,
            id_usuario_creacion=id_usuario_creacion,
            fecha_pago=fecha_pago if fecha_pago else datetime.now(),
        )
        self.db.add(pago)
        self.db.commit()
        self.db.refresh(pago)
        return pago

    def obtener_pago(self, pago_id: UUID) -> Optional[Pago]:
        """
        Obtener un pago por ID
        """
        return self.db.query(Pago).filter(Pago.id == pago_id).first()

    def obtener_pagos(
        self, skip: int = 0, limit: int = 100, contrato_id: Optional[UUID] = None
    ) -> List[Pago]:
        """
        Obtener lista de pagos con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
            contrato_id: Filtrar pagos por contrato
        """
        query = self.db.query(Pago)
        if contrato_id:
            query = query.filter(Pago.contrato_id == contrato_id)
        return query.offset(skip).limit(limit).all()

    def actualizar_pago(
        self, pago_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Pago]:
        """
        Actualizar un pago con validaciones

        Args:
            pago_id: UUID del pago
            kwargs: Campos a actualizar (monto, fecha_pago)

        Returns:
            Pago actualizado o None
        """
        pago = self.obtener_pago(pago_id)
        if not pago:
            return None

        if "monto" in kwargs and kwargs["monto"] is not None:
            if kwargs["monto"] <= 0:
                raise ValueError("El monto del pago debe ser mayor que 0")

        for key, value in kwargs.items():
            if hasattr(pago, key) and value is not None:
                setattr(pago, key, value)

        pago.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        self.db.refresh(pago)
        return pago

    def eliminar_pago(self, pago_id: UUID) -> bool:
        """
        Eliminar un pago

        Returns:
            True si se eliminó, False si no existe
        """
        pago = self.obtener_pago(pago_id)
        if pago:
            self.db.delete(pago)
            self.db.commit()
            return True
        return False
