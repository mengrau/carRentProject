from src.vehiculo import Vehiculo
import re
class Auto(Vehiculo):
    def init(self, marca, modelo, valorDia , numPuertas: int, placa: str):
        super().init(marca, modelo, valorDia)
        self.numPuertas = numPuertas
        self.placa = placa


    def validarPlacaAuto(placa: str) -> bool:
        patron = r'^[A-Z]{3}[0-9]{3}$'
        return bool(re.match(patron, placa.upper()))
    