class sistemaAlquiler:
    def __init__(self):
        self.vehiculos = []

    def agregarVehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def mostrarDisponibles(self):
        for i, v in enumerate(self.vehiculos):
            estado = "Disponible" if v.disponible else "Ocupado"
            print(f"{i}. {v.marca}{v.modelo}{v.placa}-{estado}-${v.precio_hora}/hora")
    
    def alquilarVehiculo(self, indice:int, dia:int):
        if 0 <= indice < len(self.vehiculos):
            costo = self.vehiculos[indice].alquilar(dia)
            if costo is not None:
                print(f"Vehiculo alquilado por {dia} dias. Costo ${costo}")
            else:
                print("El vehiculo ya esta alquilado.")
        else:
            print("Indice Invalido.")
    
    def devolverVehiculo(self, indice: int):
        if 0 <= indice < len(self.vehiculos):
            self.vehiculos[indice].devolver()
            print("Vehiculo devuelto con exito")
        else:
            print("Indice Inválido.")
    
    def eliminarVehiculo(self, indice:int):
        if 0 <= indice < len(self.vehiculos):
            eliminado = self.vehiculos.pop(indice)
            print(f"Vehiculo {eliminado.marca}{eliminado.modelo}{eliminado.placa} elimindado correctamente.")
        else:
            print("Indice Inválido.")