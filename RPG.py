import random

class Heroe:
    def __init__(self, nombre, puntos_salud, nivel):
        self.nombre = nombre
        self.puntos_salud = puntos_salud
        self.nivel = nivel

    def atacar(self, objetivo):
        pass

    def recibir_daño(self, cantidad):
        self.puntos_salud -= cantidad
        print(f"{self.nombre} recibió {cantidad} puntos de daño. Salud restante: {self.puntos_salud}")
        if self.puntos_salud <= 0:
            print(f"{self.nombre} ha caído en combate.")

    def recibir_sanación(self, cantidad):
        self.puntos_salud += cantidad
        print(f"{self.nombre} ha sido sanado por {cantidad} puntos de salud. Salud actual: {self.puntos_salud}")


class Guerrero(Heroe):
    def __init__(self, nombre, puntos_salud, nivel, fuerza):
        super().__init__(nombre, puntos_salud, nivel)
        self.fuerza = fuerza

    def atacar(self, objetivo):
        daño = random.randint(1, 20) + self.fuerza // 2
        print(f"{self.nombre} ataca a {objetivo.nombre} causando {daño} puntos de daño.")
        objetivo.recibir_daño(daño)


class Mago(Heroe):
    def __init__(self, nombre, puntos_salud, nivel, inteligencia):
        super().__init__(nombre, puntos_salud, nivel)
        self.inteligencia = inteligencia

    def atacar(self, objetivo):
        daño = random.randint(1, 20) + self.inteligencia
        print(f"{self.nombre} lanza un hechizo contra {objetivo.nombre} causando {daño} puntos de daño.")
        objetivo.recibir_daño(daño)


class Asesino(Heroe):
    def __init__(self, nombre, puntos_salud, nivel, destreza):
        super().__init__(nombre, puntos_salud, nivel)
        self.destreza = destreza

    def atacar(self, objetivo):
        daño = random.randint(1, 10) + random.randint(1, 10) + self.destreza * 2
        print(f"{self.nombre} ataca sigilosamente a {objetivo.nombre} causando {daño} puntos de daño.")
        objetivo.recibir_daño(daño)


class Clerigo(Heroe):
    def __init__(self, nombre, puntos_salud, nivel, fe):
        super().__init__(nombre, puntos_salud, nivel)
        self.fe = fe

    def curar(self, objetivo):
        curación = random.randint(1, 10) + self.fe
        print(f"{self.nombre} cura a {objetivo.nombre} restaurando {curación} puntos de salud.")
        objetivo.recibir_sanación(curación)

class Paladin(Heroe):
    def __init__(self, nombre, puntos_salud, nivel, fuerza, fe):
        # Inicialización explícita
        Heroe.__init__(self, nombre, puntos_salud, nivel)
        self.fuerza = fuerza
        self.fe = fe

    def atacar(self, objetivo):
        daño = random.randint(1, 10) + self.fuerza // 2
        print(f"{self.nombre} ataca a {objetivo.nombre} causando {daño} puntos de daño.")
        objetivo.recibir_daño(daño)

    def curar(self, objetivo):
        curación = random.randint(1, 5) + self.fe
        print(f"{self.nombre} cura a {objetivo.nombre} restaurando {curación} puntos de salud.")
        objetivo.recibir_sanación(curación)



# Ejemplo de combate
def combate():
    guerrero = Guerrero("Thorgar", 100, 5, 18)
    mago = Mago("Eldrin", 70, 5, 20)
    asesino = Asesino("Shadow", 80, 5, 15)
    clerigo = Clerigo("Liora", 60, 5, 25)
    paladin = Paladin("Arthas", 90, 5, 16, 20)

    equipo = [guerrero, clerigo, paladin]
    enemigos = [asesino, mago, guerrero]
    #enemigos = [Guerrero("Orco", 120, 4, 14), Mago("Nigromante", 60, 4, 18)]

    turno = 0
    while any(e.puntos_salud > 0 for e in equipo) and any(e.puntos_salud > 0 for e in enemigos):
        print(f"\n--- Turno {turno + 1} ---")
        atacante = random.choice(equipo if turno % 2 == 0 else enemigos)
        defensor = random.choice(enemigos if turno % 2 == 0 else equipo)

        if isinstance(atacante, Clerigo):
            aliado = random.choice(equipo if atacante in equipo else enemigos)
            atacante.curar(aliado)
        else:
            atacante.atacar(defensor)

        equipo = [h for h in equipo if h.puntos_salud > 0]
        enemigos = [h for h in enemigos if h.puntos_salud > 0]

        print_estado(equipo, enemigos)
        turno += 1

    if any(h.puntos_salud > 0 for h in equipo):
        print("\n¡El equipo de héroes ha ganado!")
    else:
        print("\n¡Los enemigos han ganado!")


def print_estado(equipo, enemigos):
    print("\nEstado del Equipo:")
    for h in equipo:
        print(f"{h.nombre}: {h.puntos_salud} puntos de salud")

    print("\nEstado de los Enemigos:")
    for e in enemigos:
        print(f"{e.nombre}: {e.puntos_salud} puntos de salud")

if __name__ == "__main__":
    combate()

