import random
from datetime import datetime, timedelta
import xml. etree.ElementTree as ET
import os
import time

### librerias para el publisher
import argparse
import logging
from google.cloud import pubsub_v1
import json

### librerias para el bigQuery
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.runners.interactive.interactive_runner import InteractiveRunner
import apache_beam.runners.interactive.interactive_beam as ib
from apache_beam.transforms import window
import apache_beam as beam
from google.cloud import bigquery

parser = argparse.ArgumentParser(description=("Generador de Rutas de peatones y publicadas en pub/sub"))
parser.add_argument(
    "--project_id",
    required=True,
    help="Project ID de GCloud"
)
##PREGUNTAR
parser.add_argument(
    "--peaton_topic_name",
    required=True,
    help="Topic de GCloud del peatón"
)
parser.add_argument(
    "--dataset_project_II",
    required=True,
    help="Dataset de GCloud"
)
parser.add_argument(
    "--peaton_table",
    required=True,
    help="Table de coches GCloud"
)
parser.add_argument(
    "--n_peatones",
    required=True,
    help="Numero de peatones a generar"
)

args, opts = parser.parse_known_args()

class PubSubPeatonMessage:

    def __init__(self, project_id, peaton_topic_name):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = project_id
        self.topic_name = peaton_topic_name

    def publishPeatonMessage(self, message):
        json_str = json.dumps(message)
        topic_path = self.publisher.topic_path(self.project_id, self.topic_name)
        publish_future = self.publisher.publish(topic_path, json_str.encode("utf-8"))
        publish_future.result()
        ###REVISAR ESTE MENSAJE###
        logging.info(f"El peaton {message['id_persona']}, va a esta hora {message['fecha_hora_str']} y en estas coordenadas: {message['coordenadas']}, a {message['punto_destino']}.")

    def __exit__(self):
        self.publisher.transport.close()
        logging.info("Cerrando car Publisher") 

def generar_id_persona(id):
    return id

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

def generar_edad():
    return random.randint(18, 75)

def generar_cartera():
    return round(random.uniform(2, 1000), 2)

def generar_persona():
    id_persona = generar_id_persona(id)
    nombre = generar_nombres()
    primer_apellido = generar_primer_apellido()
    segundo_apellido = generar_segundo_apellido()
    edad = generar_edad()
    cartera = generar_cartera()
    
    peaton = {
        'ID_persona':id_persona,
        'Nombre':nombre,
        'Primer_apellido':primer_apellido,
        'Segundo_apellido':segundo_apellido,
        'Edad':edad,
        'Cartera':cartera
    }

    return peaton

def id_peaton_generator(n_peatones):
    array_id = [(i + 1) for i in range(n_peatones)]
    return array_id

###HASTA AQUÍ OK FALTA COMPROBAR SOLO PARTE FLAGS

# WRITE TO BIG QUERRY
def write_peaton_to_bigquery(project_id, dataset_project_II, peaton_table, n_peatones):
    options = PipelineOptions(streaming=True)
    with beam.Pipeline(options=options) as p:
        #crea los peatones a usar
        peaton = [generar_persona(i+1) for i in range(n_peatones)]

        # Crear un PCollection con los coches
        peaton_pcollection = p | beam.Create(peaton)
 
        peaton_pcollection | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                table=f'{project_id}:{dataset_project_II}.{peaton_table}',
                schema = '{"ID_persona":"INTEGER", "Nombre":"STRING", "Primer_apellido":"STRING", "Segundo_apellido":"STRING","Edad":"INTEGER", "Cartera":"FLOAT"}',
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
# READ FROM BIG QUERRY
###REVISAR peaton_id
def read_peaton_from_bigquery(project_id, dataset_project_II, peaton_table, peaton_id):
    client = bigquery.Client(project=project_id)

    # Construye la consulta SQL para obtener el coche por ID
    query = f"""
        SELECT *
        FROM `{project_id}.{dataset_project_II}.{peaton_table}`
        WHERE ID_coche = {peaton_id}
    """
    query_job = client.query(query)

    # Devuelve el resultado como un iterows
    results = query_job.result()

    for row in results:
        peaton = dict(row.items())   # Convierte el row en un diccionario
        return peaton

    return None

# CONVERTIR A JSON -> id, coordenadas, punto destino, cartera, mood

def convertir_a_json(id_persona, coordenadas, punto_destino):
    # Construye un diccionario con la información (((FALTA VER COORDENADAS)))
    datos_peaton = {
        "id_coche": id_persona,
        "coordenadas": coordenadas,
        "punto_destino": punto_destino
    }
    return datos_peaton


