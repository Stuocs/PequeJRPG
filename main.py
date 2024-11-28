import random
import pygame
import pygame_gui
from config import *
from game_engine import GameEngine
from ui import GameUI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RPG TurnBased Game")
        
        self.engine = GameEngine()
        self.ui = GameUI()
        self.clock = pygame.time.Clock()
        
        # Inicializar el juego
        self.engine.posicionar_personajes()

    def handle_button_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if self.engine.esperando_accion and not self.engine.combate_terminado:
                    personaje_activo = self.engine.personajes[self.engine.turno_personaje]
                    
                    if event.ui_element == self.ui.atacar_boton:
                        objetivos_posibles = self.engine.get_objetivos_posibles()
                        if objetivos_posibles:
                            objetivo = random.choice(objetivos_posibles)
                            self.engine.manejar_accion('atacar', personaje_activo, objetivo)
                    
                    elif event.ui_element == self.ui.defender_boton:
                        self.engine.manejar_accion('defender', personaje_activo)
                    
                    elif event.ui_element == self.ui.curar_boton:
                        objetivos_posibles = self.engine.get_aliados_posibles()
                        if objetivos_posibles:
                            objetivo = random.choice(objetivos_posibles)
                            self.engine.manejar_accion('curar', personaje_activo, objetivo)

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.engine.combate_terminado:
                        self.engine.reiniciar_juego()
                
                self.handle_button_events(event)
                self.ui.process_events(event)

            self.ui.update(time_delta)

            # Dibujar
            self.screen.fill(DARK_GRAY)
            
            # Dibujar personajes
            for personaje in self.engine.personajes:
                self.ui.draw_personaje(self.screen, personaje)
            
            # Dibujar mensajes
            self.ui.draw_mensaje_estado(self.screen, self.engine.mensaje_estado)
            self.ui.draw_mensaje_combate(self.screen, self.engine.mensaje_combate)
            
            # Dibujar GUI
            self.ui.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
