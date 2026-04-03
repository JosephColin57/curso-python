class Libro:
    def __init__(self, titulo, autor, genero):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.leido = False
        
    def marcar_como_leido(self):
        self.leido = True

    def mostrar_informacion(self):
        estado = "Leído" if self.leido else "No leído"
        return f"Título: {self.titulo}, Autor: {self.autor}, Género: {self.genero}, Estado: {estado}"
    

class Biblioteca:
    def __init__(self):
        self.libros = []
        
    def agregar_libro(self, libro):
        self.libros.append(libro)

    def buscar_libro_por_titulo(self, titulo):
        for libro in self.libros:
            if libro.titulo == titulo:
                return libro.mostrar_informacion()
        return f"El libro '{titulo}' no se encontró en la biblioteca."
    
    def listar_todos(self):
        return [libro.mostrar_informacion() for libro in self.libros]
    
    def listar_por_genero(self, genero):
        libros_por_genero = [libro.mostrar_informacion() for libro in self.libros if libro.genero == genero]
        return libros_por_genero if libros_por_genero else f"No se encontraron libros del género '{genero}'."
    
    def guardar_en_archivo(self, nombre_archivo):
        with open(nombre_archivo, 'w') as archivo:
            for libro in self.libros:
                archivo.write(libro.mostrar_informacion() + '\n')
        return f"Los libros han sido guardados en '{nombre_archivo}'."
    
    def cargar_desde_archivo(self, nombre_archivo):
        try:
            with open(nombre_archivo, 'r') as archivo:
                for linea in archivo:
                    partes = linea.strip().split(', ')
                    if len(partes) == 4:
                        titulo = partes[0].split(': ')[1]
                        autor = partes[1].split(': ')[1]
                        genero = partes[2].split(': ')[1]
                        estado = partes[3].split(': ')[1]
                        libro = Libro(titulo, autor, genero)
                        if estado == "Leído":
                            libro.marcar_como_leido()
                        self.agregar_libro(libro)
            return f"Los libros han sido cargados desde '{nombre_archivo}'."
        except FileNotFoundError:
            return f"El archivo '{nombre_archivo}' no se encontró."
        
    def marcar_como_leido(self, titulo):
        for libro in self.libros:
            if libro.titulo == titulo:
                libro.marcar_como_leido()
                return f"El libro '{titulo}' ha sido marcado como leído."
        return f"El libro '{titulo}' no se encontró en la biblioteca."
        

biblioteca = Biblioteca()

while True:
    print("\n=== Biblioteca ===")
    print("1. Agregar libro")
    print("2. Buscar libro por título")
    print("3. Marcar libro como leído")
    print("4. Listar todos los libros")
    print("5. Listar libros por género")
    print("6. Guardar en archivo")
    print("7. Cargar desde archivo")
    print("0. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        titulo = input("Ingrese el título del libro: ")
        autor = input("Ingrese el autor del libro: ")
        genero = input("Ingrese el género del libro: ")
        libro = Libro(titulo, autor, genero)
        biblioteca.agregar_libro(libro)
        print(f"El libro '{titulo}' ha sido agregado a la biblioteca.")
    
    elif opcion == '2':
        titulo = input("Ingrese el título del libro a buscar: ")
        print(biblioteca.buscar_libro_por_titulo(titulo))

    elif opcion == '3':
        titulo = input("Ingrese el título del libro a marcar como leído: ")
        print(biblioteca.marcar_como_leido(titulo))

    elif opcion == '4':
        libros = biblioteca.listar_todos()
        if libros:
            print("\nLibros en la biblioteca:")
            for libro in libros:
                print(libro)
        else:
            print("No hay libros en la biblioteca.")

    elif opcion == '5':
        genero = input("Ingrese el género de los libros a listar: ")
        libros_por_genero = biblioteca.listar_por_genero(genero)
        if isinstance(libros_por_genero, list):
            print(f"\nLibros del género '{genero}':")
            for libro in libros_por_genero:
                print(libro)
        else:
            print(libros_por_genero)

    elif opcion == '6':
        nombre_archivo = input("Ingrese el nombre del archivo para guardar: ")
        print(biblioteca.guardar_en_archivo(nombre_archivo))

    elif opcion == '7':
        nombre_archivo = input("Ingrese el nombre del archivo para cargar: ")
        print(biblioteca.cargar_desde_archivo(nombre_archivo))
    
    elif opcion == '0':
        print("Saliendo de la biblioteca. ¡Hasta luego!")
        break

    else:
        print("Opción no válida. Por favor, intente nuevamente.")