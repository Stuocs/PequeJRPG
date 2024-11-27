import random  # Necesario para las tiradas de ataque

# Clase base para héroes y enemigos
class Personaje:
    """Un valiente personaje con salud, nivel y un nombre memorable."""
    def __init__(self, nombre, salud_inicial, nivel):
        self.nombre = nombre
        self.salud = salud_inicial
        self.nivel = nivel

    def recibir_daño(self, cantidad):
        """Recibe daño y reduce su salud. ¿Sobrevivirá?"""
        self.salud -= cantidad
        print(f"{self.nombre}: ¡Aaah! He recibido {cantidad} puntos de daño. Salud restante: {self.salud}")
        if self.salud <= 0:
            print(f"{self.nombre}: 'He caído... ¡seguiré luchando en espíritu!'")

    def estado_actual(self):
        """Informa sobre el estado actual del personaje."""
        return f"{self.nombre} tiene {self.salud} puntos de salud."

# Clase Guerrero
class Guerrero(Personaje):
    """El Guerrero lucha con fuerza bruta y resistencia."""
    def __init__(self, nombre, salud_inicial, nivel, fuerza):
        super().__init__(nombre, salud_inicial, nivel)
        self.fuerza = fuerza

    def atacar(self, enemigo):
        """Ataca con fuerza física. ¡Cuidado con los críticos!"""
        daño = random.randint(1, 20) + self.fuerza // 2
        print(f"{self.nombre}: '¡Por el honor!' golpea a {enemigo.nombre} causando {daño} de daño.")
        enemigo.recibir_daño(daño)

# Simplificación de un turno
def realizar_turno(atacante, defensor):
    """El atacante realiza su movimiento. ¡Prepárate, defensor!"""
    if isinstance(atacante, Guerrero):
        atacante.atacar(defensor)
    else:
        print(f"{atacante.nombre} no sabe cómo atacar. ¿Qué está haciendo?")

# Flujo principal simplificado
def combate_simple():
    """Simula un combate épico entre un héroe y un enemigo."""
    print("🌟 ¡Bienvenidos al campo de batalla! 🌟")
    guerrero_heroe = Guerrero("Aldrin", 100, 5, 20)
    guerrero_enemigo = Guerrero("Orco Brutal", 120, 3, 15)

    turno = 1
    while guerrero_heroe.salud > 0 and guerrero_enemigo.salud > 0:
        print(f"\n🔥 --- Turno {turno} --- 🔥")
        print(guerrero_heroe.estado_actual())
        print(guerrero_enemigo.estado_actual())
        realizar_turno(guerrero_heroe, guerrero_enemigo)
        if guerrero_enemigo.salud > 0:
            realizar_turno(guerrero_enemigo, guerrero_heroe)
        turno += 1

    ganador = guerrero_heroe if guerrero_heroe.salud > 0 else guerrero_enemigo
    print("\n✨ El combate ha terminado. ¡El ganador es...")
    print(f"🎉 {ganador.nombre.upper()} 🎉")

# Inicio del combate
if __name__ == "__main__":
    combate_simple()
