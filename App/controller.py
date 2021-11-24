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
    ufosfile = cf.data_dir + "Skylines/airports_full.csv"
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    a = next(input_file)
    firstAP = ("Nombre: "+ str(a["Name"]) + " | Ciudad: "+ str(a["City"]) + " | País: "+ 
    str(a["Country"]) + " | Latitud: "+ str(a["Latitude"]) + " | Longitud: "+ str(a["Longitude"]))
    ufosfile = cf.data_dir + "Skylines/airports_full.csv"
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")          
    for airport in input_file:
        model.addAP(analyzer, airport)
    #model.ReqExtra(analyzer)
    ufosfile = cf.data_dir + "Skylines/routes_full.csv"
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    for route in input_file:
        model.addRoute(analyzer, route)
    ufosfile = cf.data_dir + "Skylines/worldcities.csv"
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    n = 0
    for city in input_file:
        model.addCity(analyzer, city)
        k = city
        n+=1
    lastcity = ("Ciudad: "+ str(k["city"])+ " | Población: "+ str(k["population"]) +" | Latitud: "+
    str(k["lat"]) + " | Longitud: "+ str(k["lng"]))
    model.addIV(analyzer)
    return analyzer, firstAP, lastcity, n

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
