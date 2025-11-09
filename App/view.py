import sys
default_limit = 1000 
sys.setrecursionlimit(default_limit*10)
import tabulate as tb
from App import logic as lg
from DataStructures.List import array_list as lt

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
    file = input('Diga el archivo que quiere evaluar (small, medium, large)\n').strip()
    file = "data/flights_"+file+".csv"
    tiempo, trayectos = lg.load_data(control, file)
    print("Datos cargados: ")
    print("Tiempo de carga (ms): "+ str(round(tiempo, 3)))
    print("Viajes cargados: "+str(trayectos))
    p, u = lg.info_carga_datos(control)
    print("Primeros viajes: ")
    print(tb.tabulate(p, headers="keys", tablefmt= "simple_grid"))
    print("\nÚltimos viajes: ")
    print(tb.tabulate(u, headers="keys", tablefmt= "simple_grid"))
    
def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


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
        print(" Tiempo de ejecución:  ms\n" + str(round(tiempo, 3)))

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

        print(tb.tabulate(datos, headers="keys", tablefmt="simple_grid"))

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

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

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
