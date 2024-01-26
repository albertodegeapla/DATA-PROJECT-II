import random
from datetime import datetime, timedelta
import xml. etree.ElementTree as ET
import os
import time

def generar_id_persona():
    return random.randint(10000, 99999)

def cargar_txt(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def generar_nombres():
    nombre = cargar_txt('./nombre.txt')
    return random.choice(nombre)

def generar_primer_apellido():
    primer_apellido = cargar_txt('./apellido.txt')
    return random.choice(primer_apellido)

def generar_segundo_apellido():
    segundo_apellido = cargar_txt('./apellido.txt')
    return random.choice(segundo_apellido)

def generar_dni():
    numeros = random.randint(10000000, 99999999)
    letra = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return f"{numeros}-{letra}"

def generar_edad():
    return random.randint(18, 75)

def generar_cartera():
    return round(random.uniform(100, 10000), 2)

def generar_persona():
    id_persona = generar_id_persona()
    nombre = generar_nombres()
    primer_apellido = generar_primer_apellido()
    segundo_apellido = generar_segundo_apellido()
    dni = generar_dni()
    edad = generar_edad()
    cartera = generar_cartera()

    persona = {
        'ID_persona':id_persona,
        'Nombre':nombre,
        'Primer apellido':primer_apellido,
        'Segundo apellido':segundo_apellido,
        'DNI':dni,
        'Edad':edad,
        'Cartera':cartera
    }

    return persona

#SOLO DEVOLVERÁ UNA PERSONA PARA ESTE VIERNES
for _ in range(1):
    persona_generada = generar_persona()
    print(persona_generada)


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

        velocidad = 4
        tiempo_inicio = time.time()

        # Generar la fecha y hora aleatorias en cada iteración
        

        while time.time() - tiempo_inicio < velocidad:
            hora_actual = datetime.strptime(hora_str, "%d/%m/%Y %H:%M:%S") + timedelta(seconds=i * 4)
            print(f'Enviando coordenada: {coord_siguiente}, Hora actual: {hora_actual.strftime("%Y-%m-%d %H:%M:%S")}')
            time.sleep(4)

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
ruta_kml = './ruta1.kml'

# Llama a la función para obtener las coordenadas desde el archivo KML
coordenadas_ruta = leer_coordenadas_desde_kml(ruta_kml)

# Simular movimiento entre coordenadas
simular_movimiento(coordenadas_ruta)