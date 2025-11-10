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
        if viaje["id"] is None or viaje["id"] is " " or viaje["id"] is "":
            viaje["id"] = "Unknown"
        viaje["id"]= int(viaje["id"])
        
        if viaje["date"] is None or viaje["date"] is " " or viaje["date"] is "":
            viaje["date"] = "Unknown"
        viaje["date"] = viaje["date"].strip()
        
        if viaje["dep_time"] is None or viaje["dep_time"] is " " or viaje["dep_time"] is "":
            viaje["dep_time"] = "Unknown"
        viaje["dep_time"] = viaje["dep_time"].strip()
        
        if viaje["sched_dep_time"] is None or viaje["sched_dep_time"] is " " or viaje["sched_dep_time"] is "":
            viaje["sched_dep_time"] = "Unknown"
        viaje["sched_dep_time"] = viaje["sched_dep_time"].strip()
        
        if viaje["arr_time"] is None or viaje["arr_time"] is " " or viaje["arr_time"] is "":
            viaje["arr_time"] = "Unknown"
        viaje["arr_time"] = viaje["arr_time"].strip()
        
        if viaje["sched_arr_time"] is None or viaje["sched_arr_time"] is " " or viaje["sched_arr_time"] is "":
            viaje["sched_arr_time"] = "Unknown"
        viaje["sched_arr_time"] = viaje["sched_arr_time"].strip()
        
        if viaje["carrier"] is None or viaje["carrier"] is " " or viaje["carrier"] is "":
            viaje["carrier"] = "Unknown"
        viaje["carrier"] = viaje["carrier"].strip()
        
        if viaje["flight"] is None or viaje["flight"] is " " or viaje["flight"] is "":
            viaje["flight"] = "Unknown"
        viaje["flight"]= int(float(viaje["flight"]))
        
        if viaje["tailnum"] is None or viaje["tailnum"] is " " or viaje["tailnum"] is "":
            viaje["tailnum"] = "Unknown"
        viaje["tailnum"] = viaje["tailnum"].strip()
        
        if viaje["origin"] is None or viaje["origin"] is " " or viaje["origin"] is "":
            viaje["origin"] = "Unknown"
        viaje["origin"] = viaje["origin"].strip()
        
        if viaje["dest"] is None or viaje["dest"] is " " or viaje["dest"] is "":
            viaje["dest"] = "Unknown"
        viaje["dest"] = viaje["dest"].strip()
        
        if viaje["air_time"] is None or viaje["air_time"] is " " or viaje["air_time"] is "":
            viaje["air_time"] = "Unknown"
        viaje["air_time"]= int(float(viaje["air_time"]))
        
        if viaje["distance"] is None or viaje["distance"] is " " or viaje["distance"] is "":
            viaje["distance"] = "Unknown"
        viaje["distance"]= int(float(viaje["distance"]))
        
        if viaje["name"] is None or viaje["name"] is " " or viaje["name"] is "":
            viaje["name"] = "Unknown"
        viaje["name"] = viaje["name"].strip()
        
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
    while i < sl.size(lista) and suma < 5:
        l = sl.get_element(lista, i)
        for j in range(sl.size(l)):
            elem = sl.get_element(l, j)
            viaje={
                "Fecha": elem["date"],
                "H salida": elem["dep_time"],
                "H llegada":elem["arr_time"],
                "Aerolínea (Cód_Nom)": elem["carrier"]+"_"+elem["name"],
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
        i+= 1
        
    i = sl.size(lista)-1
    suma = 0
    while i >= 0 and suma < 5:
        l = sl.get_element(lista, i)
        j = sl.size(l) - 1
        while j >= 0 and suma < 5:
            elem = sl.get_element(l, j)
            viaje={
                "Fecha": elem["date"],
                "H salida":elem["dep_time"],
                "H llegada":elem["arr_time"],
                "Aerolínea (Cód_Nom)": elem["carrier"]+"_"+elem["name"],
                "Aeronave": elem["tailnum"],
                "Origen": elem["origin"],
                "Destino": elem["dest"],
                "Duración":elem["air_time"], 
                "Distancia": elem["distance"]
            }
            ultimos.insert(0,viaje)
            suma+= 1
            j -= 1
            if suma == 5:
                break
        i-= 1
    return primeros, ultimos
    
    
# Funciones de consulta sobre el catálogo

### FALTA CUMPLIR CONDICIÓN DE La respuesta debe mostrarse ordenada de forma ascendente según el retraso. Si dos vuelos tienen el mismo retraso, deben organizarse de forma cronológica por fecha y hora real de salida.
def req_1(catalog, aerolinea, rango):
    """
    Retorna el resultado del requerimiento 1
    aerolinea = Código de la aerolínea a analizar (por ejemplo: “UA”).
    rango = Rango de minutos de retraso en salida a filtrar (por ejemplo: [10,30]).
    """
    # TODO: Modificar el requerimiento 1
    start = get_time()
    
    rango[0] = int(rango[0])
    rango[1] = int(rango[1])
    trayectos = 0
    viajes_filtrados = rbt.new_map()
    viajes = catalog["aerolinea"] #Mapa
    aero = mp.get(viajes, aerolinea) #Me da un mapa de con llaves de aeropuertos
    codigos = mp.key_set(aero)
    for i in range(sl.size(codigos)):
        lista = mp.get(aero, lt.get_element(codigos, i))
        for j in range(sl.size(lista)):
            elem = sl.get_element(lista, j)
            retraso = diferencia_tiempo(elem["dep_time"], elem["sched_dep_time"])
            if rango[0] <= retraso and rango[1] >= retraso:
                trayectos += 1
                viaje = {"Id": elem["id"],
                         "Fecha": elem["date"],
                         "Nombre Aerolínea + Código": elem["name"] +" - "+ elem["carrier"],
                         "Origen": elem["origin"],
                         "Destino": elem["dest"],
                         "Retraso": retraso                    
                }
                rbt.put(viajes_filtrados, retraso, viaje)
    end = get_time()
    tiempo = delta_time(start, end)
    return tiempo, trayectos, viajes_filtrados

def req_2(catalog,dest,rango_minutos):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start= get_time()
    rango_split = [p.strip() for p in rango_minutos.split(",")]
    rango_min = int(rango_split[0])
    rango_max = int(rango_split[1])
    filtrados=0
    vuelos_filtrados= rbt.new_map()
    vuelos_dest= mp.get(catalog["destino"], dest)
    if vuelos_dest is None:
        end= get_time()
        tiempo= delta_time(start,end)
        return tiempo,0, vuelos_filtrados
    
    vuelos=me.get_value(vuelos_dest)
    for i in range (sl.size(vuelos)):
        viaje= sl.get_element(vuelos, i)
        anticipo=diferencia_tiempo(viaje["arr_time"], viaje["sched_arr_time"])
        if anticipo < 0:
            anticipo = -anticipo    # minutos de anticipo (positivo)
        else:
            continue
        
        if rango_min <= anticipo <= rango_max:
            filtrados+=1
            info={"Id": viaje["id"],
            "Codigo Vuelo": viaje["flight"],
            "Fecha": viaje["date"],
            "Nombre Aerolínea": viaje["name"],
            "Codigo Aerolínea": viaje["carrier"],
            "Origen": viaje["origin"],
            "Destino": viaje["dest"],
            "Anticipo llegada": anticipo}
            mapaf=rbt.get(vuelos_filtrados, anticipo)
            if mapaf is None:
                lista= sl.new_list()
                sl.add_last(lista, info)
                rbt.put (vuelos_filtrados, anticipo, lista)
            else:
                sl.add_last (mapaf, info)
                rbt.put (vuelos_filtrados, anticipo, mapaf)
            
    end= get_time()
    tiempo= delta_time(start,end)
    return tiempo, filtrados, vuelos_filtrados


def req_3(catalog, carrier, dest, rango_dist):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start= get_time()
    filtrado=0
    filtro=lt.new_list()
    if mp.get(catalog["aerolinea"], carrier) is not None:
        mapa= mp.get(catalog["aerolinea"], carrier)
        if mp.get(mapa, dest) is not None:
            lista= mp.get(mapa, dest)
            for i in range (sl.size(lista)):
                viaje= sl.get_element(lista, i)
                if rango_dist[0]<= viaje["distance"] <= rango_dist[1]:
                    lt.add_last(filtro, viaje)
                    filtrado+=1
    end= get_time()
    tiempo= delta_time(start,end)
    return tiempo, filtrado, filtro


def req_4(catalog,rango_fecha_ini, rango_fecha_fin, franja_hora_salida_uno, franja_hora_salida_dos, cant_aereolineas_mas_vuelos):
    """
    Retorna el resultado del requerimiento 4
    """
    start= get_time()
    # 1 Filtrar los vuelos por rango de fechas y franja horaria de salida
    rango_fecha_ini = dt.datetime.strptime(rango_fecha_ini, "%Y-%m-%d")
    rango_fecha_fin = dt.datetime.strptime(rango_fecha_fin, "%Y-%m-%d")
    resultado = lt.new_list()

    if rbt.get (catalog["viajes"],rango_fecha_ini) is not None or rbt.get (catalog["viajes"],rango_fecha_fin) is not None:
        list_por_fecha = rbt.values(catalog["viajes"], rango_fecha_ini, rango_fecha_fin)
        list_por_fanja = lt.new_list()
        for i in range(sl.size(list_por_fecha)):
            lista_dia = sl.get_element(list_por_fecha, i)
            for j in range(sl.size(lista_dia)):
                vuelo = sl.get_element(lista_dia, j)
                if franja_hora_salida_uno <= vuelo["sched_dep_time"] <= franja_hora_salida_dos:
                    lt.add_last(list_por_fanja, vuelo)
        # 2 Agrupar los vuelos por aerolínea
        aereolineas = {}
        for i in range(lt.size(list_por_fanja)):
            vuelo = lt.get_element(list_por_fanja, i)
            codigo = vuelo["carrier"]
            if codigo in aereolineas:
                aereolineas[codigo]["count"] += 1
                aereolineas[codigo]["suma_duracion"] += int(vuelo["air_time"])
                aereolineas[codigo]["suma_distancia"] += int(vuelo["distance"])
                lt.add_last(aereolineas[codigo]["lista_vuelos"], vuelo)
            else:
                aereolineas[codigo] = {
                    "count": 1,
                    "suma_duracion": int(vuelo["air_time"]),
                    "suma_distancia": int(vuelo["distance"]),
                    "lista_vuelos": lt.new_list()
                }
                lt.add_last(aereolineas[codigo]["lista_vuelos"], vuelo)

        # 3 Insertar las aerolíneas en un heap (máximo por cantidad de vuelos)
        aereo = pq.new_heap(is_min_pq=False)
        for codigo in aereolineas:
            pq.insert(aereo, aereolineas[codigo]["count"], codigo)

        # 4 Extraer las top N aerolíneas
        resultado = lt.new_list()
        n = min(cant_aereolineas_mas_vuelos, pq.size(aereo))
        for _ in range(n):  
            codigo = pq.get_first_priority(aereo) # Devuelve un diccionario con priority y value
            info = aereolineas[codigo]

            # 5 Calcular promedios
            prom_duracion = info["suma_duracion"] / info["count"]
            prom_distancia = info["suma_distancia"] / info["count"]

            # 6 Encontrar vuelo con menor duración
            menor = None
            dur_menor = 999999
            fecha_menor = None

            for j in range(lt.size(info["lista_vuelos"])):
                vuelo = lt.get_element(info["lista_vuelos"], j)
                dur = int(vuelo["air_time"])
                fecha_hora = dt.datetime.strptime(
                    vuelo["date"] + " " + vuelo["sched_dep_time"], "%Y-%m-%d %H:%M"
                )

                if dur < dur_menor or (dur == dur_menor and fecha_menor and fecha_hora < fecha_menor):
                    menor = vuelo
                    dur_menor = dur
                    fecha_menor = fecha_hora

            # 7 Agregar al resultado
            lt.add_last(resultado, {
                "Aerolínea": codigo,
                "Vuelos totales": info["count"],
                "Duración promedio": round(prom_duracion, 2),
                "Distancia promedio": round(prom_distancia, 2),
                "Vuelo menor duración": {
                    "ID": menor["id"],
                    "Código": menor["flight"],
                    "Fecha salida": menor["date"] + " " + menor["sched_dep_time"],
                    "Origen": menor["origin"],
                    "Destino": menor["dest"],
                    "Duración": menor["air_time"]
                }
            })
                
        
    end= get_time()
    tiempo= delta_time(start,end)
    return tiempo, lt.size(resultado), resultado

def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog, rango_f, rango_d, m):
    """
    Retorna el resultado del requerimiento 6
    rango_f: Rango de fechas a analizar (por ejemplo: [“2013-01-01”, “2013-03-31”]).
    rango_d: Rango de distancias (en millas) a analizar (por ejemplo: [500, 1500]). 
    m = Cantidad M de aerolíneas a mostrar (por ejemplo: M=5).
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

def diferencia_tiempo(real, programado):
    r = real.split(":")
    min1 = int(r[0])*60+int(r[1])
    p = programado.split(":")
    min2 = int(p[0])*60+int(p[1])
    diferencia = min1 - min2
    if diferencia < -720:
        diferencia += 1440
    return diferencia
