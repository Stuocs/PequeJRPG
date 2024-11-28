import pygame
import pygame_gui
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RPG TurnBased Game")

# Inicializar Pygame GUI
manager = pygame_gui.UIManager((screen_width, screen_height))

# Crear los botones de acción
atacar_boton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 450), (100, 50)),
                                            text='Atacar',
                                            manager=manager)
defender_boton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 510), (100, 50)),
                                              text='Defender',
                                              manager=manager)
curar_boton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 570), (100, 50)),
                                           text='Curar',
                                           manager=manager)

# Cargar sprites
def load_sprite(name):
    spritesheet = pygame.image.load(f'Personajes/{name}_Luchando.png')
    frames = []
    for i in range(4):
        frame = pygame.Surface((64, 64), pygame.SRCALPHA)
        frame.blit(spritesheet, (0, 0), (i * 64, 0, 64, 64))
        frame = pygame.transform.scale(frame, (100, 100))
        frames.append(frame)
    return frames

class Personaje:
    def __init__(self, nombre, vida, ataque, defensa):
        self.nombre = nombre
        self.vida = vida
        self.vida_maxima = vida
        self.ataque = ataque
        self.defensa = defensa
        self.frames = load_sprite(nombre)
        self.frame_actual = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.delay_animacion = 100
        self.animando = False
        self.rect = self.frames[0].get_rect()
        self.destacado = False
        self.tiempo_destacado = 0
        self.defensa_original = defensa
        
    def actualizar_animacion(self):
        ahora = pygame.time.get_ticks()
        if self.animando:
            if ahora - self.ultimo_update > self.delay_animacion:
                self.ultimo_update = ahora
                self.frame_actual = (self.frame_actual + 1) % len(self.frames)
                if self.frame_actual == 0:
                    self.animando = False
        else:
            self.frame_actual = 0
            
    def get_sprite(self):
        return self.frames[self.frame_actual]

    def actualizar_destacado(self):
        if self.destacado and pygame.time.get_ticks() - self.tiempo_destacado > 200:
            self.destacado = False

    def defender(self):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.defensa = self.defensa_original * 2

    def restaurar_defensa(self):
        self.defensa = self.defensa_original

    def esta_vivo(self):
        return self.vida > 0

    def reiniciar(self):
        self.vida = self.vida_maxima
        self.defensa = self.defensa_original
        self.destacado = False
        self.animando = False

class Guerrero(Personaje):
    def __init__(self):
        super().__init__("Thorgar", 100, 20, 5)
        self.fuerza = 20

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        # 1d20 + fuerza//2
        daño = random.randint(1, 20) + self.fuerza // 2
        enemigo.vida = max(0, enemigo.vida - max(0, daño - enemigo.defensa))
        enemigo.destacado = True
        enemigo.tiempo_destacado = pygame.time.get_ticks()
        return daño

class Mago(Personaje):
    def __init__(self):
        super().__init__("Eldrin", 80, 15, 3)
        self.inteligencia = 25

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        # 1d20 + inteligencia
        daño = random.randint(1, 20) + self.inteligencia
        enemigo.vida = max(0, enemigo.vida - max(0, daño - enemigo.defensa))
        enemigo.destacado = True
        enemigo.tiempo_destacado = pygame.time.get_ticks()
        return daño

class Asesino(Personaje):
    def __init__(self):
        super().__init__("Shadow", 70, 30, 3)
        self.destreza = 15

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        # 2d10 + destreza * 2
        daño = random.randint(1, 10) + random.randint(1, 10) + self.destreza * 2
        enemigo.vida = max(0, enemigo.vida - max(0, daño - enemigo.defensa))
        enemigo.destacado = True
        enemigo.tiempo_destacado = pygame.time.get_ticks()
        return daño

class Clerigo(Personaje):
    def __init__(self):
        super().__init__("Liora", 90, 0, 5)
        self.fe = 20

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        return 0  # No hace daño

    def curar(self, aliado):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        # 1d10 + fe
        curacion = random.randint(1, 10) + self.fe
        aliado.vida = min(aliado.vida_maxima, aliado.vida + curacion)
        return curacion

