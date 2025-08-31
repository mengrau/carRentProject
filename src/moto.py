import re
from src.vehiculo import Vehiculo


class Moto(Vehiculo):
    def __init__(self, marca, modelo, valorDia, cilindrada:int, placa:str):
        super().__init__(marca, modelo, valorDia)
        self.cilindrada = cilindrada
        self.placa = placa
    
    def validarPlacaMoto(placa: str) -> bool:
        patron = r'^[A-Z]{3}[0-9]{2}[A-Z]{1}$'
        return bool(re.match(patron, placa.upper()))