from src.auto import Auto
from src.bici import Bici
from src.moto import Moto

class sistemaAlquiler:
    def __init__(self):
        self.vehiculos = []

    def existeVehiculo(self, identificador: str) -> bool:
        for v in self.vehiculos:
            if isinstance(v, (Auto, Moto)) and v.placa == identificador:
                return True
            elif isinstance(v, Bici) and v.numChasis == identificador:
                return True
        return False

    def agregarVehiculo(self, vehiculo: object):
        if isinstance(vehiculo, (Auto, Moto)):
            if self.existeVehiculo(vehiculo.placa):
                print(f"Ya existe un vehículo con la placa {vehiculo.placa}. No se agregó.")
                return
        elif isinstance(vehiculo, Bici):
            if self.existeVehiculo(vehiculo.numChasis):
                print(f"Ya existe una bicicleta con el chasis {vehiculo.numChasis}. No se agregó.")
                return
        self.vehiculos.append(vehiculo)
        if isinstance(vehiculo, (Auto, Moto)):
            print(f"Vehículo agregado: {vehiculo.marca} {vehiculo.modelo} {vehiculo.placa}")
        else:
            print(f"Vehículo agregado: {vehiculo.marca} {vehiculo.modelo} {vehiculo.numChasis}")

    def mostrarInventario(self):
        if not self.vehiculos:
            print("No hay vehículos registrados.")
            return

        nombres = {
            "Auto": "Automóvil",
            "Moto": "Motocicleta",
            "Bici": "Bicicleta"
        }

        for i, v in enumerate(self.vehiculos):
            estado = "Disponible" if v._disponible else "Ocupado"
            tipo = nombres.get(v.__class__.__name__)  

            if isinstance(v, (Auto, Moto)):
                print(f"{i}. [{tipo}] {v.marca} {v.modelo} {v.placa} - {estado} - ${v.valorDia}/día")
            else: 
                print(f"{i}. [{tipo}] {v.marca} {v.modelo} {v.numChasis} - {estado} - ${v.valorDia}/día")
    
    def rentarVehiculo(self, indice:int, dias:int):
        if 0 <= indice < len(self.vehiculos):
            costo = self.vehiculos[indice].alquilar(dias)
            if costo is not None:
                print(f"Vehículo alquilado por {dias} días. Costo: ${costo}")
            else:
                print("El vehículo ya está alquilado.")
        else:
            print("Índice inválido.")
    
    def devolverVehiculo(self, identificador: str):
        for vehiculo in self.vehiculos:
            if isinstance(vehiculo, (Auto, Moto)) and vehiculo.placa == identificador:
                if not vehiculo._disponible:
                    vehiculo.devolver()
                    print(f"Vehículo {vehiculo.marca} {vehiculo.modelo} devuelto con éxito.")
                else:
                    print("Este vehículo ya está disponible, no se puede devolver.")
                return
            elif isinstance(vehiculo, Bici) and vehiculo.numChasis == identificador:
                if not vehiculo._disponible:
                    vehiculo.devolver()
                    print(f"Bicicleta {vehiculo.marca} {vehiculo.modelo} devuelta con éxito.")
                else:
                    print("Esta bicicleta ya está disponible, no se puede devolver.")
                return
        print("No se encontró ningún vehículo con ese identificador.")

    def eliminarVehiculo(self, identificador: str):
        for i, vehiculo in enumerate(self.vehiculos):
            if isinstance(vehiculo, (Auto, Moto)) and vehiculo.placa == identificador:
                eliminado = self.vehiculos.pop(i)
                print(f"Vehículo {eliminado.marca} {eliminado.modelo} {eliminado.placa} eliminado correctamente.")
                return
            elif isinstance(vehiculo, Bici) and vehiculo.numChasis == identificador:
                eliminado = self.vehiculos.pop(i)
                print(f"Bicicleta {eliminado.marca} {eliminado.modelo} {eliminado.numChasis} eliminada correctamente.")
                return
        print("No se encontró ningún vehículo con ese identificador.")