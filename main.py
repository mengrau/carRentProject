"""
Sistema de gestion con ORM SQLAlchemy y Neon PostgreSQL
Incluye autenticacion con login y CRUD para todas las entidades
"""

import getpass
from typing import Optional

import crud

from database.config import SessionLocal, create_tables
from entities.usuario import Usuario
from uuid import UUID


class SistemaGestion:
    """Sistema principal de gestion con interfaz de consola"""

    def __init__(self):
        self.db = SessionLocal()
        self.usuario_crud = crud.UsuarioCRUD(self.db)
        self.cliente_crud = crud.ClienteCRUD(self.db)
        self.empleado_crud = crud.EmpleadoCRUD(self.db)
        self.vehiculo_crud = crud.VehiculoCRUD(self.db)
        self.contrato_crud = crud.ContratoCRUD(self.db)
        self.pago_crud = crud.PagoCRUD(self.db)
        self.tipo_vehiculo_crud = crud.TipoVehiculoCRUD(self.db)
        self.usuario_actual: Optional[Usuario] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    # ---------------- LOGIN ----------------
    def mostrar_pantalla_login(self) -> bool:
        print("\n" + "=" * 50)
        print("        SISTEMA DE GESTION GENERAL")
        print("=" * 50)
        print("INICIAR SESION")
        print("=" * 50)

        intentos = 0
        while intentos < 3:
            username = input("Usuario: ").strip()
            password = getpass.getpass("Contraseña: ")
            usuario = self.usuario_crud.autenticar_usuario(username, password)
            if usuario:
                self.usuario_actual = usuario
                print(f"\nBienvenido {usuario.username} ({usuario.rol.value})")
                return True
            else:
                print("ERROR: Credenciales inválidas o usuario inactivo")
                intentos += 1
        return False

    def ejecutar(self) -> None:
        try:
            print("Iniciando Sistema de Gestion...")
            create_tables()

            if not self.mostrar_pantalla_login():
                print("Acceso denegado. Hasta luego!")
                return

            while True:
                self.mostrar_menu_principal()
                opcion = input("\nSeleccione una opcion: ").strip()

                if opcion == "1":
                    self.mostrar_menu_usuarios()
                elif opcion == "2":
                    self.mostrar_menu_clientes()
                elif opcion == "3":
                    self.mostrar_menu_empleados()
                elif opcion == "4":
                    self.mostrar_menu_vehiculos()
                elif opcion == "5":
                    self.mostrar_menu_tipos_vehiculo()
                elif opcion == "6":
                    self.mostrar_menu_contratos()
                elif opcion == "7":
                    self.mostrar_menu_pagos()
                elif opcion == "0":
                    print("Saliendo del sistema...")
                    break
                else:
                    print("Opción inválida")
        finally:
            self.db.close()

    # ---------------- MENÚ PRINCIPAL ----------------
    def mostrar_menu_principal(self):
        print("\n" + "=" * 50)
        print("         MENU PRINCIPAL")
        print("=" * 50)
        print("1. Gestion de Usuarios")
        print("2. Gestion de Clientes")
        print("3. Gestion de Empleados")
        print("4. Gestion de Vehiculos")
        print("5. Gestion de Tipos de Vehiculos")
        print("6. Gestion de Contratos")
        print("7. Gestion de Pagos")
        print("0. Salir")
        print("=" * 50)

    # ---------------- USUARIOS ----------------
    def mostrar_menu_usuarios(self):
        print("\n--- GESTION DE USUARIOS ---")
        print("1. Crear Usuario")
        print("2. Listar Usuarios")
        print("3. Actualizar Usuario")
        print("4. Eliminar Usuario")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            usuario = self.usuario_crud.crear_usuario(
                username=username, password=password
            )
            print("Usuario creado:", usuario)
        elif opcion == "2":
            usuarios = self.usuario_crud.obtener_usuarios()
            for u in usuarios:
                print(
                    f"{u.id} - {u.username} ({u.rol.value}) - {'Activo' if u.estado else 'Inactivo'}"
                )
        elif opcion == "3":
            uid = input("ID Usuario: ")
            nuevo_username = input("Nuevo username (opcional): ").strip() or None
            nueva_clave = getpass.getpass("Nueva clave (opcional): ") or None
            usuario = self.usuario_crud.actualizar_usuario(
                uid, username=nuevo_username, password=nueva_clave
            )
            print("Usuario actualizado:", usuario)
        elif opcion == "4":
            uid = input("ID Usuario: ")
            if self.usuario_crud.eliminar_usuario(uid):
                print("Usuario eliminado")
            else:
                print("Usuario no encontrado")

    # ---------------- CLIENTES ----------------
    def mostrar_menu_clientes(self):
        print("\n--- GESTION DE CLIENTES ---")
        print("1. Crear Cliente")
        print("2. Listar Clientes")
        print("3. Actualizar Cliente")
        print("4. Eliminar Cliente")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ").strip()
            email = input("Email: ").strip()
            telefono = input("Teléfono (opcional): ").strip() or None
            try:
                cliente = self.cliente_crud.crear_cliente(
                    nombre=nombre, email=email, telefono=telefono
                )
                print("Cliente creado:", cliente)
            except ValueError as e:
                print("ERROR:", str(e))

        elif opcion == "2":
            clientes = self.cliente_crud.obtener_clientes()
            for c in clientes:
                print(
                    f"{c.id} - {c.nombre} - {c.email} - {c.telefono or 'N/A'} - {'Activo' if c.activo else 'Inactivo'}"
                )

        elif opcion == "3":
            cid = input("ID Cliente: ").strip()
            nuevo_nombre = input("Nuevo nombre (opcional): ").strip() or None
            nuevo_email = input("Nuevo email (opcional): ").strip() or None
            nuevo_telefono = input("Nuevo teléfono (opcional): ").strip() or None
            try:
                cliente = self.cliente_crud.actualizar_cliente(
                    cid, nombre=nuevo_nombre, email=nuevo_email, telefono=nuevo_telefono
                )
                if cliente:
                    print("Cliente actualizado:", cliente)
                else:
                    print("Cliente no encontrado")
            except ValueError as e:
                print("ERROR:", str(e))

        elif opcion == "4":
            cid = input("ID Cliente: ").strip()
            if self.cliente_crud.eliminar_cliente(cid):
                print("Cliente eliminado")
            else:
                print("Cliente no encontrado")

    # ---------------- EMPLEADOS ----------------
    def mostrar_menu_empleados(self):
        print("\n--- GESTION DE EMPLEADOS ---")
        print("1. Crear Empleado")
        print("2. Listar Empleados")
        print("3. Actualizar Empleado")
        print("4. Eliminar Empleado")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ").strip()
            email = input("Email: ").strip()
            rol = input("Rol (por defecto Asesor): ").strip() or "Asesor"
            activo = input("¿Activo? (s/n): ").strip().lower() != "n"
            try:
                empleado = self.empleado_crud.crear_empleado(
                    nombre=nombre, email=email, rol=rol, activo=activo
                )
                print("Empleado creado:", empleado)
            except ValueError as e:
                print("ERROR:", str(e))

        elif opcion == "2":
            solo_activos = input("¿Listar solo activos? (s/n): ").strip().lower() == "s"
            empleados = self.empleado_crud.obtener_empleados(solo_activos=solo_activos)
            for e in empleados:
                print(
                    f"{e.id} - {e.nombre} - {e.email} - Rol: {e.rol} - {'Activo' if e.activo else 'Inactivo'}"
                )

        elif opcion == "3":
            from uuid import UUID

            try:
                eid = UUID(input("ID Empleado: ").strip())
                nuevo_nombre = input("Nuevo nombre (opcional): ").strip() or None
                nuevo_email = input("Nuevo email (opcional): ").strip() or None
                nuevo_rol = input("Nuevo rol (opcional): ").strip() or None
                activo_input = (
                    input("¿Activo? (s/n, dejar vacío para no cambiar): ")
                    .strip()
                    .lower()
                )
                nuevo_activo = None
                if activo_input == "s":
                    nuevo_activo = True
                elif activo_input == "n":
                    nuevo_activo = False

                empleado = self.empleado_crud.actualizar_empleado(
                    eid,
                    nombre=nuevo_nombre,
                    email=nuevo_email,
                    rol=nuevo_rol,
                    activo=nuevo_activo,
                )
                if empleado:
                    print("Empleado actualizado:", empleado)
                else:
                    print("Empleado no encontrado")
            except ValueError as e:
                print("ERROR:", str(e))
            except Exception:
                print("ERROR: ID inválido, debe ser UUID")

        elif opcion == "4":
            from uuid import UUID

            try:
                eid = UUID(input("ID Empleado: ").strip())
                if self.empleado_crud.eliminar_empleado(eid):
                    print("Empleado eliminado")
                else:
                    print("Empleado no encontrado")
            except Exception:
                print("ERROR: ID inválido, debe ser UUID")

    # ---------------- VEHICULOS ----------------
    def mostrar_menu_vehiculos(self):
        print("\n--- GESTION DE VEHICULOS ---")
        print("1. Crear Vehículo")
        print("2. Listar Vehículos")
        print("3. Actualizar Vehículo")
        print("4. Eliminar Vehículo")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            marca = input("Marca: ").strip()
            modelo = input("Modelo: ").strip()
            from uuid import UUID

            try:
                tipo_id = UUID(input("ID Tipo de Vehículo: ").strip())
                placa = input("Placa (opcional): ").strip() or None
                disponible = input("¿Disponible? (s/n): ").strip().lower() != "n"
                try:
                    vehiculo = self.vehiculo_crud.crear_vehiculo(
                        marca=marca,
                        modelo=modelo,
                        tipo_id=tipo_id,
                        placa=placa,
                        disponible=disponible,
                    )
                    print("Vehículo creado:", vehiculo)
                except ValueError as e:
                    print("ERROR:", str(e))
            except Exception:
                print("ERROR: ID de Tipo inválido, debe ser UUID")

        elif opcion == "2":
            vehiculos = self.vehiculo_crud.obtener_vehiculos()
            for v in vehiculos:
                print(
                    f"{v.id} - {v.marca} {v.modelo} - Placa: {v.placa or 'N/A'} "
                    f"- {'Disponible' if v.disponible else 'No disponible'} - TipoID: {v.tipo_id}"
                )

        elif opcion == "3":
            from uuid import UUID

            try:
                vid = UUID(input("ID Vehículo: ").strip())
                nueva_marca = input("Nueva marca (opcional): ").strip() or None
                nuevo_modelo = input("Nuevo modelo (opcional): ").strip() or None
                nueva_placa = input("Nueva placa (opcional): ").strip() or None
                disponible_input = (
                    input("¿Disponible? (s/n, vacío = no cambiar): ").strip().lower()
                )
                nuevo_disponible = None
                if disponible_input == "s":
                    nuevo_disponible = True
                elif disponible_input == "n":
                    nuevo_disponible = False

                vehiculo = self.vehiculo_crud.actualizar_vehiculo(
                    vid,
                    marca=nueva_marca,
                    modelo=nuevo_modelo,
                    placa=nueva_placa,
                    disponible=nuevo_disponible,
                )
                if vehiculo:
                    print("Vehículo actualizado:", vehiculo)
                else:
                    print("Vehículo no encontrado")
            except ValueError as e:
                print("ERROR:", str(e))
            except Exception:
                print("ERROR: ID inválido, debe ser UUID")

        elif opcion == "4":
            from uuid import UUID

            try:
                vid = UUID(input("ID Vehículo: ").strip())
                if self.vehiculo_crud.eliminar_vehiculo(vid):
                    print("Vehículo eliminado")
                else:
                    print("Vehículo no encontrado")
            except Exception:
                print("ERROR: ID inválido, debe ser UUID")

    # ---------------- TIPO VEHICULOS ----------------
    def mostrar_menu_tipos_vehiculo(self):
        print("\n--- GESTION DE TIPOS DE VEHICULO ---")
        print("1. Crear Tipo de Vehículo")
        print("2. Listar Tipos de Vehículo")
        print("3. Actualizar Tipo de Vehículo")
        print("4. Eliminar Tipo de Vehículo")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ").strip()
            descripcion = input("Descripción (opcional): ").strip() or None
            activo = input("¿Activo? (s/n): ").strip().lower() != "n"
            try:
                tipo = self.tipo_vehiculo_crud.crear_tipo_vehiculo(
                    nombre=nombre, descripcion=descripcion, activo=activo
                )
                print("Tipo de Vehículo creado:", tipo)
            except ValueError as e:
                print("ERROR:", str(e))

        elif opcion == "2":
            tipos = self.tipo_vehiculo_crud.obtener_tipos_vehiculo()
            for t in tipos:
                print(
                    f"{t.id} - {t.nombre} - {t.descripcion or 'Sin descripción'} "
                    f"- {'Activo' if t.activo else 'Inactivo'}"
                )

        elif opcion == "3":
            from uuid import UUID

            try:
                tid = UUID(input("ID Tipo de Vehículo: ").strip())
                nuevo_nombre = input("Nuevo nombre (opcional): ").strip() or None
                nueva_desc = input("Nueva descripción (opcional): ").strip() or None
                activo_input = (
                    input("¿Activo? (s/n, vacío = no cambiar): ").strip().lower()
                )
                nuevo_activo = None
                if activo_input == "s":
                    nuevo_activo = True
                elif activo_input == "n":
                    nuevo_activo = False

                tipo = self.tipo_vehiculo_crud.actualizar_tipo_vehiculo(
                    tid,
                    nombre=nuevo_nombre,
                    descripcion=nueva_desc,
                    activo=nuevo_activo,
                )
                if tipo:
                    print("Tipo de Vehículo actualizado:", tipo)
                else:
                    print("Tipo de Vehículo no encontrado")
            except ValueError as e:
                print("ERROR:", str(e))
            except Exception:
                print("ERROR: ID inválido, debe ser UUID")

        elif opcion == "4":
            from uuid import UUID

            try:
                tid = UUID(input("ID Tipo de Vehículo: ").strip())
                if self.tipo_vehiculo_crud.eliminar_tipo_vehiculo(tid):
                    print("Tipo de Vehículo eliminado")
                else:
                    print("Tipo de Vehículo no encontrado")
            except Exception:
                print("ERROR: ID inválido, debe ser UUID")

    # ---------------- CONTRATOS ----------------
    def mostrar_menu_contratos(self):
        print("\n--- GESTION DE CONTRATOS ---")
        print("(Implementar CRUD completo segun ContratoCRUD)")

    # ---------------- PAGOS ----------------
    def mostrar_menu_pagos(self):
        print("\n--- GESTION DE PAGOS ---")
        print("(Implementar CRUD completo segun PagoCRUD)")


def main():
    with SistemaGestion() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()
