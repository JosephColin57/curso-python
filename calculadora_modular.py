suma = lambda a, b: a + b
resta = lambda a, b: a - b
multiplicacion = lambda a, b: a * b
division = lambda a, b: a / b if b != 0 else 'Error: División por cero'
division_entera = lambda a, b: a // b if b != 0 else 'Error: División por cero'
resto = lambda a, b: a % b if b != 0 else 'Error: División por cero'
potencia = lambda a, b: a ** b

def ejecutar_operacion(operacion, a, b):
    if operacion == "1":
        return suma(a, b)
    elif operacion == "2":
        return resta(a, b)
    elif operacion == "3":
        return multiplicacion(a, b)
    elif operacion == "4":
        return division(a, b) 
    elif operacion == "5":
        return division_entera(a, b)
    elif operacion == "6":
        return resto(a, b)
    elif operacion == "7":
        return potencia(a, b)
    else:
        return "Opción no válida"


def mostrar_menu():
    print("\nSeleccione una operación:")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    print("5. División entera")
    print("6. Resto")
    print("7. Potencia")
    print("0. Salir")

while True:
    mostrar_menu()
    opcion = input("Opción: ")

    if opcion == "0":
        print("¡Hasta luego!")
        break

    if opcion in ["1", "2", "3", "4", "5", "6", "7"]:
        num1 = float(input('Ingrese el primer número: '))
        num2 = float(input('Ingrese el segundo número: '))

        resultado = ejecutar_operacion(opcion, num1, num2)
        print(f'Resultado: {resultado}')
    else:
        print("Opción no válida. Por favor, intente de nuevo.") 