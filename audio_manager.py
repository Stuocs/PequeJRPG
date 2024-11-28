import pygame
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.volume = 0.5  # 50% volumen inicial
        self.current_bgm = None
        self.sounds = {}
        
        # Cargar efectos de sonido
        self.load_sound('attack', 'audio/se/Attack1.ogg')
        self.load_sound('heal', 'audio/se/Absorb1.ogg')
        self.load_sound('victory', 'audio/me/Victory1.ogg')
        self.load_sound('defeat', 'audio/me/Defeat1.ogg')
        self.load_sound('menu_select', 'audio/se/Bell1.ogg')
        
        # Rutas de música de fondo
        self.bgm_tracks = {
            'menu': 'audio/bgm/Theme1.ogg',
            'battle': 'audio/bgm/Battle1.ogg',
            'victory': 'audio/me/Fanfare1.ogg'
        }

    def load_sound(self, name, path):
        if os.path.exists(path):
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(self.volume)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def play_bgm(self, track_name):
        if track_name in self.bgm_tracks and os.path.exists(self.bgm_tracks[track_name]):
            if self.current_bgm != track_name:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.bgm_tracks[track_name])
                pygame.mixer.music.play(-1)  # -1 para reproducir en bucle
                pygame.mixer.music.set_volume(self.volume)
                self.current_bgm = track_name

    def set_volume(self, volume):
        self.volume = volume / 100.0  # Convertir de porcentaje a float entre 0 y 1
        pygame.mixer.music.set_volume(self.volume)
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def stop_bgm(self):
        pygame.mixer.music.stop()
        self.current_bgm = None
