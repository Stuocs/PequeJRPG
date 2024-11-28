import random
import pygame
from config import *

def load_sprite(name):
    spritesheet = pygame.image.load(f'Personajes/{name}_Luchando.png')
    frames = []
    for i in range(4):
        frame = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
        frame.blit(spritesheet, (0, 0), (i * SPRITE_SIZE, 0, SPRITE_SIZE, SPRITE_SIZE))
        frame = pygame.transform.scale(frame, (SCALED_SPRITE_SIZE, SCALED_SPRITE_SIZE))
        frames.append(frame)
    return frames

class Personaje:
    def __init__(self, nombre, vida, ataque, defensa):
        self.nombre = nombre
        self.vida = vida
        self.vida_maxima = vida
        self.ataque = ataque
        self.defensa = defensa
        self.frames = load_sprite(nombre)
        self.frame_actual = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.delay_animacion = 100
        self.animando = False
        self.rect = self.frames[0].get_rect()
        self.destacado = False
        self.tiempo_destacado = 0
        self.defensa_original = defensa
        
    def actualizar_animacion(self):
        ahora = pygame.time.get_ticks()
        if self.animando:
            if ahora - self.ultimo_update > self.delay_animacion:
                self.ultimo_update = ahora
                self.frame_actual = (self.frame_actual + 1) % len(self.frames)
                if self.frame_actual == 0:
                    self.animando = False
        else:
            self.frame_actual = 0
            
    def get_sprite(self):
        return self.frames[self.frame_actual]

    def actualizar_destacado(self):
        if self.destacado and pygame.time.get_ticks() - self.tiempo_destacado > 200:
            self.destacado = False

    def defender(self):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.defensa = self.defensa_original * 2

    def restaurar_defensa(self):
        self.defensa = self.defensa_original

    def esta_vivo(self):
        return self.vida > 0

    def reiniciar(self):
        self.vida = self.vida_maxima
        self.defensa = self.defensa_original
        self.destacado = False
        self.animando = False

class Guerrero(Personaje):
    def __init__(self):
        super().__init__("Thorgar", 100, 20, 5)
        self.fuerza = 20

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        daño = random.randint(1, 20) + self.fuerza // 2
        enemigo.vida = max(0, enemigo.vida - max(0, daño - enemigo.defensa))
        enemigo.destacado = True
        enemigo.tiempo_destacado = pygame.time.get_ticks()
        return daño

class Mago(Personaje):
    def __init__(self):
        super().__init__("Eldrin", 80, 15, 3)
        self.inteligencia = 25

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        daño = random.randint(1, 20) + self.inteligencia
        enemigo.vida = max(0, enemigo.vida - max(0, daño - enemigo.defensa))
        enemigo.destacado = True
        enemigo.tiempo_destacado = pygame.time.get_ticks()
        return daño

class Asesino(Personaje):
    def __init__(self):
        super().__init__("Shadow", 70, 30, 3)
        self.destreza = 15

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        daño = random.randint(1, 10) + random.randint(1, 10) + self.destreza * 2
        enemigo.vida = max(0, enemigo.vida - max(0, daño - enemigo.defensa))
        enemigo.destacado = True
        enemigo.tiempo_destacado = pygame.time.get_ticks()
        return daño

class Clerigo(Personaje):
    def __init__(self):
        super().__init__("Liora", 90, 0, 5)
        self.fe = 20

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        return 0

    def curar(self, aliado):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        curacion = random.randint(1, 10) + self.fe
        aliado.vida = min(aliado.vida_maxima, aliado.vida + curacion)
        return curacion

class Paladin(Personaje):
    def __init__(self):
        super().__init__("Arthas", 100, 15, 8)
        self.fuerza = 15
        self.fe = 15

    def atacar(self, enemigo):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        self.animando = True
        self.ultimo_update = pygame.time.get_ticks()
        daño = random.randint(1, 10) + self.fuerza // 2
        enemigo.vida = max(0, enemigo.vida - max(0, daño - enemigo.defensa))
        enemigo.destacado = True
        enemigo.tiempo_destacado = pygame.time.get_ticks()
        return daño

    def curar(self, aliado):
        self.destacado = True
        self.tiempo_destacado = pygame.time.get_ticks()
        curacion = random.randint(1, 5) + self.fe
        aliado.vida = min(aliado.vida_maxima, aliado.vida + curacion)
        return curacion
