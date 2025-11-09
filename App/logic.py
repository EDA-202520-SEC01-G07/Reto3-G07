import time
import csv
csv.field_size_limit(2147483647)
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sl
from DataStructures.Map import map_separate_chaining as mp
from DataStructures.Map import map_entry as me
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Priority_queue import priority_queue as pq
import math as math
import datetime as dt

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        "fecha_hora_destino": None,
        "viajes": None,            # Árbol: todos los vuelos ordenados por fecha → RBT
        "aerolinea": None,        # Mapa: llave: aerolínea, valor: Mapa: Llave: Aerop Destino, Valor: Lista viajes → Sep Chaining
        "destino": None,           # Mapa: aeropuerto destino → Sep Chaining
        "hora_salida_prg": None    # Árbol: sch_dep_time → RBT
    }
    catalog["fecha_hora_destino"] = rbt.new_map()
    catalog["viajes"] = rbt.new_map()
    catalog["aerolinea"] = mp.new_map(20, 4)
    catalog["destino"] = mp.new_map(120, 4)
    catalog["hora_salida_prg"] = rbt.new_map()
    return catalog

# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    start = get_time()
    trayectos = 0
    vuelos = filename
    input_file = csv.DictReader(open(vuelos, encoding='utf-8'))
    #El DictReader me da un diccionario por defecto de cada línea, donde sus llaves son las columnas
    
    # Por cada fila (vuelo) del CSV
    for viaje in input_file:
        viaje["id"]= int(viaje["id"])
        viaje["flight"]= int(float(viaje["flight"]))
        viaje["air_time"]= int(float(viaje["air_time"]))
        viaje["distance"]= int(float(viaje["distance"]))
        
        trayectos += 1
        # Insertamos el viaje en el árbol rojo-negro fecha_hora_destino usando combinando fecha y hora programada de salida como llave
        llave = dt.datetime.strptime(viaje["date"]+" "+viaje["sched_dep_time"], "%Y-%m-%d %H:%M")
        nodo = rbt.get(catalog["fecha_hora_destino"], llave)
        if nodo is None:
            lista = sl.new_list()
            sl.add_last(lista, viaje)
            rbt.put(catalog["fecha_hora_destino"], llave, lista)
        else:
            sl.add_last(nodo, viaje)
            
        # Insertamos el viaje en el árbol rojo-negro viajes usando la fecha como llave
        nodo = rbt.get(catalog["viajes"], dt.datetime.strptime(viaje["date"], "%Y-%m-%d"))
        if nodo is None:
            lista = sl.new_list()
            sl.add_last(lista, viaje)
            rbt.put(catalog["viajes"], dt.datetime.strptime(viaje["date"], "%Y-%m-%d"), lista)
        else:
            sl.add_last(nodo, viaje)
        
        # Insertamos el viaje en el mapa aerolinea usando la aerolínea como llave
        carrier = viaje["carrier"]
        mapa = mp.get(catalog["aerolinea"], carrier) #Obtiene el mapa de los aeropuertos de destino en esa aerolinea
        if mapa is None:
            n_mapa = mp.new_map(55000,4)
            mp.put(catalog["aerolinea"], carrier, n_mapa)
        mapa = mp.get(catalog["aerolinea"], carrier)
        lista = mp.get(mapa, viaje["dest"]) #Obtiene la lista del aeropuerto
        if lista is None:
            n_mapa = mp.new_map(16000, 4)
            l = sl.new_list()
            sl.add_last(l, viaje)
            mp.put(mapa, viaje["dest"], l)
        else:
            sl.add_last(lista, viaje)
        
        # Insertamos el viaje en el mapa destino usando el aeropuerto como llave
        lista = mp.get(catalog["destino"], viaje["dest"]) 
        if lista is None:
            lista = sl.new_list()
            mp.put(catalog["destino"], viaje["dest"], lista)
        sl.add_last(lista, viaje)
        
        # Insertamos el viaje en el árbol rojo negro hora_salida_prg
        hora = rbt.get(catalog["hora_salida_prg"], dt.datetime.strptime(viaje["sched_dep_time"], "%H:%M"))
        if hora is None:
            l = sl.new_list()
            sl.add_last(l, viaje)
            rbt.put(catalog["hora_salida_prg"], dt.datetime.strptime(viaje["sched_dep_time"], "%H:%M"), l)
        else:
            sl.add_last(hora, viaje)
        
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo, trayectos

def info_carga_datos(catalog):
    lista = rbt.value_set(catalog["fecha_hora_destino"]) #Recorre el mapa inorder y devuelve un singlelinked
    primeros = []
    ultimos = []
    i = 0
    suma = 0
    while i < sl.size(lista) and suma <= 5:
        l = sl.get_element(lista, i)
        for j in range(sl.size(l)):
            elem = sl.get_element(l, j)
            viaje={
                "Fecha": elem["date"],
                "H salida": elem["dep_time"],
                "H llegada":elem["arr_time"],
                "Aerolínea": elem["carrier"]+"_"+elem["name"],
                "Aeronave": elem["tailnum"],
                "Origen": elem["origin"],
                "Destino": elem["dest"],
                "Duración":elem["air_time"], 
                "Distancia": elem["distance"]
            }
            primeros.append(viaje)
            suma+= 1
            if suma == 5:
                break
        if suma == 5:
            break
        i+= 1
    i = sl.size(lista)-5
    suma = 0
    while i < sl.size(lista) and suma <= 5:
        l = sl.get_element(lista, i)
        for j in range(sl.size(l)):
            elem = sl.get_element(l, j)
            viaje={
                "Fecha": elem["date"],
                "H salida": elem["dep_time"],
                "H llegada":elem["arr_time"],
                "Aerolínea": elem["carrier"]+"_"+elem["name"],
                "Aeronave": elem["tailnum"],
                "Origen": elem["origin"],
                "Destino": elem["dest"],
                "Duración":elem["air_time"], 
                "Distancia": elem["distance"]
            }
            ultimos.append(viaje)
            suma+= 1
            if suma == 5:
                break
        if suma == 5:
            break
        i+= 1
    return primeros, ultimos
    
    
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
