import numpy as np
import matplotlib.pylab as plt

class Tortuga(object):
    "Tortuga sencilla"
    def __init__(self, nombre="Sin nombre"):
        "Constructor"
        self.posicion = np.array([0, 0])
        self.orientacion = np.array([0, 1])
        self.ruta = [self.posicion]
        self.nombre = nombre
    def print_info(self):
        print(f"Tortuga {self.nombre:}")
        print(f"  Posición   : {self.posicion}")
        print(f"  Orientación: {self.orientacion}")
    def avanza(self, distancia):
        "Avanza una distancia determinada"
        self.posicion = self.posicion + distancia*self.orientacion
        self.ruta.append(self.posicion)
    def gira(self, radianes):
        M = np.array([
            [np.cos(radianes), np.sin(radianes)],
            [-np.sin(radianes), np.cos(radianes)]
        ])
        self.orientacion = np.dot(M, self.orientacion)
    def plot(self):
        lista_x = [P[0] for P in t2.ruta]
        lista_y = [P[1] for P in t2.ruta]
        plt.plot(lista_x, lista_y)
