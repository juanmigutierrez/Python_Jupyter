"""Esta es la clase Flight Operations"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import KDTree
from scipy.spatial import Delaunay
from collections import defaultdict
import itertools
from scipy.spatial import distance


class FlightOperations:
    def __init__(self, borders, airports):
        # Util para guadar los puntos
        puntos = list(zip(airports["x"], airports["y"]))
        # Es necesario guardar el nombre de los aeropuertos
        self.name_airports = airports["aeropuerto"]
        # Es necesario guardar el los bordes para imprimir el mapa de colombia
        self.Borders = borders
        # Es necesario guardar el los bordes para imprimir el mapa de colombia
        self.Airports = airports
        # Es necesario guardar los puntos (x,y)
        self.Puntos = np.array(puntos)
        # EL mas utilizado sera el Voronoi
        self.Vor = Voronoi(puntos)
        # Grafo de puntos:puntos vecinos
        self.Graph_vertices_t = self.Graph_vertices()
        # Grafo de puntos:puntos vecinos
        self.Graph_vertices_vor = self.Graph_vor_vertices()

    def plot_2d(self):
        """Se encarga de graficar el diagrama de voronoi Dos-dimensional"""
        voronoi_plot_2d(
            self.Vor,
            line_colors=[
                "#1f77b4",
                "#aec7e8",
                "#ff7f0e",
                "#ffbb78",
                "#2ca02c",
                "#98df8a",
                "#d62728",
                "#ff9896",
                "#9467bd",
                "#c5b0d5",
                "#8c564b",
                "#c49c94",
                "#e377c2",
                "#f7b6d2",
                "#7f7f7f",
                "#c7c7c7",
                "#bcbd22",
                "#dbdb8d",
                "#17becf",
                "#9edae5",
            ],
            show_vertices=False,
        )
        # Grafica lineas borde
        plt.plot(self.Borders["x"], self.Borders["y"], color="gray")
        plt.scatter(x="x", y="y", data=self.Airports, color="black", s=5)
        plt.xlabel("Longitude (degrees)")
        plt.ylabel("Latitude (degrees)")
        plt.ylim([-14, 20])
        plt.xlim([-86, -64])
        plt.title("Diagrama Voronoi Colombia")
        return None

    def plot_2d_black(self):
        """Se encarga de graficar el diagrama de voronoi Dos-dimensional"""
        voronoi_plot_2d(
            self.Vor,
            show_vertices=False,
        )
        # Grafica lineas borde
        plt.plot(self.Borders["x"], self.Borders["y"], color="gray")
        plt.scatter(x="x", y="y", data=self.Airports, color="black", s=5)
        plt.xlabel("Longitude (degrees)")
        plt.ylabel("Latitude (degrees)")
        plt.ylim([-14, 20])
        plt.xlim([-86, -64])
        plt.title("Caminos Voronoi Colombia")
        return None

    def plot_2d_numbers(self):
        """Se encarga de graficar el diagrama de voronoi Dos-dimensional con
        numeracion de vertices voronoi"""
        voronoi_plot_2d(self.Vor, line_colors="gray")
        plt.plot(self.Borders["x"], self.Borders["y"], color="gray")
        plt.scatter(x="x", y="y", data=self.Airports, color="black", s=10)
        # label the points
        for j, p in enumerate(self.Vor.vertices):
            plt.text(p[0] - 0.03, p[1] + 0.03, j, ha="right")
        plt.xlabel("Longitude (degrees)")
        plt.ylabel("Latitude (degrees)")
        plt.ylim([-14, 20])
        plt.xlim([-86, -64])

    def area_polygon(self, points):
        """Calcula area de points"""
        # Only operates correctly if points are in order clockwise
        points = np.array(points)
        x = np.array(points[:, 0])
        y = np.array(points[:, 1])
        val = np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))
        return 0.5 * np.abs(val)

    def areas_airports(self):
        """Calcula El area maxima y el area minima de los aeropuertos"""
        Area_max = 0
        Area_min = 5
        indice_max = 0
        indice_min = 0
        Puntos_AM = []
        Puntos_AMI = []
        # Itera sobre las regiones
        for index, region in enumerate(self.Vor.regions):
            if region:
                # print(region)
                # Si la region es acotada
                if -1 not in region:
                    # Ifs : eleccion de area mayor y menor
                    area = self.area_polygon(self.Vor.vertices[region])
                    if area > Area_max:
                        Area_max = area
                        Puntos_AM = self.Vor.vertices[region]
                        region_max = region
                        indice_max = np.where(self.Vor.point_region == index)
                        indice_max = indice_max[0][0]
                    elif area < Area_min:
                        Area_min = area
                        Puntos_AMI = self.Vor.vertices[region]
                        region_min = region
                        indice_min = np.where(self.Vor.point_region == index)
                        indice_min = indice_min[0][0]
        print(
            "El Area Maxima es",
            Area_max,
            "del areopuerto ",
            self.name_airports[indice_max],
        )
        print(
            "El Area Minima es",
            Area_min,
            "del areopuerto ",
            self.name_airports[indice_min],
        )
        # Revisar si no funciona PEP8
        return np.array(Puntos_AM), np.array(Puntos_AMI)

    def Neigh_airports(self):
        """Encontrar el Aeropuerto que tiene mas vecinos"""
        Neigh_max = 0
        Neigh_min = 5
        indice_max = 0
        indice_min = 0
        Puntos_AM = []
        Puntos_AMI = []
        for index, region in enumerate(self.Vor.regions):
            if region:
                # print(region)
                vecinos = len(region)
                if vecinos > Neigh_max:
                    Neigh_max = vecinos
                    Puntos_AM = self.Vor.vertices[region]
                    vertice_max = np.where(self.Vor.point_region == index)[0]
                    vertice_max = vertice_max[0]
                elif vecinos < Neigh_min:
                    Neigh_min = vecinos
                    Puntos_AMI = self.Vor.vertices[region]
                    vertice_min = np.where(self.Vor.point_region == index)[0]
                    vertice_min = vertice_min[0]
        print(
            "El Punto de mayor vecinos es",
            self.Puntos[vertice_max],
            "es el areopuerto ",
            self.name_airports[vertice_max],
            "con ",
            Neigh_max,
            " vecinos",
        )
        print(
            "El Punto de menor vecinos es",
            self.Puntos[vertice_min],
            "es el areopuerto ",
            self.name_airports[vertice_min],
            "con ",
            Neigh_min,
            " vecinos",
        )
        return self.Puntos[vertice_max], self.Puntos[vertice_min]

    def Graph_vertices(self):
        """Construye grafo de puntos y sus puntos vecinos
        (No son vertices de voronoi)"""
        tri = Delaunay(self.Puntos)  # Utilizamos la triangulacion delunay
        neiList = defaultdict(set)  # Crea diccionario
        for p in tri.vertices:
            # Itera sobre cada vecino
            for i, j in itertools.combinations(p, 2):
                neiList[i].add(j)
                neiList[j].add(i)
        return neiList

    def plot_vertices_numbers(self):
        """Grafica la numeración de vertices"""
        neiList = self.Graph_vertices_t

        # Imprime vertice:vecinos
        # for key in sorted(neiList.keys()):
        #    print("%d:%s" % (key, ",".join([str(i) for i in neiList[key]])))

        vor = self.Vor
        voronoi_plot_2d(vor)
        for i, p in enumerate(vor.points):
            plt.text(p[0], p[1], "#%d" % i, ha="center")
        plt.plot(self.Borders["x"], self.Borders["y"], color="gray")
        # plt.show()

    def shortest_neigh_distance(self, point):
        """Point : Indice del punto
        Return : min (punto),indice_min (indice punto min)
        """
        min = 100
        neighs = self.Graph_vertices_t[point]
        for i in neighs:
            vecino = self.Puntos[i]
            dist = distance.euclidean(vecino, point)
            if dist < min:
                min = distance
                indice_min = i
        return min, indice_min

    def shortest_path(self, departure, destination):
        """Halla minimo camino de puntos de voronoi
        departure: punto (x,y)
        destinacion: punto (x,y)
        Return : lista_camino (puntos indices),
                 puntos_camino (Puntos (x,y))
        """
        # Puntos : Index Point
        # print("Departure", departure)
        # print("Destination", destination)
        punto_in = np.where(self.Puntos == departure)[0][0]
        punto_fin = np.where(self.Puntos == destination)[0][0]
        # print("Punto in", punto_in)
        # print("Punto fin", punto_fin)
        lista_camino = [punto_in]

        # Seleccionar vecino menor distancia con punto final iterativamente
        while punto_in != punto_fin:
            vecinos = self.Graph_vertices_t[punto_in]
            min = 1000
            vec_index_min = -1
            # Revisa menor distancia vecino con punto final
            for vec in vecinos:
                punto = self.Puntos[vec]
                dist1 = distance.euclidean(self.Puntos[punto_in], punto)
                dist2 = distance.euclidean(punto, destination)
                dist = dist1 + dist2
                if dist < min:
                    min = dist
                    vec_index_min = vec
            punto_in = vec_index_min
            lista_camino.append(punto_in)

        # Se añade punto final
        lista_camino.append(punto_fin)
        puntos_camino = self.Puntos[lista_camino]
        return lista_camino, puntos_camino

    def select_min_vor_vertices(self, point, puntos_region):
        """selecciona minimo distancia entre punto y puntos_region
        point: punto (x,y)
        puntos_region: lista de puntos (x,y)
        """
        min = 1000
        punto_min = -1
        for i in puntos_region:
            # Iterando sobre vertices de la region y comparandolo con el
            # punto de localizacion
            dist = distance.euclidean(point, i)
            # Escogiendo el minimo
            if dist < min:
                min = dist
                punto_min = i
        return punto_min

    def Graph_vor_vertices(self):
        """Crea grafo de vertices de Voronoi
        return: Diccionario
        """
        # Creando Grafo de Vertices de Voronoi
        List_vor = defaultdict(set)  # Diccionario
        for a, b in self.Vor.ridge_vertices:
            if a != -1 and b != 1:
                List_vor[a].add(b)
                List_vor[b].add(a)

        # print("Voronoi vertices graph", sorted(List_vor.items()))
        return List_vor

    def closest_point_line_f(
                            self, point, punto_min, punto_min_index,
                            lista_camino):
        """Halla la linea mas cercana del poligono frente al punto
        point: punto (x,y)
        punto_min : punto(x,y)
        punto_min_index : indice punto
        lista_camino: vecinos de punto_min
        return : punto_min, p_min (punto (x,y))
        """
        vecinos = self.Graph_vertices_vor[punto_min_index]
        p3 = point
        p1 = punto_min
        min = 1000
        p_min = [-1, -1]

        for vec in vecinos:
            # No queremos que vuelva a escoger un punto que ya recorrio

            if vec not in lista_camino:
                p2 = self.Vor.vertices[vec]
                d = np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1)
                d = np.linalg.norm(d)

                if d < min:
                    min = d
                    p_min = p2

        return np.array([punto_min, p_min])

    def closest_point_line(self, point, punto_min, punto_min_index):
        """Halla la linea mas cercana del poligono al punto
        point: punto (x,y)
        punto_min : punto(x,y)
        punto_min_index : indice punto
        lista_camino: vecinos de punto_min
        return : punto_min, p_min (punto (x,y))
        """
        vecinos = self.Graph_vertices_vor[punto_min_index]
        p3 = point
        p1 = punto_min
        min = 1000
        p_min = [-1, -1]
        for vec in vecinos:
            p2 = self.Vor.vertices[vec]
            d = np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1)
            d = np.linalg.norm(d)
            if d < min:
                min = d
                p_min = p2
        return np.array([punto_min, p_min])

    def find_point_closest_line(self, point, puntos):
        """Halla de la linea el punto mas cercano a point
        point: punto (x,y)
        puntos : np.array de puntos
        return : punto_min (punto (x,y))
        """
        x = puntos[:, 0]
        y = puntos[:, 1]

        # Hallamos la funcion de la linea que une los dos puntos
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)

        # Partimos la linea en 10 espacios iguales
        x_axis = np.linspace(puntos[0][0], puntos[1][0], 10)
        y_axis = polynomial(x_axis)
        puntos_linea = np.array(list(zip(x_axis, y_axis)))
        distancia_minima = 1000
        punto_min = [-1, -1]

        # Elige el punto de menor distancia
        for pi in puntos_linea:
            d = distance.euclidean(point, pi)
            if d < distancia_minima:
                distancia_minima = d
                punto_min[0] = pi[0]
                punto_min[1] = pi[1]
        return punto_min

    def shortest_treahd_path(self, departure, destination):
        """Halla minimo camino de puntos de voronoi
        departure: punto (x,y)
        destinacion: punto (x,y)
        Return : lista_camino (puntos indices),
                 puntos_camino (Puntos (x,y))
        """
        punto_in = np.where(self.Puntos == departure)[0][0]
        # print(punto_in)
        punto_fin = np.where(self.Puntos == destination)[0][0]

        region = self.Vor.point_region[punto_in]
        puntos_region_in = self.Vor.regions[region]
        puntos_region_in = self.Vor.vertices[puntos_region_in]
        punto_min = self.select_min_vor_vertices(
            departure, puntos_region_in
        )  # Punto coordenadas
        punto_min_index = np.where(self.Vor.vertices == punto_min)[0][0]
        # print("punto_min_index", punto_min_index)

        closest_point_in = self.closest_point_line(
            departure, punto_min, punto_min_index
        )
        # Asumo la distancia mas corta se encuentra en el vertice mas cercano
        closest_point_in = self.find_point_closest_line(
            departure, closest_point_in
        )  # Se espera la linea mas corta este en el vertice mas cercano
        # print("closest in", closest_point_in)
        # print("Punto fin", punto_fin)
        region = self.Vor.point_region[punto_fin]
        puntos_region_fin = self.Vor.regions[region]
        # puntos_region_fin = self.Vor.vertices[puntos_region_fin]
        # Util para sabe cuando ya llego a un punto de la region
        # print("Puntos_region_fin", puntos_region_fin)
        lista_camino = []
        count = 0
        while punto_min_index not in puntos_region_fin:
            vecinos = self.Graph_vertices_vor[punto_min_index]
            # print("punto_min_index",punto_min_index, "vecinos",vecinos)
            min = 1000
            vec_index_min = -1
            for vec in vecinos:
                punto = self.Vor.vertices[vec]
                dist1 = distance.euclidean(self.Vor.vertices[punto_min_index],
                                           punto)
                dist2 = distance.euclidean(punto, destination)
                dist = dist1 + dist2
                if dist < min and vec not in lista_camino:
                    min = dist
                    vec_index_min = vec
            punto_min_index = vec_index_min
            lista_camino.append(punto_min_index)
        puntos_camino = self.Vor.vertices[lista_camino]
        puntos_camino = np.insert(puntos_camino, 0, closest_point_in, axis=0)
        puntos_camino = np.insert(puntos_camino, 0, departure, axis=0)

        closest_point_fin = self.closest_point_line_f(
            destination, puntos_camino[-1], lista_camino[-1], lista_camino
        )
        closest_point_fin = np.array(closest_point_fin)
        closest_point_fin = self.find_point_closest_line(
            destination, np.array(closest_point_fin)
        )
        # print("closes fin", closest_point_fin)
        puntos_camino = np.append(puntos_camino, [closest_point_fin], axis=0)
        puntos_camino = np.append(puntos_camino, [destination], axis=0)
        return lista_camino, puntos_camino
