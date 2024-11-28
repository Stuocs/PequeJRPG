import pygame
import pygame_gui
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RPG Turn-Based Game")

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

# Definir personajes
class Personaje:
    def __init__(self, nombre, vida, ataque, defensa):
        self.nombre = nombre
        self.vida = vida
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

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        daño = self.ataque - enemigo.defensa
        if daño > 0:
            enemigo.vida -= daño
            enemigo.destacado = True
            enemigo.tiempo_destacado = pygame.time.get_ticks()
        return daño
    
    def defender(self):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.defensa *= 2
        
    def curar(self, aliado):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        aliado.vida += 30
        if aliado.vida > 100:
            aliado.vida = 100

    def actualizar_destacado(self):
        if self.destacado and pygame.time.get_ticks() - self.tiempo_destacado > 200:
            self.destacado = False

# Crear personajes
guerrero = Personaje("Thorgar", 100, 20, 5)
mago = Personaje("Eldrin", 80, 15, 10)
sanadora = Personaje("Liora", 120, 10, 15)

# Crear enemigos
caballero = Personaje("Arthas", 90, 25, 8)
asesino = Personaje("Shadow", 70, 30, 3)

# Equipos
equipo = [guerrero, mago, sanadora]
enemigos = [caballero, asesino]

# Variables globales para el estado del juego
mensaje_estado = ""
mensaje_combate = ""
combate_terminado = False
turno_personaje = 0
esperando_accion = True

def reiniciar_juego():
    global equipo, enemigos, mensaje_estado, mensaje_combate, combate_terminado, turno_personaje, esperando_accion
    equipo.clear()
    enemigos.clear()
    equipo.extend([Personaje("Thorgar", 100, 20, 5), Personaje("Eldrin", 80, 15, 10), Personaje("Liora", 120, 10, 15)])
    enemigos.extend([Personaje("Arthas", 90, 25, 8), Personaje("Shadow", 70, 30, 3)])
    posicionar_personajes()
    mensaje_estado = "Presiona ESPACIO para combatir"
    mensaje_combate = ""
    combate_terminado = False
    turno_personaje = 0
    esperando_accion = True

def parpadeo_rapido():
    original_color = screen.get_at((0, 0))
    screen.fill((100, 100, 100))
    pygame.display.flip()
    pygame.time.wait(50)
    screen.fill(original_color)
    pygame.display.flip()

def combate():
    global mensaje_estado, mensaje_combate, combate_terminado, esperando_accion, turno_personaje
    if combate_terminado:
        reiniciar_juego()
        return
    mensaje_combate = ""
    mensajes_turno = []
    parpadeo_rapido()
    for personaje in equipo:
        if personaje.vida > 0 and enemigos:
            enemigo = random.choice(enemigos)
            daño = personaje.atacar(enemigo)
            mensajes_turno.append(f"{personaje.nombre} ataca a {enemigo.nombre} y causa {daño} de daño")
            if enemigo.vida <= 0:
                mensajes_turno.append(f"{enemigo.nombre} ha sido derrotado!")
                enemigos.remove(enemigo)
    if not enemigos:
        mensaje_estado = "¡Has ganado! Presiona ESPACIO para jugar de nuevo"
        mensaje_combate = "\n".join(mensajes_turno)
        combate_terminado = True
        return
    for enemigo in enemigos:
        if enemigo.vida > 0 and equipo:
            personaje = random.choice(equipo)
            daño = enemigo.atacar(personaje)
            mensajes_turno.append(f"{enemigo.nombre} ataca a {personaje.nombre} y causa {daño} de daño")
            if personaje.vida <= 0:
                mensajes_turno.append(f"{personaje.nombre} ha sido derrotado!")
                equipo.remove(personaje)
    mensaje_combate = "\n".join(mensajes_turno)
    if not equipo:
        mensaje_estado = "¡Has perdido! Presiona ESPACIO para intentarlo de nuevo"
        combate_terminado = True
        return

def manejar_turno_personaje(accion):
    global esperando_accion, turno_personaje, mensaje_combate
    personaje = equipo[turno_personaje]
    if accion == 'atacar':
        enemigo = enemigos[0] if enemigos else None
        if enemigo:
            daño = personaje.atacar(enemigo)
            mensaje_combate = f"{personaje.nombre} ataca a {enemigo.nombre} y causa {daño} de daño"
            if enemigo.vida <= 0:
                mensaje_combate += f"\n{enemigo.nombre} ha sido derrotado!"
                enemigos.remove(enemigo)
    elif accion == 'defender':
        personaje.defender()
        mensaje_combate = f"{personaje.nombre} se defiende aumentando su defensa temporalmente"
    elif accion == 'curar':
        aliado = equipo[0] if equipo else None
        if aliado:
            personaje.curar(aliado)
            mensaje_combate = f"{personaje.nombre} cura a {aliado.nombre}, restaurando 30 puntos de vida"
    esperando_accion = False

def posicionar_personajes():
    for i, personaje in enumerate(equipo):
        personaje.rect.x = 50
        personaje.rect.y = 100 + (i * 150)
    for i, enemigo in enumerate(enemigos):
        enemigo.rect.x = screen_width - 150
        enemigo.rect.y = 100 + (i * 150)

def main():
    global mensaje_estado, turno_personaje, esperando_accion, mensaje_combate
    running = True
    posicionar_personajes()
    mensaje_estado = "Presiona ESPACIO para combatir"
    mensaje_combate = ""
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    
    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == atacar_boton:
                        manejar_turno_personaje('atacar')
                    elif event.ui_element == defender_boton:
                        manejar_turno_personaje('defender')
                    elif event.ui_element == curar_boton:
                        manejar_turno_personaje('curar')
            
            manager.process_events(event)

        manager.update(time_delta)

        screen.fill((50, 50, 50))  # Fondo gris oscuro
        
        # Dibujar personajes
        for personaje in equipo + enemigos:
            # Actualizar efecto destacado
            personaje.actualizar_destacado()
            
            # Dibujar sprite con efecto si está destacado
            if personaje.destacado:
                # Crear un borde brillante temporal
                s = pygame.Surface((104, 104))
                s.fill((255, 255, 0))  # Color amarillo para el borde
                screen.blit(s, (personaje.rect.x - 2, personaje.rect.y - 2))
            
            # Actualizar y dibujar la animación del personaje
            personaje.actualizar_animacion()
            screen.blit(personaje.get_sprite(), personaje.rect)
            
            # Dibujar barra de vida
            if personaje.vida >= 70:
                color = (0, 255, 0)  # Verde para vida alta
            elif personaje.vida >= 30:
                color = (255, 255, 0)  # Amarillo para vida media
            else:
                color = (255, 0, 0)  # Rojo para vida baja
            vida_text = font.render(f"HP: {personaje.vida}", True, color)
            screen.blit(vida_text, (personaje.rect.x, personaje.rect.y - 20))
            
        # Dibujar mensaje de estado
        instruccion = font.render(mensaje_estado, True, (255, 255, 255))
        screen.blit(instruccion, (screen_width//2 - instruccion.get_width()//2, 20))
        
        # Dibujar mensajes de combate
        if mensaje_combate:
            lineas = mensaje_combate.split('\n')
            for i, linea in enumerate(lineas):
                texto = font.render(linea, True, (255, 200, 0))  # Color amarillo para mensajes de combate
                screen.blit(texto, (screen_width//2 - texto.get_width()//2, 500 + i * 25))

        # Dibujar GUI
        manager.draw_ui(screen)
        
        pygame.display.flip()  # Actualizar pantalla

    pygame.quit()

if __name__ == "__main__":
    main()
