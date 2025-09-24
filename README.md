# 🚗 Sistema de Gestión de Alquiler de Vehículos

Sistema de gestión desarrollado en **Python 3**, con **SQLAlchemy ORM** y base de datos **PostgreSQL (Neon)**.  
Incluye autenticación de usuarios con login, creación automática de un administrador por defecto y operaciones **CRUD** para todas las entidades principales.

---

## 📂 Estructura del Proyecto

```bash
├── auth/
│   └── security.py
│
├── crud/                # Lógica CRUD por entidad
│   ├── clienteCRUD.py
│   ├── contratoCRUD.py
│   ├── empleadoCRUD.py
│   ├── pagoCRUD.py
│   ├── tipoVehiculoCRUD.py
│   ├── usuarioCRUD.py
│   └── vehiculoCRUD.py
│
├── database/            # Configuración de base de datos
│   └── config.py
│
├── entities/            # Modelos de base de datos
│   ├── cliente.py
│   ├── contrato.py
│   ├── empleado.py
│   ├── pago.py
│   ├── tipoVehiculo.py
│   ├── usuario.py
│   └── vehiculo.py
│
├── migrations/          # Migraciones con Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── src/                 # Archivos adicionales
│
├── main.py              # Punto de entrada principal
├── requirements.txt     # Dependencias del proyecto
└── README.md
```

---

## ▶️ Ejecución del Sistema

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/mengrau/carRentProject.git
   cd carRentProject
   ```

2. **Crear y activar entorno virtual (opcional pero recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Linux/Mac
   venv\Scripts\activate      # En Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   Crear un archivo `.env` en la raíz del proyecto con la conexión a Neon PostgreSQL:
   ```env
   DATABASE_URL='postgresql://neondb_owner:npg_Rsx6ZGyTC4Qk@ep-solitary-cake-ad9x7js3-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
   ```

5. **Ejecutar el sistema**
   ```bash
   python main.py
   ```

6. **Usuario administrador por defecto**
   - Usuario: `admin`  
   - Contraseña: `admin123`

---

## 🧩 Lógica de Negocio

- **Autenticación:**  
  El sistema solicita credenciales y valida usuarios contra la base de datos.  
  Si no existe un administrador, se crea automáticamente.

- **Gestión de Usuarios:**  
  Crear, listar, actualizar y eliminar usuarios del sistema.  
  Roles soportados: `admin`, `empleado`.

- **Clientes:**  
  CRUD completo de clientes con validación de email único.

- **Empleados:**  
  Administración de personal con rol y estado activo/inactivo.

- **Vehículos y Tipos de Vehículo:**  
  - Registro de vehículos con placa, marca, modelo y disponibilidad.  
  - Clasificación de vehículos por tipo.  

- **Contratos:**  
  - Asociar cliente, empleado y vehículo en un contrato.  
  - Control de fechas de inicio y fin.  
  - Estado activo/inactivo.  

- **Pagos:**  
  - Registro de pagos asociados a contratos.  
  - Permite listar, actualizar y eliminar pagos.

---

## 🛠 Tecnologías Utilizadas
- Python 3
- SQLAlchemy ORM
- PostgreSQL (Neon)
- Alembic (migraciones)
- dotenv (variables de entorno)

---
