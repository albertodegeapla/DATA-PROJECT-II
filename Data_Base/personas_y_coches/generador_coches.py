import random
from datetime import datetime, timedelta
import xml. etree.ElementTree as ET
import os
import time

def generar_id_coche():
    return random.randint(10000, 99999)

def cargar_txt(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def generar_marca():
    marca = cargar_txt('Data_Base/personas_y_coches/marcas_coche.txt')
    return random.choice(marca)

def generar_matricula():
    numeros = random.randint(0000, 9999)
    letra1 = random.choice('ABCDEFGHIJKLM')
    letra2 = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    letra3 = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return f"{numeros}-{letra1+letra2+letra3}"

def generar_edad_coche():
    return random.randint(0, 25)

def generar_plazas():
    return random.randint(1, 4)

def generar_kilometraje():
    return random.randint(1000, 200000)

def generar_precio_compra():
    return random.randint(10000, 80000)

def generar_cobro_km(kilometraje, precio_compra):
    descuento_por_kilometraje = 0.05  # Descuento del 5% por cada 10000km
    descuento = (kilometraje // 10000) * descuento_por_kilometraje
    precio_final = precio_compra - descuento

    return max(precio_final, 0)

kilometraje = generar_kilometraje()
precio_compra = generar_precio_compra()


def generar_coche():
    id_coche = generar_id_coche()
    marca = generar_marca()
    matricula = generar_matricula()
    edad_coche = generar_edad_coche()
    plazas = generar_plazas()
    kilometraje = generar_kilometraje()
    precio_compra = generar_precio_compra()
    

    coche = {
        'ID_coche':id_coche,
        'Marca':marca,
        'Matrícula':matricula,
        'Edad coche':edad_coche,
        'Kilometraje':kilometraje,
        'Precio de compra':precio_compra,
    }

    return coche


#SOLO DEVOLVERÁ UN COCHE PARA ESTE VIERNES
for _ in range(1):
    coche_generado = generar_coche()
    print(coche_generado)

def generar_fecha_hora():
    fecha = datetime.now() + timedelta(days=random.randint(1, 30))
    hora = datetime(fecha.year, fecha.month, fecha.day, random.randint(6, 9), random.randint(0, 59), random.randint(0, 59))
    hora_str = hora.strftime("%d/%m/%Y %H:%M:%S")  # Corrección en el formato
    return hora_str

def simular_movimiento(coordenadas):
    hora_str = generar_fecha_hora()
    for i in range(len(coordenadas) - 1):
        coord_actual = coordenadas[i]
        coord_siguiente = coordenadas[i + 1]

        velocidad = 2
        tiempo_inicio = time.time()

        # Generar la fecha y hora aleatorias en cada iteración
        

        while time.time() - tiempo_inicio < velocidad:
            hora_actual = datetime.strptime(hora_str, "%d/%m/%Y %H:%M:%S") + timedelta(seconds=i * 2)
            print(f'Enviando coordenada: {coord_siguiente}, Hora actual: {hora_actual.strftime("%Y-%m-%d %H:%M:%S")}')
            time.sleep(2)

    ultima_coordenada = coordenadas[-1]
    hora_llegada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Coordenada final: {ultima_coordenada}, Hora de llegada: {hora_llegada}")

def leer_coordenadas_desde_kml(ruta_archivo_kml):
    coordenadas_ruta = []
    tree = ET.parse(ruta_archivo_kml)
    root = tree.getroot()
    for coordinates_element in root.findall(".//{http://www.opengis.net/kml/2.2}coordinates"):
        coordinates_text = coordinates_element.text.strip()
        for coord in coordinates_text.split():             
            coordenadas_ruta.append(tuple(map(float, coord.split(','))))     
    return coordenadas_ruta
             
def leer_todas_las_rutas_en_carpeta(carpeta_kml):
    todas_las_rutas = []

    
    for archivo_kml in os.listdir(carpeta_kml):
        if archivo_kml.endswith(".kml"):
            ruta_completa = os.path.join(carpeta_kml, archivo_kml)
            coordenadas_ruta = leer_coordenadas_desde_kml(ruta_completa)
            todas_las_rutas.append(coordenadas_ruta)

    return todas_las_rutas


# Supongamos que 'ruta_kml' es la ruta completa al archivo KML que contiene tus coordenadas
ruta_kml = 'Data_Base/rutas/ruta_prueba_coche'

# Llama a la función para obtener las coordenadas desde el archivo KML
coordenadas_ruta = leer_coordenadas_desde_kml(ruta_kml)

# Simular movimiento entre coordenadas
simular_movimiento(coordenadas_ruta)