class Paladin(Personaje):
    def __init__(self):
        super().__init__("Arthas", 100, 15, 8)
        self.fuerza = 15
        self.fe = 15

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        # 1d10 + fuerza//2
        daño = random.randint(1, 10) + self.fuerza // 2
        enemigo.vida = max(0, enemigo.vida - max(0, daño - enemigo.defensa))
        enemigo.destacado = True
        enemigo.tiempo_destacado = pygame.time.get_ticks()
        return daño

    def curar(self, aliado):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        # 1d5 + fe
        curacion = random.randint(1, 5) + self.fe
        aliado.vida = min(aliado.vida_maxima, aliado.vida + curacion)
        return curacion

# Crear personajes
guerrero = Guerrero()
mago = Mago()
clerigo = Clerigo()
paladin = Paladin()
asesino = Asesino()

# Variables globales para el estado del juego
mensaje_estado = ""
mensaje_combate = ""
combate_terminado = False
turno_personaje = 0
esperando_accion = True
personajes = [guerrero, mago, clerigo, paladin, asesino]

def reiniciar_juego():
    global mensaje_estado, mensaje_combate, combate_terminado, turno_personaje, esperando_accion
    # Reiniciar cada personaje
    for personaje in personajes:
        personaje.reiniciar()
    posicionar_personajes()
    mensaje_estado = "Turno de Thorgar"
    mensaje_combate = ""
    combate_terminado = False
    turno_personaje = 0
    esperando_accion = True

def verificar_fin_combate():
    global mensaje_estado, combate_terminado
    # Verificar si todos los héroes están derrotados
    heroes_vivos = any(p.esta_vivo() for p in [guerrero, mago, clerigo])
    enemigos_vivos = any(p.esta_vivo() for p in [paladin, asesino])
    
    if not heroes_vivos:
        mensaje_estado = "¡Has perdido! Presiona ESPACIO para intentarlo de nuevo"
        combate_terminado = True
    elif not enemigos_vivos:
        mensaje_estado = "¡Has ganado! Presiona ESPACIO para jugar de nuevo"
        combate_terminado = True
    
    return combate_terminado

def parpadeo_rapido():
    original_color = screen.get_at((0, 0))
    screen.fill((100, 100, 100))
    pygame.display.flip()
    pygame.time.wait(50)
    screen.fill(original_color)
    pygame.display.flip()

def siguiente_turno():
    global turno_personaje, mensaje_estado, esperando_accion
    if not combate_terminado:
        # Restaurar la defensa del personaje actual antes de cambiar de turno
        personajes[turno_personaje].restaurar_defensa()
        
        # Buscar el siguiente personaje vivo
        turno_original = turno_personaje
        while True:
            turno_personaje = (turno_personaje + 1) % len(personajes)
            if personajes[turno_personaje].esta_vivo():
                break
            if turno_personaje == turno_original:  # Si hemos dado la vuelta completa
                verificar_fin_combate()
                break
        
        if not combate_terminado:
            personaje_actual = personajes[turno_personaje]
            mensaje_estado = f"Turno de {personaje_actual.nombre}"
            esperando_accion = True

def manejar_accion(accion, personaje_activo, objetivo=None):
    global esperando_accion, mensaje_combate
    if not personaje_activo.esta_vivo() or (objetivo and not objetivo.esta_vivo()):
        return

    if accion == 'atacar':
        if isinstance(personaje_activo, Clerigo):
            mensaje_combate = f"{personaje_activo.nombre} no puede atacar"
        else:
            daño = personaje_activo.atacar(objetivo)
            mensaje_combate = f"{personaje_activo.nombre} ataca a {objetivo.nombre} y causa {daño} de daño"
    elif accion == 'defender':
        personaje_activo.defender()
        mensaje_combate = f"{personaje_activo.nombre} se defiende"
    elif accion == 'curar':
        if isinstance(personaje_activo, (Clerigo, Paladin)):
            curacion = personaje_activo.curar(objetivo)
            mensaje_combate = f"{personaje_activo.nombre} cura a {objetivo.nombre} por {curacion} puntos"
        else:
            mensaje_combate = f"{personaje_activo.nombre} no puede curar"
    
    if not verificar_fin_combate():
        siguiente_turno()

