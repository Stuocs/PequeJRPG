# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)
GOLD = (255, 200, 0)
BLUE = (0, 0, 255)

# Configuración de botones del juego
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_X = 350
BUTTON_Y_ATACAR = 450
BUTTON_Y_DEFENDER = 510
BUTTON_Y_CURAR = 570

# Configuración de personajes
SPRITE_SIZE = 64
SCALED_SPRITE_SIZE = 100
HIGHLIGHT_PADDING = 2
HIGHLIGHT_SIZE = SCALED_SPRITE_SIZE + (HIGHLIGHT_PADDING * 2)

# Configuración de calidad gráfica
GRAPHICS_QUALITY = {
    'Alta': {
        'sprite_scale': 1.0,
        'animation_frames': 4,
        'particles_enabled': True
    },
    'Media': {
        'sprite_scale': 0.8,
        'animation_frames': 3,
        'particles_enabled': True
    },
    'Baja': {
        'sprite_scale': 0.6,
        'animation_frames': 2,
        'particles_enabled': False
    }
}

# Configuración de audio
AUDIO_SETTINGS = {
    'music_volume': 0.5,
    'sfx_volume': 0.7,
    'channels': 8
}

# Posiciones de personajes
HERO_START_X = 50
ENEMY_START_X = SCREEN_WIDTH - 150
POSITIONS_Y = {
    'guerrero': 100,
    'mago': 200,
    'clerigo': 300,
    'paladin': 200,
    'asesino': 300
}
