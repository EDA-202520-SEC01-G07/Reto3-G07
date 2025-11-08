import time
import csv
csv.field_size_limit(2147483647)
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Map import map_entry as me
from DataStructures.Tree import binary_search_tree as bst
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Priority_queue import priority_queue as pq
import math as math
import datetime as datetime

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        "viajes": None,            # Mapa: todos los vuelos ordenados por fecha
        "aereolinea": None,        # Mapa: aerolínea → RBT de vuelos
        "destino": None,           # Mapa: aeropuerto destino → RBT de vuelos
    }
    catalog["viajes"] = rbt.new_map()
    catalog["aereolinea"] = rbt.new_map()
    catalog["destino"] = rbt.new_map()
    return catalog

# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    start = get_time()
    
    vuelos = filename
    input_file = csv.DictReader(open(vuelos, encoding='utf-8'))
    
    # Por cada fila (vuelo) del CSV
    for viaje in input_file:
        # Creamos un diccionario con la info del vuelo
        vuelo = {
            "id": int(viaje["id"]),
            "date": viaje["date"],
            "dep_time": viaje["dep_time"],
            "sched_dep_time": viaje["sched_dep_time"],
            "arr_time": viaje["arr_time"],
            "sched_arr_time": viaje["sched_arr_time"],
            "carrier": viaje["carrier"],
            "flight": int(viaje["flight"]),
            "tailnum": viaje["tailnum"],
            "origin": viaje["origin"],
            "dest": viaje["dest"],
            "air_time": int(viaje["air_time"]),
            "distance": int(viaje["distance"]),
            "name": viaje["name"]
        }

        # Insertamos en el árbol rojo-negro usando el la fecha y hora de salida como llave
        rbt.put(catalog["viajes"])# key=(vuelo["date"]), value=vuelo)
        carrier= viaje["carrier"]
        if carrier not in catalog["aereolinea"]:
            #hacerle hash al carrier?? e ingresarlo al rbt de aereolinea
            pass
        dest = viaje["dest"]
        if dest not in catalog["destino"]:
            #hacerle hash al destino?? e ingresarlo al rbt de aereolinea
            pass
        
    end = get_time()
    tiempo = delta_time(start, end)
    
    return tiempo

# Funciones de consulta sobre el catálogo


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog, codigo_vuelo, codigo_destino, rango_distancia):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start= get_time()
    filtrado=0
    
    end= get_time()
    tiempo= delta_time(start,end)
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
