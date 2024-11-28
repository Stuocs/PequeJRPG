import pygame
import pygame_gui
from config import *

class GameUI:
    def __init__(self):
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Crear los botones de acción
        self.atacar_boton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_X, BUTTON_Y_ATACAR), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Atacar',
            manager=self.manager
        )
        
        self.defender_boton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_X, BUTTON_Y_DEFENDER), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Defender',
            manager=self.manager
        )
        
        self.curar_boton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_X, BUTTON_Y_CURAR), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Curar',
            manager=self.manager
        )
        
        self.font = pygame.font.Font(None, 36)

    def draw_personaje(self, screen, personaje):
        # Actualizar efecto destacado
        personaje.actualizar_destacado()
        
        # Dibujar sprite con efecto si está destacado
        if personaje.destacado:
            s = pygame.Surface((HIGHLIGHT_SIZE, HIGHLIGHT_SIZE))
            s.fill(YELLOW)
            screen.blit(s, (personaje.rect.x - HIGHLIGHT_PADDING, 
                          personaje.rect.y - HIGHLIGHT_PADDING))
        
        # Actualizar y dibujar la animación del personaje
        personaje.actualizar_animacion()
        screen.blit(personaje.get_sprite(), personaje.rect)
        
        # Dibujar barra de vida
        color = GREEN if personaje.vida >= 70 else YELLOW if personaje.vida >= 30 else RED
        vida_text = self.font.render(f"{personaje.nombre}: {personaje.vida} HP", True, color)
        screen.blit(vida_text, (personaje.rect.x, personaje.rect.y - 20))

    def draw_mensaje_estado(self, screen, mensaje):
        instruccion = self.font.render(mensaje, True, WHITE)
        screen.blit(instruccion, (SCREEN_WIDTH//2 - instruccion.get_width()//2, 20))

    def draw_mensaje_combate(self, screen, mensaje):
        if mensaje:
            texto = self.font.render(mensaje, True, GOLD)
            screen.blit(texto, (SCREEN_WIDTH//2 - texto.get_width()//2, 500))

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self, screen):
        self.manager.draw_ui(screen)

    def process_events(self, event):
        self.manager.process_events(event)
