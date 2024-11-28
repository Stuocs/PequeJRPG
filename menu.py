import pygame
import pygame_gui
from config import *
from audio_manager import AudioManager
from character_select import CharacterSelect

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.audio = AudioManager()
        self.state = 'main'  # Estados: 'main', 'config', 'character_select', 'game'
        
        # Calcular posiciones centrales para los botones
        self.button_width = 200
        self.button_height = 50
        self.spacing = 20
        self.start_y = SCREEN_HEIGHT // 3
        
        self.create_main_menu()
        self.create_config_menu()
        self.hide_config_menu()
        
        # Inicializar selector de personajes
        self.character_select = CharacterSelect(screen, single_character=True)
        
        # Personaje seleccionado
        self.selected_character = None
        
        # Iniciar música del menú
        self.audio.play_bgm('menu')

    def create_main_menu(self):
        # Crear botones del menú principal
        self.iniciar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - self.button_width//2, self.start_y),
                                    (self.button_width, self.button_height)),
            text='Iniciar Aventura',
            manager=self.manager
        )
        
        self.config_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - self.button_width//2, 
                                     self.start_y + self.button_height + self.spacing),
                                    (self.button_width, self.button_height)),
            text='Configuración',
            manager=self.manager
        )
        
        self.salir_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - self.button_width//2, 
                                     self.start_y + 2 * (self.button_height + self.spacing)),
                                    (self.button_width, self.button_height)),
            text='Salir',
            manager=self.manager
        )

    def create_config_menu(self):
        title_height = 30
        label_height = 20
        
        # Título de Calidad Gráfica
        self.calidad_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - self.button_width//2, self.start_y),
                                    (self.button_width, label_height)),
            text='Calidad Gráfica',
            manager=self.manager
        )
        
        # Dropdown de Calidad
        self.calidad_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['Alta', 'Media', 'Baja'],
            starting_option='Alta',
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - self.button_width//2, 
                                     self.start_y + label_height),
                                    (self.button_width, self.button_height)),
            manager=self.manager
        )
        
        # Título de Volumen
        self.volumen_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - self.button_width//2, 
                                     self.start_y + self.button_height + self.spacing + label_height),
                                    (self.button_width, label_height)),
            text='Volumen',
            manager=self.manager
        )
        
        # Slider de Volumen
        self.volumen_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - self.button_width//2, 
                                     self.start_y + self.button_height + self.spacing + label_height * 2),
                                    (self.button_width, self.button_height)),
            start_value=50,
            value_range=(0, 100),
            manager=self.manager
        )
        
        # Botón Volver
        self.volver_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - self.button_width//2, 
                                     self.start_y + 2 * (self.button_height + self.spacing) + label_height * 2),
                                    (self.button_width, self.button_height)),
            text='Volver',
            manager=self.manager
        )

    def hide_main_menu(self):
        self.iniciar_button.hide()
        self.config_button.hide()
        self.salir_button.hide()

    def show_main_menu(self):
        self.iniciar_button.show()
        self.config_button.show()
        self.salir_button.show()

    def hide_config_menu(self):
        self.calidad_label.hide()
        self.calidad_dropdown.hide()
        self.volumen_label.hide()
        self.volumen_slider.hide()
        self.volver_button.hide()

    def show_config_menu(self):
        self.calidad_label.show()
        self.calidad_dropdown.show()
        self.volumen_label.show()
        self.volumen_slider.show()
        self.volver_button.show()

    def process_events(self, event):
        if self.state == 'character_select':
            done, selected_character = self.character_select.handle_event(event)
            if done and selected_character:
                self.selected_character = selected_character
                self.state = 'game'
                return True
            return True

        if event.type == pygame.USEREVENT:
            if hasattr(event, 'user_type'):
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    self.audio.play_sound('menu_select')
                    
                    if event.ui_element == self.iniciar_button:
                        self.state = 'character_select'
                        self.hide_main_menu()
                        return True
                    
                    elif event.ui_element == self.config_button:
                        self.state = 'config'
                        self.hide_main_menu()
                        self.show_config_menu()
                    
                    elif event.ui_element == self.salir_button:
                        return False
                    
                    elif event.ui_element == self.volver_button:
                        self.state = 'main'
                        self.hide_config_menu()
                        self.show_main_menu()
                
                elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.volumen_slider:
                        self.audio.set_volume(event.value)
        
        self.manager.process_events(event)
        return True

    def update(self, time_delta):
        if self.state == 'character_select':
            self.character_select.update(time_delta)
        else:
            self.manager.update(time_delta)

    def draw(self):
        self.screen.fill(DARK_GRAY)
        if self.state == 'character_select':
            self.character_select.draw()
        else:
            self.manager.draw_ui(self.screen)

    def get_selected_teams(self):
        """Retorna el personaje seleccionado para la exploración"""
        return [self.selected_character] if self.selected_character else None, None
