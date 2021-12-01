import numpy as np
import matplotlib.pylab as plt
#lo siguiente es exclusivamente para que aparezca una tortuguita en los gráficos
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2 #forma parte del paquete opencv, para procesado de imagenes.
import imutils #mas herramientas para imagenes, conforman un paquete aparte

class Tortuga(object):
    "Tortuga sencilla"
    def __init__(self, nombre="Dora"):
        "Constructor"
        self.posicion = np.array([0, 0])
        self.orientacion = np.array([0, 1])
        self.ruta = [self.posicion]
        self.nombre = nombre
    def print_info(self):
        print(f"Tortuga {self.nombre:}")
        print(f"  Posición   : {self.posicion}")
        print(f"  Orientación: {self.orientacion}")
        print("Icono de la tortuga:\n")
        plt.imshow(self.icono)
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
    def plot(self,icono='true'):
        """Pinta la ruta de la tortuga. Pinta el icono de la tortuga en la dirección en la que apunta al final de la ruta salvo que se le indique lo contrario"""
        listax=[P[0] for P in self.ruta]
        listay=[P[1] for P in self.ruta]

        fig, ax = plt.subplots()
        plt.rcParams["figure.figsize"] = [10,10] #tamaño de la figura
        ax.plot(listax, listay)
        if icono=='true':
            im=self.icono

            #obtengo el angulo en el que apunta la tortuga al terminar la ruta, medido respecto de la parte positiva del eje OY
            angulo=np.rad2deg(np.arctan2(self.orientacion[1],self.orientacion[0]))-90
            #rotamos la imagén según el angulo recién calculado
            imr=imutils.rotate(im,angle=angulo)
            #incluimos en el plot la imagen a modo de anotación
            ab = AnnotationBbox(OffsetImage(imr,zoom=0.15), (self.posicion[0],self.posicion[1]), frameon=False)
            ax.add_artist(ab)