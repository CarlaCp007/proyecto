import pygame
import sys
from pygame.locals import *
import random
import os

# Definiciones de constantes
ANCHO = 500
ALTO = 400
FPS = 30
NEGRO = (0, 0, 0)

def resource_path(relative_path):
    """
    Obtiene la ruta absoluta al recurso, funcionando tanto en desarrollo como en el ejecutable.
    """
    try:
        # PyInstaller crea un atributo _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Fondo:
    """
    Clase para manejar el fondo del juego.
    """
    def __init__(self, image_path, velocidad):
        try:
            self.fondo = pygame.image.load(resource_path(image_path)).convert()
        except pygame.error as e:
            print(f"Error al cargar el fondo: {e}")
            pygame.quit()
            sys.exit()
        self.x = 0
        self.speed = velocidad

    def update(self):
        # Aquí podrías implementar movimiento del fondo si lo deseas
        pass

class Player(pygame.sprite.Sprite):
    """
    Clase para el sprite del jugador.
    """
    def __init__(self, image_path):
        super().__init__()
        # Cargar imagen del jugador
        try:
            self.image = pygame.image.load(resource_path(image_path)).convert_alpha()
            self.image.set_colorkey(NEGRO)  # Hace transparente el fondo negro de la imagen
        except pygame.error as e:
            print(f"Error al cargar la imagen del jugador: {e}")
            pygame.quit()
            sys.exit()
        
        # Obtener el rectángulo (sprite)
        self.rect = self.image.get_rect()
        # Centrar el rectángulo (sprite)
        self.rect.center = (ANCHO // 2, ALTO // 2)
        # Velocidad inicial del personaje
        self.velocidad_x = 0
        self.velocidad_y = 0

    def update(self):
        """
        Actualiza la posición del jugador según las teclas pulsadas y limita su movimiento dentro de la pantalla.
        """
        # Reiniciar posición si sale por debajo de la pantalla
        if self.rect.top > ALTO:
            self.rect.bottom = 0
        
        # Velocidad predeterminada en cada bucle
        self.velocidad_x = 0
        self.velocidad_y = 0

        # Obtener el estado de las teclas
        teclas = pygame.key.get_pressed()

        # Mover el personaje según las teclas pulsadas
        if teclas[pygame.K_a]:
            self.velocidad_x = -5
        if teclas[pygame.K_d]:
            self.velocidad_x = 5
        if teclas[pygame.K_w]:
            self.velocidad_y = -5
        if teclas[pygame.K_s]:
            self.velocidad_y = 5

        # Actualizar la posición del personaje
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Limitar el movimiento al área de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
        if self.rect.top < 150:
            self.rect.top = 150

    def load_icon(self, image_path):
        """
        Cargar y establecer el icono del juego.
        """
        try:
            icono = pygame.image.load(resource_path(image_path)).convert_alpha()
            pygame.display.set_icon(icono)
        except pygame.error as e:
            print(f"Error al cargar el icono del juego: {e}")
            pygame.quit()
            sys.exit()

class Enemigo(pygame.sprite.Sprite):
    """
    Clase para los sprites de los enemigos.
    """
    def __init__(self, image_path):
        super().__init__()
        # Cargar imagen del enemigo
        try:
            self.image = pygame.image.load(resource_path(image_path)).convert_alpha()
            self.image.set_colorkey(NEGRO)  # Hace transparente el fondo negro de la imagen
        except pygame.error as e:
            print(f"Error al cargar la imagen del enemigo: {e}")
            pygame.quit()
            sys.exit()
        
        # Obtener el rectángulo (sprite)
        self.rect = self.image.get_rect()
        # Ubicación aleatoria inicial
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)  # Comienza fuera de la pantalla
        # Velocidad del enemigo
        self.velocidad = random.randint(2, 5)

    def update(self):
        """
        Movimiento básico del enemigo hacia abajo y reiniciar posición si sale de la pantalla.
        """
        self.rect.x -= self.velocidad
        self.rect.y += self.velocidad
        # Reiniciar posición si sale de la pantalla
        if self.rect.top > ALTO or self.rect.right < 0:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad = random.randint(2, 5)

def main():
    """
    Función principal del juego.
    """
    pygame.init()
    PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ovejita")
    clock = pygame.time.Clock()

    # Crear grupos de sprites
    sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()

    # Instanciar el jugador
    jugador = Player('imagenes/oveja1.png')
    sprites.add(jugador)

    # Instanciar enemigos
    for _ in range(3):  # Por ejemplo, 3 enemigos
        aguila = Enemigo('imagenes/aguila.png')
        enemigos.add(aguila)

    # Cargar el icono del juego
    jugador.load_icon('imagenes/oveja.png')

    # Instanciar el fondo (opcional)
    fondo = Fondo('imagenes/fondo.png', velocidad=5)

    # Cargar la imagen de colisión una vez (fuera del bucle)
    try:
        caida = pygame.image.load(resource_path('imagenes/caido.png')).convert_alpha()
    except pygame.error as e:
        print(f"Error al cargar la imagen de colisión: {e}")
        pygame.quit()
        sys.exit()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Actualizar sprites
        sprites.update()
        enemigos.update()

        # Detección de colisión entre el jugador y los enemigos
        colision = pygame.sprite.spritecollide(jugador, enemigos, True)
        if colision:
            print("¡Colisión detectada!")

            # Dibujar el fondo
            if hasattr(fondo, 'fondo'):
                PANTALLA.blit(fondo.fondo, (fondo.x, 0))
            else:
                PANTALLA.fill(NEGRO)

            # Dibujar los sprites antes de la imagen de caída
            sprites.draw(PANTALLA)
            enemigos.draw(PANTALLA)

            # Dibujar la imagen de colisión centrada en el jugador
            caida_rect = caida.get_rect(center=jugador.rect.center)
            PANTALLA.blit(caida, caida_rect)

            # Actualizar la pantalla para mostrar la imagen de colisión
            pygame.display.flip()

            # Pausar el juego para mostrar la imagen de caída
            pygame.time.delay(3000)  # Pausa de 1 segundo

            # Reiniciar el juego
            # Resetear posición del jugador
            jugador.rect.center = (ANCHO // 2, ALTO // 2)

            # Reiniciar enemigos
            enemigos.empty()
            for _ in range(3):
                aguila = Enemigo('imagenes/aguila.png')
                enemigos.add(aguila)

            # Continuar con la siguiente iteración del bucle principal
            continue

        # Dibujar el fondo
        if hasattr(fondo, 'fondo'):
            PANTALLA.blit(fondo.fondo, (fondo.x, 0))
        else:
            PANTALLA.fill(NEGRO)

        # Dibujar todos los sprites
        sprites.draw(PANTALLA)
        enemigos.draw(PANTALLA)

        # Actualizar la pantalla completa
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
