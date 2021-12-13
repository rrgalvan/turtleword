import numpy as np
import matplotlib.pylab as plt
from importlib import resources

#lo siguiente es exclusivamente para que aparezca una tortuguita en los gráficos
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2  # forma parte del paquete opencv, para procesado de imagenes.
import imutils  # mas herramientas para imagenes, conforman un paquete aparte

from turtleworld.TortugaSencilla import TortugaSencilla
# from Ipython.display import display, Image


class TortugaConIcono(TortugaSencilla):
    """
    TortugaConIcono: Tortuga sencilla que muestra un icono en los gráficos

    Utiliza la biblioteca opencv para procesado de imágenes
    """

    def __init__(self, nombre="Dora"):
        "Constructor de un objeto de tipo TortugaConIcono"
        # Llamar al constructor de la clase base
        TortugaSencilla.__init__(self, nombre)
        with resources.open_binary("turtleworld", "turtle.png") as f:
            self.icono = plt.imread(f)

    def print_info(self):
        TortugaSencilla.print_info(self)
        print("Icono de la tortuga:\n")
        plt.rcParams["figure.figsize"] = [1, 1]  # tamaño de la figura
        plt.imshow(self.icono)

    def plot(self, icono=True):
        """Pinta la ruta de la tortuga.
        Pinta el icono de la tortuga en la dirección en la que apunta al final
        de la ruta salvo que se le indique lo contrario"""

        TortugaSencilla.plot(self)
        if icono:
            im = self.icono

            #obtengo el angulo en el que apunta la tortuga al terminar la ruta, medido respecto de la parte positiva del eje OY
            angulo = np.rad2deg(np.arctan2(
                self.orientacion[1], self.orientacion[0]))-90
            #rotamos la imagén según el angulo recién calculado
            imr = imutils.rotate(im, angle=angulo)
            #incluimos en el plot la imagen a modo de anotación
            ab = AnnotationBbox(OffsetImage(
                imr, zoom=0.15), (self.posicion[0], self.posicion[1]), frameon=False)
            self.ax.add_artist(ab)
