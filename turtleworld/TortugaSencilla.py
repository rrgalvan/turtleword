import numpy as np
import matplotlib.pylab as plt


class TortugaSencilla(object):
    "Tortuga sencilla"

    viva = True

    def __init__(self, nombre="Dora"):
        "Constructor"
        self.posicion = np.array([0, 0])
        self.orientacion = np.array([0, 1])
        self.ruta = [self.posicion]
        self.nombre = nombre
        self.posicion_original = self.posicion
        self.orientacion_original = self.orientacion

        # Sistema de ejes de esta torutuga
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        # plt.rcParams["figure.figsize"] = [7, 7]  # tamaño de la figura

    def print_info(self):
        print(f"Tortuga '{self.nombre}")
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
        """Pinta la ruta de la tortuga"""
        listax = [P[0] for P in self.ruta]
        listay = [P[1] for P in self.ruta]

        self.ax.plot(listax, listay)

    def limpia_grafica(self):
        plt.clf()

    def reinicia(self):
        self.posicion = self.posicion_original
        self.orientacion = self.orientacion_original
        self.ruta = [self.posicion]
