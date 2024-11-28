import pygame
import random
from config import *

class RoguelikeMap:
    def __init__(self, seed=None):
        self.seed = seed if seed else random.randint(0, 999999)
        random.seed(self.seed)
        
        # Tamaño del mapa (en tiles)
        self.width = 20
        self.height = 15
        
        # Tamaño de cada tile
        self.tile_size = 40
        
        # Generar el mapa usando un algoritmo más simple
        self.map = self.generate_map()
        
        # Posición del jugador (asegurando que esté en un espacio abierto)
        self.player_pos = self.find_valid_position()
        
        # Lista de enemigos en el mapa
        self.enemies = self.generate_enemies()
        
        # Cargar sprites de movimiento
        self.walking_sprites = {}
        self.load_walking_sprites()
        
        # Animación
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 100  # milisegundos
        self.moving = False
        self.facing = 'right'  # 'left', 'right', 'up', 'down'

    def load_walking_sprites(self):
        """Carga los sprites de movimiento para cada personaje"""
        character_names = ['Thorgar', 'Eldrin', 'Liora', 'Shadow', 'Arthas']
        for name in character_names:
            spritesheet = pygame.image.load(f'Personajes/{name}_Caminando.png')
            frames = []
            # Asumiendo que el spritesheet tiene 4 frames horizontalmente
            frame_width = spritesheet.get_width() // 4
            frame_height = spritesheet.get_height()
            
            for i in range(4):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(spritesheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (self.tile_size, self.tile_size))
                frames.append(frame)
            self.walking_sprites[name] = frames

    def generate_map(self):
        """Genera un mapa usando un algoritmo de salas y pasillos"""
        # Inicializar mapa con paredes
        map_array = [[1 for x in range(self.width)] for y in range(self.height)]
        
        # Crear una sala central grande
        room_x = self.width // 4
        room_y = self.height // 4
        room_w = self.width // 2
        room_h = self.height // 2
        
        for y in range(room_y, room_y + room_h):
            for x in range(room_x, room_x + room_w):
                map_array[y][x] = 0
        
        # Crear pasillos aleatorios
        for _ in range(5):
            x = random.randint(1, self.width-2)
            y = random.randint(1, self.height-2)
            length = random.randint(3, 6)
            horizontal = random.choice([True, False])
            
            if horizontal:
                for dx in range(min(length, self.width-x-1)):
                    map_array[y][x+dx] = 0
            else:
                for dy in range(min(length, self.height-y-1)):
                    map_array[y+dy][x] = 0
        
        # Asegurar que hay suficiente espacio para moverse
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                if map_array[y][x] == 0:
                    # Crear más espacio alrededor de los espacios vacíos
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if random.random() < 0.4:  # 40% de probabilidad
                                ny, nx = y + dy, x + dx
                                if 0 < ny < self.height-1 and 0 < nx < self.width-1:
                                    map_array[ny][nx] = 0
        
        return map_array

    def find_valid_position(self):
        """Encuentra una posición válida para el jugador"""
        while True:
            x = random.randint(1, self.width-2)
            y = random.randint(1, self.height-2)
            if self.map[y][x] == 0:
                # Verificar que hay al menos un camino libre adyacente
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    if self.map[y+dy][x+dx] == 0:
                        return [x, y]

    def generate_enemies(self):
        """Genera enemigos en posiciones aleatorias del mapa"""
        enemies = []
        character_names = ['Thorgar', 'Eldrin', 'Liora', 'Shadow', 'Arthas']
        num_enemies = 5
        
        for _ in range(num_enemies):
            pos = self.find_valid_position()
            if pos != self.player_pos:
                enemies.append({
                    'pos': pos,
                    'type': random.choice(character_names),
                    'active': True
                })
        
        return enemies

    def move_player(self, dx, dy):
        """Mueve al jugador en la dirección especificada"""
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Actualizar dirección
        if dx > 0:
            self.facing = 'right'
        elif dx < 0:
            self.facing = 'left'
        elif dy > 0:
            self.facing = 'down'
        elif dy < 0:
            self.facing = 'up'
        
        # Verificar colisiones
        if (0 <= new_x < self.width and 
            0 <= new_y < self.height and 
            self.map[new_y][new_x] == 0):
            self.player_pos = [new_x, new_y]
            self.moving = True
            return True
        return False

    def check_enemy_collision(self):
        """Verifica si el jugador ha colisionado con un enemigo"""
        for enemy in self.enemies:
            if enemy['active'] and enemy['pos'] == self.player_pos:
                enemy['active'] = False
                return enemy['type']
        return None

    def update(self, dt):
        """Actualiza la animación"""
        if self.moving:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_delay:
                self.current_frame = (self.current_frame + 1) % 4
                self.animation_timer = 0
                if self.current_frame == 0:
                    self.moving = False

    def draw(self, screen, player_character):
        """Dibuja el mapa y los personajes"""
        # Dibujar el mapa
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, 
                                 self.tile_size, self.tile_size)
                color = (100, 100, 100) if self.map[y][x] else (200, 200, 200)
                pygame.draw.rect(screen, color, rect)
                if self.map[y][x]:
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            if enemy['active']:
                sprite = self.walking_sprites[enemy['type']][0]
                screen.blit(sprite, 
                          (enemy['pos'][0] * self.tile_size, 
                           enemy['pos'][1] * self.tile_size))
        
        # Dibujar jugador
        frame = self.current_frame if self.moving else 0
        sprite = self.walking_sprites[player_character][frame]
        if self.facing == 'left':
            sprite = pygame.transform.flip(sprite, True, False)
        
        screen.blit(sprite, 
                   (self.player_pos[0] * self.tile_size, 
                    self.player_pos[1] * self.tile_size))
