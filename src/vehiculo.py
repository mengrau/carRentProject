class Vehiculo:
    def __init__(self, marca:str, modelo:str, valorDia:int):
        self.marca = marca
        self.modelo = modelo
        self.valorDia = valorDia
        self._disponible = True

    def alquilar (self, dias:int)->int:
        if self._disponible:
            self._disponible = False
            costo = dias * self.valorDia
            return costo
        else:
            return None

    def devolver(self):
        self._disponible = True