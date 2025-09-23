from src.vehiculo import Vehiculo


class Bici(Vehiculo):
    def __init__(self, marca, modelo, valorDia, tipo: str, numChasis: str):
        super().__init__(marca, modelo, valorDia)
        self.tipo = tipo
        self.numChasis = numChasis
