import random
from config import *
from personajes import Guerrero, Mago, Clerigo, Paladin, Asesino

class GameEngine:
    def __init__(self):
        # Crear personajes
        self.guerrero = Guerrero()
        self.mago = Mago()
        self.clerigo = Clerigo()
        self.paladin = Paladin()
        self.asesino = Asesino()
        
        # Variables de estado del juego
        self.mensaje_estado = "Turno de Thorgar"
        self.mensaje_combate = ""
        self.combate_terminado = False
        self.turno_personaje = 0
        self.esperando_accion = True
        self.personajes = [self.guerrero, self.mago, self.clerigo, self.paladin, self.asesino]

    def posicionar_personajes(self):
        # Posicionar personajes en la pantalla
        self.guerrero.rect.x = 50
        self.guerrero.rect.y = 100
        self.mago.rect.x = 50
        self.mago.rect.y = 200
        self.clerigo.rect.x = 50
        self.clerigo.rect.y = 300
        self.paladin.rect.x = SCREEN_WIDTH - 150
        self.paladin.rect.y = 200
        self.asesino.rect.x = SCREEN_WIDTH - 150
        self.asesino.rect.y = 300

    def reiniciar_juego(self):
        # Reiniciar cada personaje
        for personaje in self.personajes:
            personaje.reiniciar()
        self.posicionar_personajes()
        self.mensaje_estado = "Turno de Thorgar"
        self.mensaje_combate = ""
        self.combate_terminado = False
        self.turno_personaje = 0
        self.esperando_accion = True

    def verificar_fin_combate(self):
        # Verificar si todos los héroes están derrotados
        heroes_vivos = any(p.esta_vivo() for p in [self.guerrero, self.mago, self.clerigo])
        enemigos_vivos = any(p.esta_vivo() for p in [self.paladin, self.asesino])
        
        if not heroes_vivos:
            self.mensaje_estado = "¡Has perdido! Presiona ESPACIO para intentarlo de nuevo"
            self.combate_terminado = True
        elif not enemigos_vivos:
            self.mensaje_estado = "¡Has ganado! Presiona ESPACIO para jugar de nuevo"
            self.combate_terminado = True
        
        return self.combate_terminado

    def siguiente_turno(self):
        if not self.combate_terminado:
            # Restaurar la defensa del personaje actual antes de cambiar de turno
            self.personajes[self.turno_personaje].restaurar_defensa()
            
            # Buscar el siguiente personaje vivo
            turno_original = self.turno_personaje
            while True:
                self.turno_personaje = (self.turno_personaje + 1) % len(self.personajes)
                if self.personajes[self.turno_personaje].esta_vivo():
                    break
                if self.turno_personaje == turno_original:  # Si hemos dado la vuelta completa
                    self.verificar_fin_combate()
                    break
            
            if not self.combate_terminado:
                personaje_actual = self.personajes[self.turno_personaje]
                self.mensaje_estado = f"Turno de {personaje_actual.nombre}"
                self.esperando_accion = True

    def manejar_accion(self, accion, personaje_activo, objetivo=None):
        if not personaje_activo.esta_vivo() or (objetivo and not objetivo.esta_vivo()):
            return

        if accion == 'atacar':
            if isinstance(personaje_activo, Clerigo):
                self.mensaje_combate = f"{personaje_activo.nombre} no puede atacar"
            else:
                daño = personaje_activo.atacar(objetivo)
                self.mensaje_combate = f"{personaje_activo.nombre} ataca a {objetivo.nombre} y causa {daño} de daño"
        elif accion == 'defender':
            personaje_activo.defender()
            self.mensaje_combate = f"{personaje_activo.nombre} se defiende"
        elif accion == 'curar':
            if isinstance(personaje_activo, (Clerigo, Paladin)):
                curacion = personaje_activo.curar(objetivo)
                self.mensaje_combate = f"{personaje_activo.nombre} cura a {objetivo.nombre} por {curacion} puntos"
            else:
                self.mensaje_combate = f"{personaje_activo.nombre} no puede curar"
        
        if not self.verificar_fin_combate():
            self.siguiente_turno()

    def get_objetivos_posibles(self):
        if self.turno_personaje < 3:  # Personajes aliados
            return [p for p in [self.paladin, self.asesino] if p.esta_vivo()]
        else:  # Enemigos
            return [p for p in [self.guerrero, self.mago, self.clerigo] if p.esta_vivo()]

    def get_aliados_posibles(self):
        if self.turno_personaje < 3:  # Personajes aliados
            return [p for p in [self.guerrero, self.mago, self.clerigo] if p.esta_vivo()]
        else:  # Enemigos
            return [p for p in [self.paladin, self.asesino] if p.esta_vivo()]
