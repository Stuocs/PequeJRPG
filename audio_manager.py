import pygame
import os

class AudioManager:
    def __init__(self):
        # Inicializar el mezclador de audio con configuración optimizada
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        
        # Configurar volumen inicial
        self.volume = 0.5
        self.current_bgm = None
        self.sounds = {}
        self.bgm_sounds = {}
        
        print("Iniciando carga de audio...")
        
        # Configurar canales de audio
        pygame.mixer.set_num_channels(8)
        self.music_channel = pygame.mixer.Channel(0)
        self.effect_channel = pygame.mixer.Channel(1)
        
        # Pre-cargar efectos de sonido
        self._preload_sound_effects()
        
        # Pre-cargar música de fondo
        self._preload_background_music()
        
        print("Audio cargado!")

    def _preload_sound_effects(self):
        """Pre-carga todos los efectos de sonido"""
        sound_files = {
            'attack': 'audio/se/Attack1.ogg',
            'heal': 'audio/se/Absorb1.ogg',
            'defend': 'audio/se/Bell1.ogg',
            'menu_select': 'audio/se/Bell2.ogg'
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(self.volume)
                    self.sounds[name] = sound
                    print(f"Cargado efecto de sonido: {name}")
                except:
                    print(f"Error al cargar el sonido: {path}")

    def _preload_background_music(self):
        """Pre-carga toda la música de fondo"""
        music_files = {
            'menu': 'audio/bgm/Theme1.ogg',
            'battle': 'audio/bgm/Battle1.ogg'
        }
        
        for name, path in music_files.items():
            if os.path.exists(path):
                try:
                    music = pygame.mixer.Sound(path)
                    music.set_volume(self.volume)
                    self.bgm_sounds[name] = music
                    print(f"Cargada música: {name}")
                except:
                    print(f"Error al cargar la música: {path}")

    def play_sound(self, name):
        """Reproduce un efecto de sonido"""
        if name in self.sounds:
            # Usar un canal específico para efectos de sonido
            self.effect_channel.play(self.sounds[name])

    def play_bgm(self, track_name):
        """Cambia la música de fondo"""
        if track_name in self.bgm_sounds and self.current_bgm != track_name:
            # Detener la música actual si existe
            if self.current_bgm and self.current_bgm in self.bgm_sounds:
                self.bgm_sounds[self.current_bgm].stop()
            
            # Reproducir la nueva música
            self.current_bgm = track_name
            self.music_channel.play(self.bgm_sounds[track_name], loops=-1)

    def set_volume(self, volume):
        """Establece el volumen global"""
        self.volume = volume / 100.0
        
        # Actualizar volumen de efectos de sonido
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
        
        # Actualizar volumen de música
        for music in self.bgm_sounds.values():
            music.set_volume(self.volume)
        
        # Actualizar volumen de canales
        self.music_channel.set_volume(self.volume)
        self.effect_channel.set_volume(self.volume)

    def stop_bgm(self):
        """Detiene la música actual"""
        if self.current_bgm and self.current_bgm in self.bgm_sounds:
            self.bgm_sounds[self.current_bgm].stop()
        self.current_bgm = None

    def cleanup(self):
        """Limpia todos los recursos de audio"""
        self.stop_bgm()
        pygame.mixer.quit()
