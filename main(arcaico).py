from src.auto import Auto
from src.bici import Bici
from src.moto import Moto
from src.sistemaAlquiler import sistemaAlquiler


class main:
    sistema = sistemaAlquiler()
    menu = """
        ---------- MENÚ ----------
        1. Ingresar nuevo vehículo
        2. Mostrar disponibilidad
        3. Alquilar vehículo
        4. Devolver vehículo
        5. Retirar vehículo
        6. Salir
        """
    while True:
        print(menu)
        opcion = int(input("Elige una opción: "))
        match opcion:
            case 1:
                tipo = int(
                    input(
                        """
        Ingrese el tipo de vehículo
        1. Automóvil
        2. Motocicleta 
        3. Bicicleta
        """
                    )
                )
                while True:
                    if tipo == 1:
                        while True:
                            placa = input("Ingrese la placa del automóvil: ").upper()
                            if Auto.validarPlacaAuto(placa):
                                break
                            else:
                                print("Formato de placa inválido")
                        marca = input("Ingrese la marca del automóvil: ").upper()
                        modelo = input("Ingrese la referencia del automóvil: ").upper()
                        valorDia = int(
                            input("Ingrese el valor por día del automóvil: ")
                        )
                        numPuertas = int(
                            input("Ingrese la cantidad de puertas del automóvil: ")
                        )
                        sistema.agregarVehiculo(
                            Auto(marca, modelo, valorDia, numPuertas, placa)
                        )
                        break
                    elif tipo == 2:
                        while True:
                            placa = input(
                                "Ingrese la placa de la motocicleta: "
                            ).upper()
                            if Moto.validarPlacaMoto(placa):
                                break
                            else:
                                print("Formato de placa inválido")
                        marca = input("Ingrese la marca de la motocicleta: ").upper()
                        modelo = input(
                            "Ingrese la referencia de la motocicleta: "
                        ).upper()
                        valorDia = int(
                            input("Ingrese el valor por día de la motocicleta: ")
                        )
                        cilindrada = int(
                            input("Ingrese el cilindraje de la motocicleta: ")
                        )
                        sistema.agregarVehiculo(
                            Moto(marca, modelo, valorDia, cilindrada, placa)
                        )
                        break
                    elif tipo == 3:
                        numChasis = input(
                            "Ingrese el número de chasis de la bicicleta: "
                        )
                        marca = input("Ingrese la marca de la bicicleta: ").upper()
                        modelo = input(
                            "Ingrese la referencia de la bicicleta: "
                        ).upper()
                        valorDia = int(
                            input("Ingrese el valor por día de la bicicleta: ")
                        )
                        tipoBici = input("Ingrese el tipo de bicicleta: ")
                        sistema.agregarVehiculo(
                            Bici(marca, modelo, valorDia, tipoBici, numChasis)
                        )
                        break
                    else:
                        print("Opción no válida")
            case 2:
                print("Vehículos disponibles")
                sistema.mostrarInventario()
            case 3:
                print("Vehículos disponibles")
                sistema.mostrarInventario()
                indice = int(input("Ingrese el índice del vehículo: "))
                dias = int(input("Ingrese la cantidad de días: "))
                sistema.rentarVehiculo(indice, dias)
            case 4:
                sistema.mostrarInventario()
                identificador = input("Ingrese el identificador del vehículo: ").upper()
                sistema.devolverVehiculo(identificador)
            case 5:
                sistema.mostrarInventario()
                identificador = input("Ingrese el identificador del vehículo: ").upper()
                sistema.eliminarVehiculo(identificador)
            case 6:
                print("Gracias por usar el sistema de alquiler.")
                break
            case _:
                print("Opción no válida")
