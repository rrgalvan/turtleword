import sys
import pygame
import numpy as np
from pygame.locals import *

# ---------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------


WIDTH = 900
HEIGHT = 900


# ---------------------------------------------------------------------
# Clases
# ----------------------------------------------------------------------


class Bala(pygame.sprite.Sprite):

    def __init__(self, dueno, orient, predSpeed, coordx=0, coordy=0, img="bala.png"):

        pygame.sprite.Sprite.__init__(self)

        self.dueno = dueno
        self.orientacion = orient
        self.image = pygame.transform.rotate(
            load_image(img, True), self.orientacion-90)
        self.rect = self.image.get_rect()
        self.rect.centerx = coordx
        self.rect.centery = coordy
        self.speed = predSpeed
        self.timeExp = 40

    def explode(self, screen):

        self.speed = 0

        if self.timeExp >= 0:
            self.timeExp -= 1
            screen.blit(load_image("misilfuera.png", True), self.rect)

    def avanzar(self, time, screen):

        if self.rect.left <= 0 or self.rect.right >= WIDTH or self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.image = load_image("smalltrans.png", True)
            self.explode(screen)

        else:
            self.rect.centerx += self.speed * \
                np.sin(self.orientacion/180*np.pi) * time
            self.rect.centery += self.speed * \
                np.cos(self.orientacion/180*np.pi) * time

    def check_collide(self, tort, screen, listTort):
        if tort.nombre != self.dueno:
            if pygame.sprite.collide_rect(self, tort):
                self.image = load_image("smalltrans.png", True)
                self.explode(screen)
                tort.die(listTort)


class TortugaPacifica(pygame.sprite.Sprite):

    def __init__(self, nombre="Dora", coordx=0, coordy=0, img="turtle.png"):

        pygame.sprite.Sprite.__init__(self)

        self.nombre = nombre
        self.image = load_image(img, True)
        self.origImage = load_image(img, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = coordx
        self.rect.centery = coordy
        self.speed = 0
        self.orientacion = 180

    def avanzar(self, time):

        if self.rect.left <= 0 and self.orientacion % 360 >= 180 and self.orientacion % 360 <= 360:
            self.speed = 0

        elif self.rect.right >= WIDTH and self.orientacion % 360 >= 0 and self.orientacion % 360 <= 180:
            self.speed = 0

        elif self.rect.top <= 0 and self.orientacion % 360 >= 90 and self.orientacion % 360 <= 270:
            self.speed = 0

        elif self.rect.bottom >= HEIGHT and ((self.orientacion % 360 >= 0 and self.orientacion % 360 <= 90) or (self.orientacion % 360 >= 270 and self.orientacion % 360 <= 360)):
            self.speed = 0

        else:
            self.rect.centerx += self.speed * \
                np.sin(self.orientacion/180*np.pi) * time
            self.rect.centery += self.speed * \
                np.cos(self.orientacion/180*np.pi) * time

    def girar(self, angulo):

        self.orientacion += angulo
        self.image = pygame.transform.rotate(
            self.origImage, self.orientacion-180)
        self.rect = self.image.get_rect(
            center=self.rect.center)

    def die(self, listTort):

        self.speed = 0
        self.image = load_image("ceniza.png", True)
        listTort.remove(self)


class TortugaGuerrillera(TortugaPacifica):

    def __init__(self, nombre="Fulgencio", coordx=0, coordy=0, img="tortugaCañon.png"):

        TortugaPacifica.__init__(self, nombre, coordx, coordy, img)
        self.ammo = 10

    def fire(self):

        self.ammo -= 1
        x = Bala(
            self.nombre, self.orientacion, 0.3,
            self.rect.centerx, self.rect.centery)
        return x

# ---------------------------------------------------------------------

# Funciones

# ---------------------------------------------------------------------


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    pygame.display.set_caption("TurtleWorld")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    clock = pygame.time.Clock()

    Emiliano = TortugaGuerrillera("Emiliano", 220, 220)
    Fulgencio = TortugaPacifica("Fulgencio", 600, 600)
    Manolito = TortugaPacifica("Manolito", 500, 100)
    Paquito = TortugaPacifica("Paquito", 100, 500)

    Balas = []
    Tortugas = [Emiliano, Fulgencio, Manolito, Paquito]
    TortugasVivas = [Emiliano, Fulgencio, Manolito, Paquito]

    while True:

        time = clock.tick(60)

        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
            elif eventos.type == pygame.KEYDOWN:

                if eventos.key == K_RIGHT:
                    Emiliano.girar(-15)

                if eventos.key == K_LEFT:
                    Emiliano.girar(15)

                if eventos.key == K_UP:
                    if Emiliano.speed < 0.3:
                        Emiliano.speed += 0.1

                if eventos.key == K_DOWN:
                    if Emiliano.speed > 0:
                        Emiliano.speed -= 0.1

                if eventos.key == K_SPACE:
                    Balas.append(Emiliano.fire())

        screen.blit(background, (0, 0))

        for tortuga in Tortugas:
            tortuga.avanzar(time)
            screen.blit(tortuga.image, tortuga.rect)

        for bala in Balas:
            bala.avanzar(time, screen)
            for tortuga in TortugasVivas:
                bala.check_collide(tortuga, screen, TortugasVivas)
            screen.blit(bala.image, bala.rect)

        pygame.display.flip()

    return 0


def load_image(filename, transparent=False):
    image = pygame.image.load(filename)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image
# ---------------------------------------------------------------------


pygame.init()
main()