def generar_fecha_hora():
    fecha_hora = datetime.now()
    fecha_hora_str = fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
    return fecha_hora_str


# DECODE MESSAGE DE COCHES CTRL C (((REVISAR NO VEO DECODE)))

def publicar_movimiento(coordenadas, project_id, dataset_project_II, peaton_table, id_persona):
    fecha_hora = generar_fecha_hora()

    longitud_ruta = len(coordenadas)
    punto_destino = coordenadas[longitud_ruta-1]
    for i in range(len(coordenadas)-1):

        peaton = read_peaton_from_bigquery(project_id, dataset_project_II, peaton_table, id_persona)
        coord_restantes = longitud_ruta - i - 1

        coord_actual = coordenadas[i]
        coord_siguiente = coordenadas[i + 1]

        velocidad = 2
        tiempo_inicio = time.time()

        while time.time() - tiempo_inicio < velocidad:
            hora_actual = datetime.strptime(fecha_hora, "%d/%m/%Y %H:%M:%S") + timedelta(seconds=i * 2)
            # AÑADIR PUNTO MAPA
            punto_mapa = (hora_actual.strftime("%Y-%m-%d %H:%M:%S"), coord_siguiente)

            # AÑADIR EL PRIMER TRY 274-279 hasta linea 289
            try:
                peaton_publisher = PubSubPeatonMessage(project_id, dataset_project_II)
                message: dict = convertir_a_json(id_persona, coordenadas, punto_destino)
                peaton_publisher.publishCarMessage(message)
                
            except Exception as e:
                logging.error("Error while inserting data into ruta_coche Topic: %s", e)
            finally:
                peaton_publisher.__exit__()

            time.sleep(2)


def leer_coordenadas_desde_kml(ruta_archivo_kml):
    coordenadas_ruta = []
    tree = ET.parse(ruta_archivo_kml)
    root = tree.getroot()
    for coordinates_element in root.findall(".//{http://www.opengis.net/kml/2.2}coordinates"):
        coordinates_text = coordinates_element.text.strip()
        ### MIRAR CODE DE GEN COCHE
        i = 0
        for coord in coordinates_text.split():
            cords = (tuple(map(float, coord.split(','))))
            cordenada1 = cords[1]
            cordenada2 = cords[0]
            coordenada = (cordenada1, cordenada2)            
            coordenadas_ruta.append(coordenada)

    return coordenadas_ruta

# AÑADIR FUNCION QUE COJA UNA RUTS RANDOM

# FUNCION RANDOM DEL 1 AL X, TE DEVUELEVE UN NUEMRO Y AL RUTA f(./carpeta_peaton/ruta{numero_random}.kml)           
def leer_todas_las_rutas_en_carpeta(carpeta_kml):
    todas_las_rutas = []

    for archivo_kml in os.listdir(carpeta_kml):
        if archivo_kml.endswith(".kml"):
            ruta_completa = os.path.join(carpeta_kml, archivo_kml)
            coordenadas_ruta = leer_coordenadas_desde_kml(ruta_completa)
            todas_las_rutas.append(coordenadas_ruta)

    return todas_las_rutas


#### if __name__ == "__main__":
if __name__ == "__main__":

    project_id = args.project_id
    topic_peaton = args.peaton_topic_name
    dataset_id = args.dataset_project_II
    table_id = args.peaton_table

    n_peatones = int(args.n_peatones)

    # publicar en bigquery el num de peatones a usar
    id_peaton = id_peaton_generator(n_peatones)
#### a partir del while = True
    while(True):

        # HAY QUE VALIDAR QUE EL peaton NO ESTA EN RUTA (LUEGO)
        peaton_elegido = random.choice(id_peaton)        

        #FALTA POR HACER
        carpeta_kml = './ruta_peaton'
        archivos_kml = [archivo for archivo in os.listdir(carpeta_kml) if archivo.endswith('.kml')]
        if not archivos_kml:
            print("No hay archivos KML en la carpeta especificada.")
        else:
            archivo_seleccionado = random.choice(archivos_kml)
            ruta_completa = os.path.join(carpeta_kml, archivo_seleccionado)

            with open(ruta_completa, 'r') as archivo:
                contenido_kml = archivo.read()

        coordenadas_ruta = leer_coordenadas_desde_kml(carpeta_kml)
        
        # print de lo que publicamos en el topic
        logging.getLogger().setLevel(logging.INFO)

        #leemos de big query el coche con sus datos
        publicar_movimiento(coordenadas_ruta, project_id, topic_peaton, dataset_id, table_id, peaton_elegido)
