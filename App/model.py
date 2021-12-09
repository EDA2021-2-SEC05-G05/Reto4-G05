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


from ctypes import LittleEndianStructure
import config as cf
from math import radians, cos, sin, asin, sqrt
import math as df
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import bfs as bfs
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import dijsktra as alg


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
    analyzer["byCity"] = mp.newMap(10000, 
                                    maptype="CHAINING", 
                                    loadfactor=4.0)    
    analyzer["routes"] = gr.newGraph(datastructure="ADJ_LIST", 
                                    directed=True, 
                                    size=92607)                               
    analyzer["airportsIV"] = gr.newGraph(datastructure="ADJ_LIST", 
                                        size=92607)
    analyzer["markedroutes"] = mp.newMap(100000, 
                                    maptype="CHAINING", 
                                    loadfactor=4.0) 
                                    
    return analyzer                              

# Funciones para agregar informacion al catalogo

def addAP(analyzer, airport):
    mp.put(analyzer["IATAs"], airport["IATA"], airport)
    if mp.contains(analyzer["byCity"], airport["City"]):
        v = mp.get(analyzer["byCity"], airport["City"])
        v = me.getValue(v)
        lt.addLast(v, airport)
    else:
        lst = lt.newList()
        lt.addLast(lst, airport)
        mp.put(analyzer["byCity"], airport["City"], lst)

def addRoute(analyzer, route):
    a = mp.get(analyzer["IATAs"], route["Departure"])
    aa = me.getKey(a)
    if not gr.containsVertex(analyzer["routes"], aa):
        gr.insertVertex(analyzer["routes"], aa)
        gr.insertVertex(analyzer["airportsIV"], aa)
    b = mp.get(analyzer["IATAs"], route["Destination"])
    b = me.getKey(b)
    if not gr.containsVertex(analyzer["routes"], b):
        gr.insertVertex(analyzer["routes"], b)
        gr.insertVertex(analyzer["airportsIV"], b)
    #if gr.getEdge(analyzer["routes"], aa, b) == None:
    gr.addEdge(analyzer["routes"], aa, b, float(route["distance_km"]))
    return aa, b

def addG(analyzer, route, dep, des, k):
    m = analyzer["markedroutes"]
    mp.put(m, (route["Departure"], "-", route["Destination"]), route)
    if mp.contains(m, (route["Destination"], "-", route["Departure"])):
        k+=1
        if gr.getEdge(analyzer["airportsIV"], dep, des) == None:
            gr.addEdge(analyzer["airportsIV"], dep, des, float(route["distance_km"]))
    return k

def addCity(analyzer, city):
    city = addAPtoCity(analyzer, city)
    ciudades = analyzer["cities"]
    if mp.contains(ciudades, city["city_ascii"]):
        k = mp.get(ciudades, city["city_ascii"])
        v = me.getValue(k)
        lt.addLast(v, city)
    else:
        l = lt.newList()
        lt.addLast(l, city)
        mp.put(ciudades, city["city_ascii"], l)
    

def addAPtoCity(analyzer, city):
    v = mp.get(analyzer["byCity"], city["city_ascii"])
    if v != None:
        v = me.getValue(v)
        ap = lt.getElement(v, 1)
        if lt.size(v) == 1:
            city["airport"] = ap["IATA"]
            city["distairport"] = haversine(float(ap["Longitude"]), 
            float(ap["Latitude"]), float(city["lng"]), float(city["lat"]))
        else:
            dist = haversine(float(ap["Longitude"]), 
            float(ap["Latitude"]), float(city["lng"]), float(city["lat"]))
            i = 2
            while i<=lt.size(v):
                airp = lt.getElement(v, i)
                hav = haversine(float(airp["Longitude"]), 
                float(airp["Latitude"]), float(city["lng"]), float(city["lat"]))
                if hav > dist:
                    dist = hav
                i+=1
    else:
        city["distairport"] = 0
    return city


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return abs(c * r)

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
            if gr.getEdge(analyzer["routes"], ver, vy) != None and gr.getEdge(analyzer["routes"], vy, ver) != None:
                gr.addEdge(analyzer["airportsIV"], ver, vy, y["weight"])
    return analyzer


# Funciones para creacion de datos

def Components(analyzer):
    analyzer["top5"] = lt.newList()
    analyzer["scc"] = scc.KosarajuSCC(analyzer["routes"])

# Funciones de consulta

