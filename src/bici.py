from src.vehiculo import Vehiculo

class Bici(Vehiculo):
    def __init__(self, marca, modelo, valorDia, tipo:str):
        super().__init__(marca, modelo, valorDia)
        self.tipo = tipo