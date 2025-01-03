import pygame
import sys
from pygame.locals import *

# Constantes de configuración
WIDTH, HEIGHT = 500, 400
FPS = 20
BLACK = (0, 0, 0)
MIN_VOLUME = 0.0
MAX_VOLUME = 1.0
VOLUME_STEP = 0.05

class SoundManager:
    def __init__(self, music_path, sonido_img, mute_img, icon_position):
        # Cargar música de fondo
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)  # Volumen inicial
        except pygame.error as e:
            print(f"Error al cargar la música: {e}")
            pygame.quit()
            sys.exit()

        self.icon_position = icon_position

  

class Player:
    def __init__(self, images, position, velocidad, pantalla_width):
        self.quieto = images['quieto']
        self.camina = images['camina']
        self.pos_x, self.pos_y = position
        self.velocidad = velocidad
        self.izquierda = False
        self.derecha = False
        self.salto = False
        self.cuentaSalto = 10
        self.cuentaPasos = 0
        self.ancho = 40
        self.pantalla_width = pantalla_width

    def handle_movement(self, keys):
        # Movimientos horizontales
        if keys[K_a] and self.pos_x > self.velocidad:
            self.pos_x -= self.velocidad
            self.izquierda = True
            self.derecha = False
        elif keys[K_d] and self.pos_x < self.pantalla_width - self.velocidad - self.ancho:
            self.pos_x += self.velocidad
            self.izquierda = False
            self.derecha = True
        else:
            self.izquierda = False
            self.derecha = False
            self.cuentaPasos = 0

        # Movimientos verticales
        if keys[K_w] and self.pos_y > 100:
            self.pos_y -= self.velocidad
        if keys[K_s] and self.pos_y < 300:
            self.pos_y += self.velocidad

        # Lógica de salto
        if not self.salto:
            if keys[K_SPACE]:
                self.salto = True
                self.izquierda = False
                self.derecha = False
                self.cuentaPasos = 0
        else:
            if self.cuentaSalto >= -10:
                self.pos_y -= (self.cuentaSalto * abs(self.cuentaSalto)) * 0.5
                self.cuentaSalto -= 1
            else:
                self.cuentaSalto = 10
                self.salto = False

    def update(self, pantalla, fondo_width, fondo_velocity):
        # Animación del fondo
        fondo_x_relativa = fondo_velocity.x % fondo_width
        pantalla.blit(fondo_velocity.fondo, (fondo_x_relativa - fondo_width, 0))
        if fondo_x_relativa < WIDTH:
            pantalla.blit(fondo_velocity.fondo, (fondo_x_relativa, 0))
        fondo_velocity.x -= fondo_velocity.speed

        # Animación del personaje
        if self.cuentaPasos >= len(self.camina):
            self.cuentaPasos = 0

        if self.izquierda or self.derecha or self.salto:
            pantalla.blit(self.camina[self.cuentaPasos], (int(self.pos_x), int(self.pos_y)))
            self.cuentaPasos += 1
        else:
            pantalla.blit(self.quieto, (int(self.pos_x), int(self.pos_y)))


class Fondo:
    def __init__(self, image_path, velocidad):
        try:
            self.fondo = pygame.image.load(image_path).convert()
        except pygame.error as e:
            print(f"Error al cargar el fondo: {e}")
            pygame.quit()
            sys.exit()
        self.x = 0
        self.speed = velocidad

class Game:
    def __init__(self):
        # Inicialización de Pygame
        pygame.init()

        # Configuración de la pantalla
        self.pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ovejita")

        # Configuración del reloj para controlar FPS
        self.clock = pygame.time.Clock()

        # Cargar y configurar música y sonido
        self.sound_manager = SoundManager(
            music_path='sonido.ogg',
            sonido_img='imagenes/sonido.png',
            mute_img='imagenes/mute.png',
            icon_position=(450, 25)
        )

        # Cargar imágenes y configurarlas
        self.load_images()

        # Crear instancias de fondo y jugador
        self.fondo = Fondo("imagenes/fondo.png", velocidad=5)
        self.player = Player(
            images={
                'quieto': self.quieto,
                'camina': self.camina
            },
            position=(50, 200),
            velocidad=10,
            pantalla_width=WIDTH
        )

    def update(self):
        self.player.y+=10
        if self.player.top>400:
            self.player.bottom=400
        self.velocidad_x = 0
        self.velocidad_y = 0
        if self.player.right > HEIGHT:
	        self.player.right = HEIGHT
        elif self.player.left<0:
            self.player.left=0

    def load_images(self):
        # Cargar imágenes necesarias
        try:
            self.icono = pygame.image.load("imagenes/oveja.png").convert_alpha()
            pygame.display.set_icon(self.icono)

            self.quieto = pygame.image.load('imagenes/oveja1.png').convert_alpha()
            camina_images = [
                pygame.image.load('imagenes/oveja2.png').convert_alpha(),
                pygame.image.load('imagenes/oveja3.png').convert_alpha(),
                pygame.image.load('imagenes/oveja4.png').convert_alpha(),
                pygame.image.load('imagenes/oveja5.png').convert_alpha(),
                pygame.image.load('imagenes/oveja5.png').convert_alpha()
            ]
            self.camina = camina_images
        except pygame.error as e:
            print(f"Error al cargar imágenes: {e}")
            pygame.quit()
            sys.exit()

        
    def run(self):
        # Bucle principal del juego
        ejecuta = True
        while ejecuta:
            # Controlar FPS
            self.clock.tick(FPS)

            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ejecuta = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_9:
                        self.sound_manager.decrease_volume()
                    elif event.key == pygame.K_0:
                        self.sound_manager.increase_volume()
                    elif event.key == pygame.K_m:
                        self.sound_manager.mute_sound()
                    elif event.key == pygame.K_COMMA:
                        self.sound_manager.unmute_sound()

            # Obtener el estado de las teclas
            keys = pygame.key.get_pressed()

            # Actualizar movimientos del jugador
            self.player.handle_movement(keys)

            # Actualizar y dibujar fondo y jugador
            self.player.update(self.pantalla, self.fondo.fondo.get_rect().width, self.fondo)

            # Actualizar la pantalla
            pygame.display.update()

        # Salida del juego
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
