

class bala (object, dueño, mundo):

    cont = 3
    enabled = True

    def check_collision():
        for tort in mundo.ListaTortugas:
            if self.posicion == tort.posicion:
                tort.viva = False
                self.enabled = False
        self.explodes()

    def __init__(self):
        self.posicion = dueño.posicion
        self.orientacion = dueño.orientacion
        self.check_collision()

    def bala_avanza():
        if self.enabled == True:
            bala.posicion = bala.posicion+orientacion
            self.check_collision()
            self.cont = self.cont-1

    def explodes():
        if (self.cont == 0 and self.enabled == True):
            for tort in mundo.ListaTortugas:
                if (((self.posicion[0]-tort.posicion[0])**2+(self.posicion[0]-tort.posicion[0])**2)**(1/2) <= 1):
                    tort.viva = False
            self.enabled = False