def posicionar_personajes():
    # Posicionar personajes en la pantalla
    guerrero.rect.x = 50
    guerrero.rect.y = 100
    mago.rect.x = 50
    mago.rect.y = 200
    clerigo.rect.x = 50
    clerigo.rect.y = 300
    paladin.rect.x = screen_width - 150
    paladin.rect.y = 200
    asesino.rect.x = screen_width - 150
    asesino.rect.y = 300

def main():
    global mensaje_estado, turno_personaje, esperando_accion, mensaje_combate
    running = True
    posicionar_personajes()
    mensaje_estado = "Turno de Thorgar"
    mensaje_combate = ""
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    
    while running:
        time_delta = clock.tick(60)/1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and combate_terminado:
                    reiniciar_juego()
                
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if esperando_accion and not combate_terminado:
                        personaje_activo = personajes[turno_personaje]
                        if event.ui_element == atacar_boton:
                            # Los aliados atacan a los enemigos y viceversa
                            if turno_personaje < 3:  # Personajes aliados
                                objetivos_posibles = [p for p in [paladin, asesino] if p.esta_vivo()]
                            else:  # Enemigos
                                objetivos_posibles = [p for p in [guerrero, mago, clerigo] if p.esta_vivo()]
                            
                            if objetivos_posibles:
                                objetivo = random.choice(objetivos_posibles)
                                manejar_accion('atacar', personaje_activo, objetivo)
                        elif event.ui_element == defender_boton:
                            manejar_accion('defender', personaje_activo)
                        elif event.ui_element == curar_boton:
                            if turno_personaje < 3:  # Personajes aliados
                                objetivos_posibles = [p for p in [guerrero, mago, clerigo] if p.esta_vivo()]
                            else:  # Enemigos
                                objetivos_posibles = [p for p in [paladin, asesino] if p.esta_vivo()]
                            
                            if objetivos_posibles:
                                objetivo = random.choice(objetivos_posibles)
                                manejar_accion('curar', personaje_activo, objetivo)
            
            manager.process_events(event)

        manager.update(time_delta)

        screen.fill((50, 50, 50))  # Fondo gris oscuro
        
        # Dibujar personajes
        for personaje in personajes:
            # Actualizar efecto destacado
            personaje.actualizar_destacado()
            
            # Dibujar sprite con efecto si está destacado
            if personaje.destacado:
                s = pygame.Surface((104, 104))
                s.fill((255, 255, 0))
                screen.blit(s, (personaje.rect.x - 2, personaje.rect.y - 2))
            
            # Actualizar y dibujar la animación del personaje
            personaje.actualizar_animacion()
            screen.blit(personaje.get_sprite(), personaje.rect)
            
            # Dibujar barra de vida
            if personaje.vida >= 70:
                color = (0, 255, 0)  # Verde
            elif personaje.vida >= 30:
                color = (255, 255, 0)  # Amarillo
            else:
                color = (255, 0, 0)  # Rojo
            vida_text = font.render(f"{personaje.nombre}: {personaje.vida} HP", True, color)
            screen.blit(vida_text, (personaje.rect.x, personaje.rect.y - 20))
        
        # Dibujar mensaje de estado
        instruccion = font.render(mensaje_estado, True, (255, 255, 255))
        screen.blit(instruccion, (screen_width//2 - instruccion.get_width()//2, 20))
        
        # Dibujar mensajes de combate
        if mensaje_combate:
            texto = font.render(mensaje_combate, True, (255, 200, 0))
            screen.blit(texto, (screen_width//2 - texto.get_width()//2, 500))

        # Dibujar GUI
        manager.draw_ui(screen)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()