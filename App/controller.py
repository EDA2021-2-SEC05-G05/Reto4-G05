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
 """

import config as cf
import model
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    ufosfile = cf.data_dir + "Skylines/airports-utf8-large.csv"
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    x = 100
    y = 100
    lastAP = ""
    firstAP = ""
    apC = 0
    for airport in input_file:
        model.addAP(analyzer, airport)
        apC+=1
        if int(airport["id"]) < x:
            x = int(airport["id"])
            firstAP = airport
        if int(airport["id"]) > y:
            y = int(airport["id"])
            lastAP = airport
    lastAP = APFix(lastAP)
    firstAP = APFix(firstAP)

    ufosfile = cf.data_dir + "Skylines/routes-utf8-large.csv"
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    RoutesC = 0
    h = 0
    for route in input_file:
        r = model.addRoute(analyzer, route)
        h = model.addG(analyzer, route, r[0], r[1], h)
        RoutesC+=1
    
    ufosfile = cf.data_dir + "Skylines/worldcities-utf8.csv"
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    firstcity = next(input_file)
    model.addCity(analyzer, firstcity)
    firstcity = CityFix(firstcity)           
    n = 1
    for city in input_file:
        model.addCity(analyzer, city)
        k = city
        n+=1
    lastcity = CityFix(k)
    #model.addIV(analyzer)
    model.Components(analyzer)
    return analyzer, firstAP, lastcity, n, apC, lastAP, RoutesC, firstcity, h

def APFix(ap):
    return ("Nombre: "+ str(ap["Name"]) + " | Ciudad: "+ str(ap["City"]) + " | País: "+ 
            str(ap["Country"]) + " | Latitud: "+ str(ap["Latitude"]) + " | Longitud: "+ str(ap["Longitude"]))
def CityFix(city):
    return ("Ciudad: "+ str(city["city"])+ " | Población: "+ str(city["population"]) +" | Latitud: "+
    str(city["lat"]) + " | Longitud: "+ str(city["lng"]))
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getInter(analyzer):
    return model.Inter(analyzer)

def getCity(analyzer, city):
    model.getCity(analyzer, city)

def getAfected(analyzer, ap):
    return model.Afected(analyzer, ap)

def clusters(analyzer, ap1, ap2):
    return model.clusters(analyzer, ap1, ap2)

