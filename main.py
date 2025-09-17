"""
Sistema de gestion con ORM SQLAlchemy y Neon PostgreSQL
Incluye autenticacion con login y CRUD para todas las entidades
"""

import getpass
from typing import Optional

import crud

from database.config import SessionLocal, create_tables
from entities.usuario import Usuario


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
                    self.mostrar_menu_tipo_vehiculos()
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
            usuario = self.usuario_crud.crear_usuario(username=username, password=password)
            print("Usuario creado:", usuario)
        elif opcion == "2":
            usuarios = self.usuario_crud.obtener_usuarios()
            for u in usuarios:
                print(f"{u.id} - {u.username} ({u.rol.value}) - {'Activo' if u.estado else 'Inactivo'}")
        elif opcion == "3":
            uid = input("ID Usuario: ")
            nuevo_username = input("Nuevo username (opcional): ").strip() or None
            nueva_clave = getpass.getpass("Nueva clave (opcional): ") or None
            usuario = self.usuario_crud.actualizar_usuario(uid, username=nuevo_username, password=nueva_clave)
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
        print("(Implementar CRUD completo segun ClienteCRUD)")

    # ---------------- EMPLEADOS ----------------
    def mostrar_menu_empleados(self):
        print("\n--- GESTION DE EMPLEADOS ---")
        print("(Implementar CRUD completo segun EmpleadoCRUD)")

    # ---------------- VEHICULOS ----------------
    def mostrar_menu_vehiculos(self):
        print("\n--- GESTION DE VEHICULOS ---")
        print("(Implementar CRUD completo segun VehiculoCRUD)")

    # ---------------- TIPO VEHICULOS ----------------
    def mostrar_menu_tipo_vehiculos(self):
        print("\n--- GESTION DE TIPO DE VEHICULOS ---")
        print("(Implementar CRUD completo segun TipoVehiculoCRUD)")

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
