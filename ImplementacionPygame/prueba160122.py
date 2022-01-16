import sys
import pygame
import numpy as np
from pygame.locals import *
from random import randrange

# ---------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------


WIDTH = 800
HEIGHT = 800


# ---------------------------------------------------------------------
# Clases
# ----------------------------------------------------------------------


class Bala(pygame.sprite.Sprite):

    def __init__(self, dueno, orient, predSpeed, coordx=0, coordy=0, img="bala.png"):

        pygame.sprite.Sprite.__init__(self)
        # Inicializa la bala con una serie de parámetros
        self.dueno = dueno
        # Dueño de la bala
        self.orientacion = orient
        # Orientación de la bala
        self.image = pygame.transform.rotate(
            load_image(img, True), self.orientacion-90)
        # Inicializa la imagen girada
        self.rect = self.image.get_rect()
        self.rect.centerx = coordx
        self.rect.centery = coordy
        # Inicializa los rectángulos de las surfaces
        self.speed = predSpeed
        # Velocidad de la bala
        self.timeExp = 40
        # Tiempo que dura la explosión de la bala

    def explode(self, screen, Balas):
        # Método de explosión de la bala
        self.speed = 0
        # La bala se para
        if self.timeExp > 0:
            # Muestra un sprite de explosión durante 40 ticks
            self.timeExp -= 1
            screen.blit(load_image("misilfuera.png", True), self.rect)
        elif self.timeExp == 0:
            # Fin de la explosión
            Balas.remove(self)
            self.timeExp -= 1

    def avanzar(self, time, screen, Balas):
        # Método de avance de la bala
        if self.rect.left <= 0 or self.rect.right >= WIDTH or self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.image = load_image("smalltrans.png", True)
            self.explode(screen, Balas)
        # La bala explota si alcanza los límites de la pantalla
        else:
            # La bala avanza normalmente
            self.rect.centerx += self.speed * \
                np.sin(self.orientacion/180*np.pi) * time
            self.rect.centery += self.speed * \
                np.cos(self.orientacion/180*np.pi) * time

    def check_collide(self, tort, screen, listTort, Balas):
        # Comprueba si la bala colisiona con las tortugas vivas (listTort)
        if tort.nombre != self.dueno:
            if pygame.sprite.collide_rect(self, tort):
                # Si es así, la mata y la hace desaparecer
                self.image = load_image("smalltrans.png", True)
                self.explode(screen, Balas)
                tort.die(listTort)


