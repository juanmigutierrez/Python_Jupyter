from FlightOperations import FlightOperations
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

if __name__ == "__main__":
    names1 = ["y", "x"]
    borders = "borders_CO.dat"
    Borders = pd.read_csv(borders, sep=r"\s\s", header=None, names=names1,
                          engine='python')
    Airports = pd.read_csv("airports_CO.dat", sep=r"\s\s\s", header=None,
                           engine='python')
    Airports = Airports.drop(columns=[3])
    Airports.columns = ["y", "x", "elevation", "ciudad",
                        "departamento", "aeropuerto"]

    # Punto 1 - Plot
    Map = FlightOperations(Borders, Airports)
    Map.plot_2d()
    plt.show()

    # Punto 2 - Airpot Coverage Area
    print("----------------- Punto 2 --------------")
    Puntos_AM, Puntos_AMI = Map.areas_airports()
    # Punto 3 - Most and LEast crowded airports
    print("----------------- Punto 3 --------------")
    Punto1, Punto2 = Map.Neigh_airports()

    # Punto 4 - Airpot-based fligh path
    print("----------------- Punto 4 --------------")
    camino, puntos = Map.shortest_path(Map.Puntos[68], Map.Puntos[42])
    print("El camino de localizaciones de areopuertos en orden es \n ", puntos)

    # Punto 5 - Threat-based flight path
    camino, puntos2 = Map.shortest_treahd_path(Map.Puntos[52], Map.Puntos[35])
    print("El camino de localizaciones de amenaza en orden es \n ", puntos2)

    # Grafica Caminos
    Map.plot_2d_black()
    plt.plot(puntos[:, 0], puntos[:, 1], color="red", label="Aiport-based")
    plt.plot(puntos2[:, 0], puntos2[:, 1], color="blue", label="Aiport-based")
    plt.legend()
    plt.show()

    # Funciones extras que hice por que me fueron utiles
    # Map.plot_vertices_numbers()
