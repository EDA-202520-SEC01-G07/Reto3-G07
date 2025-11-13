import sys
default_limit = 1000 
sys.setrecursionlimit(default_limit*10)
import tabulate as tb
from App import logic as lg
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.List import single_linked_list as sl
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.List import array_list as lt
import datetime as dt

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    return lg.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    file = input('Diga el archivo que quiere evaluar (small, medium, large)\n').strip().lower()
    file = "data/flights_"+file+".csv"
    tiempo, trayectos = lg.load_data(control, file)
    print("Datos cargados: ")
    print("Tiempo de carga (ms): "+ str(round(tiempo, 3)))
    print("Viajes cargados: "+str(trayectos))
    p, u = lg.info_carga_datos(control)
    print("Primeros viajes: ")
    print(tb.tabulate(p, headers="keys", tablefmt= "fancy_grid"))
    print("\nÚltimos viajes: ")
    print(tb.tabulate(u, headers="keys", tablefmt= "fancy_grid"))
    
def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    aerolinea = input("Diga el código de la aerolínea: ").upper()
    a = input("Diga el mínimo del rango de minutos (a): ")
    b = input("Diga el máximo del rango de minutos (b): ")
    rango = [a, b]
    tiempo, trayectos, viajes_filtrados = lg.req_1(control, aerolinea, rango)
    print("Tiempo de ejecución: "+str(round(tiempo, 2)))
    print("Número de viajes filtrados: "+str(trayectos))
    tam =  pq.size(viajes_filtrados)
    lista = []
    while not pq.is_empty(viajes_filtrados):
        lista.append(pq.remove(viajes_filtrados))
        
    if tam>10:
        primeros = lista[:5]
        ultimos = lista[-5:]
        print("Primeros viajes filtrados: ")
        print(tb.tabulate(primeros, headers="keys", tablefmt="fancy_grid"))
        print("\nÚltimos viajes filtrados: ")
        print(tb.tabulate(ultimos, headers="keys", tablefmt="fancy_grid"))
    else:
        print(tb.tabulate(lista, headers="keys", tablefmt="fancy_grid"))
        


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    dest = input("Diga el código del aeropuerto de destino: ").upper().strip()
    rango_minutos = input("Diga el rango de minutos de anticipo (min,max): ").strip()

    tiempo, filtrados, vuelos_filtrados = lg.req_2(control, dest, rango_minutos)

    print("\n=== Requerimiento 2: Vuelos con anticipo en la llegada ===")
    print("Tiempo de ejecución (ms):", round(tiempo, 2))
    print("Número de vuelos filtrados:", filtrados)

    valores = rbt.value_set(vuelos_filtrados)

    vuelos_flat = []
    i = 0
    while i < sl.size(valores):
        mapaf = sl.get_element(valores, i)
        j = 0
        while j < sl.size(mapaf):
            vuelos_flat.append(sl.get_element(mapaf, j))
            j += 1
        i += 1

    total = len(vuelos_flat)
    if total == 0:
        print("\nNo se encontraron vuelos en el rango indicado.")
        return

    if total > 10:
        primeros = vuelos_flat[:5]
        ultimos = vuelos_flat[-5:]

        print("\n-- Primeros vuelos filtrados --")
        print(tb.tabulate(primeros, headers="keys", tablefmt="fancy_grid"))

        print("\n-- Últimos vuelos filtrados --")
        print(tb.tabulate(ultimos, headers="keys", tablefmt="fancy_grid"))
    else:
        print("\n-- Vuelos filtrados --")
        print(tb.tabulate(vuelos_flat, headers="keys", tablefmt="fancy_grid"))



