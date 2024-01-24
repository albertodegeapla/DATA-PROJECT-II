import random
from datetime import datetime, timedelta
from generador_coches import generar_id_coche
from generador_personas import generar_id_persona
import xml. etree.ElementTree as ET
import os
 
class Persona:
    def __init__(self, id_persona):
        self.id_persona = id_persona

id_persona = generar_id_persona
 
class Coche:
    def __init__(self, id_coche):
        self.id_coche = id_coche

id_coche = generar_id_coche
 
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

def generar_ruta_salida(coordenadas_ruta):
    porcentaje_ruta_salida = 0.1  
    cantidad_puntos_salida = int(len(coordenadas_ruta) * porcentaje_ruta_salida)
    ruta_salida = coordenadas_ruta[:cantidad_puntos_salida]
    return ruta_salida

def generar_ruta_llegada(coordenadas_ruta):
    porcentaje_ruta_llegada = 0.1 
    cantidad_puntos_llegada = int(len(coordenadas_ruta) * porcentaje_ruta_llegada)
    ruta_llegada = coordenadas_ruta[-cantidad_puntos_llegada:]
    return ruta_llegada

def generar_informacion_ruta(ruta):
    longitud_total = len(ruta)
    hora_salida = datetime(2024, 1, 1, random.randint(6, 9), random.randint(0, 59))

    
    duracion_total_minutos = random.randint(30, 120)

    
    hora_llegada = hora_salida + timedelta(minutes=duracion_total_minutos)

   
    ruta_salida = generar_ruta_salida(ruta)
    ruta_llegada = generar_ruta_llegada(ruta)

   
    punto_salida = ruta_salida[0]
    punto_llegada = ruta_llegada[-1]

    
    fecha = datetime.now() + timedelta(days=random.randint(1, 7))

    return {
        'hora_salida': hora_salida,
        'hora_llegada': hora_llegada,
        'fecha': fecha,
        'punto_salida': punto_salida,
        'punto_llegada': punto_llegada
    }

carpeta_kml = "rutas/ruta_prueba_coche" 
todas_las_rutas = leer_todas_las_rutas_en_carpeta(carpeta_kml)

una_ruta = random.choice(todas_las_rutas)


informacion_ruta = generar_informacion_ruta(una_ruta)
print(una_ruta)
print(informacion_ruta)
