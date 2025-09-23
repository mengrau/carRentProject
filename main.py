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
from datetime import datetime


def create_admin_user():
    """Crear usuario administrador por defecto"""
    print("\n=== CREANDO USUARIO ADMINISTRADOR ===\n")

    try:
        from database.config import SessionLocal
        from entities.usuario import Usuario, hash_password, RolEnum

        db = SessionLocal()

        # Verificar si ya existe un admin (buscando por rol)
        admin_exists = db.query(Usuario).filter(Usuario.rol == RolEnum.admin).first()

        if admin_exists:
            print(f"[OK] Usuario administrador ya existe: {admin_exists.username}")
            db.close()
            return True

        # Crear usuario admin
        admin_user = Usuario(
            username="admin",
            id_usuario_creacion=None,
            password_hash=hash_password("admin123"),
            rol=RolEnum.admin,
            estado=True,
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"[OK] Usuario administrador creado exitosamente")
        print(f"     ID: {admin_user.id}")
        print(f"     Rol: {admin_user.rol.value}")
        print(f"     Nombre: {admin_user.username}")

        db.close()
        return True

    except Exception as e:
        print(f"[ERROR] Error creando usuario administrador: {e}")
        return False


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
            create_admin_user()

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
                username=username,
                id_usuario_creacion=self.usuario_actual.id,
                password=password,
            )
            print("Usuario creado:", usuario)
        elif opcion == "2":
            usuarios = self.usuario_crud.obtener_usuarios()
            for u in usuarios:
                print(
                    f"{u.id} - {u.username} ({u.rol.value}) - {'Activo' if u.estado else 'Inactivo'}"
                )
        elif opcion == "3":
            username_actual = input("Username actual: ").strip()
            nuevo_username = input("Nuevo username (opcional): ").strip() or None
            nueva_clave = getpass.getpass("Nueva clave (opcional): ") or None

            try:

                usuario_obj = self.usuario_crud.obtener_usuario_por_username(
                    username_actual
                )

                if not usuario_obj:
                    print("Usuario no encontrado con ese username")
                else:
                    usuario = self.usuario_crud.actualizar_usuario(
                        usuario_obj.id,
                        username=nuevo_username,
                        password=nueva_clave,
                        id_usuario_edicion=self.usuario_actual.id,
                    )
                    print("Usuario actualizado:", usuario)

            except ValueError as e:
                print("ERROR:", str(e))

        elif opcion == "4":
            username_actual = input("Username del usuario a eliminar: ").strip()

            try:
                usuario_obj = self.usuario_crud.obtener_usuario_por_username(
                    username_actual
                )

                if not usuario_obj:
                    print("Usuario no encontrado con ese username")
                else:
                    if self.usuario_crud.eliminar_usuario(usuario_obj.id):
                        print("Usuario eliminado")
                    else:
                        print("No se pudo eliminar el usuario")

            except Exception as e:
                print("ERROR:", str(e))
        elif opcion == "0":
            return

        else:
            print("Opción no válida, intente de nuevo")

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
                    nombre=nombre,
                    email=email,
                    telefono=telefono,
                    id_usuario_creacion=self.usuario_actual.id,
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
            email_actual = input("Email actual del cliente: ").strip().lower()
            nuevo_nombre = input("Nuevo nombre (opcional): ").strip() or None
            nuevo_email = input("Nuevo email (opcional): ").strip() or None
            nuevo_telefono = input("Nuevo teléfono (opcional): ").strip() or None
            try:

                cliente_obj = self.cliente_crud.obtener_cliente_por_email(email_actual)

                if not cliente_obj:
                    print("Cliente no encontrado con ese email")
                else:
                    cliente = self.cliente_crud.actualizar_cliente(
                        cliente_obj.id,
                        id_usuario_edicion=self.usuario_actual.id,
                        nombre=nuevo_nombre,
                        email=nuevo_email,
                        telefono=nuevo_telefono,
                    )
                    print("Cliente actualizado:", cliente)

            except ValueError as e:
                print("ERROR:", str(e))

        elif opcion == "4":
            cid = input("ID Cliente: ").strip()
            if self.cliente_crud.eliminar_cliente(cid):
                print("Cliente eliminado")
            else:
                print("Cliente no encontrado")
        elif opcion == "0":
            return
        else:
            print("Opción no válida, intente de nuevo")

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
                    nombre=nombre,
                    email=email,
                    id_usuario_creacion=self.usuario_actual.id,
                    rol=rol,
                    activo=activo,
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
            try:
                email_actual = input("Email actual del empleado: ").strip().lower()

                nuevo_nombre = input("Nuevo nombre (opcional): ").strip() or None

                tmp = input("Nuevo email (opcional): ").strip()
                nuevo_email = tmp.lower() if tmp else None

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

                empleado_obj = self.empleado_crud.obtener_empleado_por_email(
                    email_actual
                )

                if not empleado_obj:
                    print("Empleado no encontrado con ese email")
                else:
                    empleado = self.empleado_crud.actualizar_empleado(
                        empleado_obj.id,
                        id_usuario_edicion=self.usuario_actual.id,
                        nombre=nuevo_nombre,
                        email=nuevo_email,
                        rol=nuevo_rol,
                        activo=nuevo_activo,
                    )
                    if empleado:
                        print("Empleado actualizado:", empleado)
                    else:
                        print("Error al actualizar empleado")
            except ValueError as e:
                print("ERROR:", str(e))
            except Exception as e:
                print("ERROR inesperado:", str(e))

        elif opcion == "4":
            email_actual = input("Email del empleado a eliminar: ").strip().lower()

            try:

                empleado_obj = self.empleado_crud.obtener_empleado_por_email(
                    email_actual
                )

                if not empleado_obj:
                    print("Empleado no encontrado con ese email")
                else:
                    if self.empleado_crud.eliminar_empleado(empleado_obj.id):
                        print("Empleado eliminado")
                    else:
                        print("No se pudo eliminar el empleado")

            except Exception as e:
                print("ERROR:", str(e))

        elif opcion == "0":
            return
        else:
            print("Opción no válida, intente de nuevo")

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
                        id_usuario_creacion=self.usuario_actual.id,
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
            placa_actual = input("Placa actual del vehículo: ").strip().upper()
            nueva_marca = input("Nueva marca (opcional): ").strip() or None
            nuevo_modelo = input("Nuevo modelo (opcional): ").strip() or None
            nueva_placa = input("Nueva placa (opcional): ").strip().upper() or None
            disponible_input = (
                input("¿Disponible? (s/n, vacío = no cambiar): ").strip().lower()
            )

            nuevo_disponible = None
            if disponible_input == "s":
                nuevo_disponible = True
            elif disponible_input == "n":
                nuevo_disponible = False

            try:

                vehiculo_obj = self.vehiculo_crud.obtener_vehiculo_por_placa(
                    placa_actual
                )

                if not vehiculo_obj:
                    print("Vehículo no encontrado con esa placa")
                else:

                    vehiculo = self.vehiculo_crud.actualizar_vehiculo(
                        vehiculo_obj.id,
                        id_usuario_edicion=self.usuario_actual.id,
                        marca=nueva_marca,
                        modelo=nuevo_modelo,
                        placa=nueva_placa,
                        disponible=nuevo_disponible,
                    )
                    print("Vehículo actualizado:", vehiculo)

            except ValueError as e:
                print("ERROR:", str(e))

        elif opcion == "4":
            placa_actual = input("Placa del vehículo a eliminar: ").strip().upper()
            try:

                vehiculo_obj = self.vehiculo_crud.obtener_vehiculo_por_placa(
                    placa_actual
                )

                if not vehiculo_obj:
                    print("Vehículo no encontrado con esa placa")
                else:
                    if self.vehiculo_crud.eliminar_vehiculo(vehiculo_obj.id):
                        print("Vehículo eliminado")
                    else:
                        print("Error al eliminar el vehículo")
            except Exception as e:
                print("ERROR:", str(e))
        elif opcion == "0":
            return
        else:
            print("Opción no válida, intente de nuevo")

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
                    nombre=nombre,
                    id_usuario_cracion=self.usuario_actual.id,
                    descripcion=descripcion,
                    activo=activo,
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
                    id_usuario_edicion=self.usuario_actual.id,
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
        elif opcion == "0":
            return
        else:
            print("Opción no válida, intente de nuevo")

    # ---------------- CONTRATOS ----------------
    def mostrar_menu_contratos(self):

        print("\n--- GESTION DE CONTRATOS ---")
        print("1. Crear Contrato (con pago obligatorio)")
        print("2. Listar Contratos")
        print("3. Obtener Contrato por ID")
        print("4. Actualizar Contrato")
        print("5. Eliminar Contrato")
        print("6. Gestionar Pagos de un Contrato")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            try:
                cliente_id = UUID(input("ID Cliente: ").strip())
                vehiculo_id = UUID(input("ID Vehículo: ").strip())
                empleado_id = UUID(input("ID Empleado: ").strip())
                fecha_inicio = datetime.fromisoformat(
                    input("Fecha inicio (YYYY-MM-DD): ").strip()
                )
                fecha_fin_input = input("Fecha fin (YYYY-MM-DD, opcional): ").strip()
                fecha_fin = (
                    datetime.fromisoformat(fecha_fin_input) if fecha_fin_input else None
                )

                contrato = self.contrato_crud.crear_contrato(
                    cliente_id=cliente_id,
                    vehiculo_id=vehiculo_id,
                    empleado_id=empleado_id,
                    id_usuario_creacion=self.usuario_actual.id,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                )
                print("Contrato creado:", contrato)

                monto = float(
                    input("Monto inicial del contrato (obligatorio): ").strip()
                )
                fecha_pago_input = input(
                    "Fecha del pago (YYYY-MM-DD, opcional): "
                ).strip()
                fecha_pago = (
                    datetime.fromisoformat(fecha_pago_input)
                    if fecha_pago_input
                    else None
                )
                pago = self.pago_crud.crear_pago(
                    contrato_id=contrato.id, monto=monto, fecha_pago=fecha_pago
                )
                print("Pago registrado automáticamente:", pago)

            except Exception as e:
                print("ERROR:", str(e))

        elif opcion == "2":
            try:
                activos_input = input("¿Solo activos? (s/n): ").strip().lower()
                solo_activos = activos_input == "s"
                contratos = self.contrato_crud.obtener_contratos(
                    solo_activos=solo_activos
                )
                for c in contratos:
                    print(
                        f"{c.id} - Cliente: {c.cliente_id} - Vehículo: {c.vehiculo_id} "
                        f"- Empleado: {c.empleado_id} - Inicio: {c.fecha_inicio} "
                        f"- Fin: {c.fecha_fin or 'N/A'} - {'Activo' if c.activo else 'Inactivo'}"
                    )
            except Exception as e:
                print("ERROR:", str(e))

        elif opcion == "3":
            try:
                cid = UUID(input("ID Contrato: ").strip())
                contrato = self.contrato_crud.obtener_contrato(cid)
                if contrato:
                    print(
                        f"{contrato.id} - Cliente: {contrato.cliente_id} - Vehículo: {contrato.vehiculo_id} "
                        f"- Empleado: {contrato.empleado_id} - Inicio: {contrato.fecha_inicio} "
                        f"- Fin: {contrato.fecha_fin or 'N/A'} - {'Activo' if contrato.activo else 'Inactivo'}"
                    )
                    pagos = self.pago_crud.obtener_pagos(contrato_id=contrato.id)
                    if pagos:
                        print("Pagos asociados:")
                        for p in pagos:
                            print(
                                f"   Pago {p.id} - Monto: {p.monto} - Fecha: {p.fecha_pago}"
                            )
                    else:
                        print("   No hay pagos registrados.")
                else:
                    print("Contrato no encontrado")
            except Exception:
                print("ERROR: ID inválido, debe ser UUID")

        elif opcion == "4":
            try:
                cid = UUID(input("ID Contrato: ").strip())
                nuevo_inicio = input(
                    "Nueva fecha inicio (YYYY-MM-DD, opcional): "
                ).strip()
                nuevo_fin = input("Nueva fecha fin (YYYY-MM-DD, opcional): ").strip()
                nuevo_activo_input = (
                    input("¿Activo? (s/n, vacío = no cambiar): ").strip().lower()
                )

                kwargs = {}
                if nuevo_inicio:
                    kwargs["fecha_inicio"] = datetime.fromisoformat(nuevo_inicio)
                if nuevo_fin:
                    kwargs["fecha_fin"] = datetime.fromisoformat(nuevo_fin)
                if nuevo_activo_input == "s":
                    kwargs["activo"] = True
                elif nuevo_activo_input == "n":
                    kwargs["activo"] = False

                contrato = self.contrato_crud.actualizar_contrato(
                    cid, id_usuario_edicion=self.usuario_actual.id, **kwargs
                )
                if contrato:
                    print("Contrato actualizado:", contrato)
                else:
                    print("Contrato no encontrado")
            except Exception as e:
                print("ERROR:", str(e))

        elif opcion == "5":
            try:
                cid = UUID(input("ID Contrato: ").strip())
                if self.contrato_crud.eliminar_contrato(cid):
                    print("Contrato eliminado")
                else:
                    print("Contrato no encontrado")
            except Exception:
                print("ERROR: ID inválido, debe ser UUID")

        elif opcion == "6":
            self.mostrar_menu_pagos()

        elif opcion == "0":
            return
        else:
            print("Opción inválida")

    # ---------------- PAGOS ----------------
    def mostrar_menu_pagos(self):
        print("\n--- GESTION DE PAGOS ---")
        print("1. Listar Pagos de un Contrato")
        print("2. Actualizar Pago")
        print("3. Eliminar Pago")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            try:
                contrato_id = UUID(input("ID Contrato: ").strip())
                pagos = self.pago_crud.obtener_pagos(contrato_id=contrato_id)
                if pagos:
                    for p in pagos:
                        print(f"{p.id} - Monto: {p.monto} - Fecha: {p.fecha_pago}")
                else:
                    print("No hay pagos para este contrato")
            except Exception as e:
                print("ERROR:", str(e))

        elif opcion == "2":
            try:
                pago_id = UUID(input("ID Pago: ").strip())
                nuevo_monto = input("Nuevo monto (opcional): ").strip()
                nueva_fecha = input("Nueva fecha (YYYY-MM-DD, opcional): ").strip()
                kwargs = {}
                if nuevo_monto:
                    kwargs["monto"] = float(nuevo_monto)
                if nueva_fecha:
                    kwargs["fecha_pago"] = datetime.fromisoformat(nueva_fecha)
                pago = self.pago_crud.actualizar_pago(
                    pago_id, id_usuario_edicion=self.usuario_actual.id, **kwargs
                )
                if pago:
                    print("Pago actualizado:", pago)
                else:
                    print("Pago no encontrado")
            except Exception as e:
                print("ERROR:", str(e))

        elif opcion == "3":
            try:
                pago_id = UUID(input("ID Pago: ").strip())
                if self.pago_crud.eliminar_pago(pago_id):
                    print("Pago eliminado")
                else:
                    print("Pago no encontrado")
            except Exception:
                print("ERROR: ID inválido, debe ser UUID")

        elif opcion == "0":
            return
        else:
            print("Opción inválida")


def main():
    with SistemaGestion() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()