def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    carrier = input("Ingrese el código de la aerolínea (por ejemplo: 'AA', 'UA'): ").upper()
    dest = input("Ingrese el código del aeropuerto de destino (por ejemplo: 'JFK', 'LAX'): ").upper()
    min_dist = int(input("Ingrese la distancia mínima (en millas): "))
    max_dist = int(input("Ingrese la distancia máxima (en millas): "))
    tiempo, total, lista = lg.req_3(control, carrier, dest, [min_dist, max_dist])
    if total == 0:
        print(" No se encontraron vuelos que cumplan con los criterios indicados.")
    else:
        print("Total de vuelos encontrados: "+ str(total))
        print(" Tiempo de ejecución [ms]: \n" + str(round(tiempo, 3)))

        # Mostrar máximo 10 vuelos (5 primeros + 5 últimos)
        datos = []
        n = lt.size(lista)
        for i in range(n):
            vuelo = lt.get_element(lista, i)
            fila = {
                "ID": vuelo["id"],
                "Código vuelo": vuelo["flight"],
                "Fecha": vuelo["date"],
                "Aerolínea": vuelo["name"],
                "Código": vuelo["carrier"],
                "Origen": vuelo["origin"],
                "Destino": vuelo["dest"],
                "Distancia": vuelo["distance"]
            }
            datos.append(fila)

        if total > 10:
            datos = datos[:5] + datos[-5:]

        print(tb.tabulate(datos, headers="keys", tablefmt="fancy_grid"))

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    print("\n=== Requerimiento 4 ===")
    print("Identificar las N aerolíneas con mayor número de vuelos y su vuelo de menor duración.\n")

    # Solicitar parámetros
    fecha_ini = input("Ingrese la fecha inicial (YYYY-MM-DD): ").strip()
    fecha_fin = input("Ingrese la fecha final (YYYY-MM-DD): ").strip()
    hora_ini = input("Ingrese la hora inicial (HH:MM): ").strip()
    hora_fin = input("Ingrese la hora final (HH:MM): ").strip()
    n = int(input("Ingrese la cantidad de aerolíneas a mostrar (N): "))

    # Llamar a la función lógica
    tiempo, total, resultado = lg.req_4(control, fecha_ini, fecha_fin, hora_ini, hora_fin, n)

    # Verificar si hay resultados
    if total == 0:
        print("\nNo se encontraron vuelos dentro del rango indicado.")
        return

    print("\nTiempo de ejecución: ms" + str(round(tiempo, 3)))
    print("Aerolíneas encontradas: " + str(total) + "\n")

    # Crear tabla resumen principal
    datos_tabla = []
    for i in range(lt.size(resultado)):
        aero = lt.get_element(resultado, i)
        fila = {
            "Aerolínea": aero["Aerolínea"],
            "Vuelos totales": aero["Vuelos totales"],
            "Duración promedio": aero["Duración promedio"],
            "Distancia promedio": aero["Distancia promedio"]
        }
        datos_tabla.append(fila)

    print("=== Aerolíneas con mayor número de vuelos ===")
    print(tb.tabulate(datos_tabla, headers="keys", tablefmt="fancy_grid"))

    # Mostrar detalle del vuelo de menor duración por aerolínea
    print("\n=== Vuelo con menor duración por aerolínea ===")
    vuelos_tabla = []
    for i in range(lt.size(resultado)):
        aero = lt.get_element(resultado, i)
        menor = aero["Vuelo menor duración"]
        fila = {
            "Aerolínea": aero["Aerolínea"],
            "ID vuelo": menor["ID"],
            "Código": menor["Código"],
            "Fecha salida": menor["Fecha salida"],
            "Origen": menor["Origen"],
            "Destino": menor["Destino"],
            "Duración": menor["Duración"]
        }
        vuelos_tabla.append(fila)
    print(tb.tabulate(vuelos_tabla, headers="keys", tablefmt="fancy_grid"))



def print_req_5(control):
    """
    Vista Req. 5
    """
    rango = input("Rango de fechas (YYYY-MM-DD,YYYY-MM-DD): ").strip()
    dest  = input("Código de aeropuerto destino (ej. JFK): ").upper().strip()
    n     = int(input("Cantidad de aerolíneas a mostrar (N): ").strip())

    partes = [p.strip() for p in rango.split(",")]
    if len(partes) != 2:
        print("Formato inválido. Usa: YYYY-MM-DD,YYYY-MM-DD")
        return

    tiempo, total_aero, arbol = lg.req_5(control, partes, dest, n)

    print("\n=== Requerimiento 5: Aerolíneas más puntuales (llegada) ===")
    print("Tiempo de ejecución (ms):", round(tiempo, 2))
    print("Aerolíneas consideradas (M):", total_aero)

    valores = rbt.value_set(arbol)   
    filas = []

    i = 0
    while i < sl.size(valores) and len(filas) < n:
        bucket = sl.get_element(valores, i)  
        j = 0
        while j < lt.size(bucket) and len(filas) < n:
            item = lt.get_element(bucket, j)
            maxf = item["Vuelo mayor distancia"]
            filas.append({
                "Carrier": item["Aerolínea"],
                "Vuelos totales": item["Vuelos totales"],
                "Retraso prom. (min)": item["Retraso promedio llegada (min)"],
                "Duración prom. (min)": item["Duración promedio vuelo (min)"],
                "Dist. prom. (mi)": item["Distancia promedio vuelo (millas)"],
                "Max ID": maxf["id"],
                "Max Vuelo": maxf["flight"],
                "Max Fecha": maxf["date"],
                "Max Dep": maxf["dep_time"],
                "Max Origen": maxf["origin"],
                "Max Destino": maxf["dest"],
                "Max AirTime (min)": maxf["air_time"],
                "Max Dist (mi)": maxf["distance"],
            })
            j += 1
        i += 1

    if not filas:
        print("\nNo se encontraron aerolíneas para ese destino y rango de fechas.")
        return

    print(f"\n-- Top {len(filas)} aerolíneas --")
    print(tb.tabulate(filas, headers="keys", tablefmt="fancy_grid"))





def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    print("Indique el rango de fechas: ")
    f1 = dt.datetime.strptime(input("Fechas mínima: "), "%Y-%m-%d")
    f2 = dt.datetime.strptime(input("Fecha máxima: "), "%Y-%m-%d")
    r_fechas = [f1, f2]
    print("Indique el rango de distancias: ")
    d1 = float(input("Distancia mínima: "))
    d2 = float(input("Distancia máxima: "))
    r_distancias = [d1, d2]
    m = int(input("Diga el número de aerolíneas a mostrar: "))
    
    tiempo, aerolineas = lg.req_6(control, r_fechas, r_distancias, m)
    print("Tiempo de ejecución: "+str(round(tiempo, 3)))
    print("Aerolíneas analizadas: "+str(m))
    
    lista = []
    while not pq.is_empty(aerolineas):
        lista.append(pq.remove(aerolineas))
    if m < len(lista):
        lista = lista[:m]
    else:
        print("No hay "+str(m)+" viajes.")
        if len(lista) == 0:
            print("No hay ningún vuelo.")
        else:
            print("Se presentan todos los viajes: ")
    print(tb.tabulate(lista, headers="keys", tablefmt="fancy_grid"))

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
