"""
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
from DISClib.DataStructures import mapentry as me
import time

sys.setrecursionlimit(10000)

def printR1Results(list):
    i = 1
    while i <=5:
        m = lt.getElement(list, i)
        print("Nombre: ", m["Name"], " | Ciudad :", m["City"], " | País: ", m["Country"], " | IATA: ",
        m["IATA"], " | connections: ", m["connections"], " | inbound: ", m["inbound"], " | outbound :", 
        m["outbound"])
        i+=1

def printR5Results(list):
    i = 1
    while i <=3:
        m = lt.getElement(list, i)
        m = mp.get(analyzer["IATAs"], m)
        m = me.getValue(m)
        print("IATA: ", m["IATA"], " | Name: ", m["Name"], " | Ciudad: ", m["City"], " | País: ", m["Country"])
        i+=1
    print("- \n"*3)
    n = 2
    while n>=0:
        m = lt.getElement(list, lt.size(list)-n)
        m = mp.get(analyzer["IATAs"], m)
        m = me.getValue(m)
        print("IATA: ", m["IATA"], " | Name: ", m["Name"], " | Ciudad: ", m["City"], " | País: ", m["Country"])
        n-=1

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
        start_time = time.process_time()
        con = controller.getInter(analyzer)
        print("Número de aeropuertos interconectados: ", con[1])
        printR1Results(con[0])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    elif int(inputs[0]) == 3:
        start_time = time.process_time()
        ap1 = input("Ingrese el IATA del aeropuerto 1: ")
        ap2 = input("Ingrese el IATA del aeropuerto 2: ")
        r = controller.clusters(analyzer, ap1, ap2)
        print(r[0])
        print("Número de elementos conectados: ", r[1])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    elif int(inputs[0]) == 4:
        """
        Aviso: Se está usando la columna city, no city_ascii, por si es relevante para las pruebas
        """
        start_time = time.process_time()
        city0 = input("Ingrese la primera ciudad: \n")
        cityF = input("Ingrese la segunda ciudad: \n")
        controller.shortcut(analyzer, city0, cityF)

        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    elif int(inputs[0]) == 5:
        start_time = time.process_time()

        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    elif int(inputs[0]) == 6:
        start_time = time.process_time()
        ap = input("Ingrese al IATA del aeropuerto a dejar de funcionar: ")
        r = controller.getAfected(analyzer, ap)
        print("Numero de aeropuertos afectados: ", lt.size(r))
        printR5Results(r)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    else:
        sys.exit(0)
sys.exit(0)
