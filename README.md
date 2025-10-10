# 🚗 Sistema de Gestión de Contratos y Vehículos

Este proyecto es una **API REST** desarrollada con **FastAPI**, diseñada para administrar contratos, clientes, empleados, pagos, usuarios y vehículos.  
El sistema permite crear, leer, actualizar y eliminar información de las entidades principales, manteniendo relaciones entre ellas mediante una base de datos relacional.

---

## 🧩 Características principales

- 🧾 **Gestión completa de contratos** entre clientes, vehículos y empleados.  
- 🚘 **Administración de vehículos** y tipos de vehículo.  
- 💳 **Registro y control de pagos** asociados a los contratos.  
- 👥 **Gestión de usuarios, clientes y empleados.**  
- 🧱 **Modelos relacionales** usando SQLAlchemy.  
- ⚙️ **Migraciones automáticas** con Alembic.  
- 🌐 **Documentación interactiva de la API** generada automáticamente por FastAPI (`/docs` o `/redoc`).

---

## 📂 Estructura del proyecto

```bash
├── Apis/                     # 📡 Endpoints de la API (routers)
│   ├── cliente.py
│   ├── contrato.py
│   ├── empleado.py
│   ├── pago.py
│   ├── tipoVehiculo.py
│   ├── usuario.py
│   └── vehiculo.py
│
├── crud/                     # 🧩 Lógica CRUD por entidad
│   ├── clienteCRUD.py
│   ├── contratoCRUD.py
│   ├── empleadoCRUD.py
│   ├── pagoCRUD.py
│   ├── tipoVehiculoCRUD.py
│   ├── usuarioCRUD.py
│   └── vehiculoCRUD.py
│
├── database/                 # 🗄️ Configuración de base de datos
│   └── config.py
│
├── entities/                 # 🧱 Modelos (SQLAlchemy)
│   ├── cliente.py
│   ├── contrato.py
│   ├── empleado.py
│   ├── pago.py
│   ├── tipoVehiculo.py
│   ├── usuario.py
│   └── vehiculo.py
│
├── migrations/               # 🧬 Migraciones con Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── src/                      # 📦 Código auxiliar (servicios, utilidades, etc.)
│
├── models.py                 # 🧾 Modelos Pydantic (schemas)
│
├── main.py                   # 🚀 Punto de entrada principal
│
├── requirements.txt           # 📋 Dependencias del proyecto
│
└── README.md                  # 📘 Documentación general
```

---

## ⚙️ Instalación y configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/mengrau/carRentProject.git
cd carRentProject
```

### 2️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```


## 🚀 Ejecución del proyecto

Inicia el servidor FastAPI:
```bash
py main.py
```

Por defecto, la API estará disponible en:  
> 🌐 http://127.0.0.1:8000

---

## 🧭 Documentación de la API

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- Redoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧰 Tecnologías utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
- [PostgreSQL](https://www.postgresql.org/) *(adaptable a SQLite o MySQL)*

---

## 🧑‍💻 Autores

**Emmanuel Orozco Muñoz**
**Andrés Felipe Méndez Cano**  
💼 Desarrolladores Backend – Python / FastAPI 

---