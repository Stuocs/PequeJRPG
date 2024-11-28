import pygame
import random
import pygame_gui
from config import *
from game_engine import GameEngine
from ui import GameUI
from menu import Menu
from audio_manager import AudioManager
from roguelike_map import RoguelikeMap

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
        self.game_state = 'menu'  # Estados: 'menu', 'map', 'battle'
        
        # Componentes del mapa
        self.map = None
        self.selected_character = 'Thorgar'  # Personaje inicial
        
        # Control de movimiento
        self.last_movement = pygame.time.get_ticks()
        self.movement_delay = 150  # ms entre movimientos
        self.movement_keys = {
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0)
        }
        
        # Batalla actual
        self.current_battle_enemies = []

    def init_game(self, selected_allies, selected_enemies=None):
        """Inicializa el juego con los equipos seleccionados"""
        if selected_enemies:
            # Iniciar batalla directamente
            self.engine = GameEngine(selected_allies, selected_enemies)
            self.ui = GameUI()
            self.engine.posicionar_personajes()
            self.audio.play_bgm('battle')
            self.game_state = 'battle'
        else:
            # Iniciar exploración del mapa
            self.selected_character = selected_allies[0]
            self.map = RoguelikeMap()
            self.audio.play_bgm('menu')  # Cambiar por música de exploración
            self.game_state = 'map'

    def handle_map_events(self, event):
        """Maneja los eventos durante la exploración del mapa"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state = 'menu'
                self.audio.play_bgm('menu')

    def update_map(self, dt):
        """Actualiza el estado del mapa y maneja el movimiento"""
        current_time = pygame.time.get_ticks()
        
        # Solo procesar movimiento si ha pasado suficiente tiempo
        if current_time - self.last_movement >= self.movement_delay:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            
            # Procesar movimiento
            for key, (move_x, move_y) in self.movement_keys.items():
                if keys[key]:
                    dx, dy = move_x, move_y
                    break
            
            if dx != 0 or dy != 0:
                if self.map.move_player(dx, dy):
                    self.last_movement = current_time
                    self.audio.play_sound('menu_select')  # Sonido de pasos
                    
                    # Verificar colisión con enemigos
                    enemy_type = self.map.check_enemy_collision()
                    if enemy_type:
                        # Generar equipo enemigo aleatorio
                        enemy_team = [enemy_type]
                        available_enemies = ['Thorgar', 'Eldrin', 'Liora', 'Shadow', 'Arthas']
                        available_enemies.remove(enemy_type)
                        
                        # Agregar 1-2 enemigos adicionales
                        num_additional = random.randint(1, 2)
                        enemy_team.extend(random.sample(available_enemies, num_additional))
                        
                        # Iniciar batalla
                        self.init_game([self.selected_character], enemy_team)
        
        # Actualizar animaciones
        self.map.update(dt)

    def handle_battle_events(self, event):
        """Maneja los eventos durante la batalla"""
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
                self.game_state = 'map'
                self.audio.play_bgm('menu')
            elif event.key == pygame.K_SPACE and self.engine.combate_terminado:
                if "ganado" in self.engine.mensaje_estado:
                    self.audio.play_sound('victory')
                else:
                    self.audio.play_sound('defeat')
                self.game_state = 'map'
                self.audio.play_bgm('menu')

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
                        allies, _ = self.menu.get_selected_teams()
                        if allies:
                            self.init_game(allies)
                
                elif self.game_state == 'map':
                    self.handle_map_events(event)
                
                elif self.game_state == 'battle':
                    self.handle_battle_events(event)
                    if self.ui:
                        self.ui.process_events(event)

            # Actualizar y dibujar según el estado actual
            if self.game_state == 'menu':
                self.menu.update(time_delta)
                self.menu.draw()
            
            elif self.game_state == 'map':
                self.update_map(time_delta)
                self.screen.fill(DARK_GRAY)
                self.map.draw(self.screen, self.selected_character)
            
            elif self.game_state == 'battle':
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
