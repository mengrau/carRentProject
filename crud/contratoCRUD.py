"""
Operaciones CRUD para Contrato
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from entities.contrato import Contrato
from entities.vehiculo import Vehiculo
from sqlalchemy.orm import Session


class ContratoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_contrato(
        self,
        cliente_id: UUID,
        vehiculo_id: UUID,
        empleado_id: UUID,
        id_usuario_creacion: UUID,
        fecha_inicio: datetime,
        fecha_fin: Optional[datetime] = None,
    ) -> Contrato:
        """
        Crear un nuevo contrato con validaciones y marcar el vehículo como no disponible

        Args:
            cliente_id: UUID del cliente
            vehiculo_id: UUID del vehículo
            empleado_id: UUID del empleado
            id_usuario_creacion: Usuario que crea el contrato
            fecha_inicio: Fecha de inicio del contrato
            fecha_fin: Fecha opcional de fin del contrato

        Returns:
            Contrato creado

        Raises:
            ValueError: Si los datos no son válidos o el vehículo no está disponible
        """
        if fecha_fin and fecha_fin < fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio")

        vehiculo = self.db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
        if not vehiculo:
            raise ValueError("El vehículo no existe")
        if not vehiculo.disponible:
            raise ValueError("El vehículo no está disponible para contrato")

        contrato = Contrato(
            cliente_id=cliente_id,
            vehiculo_id=vehiculo_id,
            empleado_id=empleado_id,
            id_usuario_creacion=id_usuario_creacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            activo=True,
        )

        vehiculo.disponible = False
        vehiculo.id_usuario_edicion = id_usuario_creacion

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
        self, contrato_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Contrato]:
        """
        Actualizar un contrato con validaciones

        Args:
            contrato_id: UUID del contrato
            id_usuario_edicion: UUID del usuario que edita
            kwargs: Campos a actualizar

        Returns:
            Contrato actualizado o None

        Raises:
            ValueError: Si las fechas no son válidas
        """
        contrato = self.obtener_contrato(contrato_id)
        if not contrato:
            return None

        if "fecha_inicio" in kwargs and kwargs["fecha_inicio"]:
            fecha_fin_comparar = kwargs.get("fecha_fin", contrato.fecha_fin)
            if fecha_fin_comparar and kwargs["fecha_inicio"] > fecha_fin_comparar:
                raise ValueError("La fecha de inicio no puede ser mayor a la de fin")

        if "fecha_fin" in kwargs and kwargs["fecha_fin"]:
            fecha_inicio_comparar = kwargs.get("fecha_inicio", contrato.fecha_inicio)
            if kwargs["fecha_fin"] < fecha_inicio_comparar:
                raise ValueError("La fecha de fin no puede ser anterior a la de inicio")
        for key, value in kwargs.items():
            if hasattr(contrato, key) and value is not None:
                setattr(contrato, key, value)

        if "activo" in kwargs and kwargs["activo"] is False:
            if contrato.vehiculo:
                contrato.vehiculo.disponible = True

        contrato.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        self.db.refresh(contrato)
        return contrato

    def eliminar_contrato(self, contrato_id: UUID) -> bool:
        """
        Eliminar un contrato y marcar el vehiculo como disponible

        Returns:
            True si se eliminó, False si no existe
        """
        contrato = self.obtener_contrato(contrato_id)
        if contrato:

            vehiculo = (
                self.db.query(Vehiculo)
                .filter(Vehiculo.id == contrato.vehiculo_id)
                .first()
            )
            if vehiculo:
                vehiculo.disponible = True
                vehiculo.id_usuario_edicion = contrato.id_usuario_creacion

            self.db.delete(contrato)
            self.db.commit()
            return True
        return False
