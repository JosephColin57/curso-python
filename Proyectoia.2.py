import random
numero = random.randint(1, 100)

print('¡Bienvenido al juego de adivinar el número!')
print('Estoy pensando en un número entre 1 y 100. ¿Puedes adivinarlo?')
intentos = 0
max_intentos = 10

while intentos < max_intentos:
    intentos += 1
    adivinanza = int(input('Ingresa tu adivinanza: '))
    if adivinanza < numero:
        print('Demasiado bajo. Intenta de nuevo.')
    elif adivinanza > numero:
        print('Demasiado alto. Intenta de nuevo.')
    else:
        print(f'¡Felicidades! Adivinaste el número {numero} en {intentos} intentos.')
        break
else:
    print(f'Lo siento, no lograste adivinar el número. Era {numero}.')


# ----------------------------------------------------------------------------------

secreto = lambda: random.randint(1, 100)

adivinanza = lambda: int(input('Ingresa tu adivinanza: '))

intentos = 0
max_intentos = 10

def verificar(adivinanza, secreto):
        adivinanza = int(input('Ingresa tu adivinanza: '))
        if adivinanza < secreto():
            print('Demasiado bajo. Intenta de nuevo.')
        elif adivinanza > secreto():
            print('Demasiado alto. Intenta de nuevo.')
        else:
            print(f'¡Felicidades! Adivinaste el número {secreto()} en {intentos} intentos.')
            return True
        

print('¡Bienvenido al juego de adivinar el número!')
print('Estoy pensando en un número entre 1 y 100. ¿Puedes adivinarlo?')

while intentos < max_intentos:
    intentos += 1
    if verificar(adivinanza, secreto):
        break
else:
    print(f'Lo siento, no lograste adivinar el número. Era {secreto()}.')