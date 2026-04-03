num1 = int(input('Ingrese un número: '))
num2 = int(input('Ingrese otro número: '))

print(f'Suma:             {num1 + num2}')
print(f'Resta:            {num1 - num2}')
print(f'Multiplicación:   {num1 * num2}')
print(f'División:         {round(num1 / num2, 2)}')
print(f'División entera:  {num1 // num2}')
print(f'Resto:            {num1 % num2}')
print(f'Potencia:         {num1 ** num2}')

print(f'¿El primer número es mayor que el segundo? {num1 > num2}')
print(f'¿Los números son iguales? {num1 == num2}')
print(f'¿El primer número es par? {num1 % 2 == 0}')

#----------------------------------------------------------------------
while True:
    valor = float(input('\nIngrese un valor (0 para salir): '))
    
    if valor == 0:
        print('¡Hasta luego!')
        break

    opcion = input("""
Seleccione una opción:
1. Kilómetros a millas
2. Celsius a Fahrenheit
3. Kilogramos a libras
Opción: """)

    if opcion == "1":
        millas = valor * 0.621371
        print(f'{valor} km = {round(millas, 2)} millas')
    elif opcion == "2":
        fahrenheit = (valor * 9/5) + 32
        print(f'{valor} °C = {round(fahrenheit, 2)} °F')
    elif opcion == "3":
        libras = valor * 2.20462
        print(f'{valor} kg = {round(libras, 2)} libras')
    else:
        print('Opción no válida')

#--------------------------------------------------------------------------

edad = int(input('¿Cuántos años tenés? '))
if edad >= 18:
    print('Sos mayor de edad')
elif edad >= 13:
    print('Sos adolescente')
else:
    print('Sos menor de edad')

# --------------------------------------------------------------------------

valor = int(input('De que numero quieres la tabla de multiplicar?: '))

for i in range(1, 11):
    print(f'{valor} x {i} = {valor * i}')


# --------------------------------------------------------------------------

for tabla in range(1, 11):
    print(f'\n--- Tabla del {tabla} ---')
    for i in range(1, 11):
        print(f'{tabla} x {i} = {tabla * i}')