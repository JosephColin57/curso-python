class Animal:
    def __init__(self, nombre, edad, dueño):
        self.nombre = nombre
        self.edad = edad
        self.dueño = dueño

    def presentarse(self):
        print(f"Soy {self.nombre} y tengo {self.edad} años")

    def hacer_sonido(self):
        print("...")  # genérico, cada animal lo sobreescribe

    def info_completa(self):
        self.presentarse()
        print(f"Mi dueño es {self.dueño}")

class Perro(Animal):  # Perro hereda de Animal
    def __init__(self, nombre, edad, dueño, raza):
        super().__init__(nombre, edad, dueño)
        self.raza = raza

    def hacer_sonido(self):
        print("¡Guau!")

    def buscar_pelota(self):
        print(f"{self.nombre} busca la pelota")

    def info_completa(self):
        super().info_completa()  # llama al de Animal
        print(f"Raza: {self.raza}")

class Gato(Animal):
    def __init__(self, nombre, edad, dueño, es_indoor):
        super().__init__(nombre, edad, dueño)
        self.es_indoor = es_indoor

    def hacer_sonido(self):
        print("¡Miau!")

    def ronronear(self):
        print(f"{self.nombre} está ronroneando")

    def info_completa(self):
        super().info_completa()  # llama al de Animal
        print(f"Indoor: {'Sí' if self.es_indoor else 'No'}")

# Ejemplo de uso
mi_perro = Perro("Rex", 5, "Carlos", "Labrador")
mi_gato = Gato("Mia", 3, "Ana", True)

mi_perro.info_completa()
mi_gato.info_completa()

mascotas = [mi_perro, mi_gato]
for mascota in mascotas:
    mascota.hacer_sonido()