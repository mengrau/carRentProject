# Sistema de Alquiler de Vehículos

Este proyecto implementa un **sistema de alquiler de automóviles, motocicletas y bicicletas** en Python. Permite **registrar, mostrar, alquilar, devolver y eliminar** vehículos mediante un menú interactivo por consola.

---

## 🚀 Requisitos

* **Python 3.10+**
* Git (opcional, para clonar el repositorio)

No requiere librerías externas adicionales.

---

## 📂 Estructura de carpetas

```
mi_proyecto/
├─ src/
│  ├─ __init__.py
│  ├─ vehiculo.py
│  ├─ auto.py
│  ├─ moto.py
│  ├─ bici.py
│  └─ sistemaAlquiler.py
├─ main.py
└─ README.md
```

---

## ⚙️ Instalación

### 1. Clonar o descargar el repositorio

```bash
git clone <https://github.com/mengrau/carRentProject.git>
cd mi_proyecto
```

O descarga el ZIP y descomprímelo.

### 2. Crear y activar entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> Este paso es opcional, pero recomendado.

### 3. Instalar dependencias (si aplicas)

Si no tienes `requirements.txt`, puedes omitir este paso.

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

Ejecuta el programa desde la raíz del proyecto:

**Windows:**

```powershell
python .\main.py
```

**macOS / Linux:**

```bash
python3 ./main.py
```

---

## 📖 Uso del sistema

Al iniciar, se muestra un menú interactivo:

```
---------- MENÚ ----------
1. Ingresar nuevo vehículo
2. Mostrar disponibilidad
3. Alquilar vehículo
4. Devolver vehículo
5. Retirar vehículo
6. Salir
```

### 1. Ingresar nuevo vehículo

* Selecciona si deseas ingresar un **automóvil, motocicleta o bicicleta**.
* Ingresa sus datos (marca, modelo, placa o chasis, valor por día, etc.).
* El sistema valida automáticamente las placas de autos y motos con expresiones regulares.

### 2. Mostrar disponibilidad

Lista los vehículos registrados indicando:

* Tipo (Automóvil, Motocicleta, Bicicleta)
* Marca y modelo
* Identificador (placa o chasis)
* Estado (**Disponible** o **Ocupado**)
* Valor por día

### 3. Alquilar vehículo

* Muestra el inventario con índices.
* Selecciona el índice y número de días.
* El sistema marca el vehículo como ocupado y calcula el costo.

### 4. Devolver vehículo

* Ingresa el identificador (placa o chasis).
* El sistema cambia el estado a **Disponible**.

### 5. Retirar vehículo

* Ingresa el identificador (placa o chasis).
* El vehículo se elimina del inventario.

### 6. Salir

Finaliza el programa.

---

## 🧑‍💻 Uso programático (ejemplo en Python)

```python
from src.auto import Auto
from src.moto import Moto
from src.bici import Bici
from src.sistemaAlquiler import sistemaAlquiler

sistema = sistemaAlquiler()
sistema.agregarVehiculo(Auto("Toyota", "Corolla", 80000, 4, "ABC123"))
sistema.agregarVehiculo(Moto("Honda", "CBR", 50000, 150, "XYZ12A"))
sistema.agregarVehiculo(Bici("Trek", "X-Caliber", 20000, "Montaña", "CHS1234"))

sistema.mostrarInventario()
costo = sistema.rentarVehiculo(0, 3)
print("Costo total:", costo)
sistema.devolverVehiculo("ABC123")
```

---

## ❗ Errores comunes

* **`ModuleNotFoundError: No module named 'src'`** → Ejecuta el programa desde la raíz y asegúrate de tener `__init__.py` en `src/`.
* **Placa inválida** → El sistema valida que:

  * Auto: 3 letras + 3 números (ej: `ABC123`)
  * Moto: 3 letras + 2 números + 1 letra opcional (ej: `XYZ12A`)

---

## 📜 Licencia

Este proyecto es de uso libre para fines educativos.
