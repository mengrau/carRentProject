"""
Operaciones CRUD para Empleado
"""

from typing import List, Optional
from uuid import UUID

from entities.empleado import Empleado
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class EmpleadoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_empleado(
        self, nombre: str, email: str, rol: str = "Asesor", activo: bool = True
    ) -> Empleado:
        """
        Crear un nuevo empleado con validaciones

        Args:
            nombre: Nombre del empleado
            email: Correo único
            rol: Rol del empleado (por defecto "Asesor")
            activo: Estado del empleado (True = activo)

        Returns:
            Empleado creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del empleado es obligatorio")

        if self.obtener_empleado_por_email(email):
            raise ValueError("Ya existe un empleado con ese correo")

        empleado = Empleado(
            nombre=nombre.strip().title(),
            email=email.strip().lower(),
            rol=rol.strip().title(),
            activo=activo,
        )

        try:
            self.db.add(empleado)
            self.db.commit()
            self.db.refresh(empleado)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Error al crear empleado: email ya registrado")

        return empleado

    def obtener_empleado(self, empleado_id: UUID) -> Optional[Empleado]:
        """
        Obtener un empleado por ID
        """
        return self.db.query(Empleado).filter(Empleado.id == empleado_id).first()

    def obtener_empleado_por_email(self, email: str) -> Optional[Empleado]:
        """
        Obtener un empleado por correo
        """
        return self.db.query(Empleado).filter(Empleado.email == email.strip().lower()).first()

    def obtener_empleados(
        self, skip: int = 0, limit: int = 100, solo_activos: bool = False
    ) -> List[Empleado]:
        """
        Obtener lista de empleados con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
            solo_activos: Si True, solo devuelve empleados activos
        """
        query = self.db.query(Empleado)
        if solo_activos:
            query = query.filter(Empleado.activo == True)
        return query.offset(skip).limit(limit).all()

    def actualizar_empleado(
        self, empleado_id: UUID, **kwargs
    ) -> Optional[Empleado]:
        """
        Actualizar un empleado con validaciones

        Args:
            empleado_id: UUID del empleado
            kwargs: Campos a actualizar

        Returns:
            Empleado actualizado o None
        """
        empleado = self.obtener_empleado(empleado_id)
        if not empleado:
            return None

        if "email" in kwargs and kwargs["email"]:
            nuevo_email = kwargs["email"].strip().lower()
            existente = self.obtener_empleado_por_email(nuevo_email)
            if existente and existente.id != empleado_id:
                raise ValueError("Ya existe un empleado con ese correo")
            kwargs["email"] = nuevo_email

        if "nombre" in kwargs and kwargs["nombre"]:
            kwargs["nombre"] = kwargs["nombre"].strip().title()

        if "rol" in kwargs and kwargs["rol"]:
            kwargs["rol"] = kwargs["rol"].strip().title()

        for key, value in kwargs.items():
            if hasattr(empleado, key) and value is not None:
                setattr(empleado, key, value)

        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def eliminar_empleado(self, empleado_id: UUID) -> bool:
        """
        Eliminar un empleado

        Returns:
            True si se eliminó, False si no existe
        """
        empleado = self.obtener_empleado(empleado_id)
        if empleado:
            self.db.delete(empleado)
            self.db.commit()
            return True
        return False
