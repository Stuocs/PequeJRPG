import pygame
import pygame_gui
import os
from config import *

class CharacterSelect:
    def __init__(self, screen):
        self.screen = screen
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.selected_allies = []
        self.selected_enemies = []
        self.characters = self.load_characters()
        self.current_team = 'allies'  # 'allies' o 'enemies'
        self.setup_ui()
        
        # Agregar botón para reiniciar selección
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 130), (200, 50)),
            text='Reiniciar Selección',
            manager=self.manager
        )

    def load_characters(self):
        """Carga la información de los personajes disponibles"""
        characters = {}
        for char_name in ['Thorgar', 'Eldrin', 'Liora', 'Shadow', 'Arthas']:
            portrait_path = f'Personajes/{char_name}_Rostro.png'
            if os.path.exists(portrait_path):
                portrait = pygame.image.load(portrait_path)
                portrait = pygame.transform.scale(portrait, (100, 100))
                characters[char_name] = {
                    'portrait': portrait,
                    'selected_allies': False,
                    'selected_enemies': False,
                    'rect': None
                }
        return characters

    def setup_ui(self):
        # Título para la selección de equipo
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - 200, 20), (400, 50)),
            text='Selecciona tu Equipo (0/3)',
            manager=self.manager
        )

        # Botón para confirmar selección
        self.confirm_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 70), (200, 50)),
            text='Confirmar Selección',
            manager=self.manager
        )
        self.confirm_button.disable()

        # Posicionar los retratos de los personajes
        x_start = 50
        y_start = 100
        spacing = 120
        for i, (name, char) in enumerate(self.characters.items()):
            char['rect'] = pygame.Rect(x_start + (i * spacing), y_start, 100, 100)

    def reset_selection(self):
        """Reinicia la selección actual"""
        if self.current_team == 'allies':
            for name in self.selected_allies:
                self.characters[name]['selected_allies'] = False
            self.selected_allies = []
        else:
            for name in self.selected_enemies:
                self.characters[name]['selected_enemies'] = False
            self.selected_enemies = []

    def toggle_character(self, name):
        """Alterna la selección de un personaje"""
        char = self.characters[name]
        current_selection = self.selected_allies if self.current_team == 'allies' else self.selected_enemies
        
        # Si el personaje ya está seleccionado en el equipo actual
        if (self.current_team == 'allies' and char['selected_allies']) or \
           (self.current_team == 'enemies' and char['selected_enemies']):
            # Deseleccionar
            if self.current_team == 'allies':
                char['selected_allies'] = False
                self.selected_allies.remove(name)
            else:
                char['selected_enemies'] = False
                self.selected_enemies.remove(name)
        # Si hay espacio para más personajes en el equipo actual
        elif len(current_selection) < 3:
            # Seleccionar
            if self.current_team == 'allies':
                char['selected_allies'] = True
                self.selected_allies.append(name)
            else:
                char['selected_enemies'] = True
                self.selected_enemies.append(name)

    def handle_event(self, event):
        self.manager.process_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo
                for name, char in self.characters.items():
                    if char['rect'].collidepoint(event.pos):
                        self.toggle_character(name)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.confirm_button:
                    if self.current_team == 'allies' and len(self.selected_allies) > 0:
                        self.current_team = 'enemies'
                        self.title_label.set_text('Selecciona el Equipo Enemigo (0/3)')
                    elif self.current_team == 'enemies' and len(self.selected_enemies) > 0:
                        return True, self.selected_allies, self.selected_enemies
                elif event.ui_element == self.reset_button:
                    self.reset_selection()

        # Actualizar estado del botón de confirmación
        if self.current_team == 'allies':
            self.confirm_button.enable() if len(self.selected_allies) > 0 else self.confirm_button.disable()
        else:
            self.confirm_button.enable() if len(self.selected_enemies) > 0 else self.confirm_button.disable()

        # Actualizar texto del título
        if self.current_team == 'allies':
            self.title_label.set_text(f'Selecciona tu Equipo ({len(self.selected_allies)}/3)')
        else:
            self.title_label.set_text(f'Selecciona el Equipo Enemigo ({len(self.selected_enemies)}/3)')

        return False, None, None

    def draw(self):
        self.screen.fill(DARK_GRAY)
        
        # Dibujar retratos
        for name, char in self.characters.items():
            # Dibujar marco según la selección actual
            if (self.current_team == 'allies' and char['selected_allies']) or \
               (self.current_team == 'enemies' and char['selected_enemies']):
                color = (0, 255, 0) if self.current_team == 'allies' else (255, 0, 0)
                pygame.draw.rect(self.screen, color, char['rect'].inflate(4, 4), 2)
            
            # Dibujar el retrato
            self.screen.blit(char['portrait'], char['rect'])
            
            # Dibujar nombre del personaje
            name_text = self.font.render(name, True, (255, 255, 255))
            name_rect = name_text.get_rect(centerx=char['rect'].centerx, 
                                         top=char['rect'].bottom + 10)
            self.screen.blit(name_text, name_rect)

        self.manager.draw_ui(self.screen)

    def update(self, time_delta):
        self.manager.update(time_delta)
