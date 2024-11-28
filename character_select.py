import pygame
import pygame_gui
import os
from config import *

class CharacterSelect:
    def __init__(self, screen, single_character=False):
        self.screen = screen
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.single_character = single_character
        self.selected_character = None
        self.characters = self.load_characters()
        self.setup_ui()

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
                    'selected': False,
                    'rect': None,
                    'description': self.get_character_description(char_name)
                }
        return characters

    def get_character_description(self, name):
        """Retorna la descripción del personaje"""
        descriptions = {
            'Thorgar': "Guerrero: Especialista en combate cuerpo a cuerpo",
            'Eldrin': "Mago: Domina los elementos y la magia",
            'Liora': "Clérigo: Experta en curación y apoyo",
            'Shadow': "Asesino: Maestro del sigilo y daño rápido",
            'Arthas': "Paladín: Combina fuerza y magia sagrada"
        }
        return descriptions.get(name, "")

    def setup_ui(self):
        # Título para la selección
        title_text = "Selecciona tu Personaje" if self.single_character else "Selecciona tu Equipo (0/3)"
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - 200, 20), (400, 50)),
            text=title_text,
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

    def handle_event(self, event):
        self.manager.process_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo
                for name, char in self.characters.items():
                    if char['rect'].collidepoint(event.pos):
                        if self.single_character:
                            # Deseleccionar personaje anterior
                            if self.selected_character:
                                self.characters[self.selected_character]['selected'] = False
                            # Seleccionar nuevo personaje
                            char['selected'] = True
                            self.selected_character = name
                        else:
                            char['selected'] = not char['selected']

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.confirm_button:
                    if self.single_character:
                        return True, self.selected_character
                    else:
                        selected = [name for name, char in self.characters.items() if char['selected']]
                        if selected:
                            return True, selected

        # Actualizar estado del botón de confirmación
        if self.single_character:
            self.confirm_button.enable() if self.selected_character else self.confirm_button.disable()
        else:
            selected = len([char for char in self.characters.values() if char['selected']])
            self.confirm_button.enable() if 0 < selected <= 3 else self.confirm_button.disable()
            self.title_label.set_text(f'Selecciona tu Equipo ({selected}/3)')

        return False, None

    def draw(self):
        self.screen.fill(DARK_GRAY)
        
        # Dibujar retratos
        for name, char in self.characters.items():
            # Dibujar marco de selección si está seleccionado
            if char['selected']:
                pygame.draw.rect(self.screen, (0, 255, 0), char['rect'].inflate(4, 4), 2)
            
            # Dibujar retrato
            self.screen.blit(char['portrait'], char['rect'])
            
            # Dibujar nombre del personaje
            name_text = self.font.render(name, True, (255, 255, 255))
            name_rect = name_text.get_rect(centerx=char['rect'].centerx, 
                                         top=char['rect'].bottom + 10)
            self.screen.blit(name_text, name_rect)
            
            # Dibujar descripción si está seleccionado
            if char['selected']:
                desc_text = self.font.render(char['description'], True, (200, 200, 200))
                desc_rect = desc_text.get_rect(centerx=SCREEN_WIDTH//2,
                                             top=char['rect'].bottom + 50)
                self.screen.blit(desc_text, desc_rect)

        self.manager.draw_ui(self.screen)

    def update(self, time_delta):
        self.manager.update(time_delta)