class TortugaPacifica(pygame.sprite.Sprite):

    def __init__(self, nombre="Dora", coordx=0, coordy=0, Player=False, img="turtle.png"):

        pygame.sprite.Sprite.__init__(self)
        # Inicializa una Tortuga Pacífica con una serie de parámetros
        self.nombre = nombre
        self.image = load_image(img, True)
        self.origImage = load_image(img, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = coordx
        self.rect.centery = coordy
        self.speed = 0
        self.IA = Player

        # Da una orientación aleatoria a las tortugas controladas por IA
        if self.IA:
            self.orientacion = 180
            self.image = load_image(img, True)
        else:
            self.orientacion = randrange(0, 360, 3)
            self.image = pygame.transform.rotate(
                self.origImage, self.orientacion-180)
            self.rect = self.image.get_rect(
                center=self.rect.center)

    def avanzar(self, time):
        # Avance de la tortuga, si la tortuga es manejada por jugador, parará
        # al llegar a un borde, en caso contrario, girará y seguirá moviéndose

        if self.rect.left <= 0 and self.orientacion % 360 >= 180 and self.orientacion % 360 <= 360:
            if self.IA is not False:
                self.speed = 0
            else:
                if self.orientacion >= 180 and self.orientacion < 270:
                    self.girar(randrange(90, 270, 3))
                else:
                    self.girar(randrange(90, 270, 3))

        elif self.rect.right >= WIDTH and self.orientacion % 360 >= 0 and self.orientacion % 360 <= 180:
            if self.IA is not False:
                self.speed = 0
            else:
                if self.orientacion >= 0 and self.orientacion < 90:
                    self.girar(randrange(90, 270, 3))
                else:
                    self.girar(randrange(90, 270, 3))

        elif self.rect.top <= 0 and self.orientacion % 360 >= 90 and self.orientacion % 360 <= 270:
            if self.IA is not False:
                self.speed = 0
            else:
                if self.orientacion >= 90 and self.orientacion < 180:
                    self.girar(randrange(90, 270, 3))
                else:
                    self.girar(randrange(90, 270, 3))

        elif self.rect.bottom >= HEIGHT and ((self.orientacion % 360 >= 0 and self.orientacion % 360 <= 90) or (self.orientacion % 360 >= 270 and self.orientacion % 360 <= 360)):
            if self.IA is not False:
                self.speed = 0
            else:
                if self.orientacion >= 0 and self.orientacion < 90:
                    self.girar(randrange(90, 270, 3))
                else:
                    self.girar(randrange(90, 270, 3))

        else:
            self.rect.centerx += self.speed * \
                np.sin(self.orientacion/180*np.pi) * time
            self.rect.centery += self.speed * \
                np.cos(self.orientacion/180*np.pi) * time

    def girar(self, angulo):
        # Giro de la tortuga
        # El método de giro es destructivo, por lo que necesita girar la
        # imagen original

        self.orientacion += angulo
        self.image = pygame.transform.rotate(
            self.origImage, self.orientacion-180)
        self.rect = self.image.get_rect(
            center=self.rect.center)

    def die(self, listTort):
        # La tortuga al morir se para y convierte en ceniza
        self.speed = 0
        self.image = load_image("ceniza.png", True)
        listTort.remove(self)


class TortugaGuerrillera(TortugaPacifica):

    def __init__(self, nombre="Fulgencio", coordx=0, coordy=0, Player=False, img="tortugaCañon.png"):

        TortugaPacifica.__init__(self, nombre, coordx, coordy, Player, img)
        # Tortuga Guerrillera con 10 de munición
        self.ammo = 20

    def fire(self):
        # Método de disparo de la TortugaGuerrillera
        if self.ammo > 0:
            # Dispara si hay munición
            self.ammo -= 1
            x = Bala(
                self.nombre, self.orientacion, 0.3,
                self.rect.centerx, self.rect.centery)
            return x
        else:
            return False

# ---------------------------------------------------------------------

# Funciones

# ---------------------------------------------------------------------


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    # Crea un entorno en el que jugar
    pygame.display.set_caption("TurtleWorld")
    # Establece el nombre de la ventana

    background = pygame.Surface(screen.get_size())
    # Crea un fondo
    background = background.convert()
    # Coloca el fondo en el tipo adecuado
    background.fill((170, 238, 187))
    # Da color al fondo

    clock = pygame.time.Clock()
    # Crea un  reloj

    # Creo unas pocas de tortugas
    Emiliano = TortugaGuerrillera("Emiliano", 220, 220, True)
    Fulgencio = TortugaPacifica("Fulgencio", 600, 600)
    Manolito = TortugaPacifica("Manolito", 500, 100)
    Paquito = TortugaPacifica("Paquito", 100, 500)

    Fulgencio.speed = 0.2
    Manolito.speed = 0.2
    Paquito.speed = 0.2

    # Creo lista de balas, tortugas y tortugas vivas
    Balas = []
    Tortugas = [Emiliano, Fulgencio, Manolito, Paquito]
    TortugasVivas = [Emiliano, Fulgencio, Manolito, Paquito]
    # TortugasIA = [Fulgencio, Manolito, Paquito]

    while True:

        time = clock.tick(60)
        # Gestiona el tiempo en el juego

        keys = pygame.key.get_pressed()  # Comprobando las teclas pulsadas
        if keys[pygame.K_RIGHT]:
            Emiliano.girar(-3)

        if keys[pygame.K_LEFT]:
            Emiliano.girar(3)

        if keys[pygame.K_UP]:
            Emiliano.speed = 0.2
        else:
            Emiliano.speed = 0

        for eventos in pygame.event.get():
            # Gestiona los distintos eventos que suceden (teclas, etc)
            if eventos.type == QUIT:
                sys.exit(0)
            elif eventos.type == pygame.KEYDOWN:
                if eventos.key == K_SPACE:
                    aux = Emiliano.fire()
                    if aux is not False:
                        Balas.append(aux)

        # Cada objeto que deba seguir representado necesita que se haga
        # un blit en cada iteración del bucle

        screen.blit(background, (0, 0))

        for tortuga in Tortugas:
            # Las tortugas avanzan y hacen blit
            tortuga.avanzar(time)
            screen.blit(tortuga.image, tortuga.rect)

        for bala in Balas:
            # Las balas avanzan, comprueban las colisiones con las tortugas
            # vivas y hacen blit
            bala.avanzar(time, screen, Balas)
            for tortuga in TortugasVivas:
                bala.check_collide(tortuga, screen, TortugasVivas, Balas)
            screen.blit(bala.image, bala.rect)

        pygame.display.flip()
        # Actualiza la pantalla en su totalidad con todos los blit

    return 0


def load_image(filename, transparent=False):
    # Copiado del tutorial, importa las imágenes para su utilización
    image = pygame.image.load(filename)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image
# ---------------------------------------------------------------------


pygame.init()
main()
