import pygame
import sys
from pygame.locals import *
import random
import os

ANCHO = 500
ALTO = 400
FPS = 30
NEGRO = (0, 0, 0)

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller."""
    try:
        # PyInstaller crea un atributo _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Fondo:
    def __init__(self, image_path, velocidad):
        try:
            self.fondo = pygame.image.load(resource_path(image_path)).convert()
        except pygame.error as e:
            print(f"Error al cargar el fondo: {e}")
            pygame.quit()
            sys.exit()
        self.x = 0
        self.speed = velocidad

class Player(pygame.sprite.Sprite):
    """Sprite del jugador"""
    def __init__(self, image_path):
        super().__init__()
        # Jugador
        try:
            self.image = pygame.image.load(resource_path(image_path)).convert()
            self.image.set_colorkey(NEGRO)  # Hace transparente el fondo negro de la imagen
        except pygame.error as e:
            print(f"Error al cargar la imagen del jugador: {e}")
            pygame.quit()
            sys.exit()
        
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        # Centra el rectángulo (sprite)
        self.rect.center = (ANCHO // 2, ALTO // 2)
        # Velocidad inicial del personaje
        self.velocidad_x = 0
        self.velocidad_y = 0

    def update(self):
        # Actualiza esto cada vuelta de bucle.
        # self.rect.x += 1  # Movimiento automático, opcional
        if self.rect.top > ALTO:
            self.rect.bottom = 0
        
        # Velocidad predeterminada en cada bucle
        self.velocidad_x = 0
        self.velocidad_y = 0

        # Mantiene las teclas pulsadas
        teclas = pygame.key.get_pressed()

        # Mueve el personaje hacia la izquierda
        if teclas[pygame.K_a]:
            self.velocidad_x = -5
        # Mueve el personaje hacia la derecha
        if teclas[pygame.K_d]:
            self.velocidad_x = 5
        # Mueve el personaje hacia arriba
        if teclas[pygame.K_w]:
            self.velocidad_y = -5
        # Mueve el personaje hacia abajo
        if teclas[pygame.K_s]:
            self.velocidad_y = 5

        # Actualiza la velocidad del personaje
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0
        # Limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

        # Limita el margen inferior
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

        # Limita el margen superior
        if self.rect.top < 0:
            self.rect.top = 0

    def load_images(self, image_path):
        """Cargar imágenes necesarias"""
        try:
            self.icono = pygame.image.load(resource_path(image_path)).convert_alpha()
            pygame.display.set_icon(self.icono)
        except pygame.error as e:
            print(f"Error al cargar imágenes: {e}")
            pygame.quit()
            sys.exit()

class Enemigos(pygame.sprite.Sprite):
    """Sprite de los enemigos"""
    def __init__(self, image_path):
        super().__init__()
        # Enemigo
        try:
            self.image = pygame.image.load(resource_path(image_path)).convert()
            self.image.set_colorkey(NEGRO)  # Hace transparente el fondo negro de la imagen
        except pygame.error as e:
            print(f"Error al cargar la imagen del enemigo: {e}")
            pygame.quit()
            sys.exit()
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        # Ubicación aleatoria para el sprite
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)  # Comienza fuera de la pantalla
        # Velocidad del enemigo
        self.velocidad = random.randint(1, 5)

    def update(self):
        """Movimiento básico del enemigo"""
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad = random.randint(1, 5)

pygame.init()
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ovejita")
clock = pygame.time.Clock()

# Grupo de sprites, instanciación del objeto jugador.
sprites = pygame.sprite.Group()
jugador = Player('imagenes/oveja1.png')
sprites.add(jugador)

# Instanciación de enemigos
enemigos = pygame.sprite.Group()
for _ in range(5):  # Por ejemplo, 5 enemigos
    enemigo = Enemigos('imagenes/aguila.png')
    enemigos.add(enemigo)
sprites.add(enemigos)

# Opcional: Cargar el icono del juego
jugador.load_images('imagenes/oveja.png')

# Clase Fondo (opcional, si deseas agregar un fondo en movimiento)
fondo = Fondo('imagenes/fondo.png', velocidad=5)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Actualizar sprites
    sprites.update()

    # Dibujar en la pantalla
    if hasattr(fondo, 'fondo'):
        PANTALLA.blit(fondo.fondo, (fondo.x, 0))  # Dibujar el fondo
    else:
        PANTALLA.fill(NEGRO)
    sprites.draw(PANTALLA)

    pygame.display.flip()  # Actualiza la pantalla completa
    clock.tick(FPS)
