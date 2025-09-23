"""
Operaciones CRUD para Cliente
"""

from typing import List, Optional
from uuid import UUID

from entities.cliente import Cliente
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class ClienteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_cliente(
        self,
        nombre: str,
        email: str,
        telefono: Optional[str] = None,
        id_usuario_creacion: str = None,
    ) -> Cliente:
        """
        Crear un nuevo cliente con validaciones

        Args:
            nombre: Nombre del cliente
            email: Email único
            telefono: Teléfono opcional

        Returns:
            Cliente creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del cliente es obligatorio")

        if self.obtener_cliente_por_email(email):
            raise ValueError("Ya existe un cliente con ese correo")

        cliente = Cliente(
            nombre=nombre.strip().title(),
            email=email.strip().lower(),
            telefono=telefono.strip() if telefono else None,
            id_usuario_creacion=id_usuario_creacion,
            activo=True,
        )

        try:
            self.db.add(cliente)
            self.db.commit()
            self.db.refresh(cliente)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Error al crear cliente: email ya registrado")

        return cliente

    def obtener_cliente(self, cliente_id: UUID) -> Optional[Cliente]:
        """
        Obtener un cliente por ID
        """
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def obtener_cliente_por_email(self, email: str) -> Optional[Cliente]:
        """
        Obtener un cliente por correo
        """
        return (
            self.db.query(Cliente)
            .filter(Cliente.email == email.strip().lower())
            .first()
        )

    def obtener_clientes(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """
        Obtener lista de clientes con paginación
        """
        return self.db.query(Cliente).offset(skip).limit(limit).all()

    def actualizar_cliente(
        self, cliente_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Cliente]:
        """
        Actualizar un cliente con validaciones

        Args:
            cliente_id: UUID del cliente
            kwargs: Campos a actualizar

        Returns:
            Cliente actualizado o None
        """
        cliente = self.obtener_cliente(cliente_id)
        if not cliente:
            return None

        if "email" in kwargs and kwargs["email"]:
            nuevo_email = kwargs["email"].strip().lower()
            existente = self.obtener_cliente_por_email(nuevo_email)
            if existente and existente.id != cliente_id:
                raise ValueError("Ya existe un cliente con ese correo")
            kwargs["email"] = nuevo_email

        if "nombre" in kwargs and kwargs["nombre"]:
            kwargs["nombre"] = kwargs["nombre"].strip().title()

        for key, value in kwargs.items():
            if hasattr(cliente, key) and value is not None:
                setattr(cliente, key, value)

        cliente.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def eliminar_cliente(self, cliente_id: UUID) -> bool:
        """
        Eliminar un cliente

        Returns:
            True si se eliminó, False si no existe
        """
        cliente = self.obtener_cliente(cliente_id)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False
