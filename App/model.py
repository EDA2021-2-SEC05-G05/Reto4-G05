"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import bfs as bfs
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mr
from DISClib.ADT import orderedmap as om
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    analyzer = {'routes': None,
                "cities":None,
                "airports": None

                }
    analyzer["IATAs"] = mp.newMap(10000, 
                                    maptype="CHAINING", 
                                    loadfactor=4.0)
    analyzer["airports"] = mp.newMap(10000, 
                                    maptype="CHAINING", 
                                    loadfactor=4.0) 
    analyzer["cities"] = mp.newMap(41010, 
                                    maptype="CHAINING", 
                                    loadfactor=4.0)  
    analyzer["routes"] = gr.newGraph(datastructure="ADJ_LIST", 
                                    directed=True, 
                                    size=92607)                               
    analyzer["airportsIV"] = gr.newGraph(datastructure="ADJ_LIST", 
                                        size=92607)
                                    
    return analyzer                              

# Funciones para agregar informacion al catalogo

def addAP(analyzer, airport):
    mp.put(analyzer["IATAs"], airport["IATA"], airport)
    #mp.put(analyzer["airports"], airport["Name"], airport)

def addRoute(analyzer, route):
    a = mp.get(analyzer["IATAs"], route["Departure"])
    aa = me.getKey(a)
    if not gr.containsVertex(analyzer["IATAs"], aa):
        gr.insertVertex(analyzer["routes"], aa)
    b = mp.get(analyzer["IATAs"], route["Destination"])
    b = me.getKey(b)
    if not gr.containsVertex(analyzer["IATAs"], b):
        gr.insertVertex(analyzer["routes"], b)
    gr.addEdge(analyzer["routes"], aa, b, float(route["distance_km"]))

def addCity(analyzer, city):
    ciudades = analyzer["cities"]
    if mp.contains(ciudades, city["city"]):
        k = mp.get(ciudades, city["city"])
        v = me.getValue(k)
        lt.addLast(v, city)
    else:
        l = lt.newList()
        lt.addLast(l, city)
        mp.put(ciudades, city["city"], l)


def addIV(analyzer):
    vers = analyzer["routes"]
    vers = gr.vertices(vers)
    for ver in lt.iterator(vers):
        if not gr.containsVertex(analyzer["airportsIV"], ver):
            gr.insertVertex(analyzer["airportsIV"], ver)
        g = gr.adjacentEdges(analyzer["routes"], ver)
        for y in lt.iterator(g):
            vy = y["vertexB"]
            if not gr.containsVertex(analyzer["airportsIV"], vy):
                gr.insertVertex(analyzer["airportsIV"], vy)
            if gr.getEdge(analyzer["airportsIV"], ver, vy) == None and gr.getEdge(analyzer["airportsIV"], vy, ver) == None:
                gr.addEdge(analyzer["airportsIV"], ver, vy, y["weight"])
    return analyzer


# Funciones para creacion de datos

# Funciones de consulta

def getCity(analyzer, city):
    a = mp.get(analyzer["cities"], city)
    a = me.getValue(a)
    if lt.size(a) > 1:
        print("Se han encontrado varias ciudades bajo el mismo nombre\n")
        i = 1
        ciduadesr = lt.newList()
        for city in lt.iterator(a):
            lt.addLast(ciduadesr, city)
            print("Presione ", i, " para selecionar a ", city["city"], ", ", city["admin_name"], "-"
            , city["country"], " | Lat: ", city["lat"], " Long: ", city["lng"])
            i+=1
        num = input("Ingrese el número de la ciudad que desea: ")
        print("Usted ha elegido: ", lt.getElement(ciduadesr, int(num)))
    else:
        print("Usted ha elegido: ", lt.getElement(a, 1))

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