def Inter(analyzer):
    rts = analyzer["routes"]
    v = gr.vertices(rts)
    n = 0
    for ver in lt.iterator(v):
        inb = gr.indegree(rts, ver)
        out = gr.outdegree(rts, ver)
        if inb>=1 or out>=1:
            n+=1
        conn = int(inb)+int(out)
        ap = mp.get(analyzer["IATAs"], ver)
        ap = me.getValue(ap)
        ap["connections"] = conn
        ap["inbound"] = inb
        ap["outbound"] = out
        top5(analyzer, ap)
    return analyzer["top5"], n
    
def top5 (analyzer, ap):
    if lt.size(analyzer["top5"])<4:
        lt.addLast(analyzer["top5"], ap)
    elif lt.size(analyzer["top5"])==4:
        lt.addLast(analyzer["top5"], ap)
        qs.sort(analyzer["top5"], cmpCIO)
    else:
        checktop5(analyzer["top5"], ap)

def checktop5(list, ap):
    i = 0
    while i <= 5:
        if ap["connections"] > lt.getElement(list, i)["connections"]:
            old = lt.getElement(list, i)
            lt.changeInfo(list, i, ap)
            checktop5(list, old)
            break
        i +=1

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


def Afected(analyzer, ap):
    g = gr.adjacents(analyzer["routes"], ap)
    gg = lt.newList()
    for r in lt.iterator(g):
        if lt.isPresent(gg, r) == 0:
            lt.addLast(gg, r)
    return qs.sort(gg, ggcmp)

def ggcmp (r1, r2):
    return r1<r2

def clusters(analyzer, ap1, ap2):
    ks = analyzer["scc"]
    aps = analyzer["IATAs"]
    if mp.get(ks["idscc"], ap1) == None or mp.get(ks["idscc"], ap2) == None:
        bt = str(me.getValue(mp.get(aps, ap1))["Name"])+ " NO se encuentra en el mismo clúster que "+str(me.getValue(mp.get(aps, ap2))["Name"]) 
    else:
        bt = mp.get(ks["idscc"], ap1)["value"] == mp.get(ks["idscc"], ap2)["value"]
        if bt:
            bt = str(me.getValue(mp.get(aps, ap1))["Name"])+ " NO se encuentra en el mismo clúster que "+str(me.getValue(mp.get(aps, ap2))["Name"])
        else:
            bt = str(me.getValue(mp.get(aps, ap1))["Name"])+ " NO se encuentra en el mismo clúster que "+str(me.getValue(mp.get(aps, ap2))["Name"])
    return bt, scc.connectedComponents(ks)

def distance(lati0,long0,lati1,long1):

    Oppsite  = 20000
    long0, lati0, long1, lati1 = df(df.radians, [long0, lati0, long1, lati1])
    distancelong = long1 - long0
    distancelati = lati1 - lati0
    a = df.sin(distancelati/2)*2 + df.cos(lati0) * df.cos(lati1) * df.sin(distancelong/2)*2
    b = 2 * df.atan2(df.sqrt(a), df.sqrt(1-a))
    c = 6371 * b

    d =df.atan2(df.cos(lati0)*df.sin(lati1)-df.sin(lati0)*df.cos(lati1)*df.cos(long1-long0), df.sin(long1-long0)*df.cos(lati1)) 
    d = df.degrees(d)
    c2 = c * 1000
    distance = c2 + Oppsite * 2 / 2

    roundedDistance = distance/1000
    return roundedDistance

def route(analyzer,tupla):

    MapAirports = analyzer["airportsIV"]
    ini=111111111111111111111110

    for i in lt.iterator(mp.keySet(MapAirports)): 
        value= mp.get(MapAirports,i)["value"]
        route= distance(tupla[0], tupla[1], float(value["Latitude"]), float(value["Longitude"]) )
        
        if route<ini and gr.containsVertex(analyzer["airportsIV"], value["IATAs"]):
            ini=route
            name = value["Name"]
            IATA=value["IATAs"]
        
    finalList=lt.newList("ARRAY_LIST")
    lt.addLast(finalList,name)
    lt.addLast(finalList,IATA)
    return finalList

def shortcut(analyzer, city0,cityF):

    travelmap = analyzer["cities"]

    city0=mp.get(travelmap,city0)["value"]
    cityF=mp.get(travelmap,cityF)['value']

    initialCity = (float(city0["Latitude"]) , float(city0["Longitude"]))
    finalCity=(float(cityF["Latitude"]) , float(cityF["Longitude"]))
    
    first= route(analyzer,initialCity)
    f0=lt.getElement(first,2)
    
    second=route(analyzer,finalCity)
    f1=lt.getElement(second,2)

    dijsktra = alg.Dijkstra(analyzer["airportsIV"], f0)
    
    return  alg.pathTo(dijsktra, f1)


# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def cmpCIO(ap1, ap2):
    return ap1["connections"]>ap2["connections"]
