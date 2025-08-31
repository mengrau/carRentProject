from src.auto import Auto
'''from src.bici import Bici
from src.moto import Moto'''
#from src.sistemaAlquiler import sistemaAlquiler

class main:
    menu = """
        ----------MENU----------
        1. Ingresar nuevo vehiculo
        2. Mostrar disponibilidad
        3. Alquilar vehiculo
        4. Devolver vehiculo
        5. Retirar vehiculo
        6. Salir
        """
    while True:
        print(menu)
        opcion = int(input("Elige una opcion: "))
        match opcion:
            case 1:
                tipo = int(input("""
        Ingrese el tipo de vehiculo
        1. Auto
        2. Moto 
        3. Bicicleta
        """))
                if tipo == 1:
                    while True:
                        placa = (input("Ingrese la placa del automovil: "))
                        if Auto.validarPlacaAuto(placa):
                            break
                        else:
                            print("Formato de placa invalido")
                    marca = (input("Ingrese la marca del automovil: ").capitalize)
                    modelo = (input("Ingrese la referencia del automovil: ").capitalize)
                    valorDia = (input("Ingrese el valor por dia del automovil: ").capitalize)
                    numPuertas = (input("Ingrese la cantidad de puertas automovil: ").capitalize)
                    #sistemaAlquiler.agregarVehiculo(Auto(marca, modelo, valorDia, numPuertas))
            case 2:
                print("Mostrar disponibilidad")
                
            case 3:
                print("Rentar vehículo")
            case 4:
                print("Devolver vehículo")
            case 5:
                print("Retirar vehículo")
            case 6:
                print("Salir")
            case _:
                print("Opción no válida")
        break