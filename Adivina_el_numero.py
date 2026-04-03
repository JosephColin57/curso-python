import random

def verificar(adivinanza, secreto, intentos):
    if adivinanza < secreto:
        print('Demasiado bajo. Intentá de nuevo.')
    elif adivinanza > secreto:
        print('Demasiado alto. Intentá de nuevo.')
    else:
        print(f'¡Felicidades! Adivinaste el número {secreto} en {intentos} intentos.')
        return True
    return False

print('¡Bienvenido al juego de adivinar el número!')
print('Estoy pensando en un número entre 1 y 100...')

secreto = random.randint(1, 100)
intentos = 0
max_intentos = 10

while intentos < max_intentos:
    intentos += 1
    adivinanza = int(input(f'Intento {intentos}/{max_intentos} — Tu número: '))
    if verificar(adivinanza, secreto, intentos):
        break
else:
    print(f'¡Se acabaron los intentos! El número era {secreto}.')


    