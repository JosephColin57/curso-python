contactos = [{'nombre': 'Juan', 'telefono': '123456789', 'email': 'juan@example.com'},
             {'nombre': 'Maria', 'telefono': '987654321', 'email': 'maria@example.com'},
             {'nombre': 'Pedro', 'telefono': '555555555', 'email': 'pedro@example.com'}]

def cargar_contactos():
    contactos = []
    try:
        with open('contactos.txt', 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    nombre, telefono, email = linea.split(',')
                    contactos.append({'nombre': nombre, 'telefono': telefono, 'email': email})
    except FileNotFoundError:
        print('Iniciando con lista vacía.')
    return contactos

def agregar_contacto(contactos):
    nombre = input('Ingrese el nombre: ')
    telefono = input('Ingrese el teléfono: ')
    email = input('Ingrese el email: ')
    contactos.append({'nombre': nombre, 'telefono': telefono, 'email': email})
    guardar_contactos(contactos)
    print('Contacto agregado y guardado.')

def buscar_contacto(contactos, nombre):
    for contacto in contactos:
        if contacto['nombre'].lower() == nombre.lower():
            print(f"Nombre: {contacto['nombre']}")
            print(f"Teléfono: {contacto['telefono']}")
            print(f"Email: {contacto['email']}")
            return
    print('Contacto no encontrado.')

def eliminar_contacto(contactos, nombre):
    for contacto in contactos:
        if contacto['nombre'].lower() == nombre.lower():
            contactos.remove(contacto)
            guardar_contactos(contactos)
            print('Contacto eliminado y guardado.')
            return
    print('Contacto no encontrado.')

def listar_contactos(contactos):
    if not contactos:
        print('No hay contactos para mostrar.')
        return
    for i, contacto in enumerate(contactos, 1):
        print(f"{i}. {contacto['nombre']} — {contacto['telefono']} — {contacto['email']}")

def guardar_contactos(contactos):
    with open('contactos.txt', 'w') as archivo:
        for contacto in contactos:
            archivo.write(f"{contacto['nombre']},{contacto['telefono']},{contacto['email']}\n")

contactos = cargar_contactos()

while True:
    print('\n=== Agenda de contactos ===')
    print('1. Agregar contacto')
    print('2. Buscar contacto')
    print('3. Eliminar contacto')
    print('4. Listar todos')
    print('0. Salir')

    opcion = input('Opción: ')

    if opcion == '0':
        print('¡Hasta luego!')
        break
    elif opcion == '1':
        agregar_contacto(contactos)
    elif opcion == '2':
        nombre = input('Nombre a buscar: ')
        buscar_contacto(contactos, nombre)
    elif opcion == '3':
        nombre = input('Nombre a eliminar: ')
        eliminar_contacto(contactos, nombre)
    elif opcion == '4':
        listar_contactos(contactos)
    else:
        print('Opción no válida')