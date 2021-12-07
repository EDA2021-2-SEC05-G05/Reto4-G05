﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Puntos de interconexión aérea")
    print("3- Clústeres de tráfico aéreo")
    print("4- Ruta más corta entre ciudades")
    print("5- Millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        analyzer = controller.init()
        r = controller.loadData(analyzer)
        print("Cargando información de los archivos ....")
        print("Total de aeropuertos en el dígrafo: ", r[4])
        print("Total de rutas aéreos en el dígrafo: ", r[6])
        print("Primer aeropuerto cargado en el dígrafo: ", r[1])
        print("Último aeropuerto cargado en el dígrafo: ", r[5], "\n")
        print("Total de aeropuertos en el grafo no dirigido: ", r[4])
        print("Total de rutas aéreos en el grafo no dirigido: ", r[8])
        print("Primer aeropuerto cargado en el grafo no dirigido: ", r[1])
        print("Último aeropuerto cargado en el grafo no dirigido: ", r[5], "\n")
        print("Total de ciudades: ", r[3])
        print("Primera ciudad cargada: ", r[7])
        print("Última ciudad cargada: ", r[2])
    elif int(inputs[0]) == 2:
        pass
    elif int(inputs[0]) == 3:
        pass
    elif int(inputs[0]) == 4:
        """
        Aviso: Se está usando la columna city, no city_ascii, por si es relevante para las pruebas
        """
        city0 = input("Ingrese la primera ciudad: \n")
        controller.getCity(analyzer, city0)
        cityF = input("Ingrese la segunda ciudad: \n")
        controller.getCity(analyzer, cityF)
    elif int(inputs[0]) == 5:
        pass
    elif int(inputs[0]) == 6:
        pass
    else:
        sys.exit(0)
sys.exit(0)
