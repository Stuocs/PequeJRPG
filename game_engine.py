import random
from config import *
from personajes import Guerrero, Mago, Clerigo, Paladin, Asesino

class GameEngine:
    def __init__(self, selected_allies=None, selected_enemies=None):
        # Mapeo de nombres a clases de personajes
        self.character_classes = {
            'Thorgar': Guerrero,
            'Eldrin': Mago,
            'Liora': Clerigo,
            'Arthas': Paladin,
            'Shadow': Asesino
        }
        
        # Crear personajes basados en la selección
        self.personajes = []
        
        if selected_allies and selected_enemies:
            # Crear equipo aliado
            for i, name in enumerate(selected_allies):
                if name in self.character_classes:
                    # Crear una nueva instancia con un nombre único si es necesario
                    character = self.character_classes[name]()
                    if name in selected_enemies:
                        character.nombre = f"{name} (Aliado)"
                    self.personajes.append(character)
            
            # Crear equipo enemigo
            for i, name in enumerate(selected_enemies):
                if name in self.character_classes:
                    # Crear una nueva instancia con un nombre único si es necesario
                    character = self.character_classes[name]()
                    if name in selected_allies:
                        character.nombre = f"{name} (Enemigo)"
                    self.personajes.append(character)
        else:
            # Configuración por defecto si no hay selección
            self.personajes = [
                Guerrero(),
                Mago(),
                Clerigo(),
                Paladin(),
                Asesino()
            ]
        
        # Variables de estado del juego
        self.mensaje_estado = f"Turno de {self.personajes[0].nombre}" if self.personajes else "Inicia el juego"
        self.mensaje_combate = ""
        self.combate_terminado = False
        self.turno_personaje = 0
        self.esperando_accion = True

    def posicionar_personajes(self):
        # Separar aliados y enemigos
        num_allies = len([p for p in self.personajes if isinstance(p, (Guerrero, Mago, Clerigo))])
        num_enemies = len([p for p in self.personajes if isinstance(p, (Paladin, Asesino))])
        
        # Calcular espaciado vertical
        ally_spacing = min(200, (SCREEN_HEIGHT - 200) // max(num_allies, 1))
        enemy_spacing = min(200, (SCREEN_HEIGHT - 200) // max(num_enemies, 1))
        
        # Posicionar aliados (lado izquierdo)
        ally_start_y = (SCREEN_HEIGHT - ((num_allies - 1) * ally_spacing)) // 2
        ally_count = 0
        
        # Posicionar enemigos (lado derecho)
        enemy_start_y = (SCREEN_HEIGHT - ((num_enemies - 1) * enemy_spacing)) // 2
        enemy_count = 0
        
        for personaje in self.personajes:
            if isinstance(personaje, (Guerrero, Mago, Clerigo)):
                personaje.rect.x = 50
                personaje.rect.y = ally_start_y + (ally_count * ally_spacing)
                ally_count += 1
            else:
                personaje.rect.x = SCREEN_WIDTH - 150
                personaje.rect.y = enemy_start_y + (enemy_count * enemy_spacing)
                enemy_count += 1

    def get_objetivos_posibles(self):
        """Retorna los objetivos posibles para el personaje actual"""
        personaje_actual = self.personajes[self.turno_personaje]
        
        # Si es aliado, atacar a enemigos
        if isinstance(personaje_actual, (Guerrero, Mago, Clerigo)):
            return [p for p in self.personajes if isinstance(p, (Paladin, Asesino)) and p.esta_vivo()]
        # Si es enemigo, atacar a aliados
        else:
            return [p for p in self.personajes if isinstance(p, (Guerrero, Mago, Clerigo)) and p.esta_vivo()]

    def get_aliados_posibles(self):
        """Retorna los aliados posibles para curar"""
        personaje_actual = self.personajes[self.turno_personaje]
        
        # Si es aliado, curar a aliados
        if isinstance(personaje_actual, (Guerrero, Mago, Clerigo)):
            return [p for p in self.personajes if isinstance(p, (Guerrero, Mago, Clerigo)) and p.esta_vivo()]
        # Si es enemigo, curar a enemigos
        else:
            return [p for p in self.personajes if isinstance(p, (Paladin, Asesino)) and p.esta_vivo()]

    def verificar_fin_combate(self):
        """Verifica si el combate ha terminado"""
        # Verificar si todos los héroes están derrotados
        heroes_vivos = any(p.esta_vivo() for p in self.personajes if isinstance(p, (Guerrero, Mago, Clerigo)))
        enemigos_vivos = any(p.esta_vivo() for p in self.personajes if isinstance(p, (Paladin, Asesino)))
        
        if not heroes_vivos:
            self.mensaje_estado = "¡Has perdido! Presiona ESPACIO para intentarlo de nuevo"
            self.combate_terminado = True
        elif not enemigos_vivos:
            self.mensaje_estado = "¡Has ganado! Presiona ESPACIO para jugar de nuevo"
            self.combate_terminado = True
        
        return self.combate_terminado

    def siguiente_turno(self):
        """Pasa al siguiente turno"""
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
        """Maneja las acciones de los personajes"""
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

    def reiniciar_juego(self):
        """Reinicia el estado del juego"""
        for personaje in self.personajes:
            personaje.reiniciar()
        self.posicionar_personajes()
        self.mensaje_estado = f"Turno de {self.personajes[0].nombre}"
        self.mensaje_combate = ""
        self.combate_terminado = False
        self.turno_personaje = 0
        self.esperando_accion = True
