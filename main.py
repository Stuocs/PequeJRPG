import pygame
import random
import pygame_gui
from config import *
from game_engine import GameEngine
from ui import GameUI
from menu import Menu
from audio_manager import AudioManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RPG TurnBased Game")
        
        # Inicializar componentes
        self.menu = Menu(self.screen)
        self.engine = None
        self.ui = None
        self.audio = AudioManager()
        self.clock = pygame.time.Clock()
        self.game_state = 'menu'  # Estados: 'menu', 'game'

    def init_game(self, selected_allies, selected_enemies):
        """Inicializa el juego con los equipos seleccionados"""
        self.engine = GameEngine(selected_allies, selected_enemies)
        self.ui = GameUI()
        self.engine.posicionar_personajes()
        self.audio.play_bgm('battle')

    def handle_game_events(self, event):
        """Maneja los eventos durante el juego"""
        if event.type == pygame.USEREVENT:
            if hasattr(event, 'user_type'):
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if self.engine.esperando_accion and not self.engine.combate_terminado:
                        personaje_activo = self.engine.personajes[self.engine.turno_personaje]
                        
                        if event.ui_element == self.ui.atacar_boton:
                            objetivos_posibles = self.engine.get_objetivos_posibles()
                            if objetivos_posibles:
                                objetivo = random.choice(objetivos_posibles)
                                self.engine.manejar_accion('atacar', personaje_activo, objetivo)
                                self.audio.play_sound('attack')
                        
                        elif event.ui_element == self.ui.defender_boton:
                            self.engine.manejar_accion('defender', personaje_activo)
                            self.audio.play_sound('defend')
                        
                        elif event.ui_element == self.ui.curar_boton:
                            objetivos_posibles = self.engine.get_aliados_posibles()
                            if objetivos_posibles:
                                objetivo = random.choice(objetivos_posibles)
                                self.engine.manejar_accion('curar', personaje_activo, objetivo)
                                self.audio.play_sound('heal')

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state = 'menu'
                self.audio.play_bgm('menu')
            elif event.key == pygame.K_SPACE and self.engine and self.engine.combate_terminado:
                if "ganado" in self.engine.mensaje_estado:
                    self.audio.play_sound('victory')
                else:
                    self.audio.play_sound('defeat')
                self.engine.reiniciar_juego()

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.game_state == 'menu':
                    # Procesar eventos del menú
                    if not self.menu.process_events(event):
                        running = False
                    
                    # Verificar si debemos cambiar al estado de juego
                    if self.menu.state == 'game':
                        self.game_state = 'game'
                        allies, enemies = self.menu.get_selected_teams()
                        if allies and enemies:
                            self.init_game(allies, enemies)
                else:
                    self.handle_game_events(event)
                    if self.ui:
                        self.ui.process_events(event)

            # Actualizar y dibujar según el estado actual
            if self.game_state == 'menu':
                self.menu.update(time_delta)
                self.menu.draw()
            else:
                if self.ui and self.engine:
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

        # Limpiar recursos al salir
        self.audio.stop_bgm()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
