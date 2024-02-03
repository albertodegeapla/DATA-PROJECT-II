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
parser.add_argument(
    "--peaton_topic_name",
    required=True,
    help="Topic de GCloud del peatón"
)
parser.add_argument(
    "--dataset_id",
    required=True,
    help="Dataset de GCloud"
)
parser.add_argument(
    "--table_peaton",
    required=True,
    help="Table de peatones GCloud"
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
        logging.info(f"El peaton {message['id_persona']}, va a esta hora y en estas coordenadas: {message['coordenadas']}, a {message['punto_destino']} y tiene en la cartera {message['cartera']}.")

    def __exit__(self):
        self.publisher.transport.close()
        logging.info("Cerrando peaton Publisher") 

# Funciones
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

###AÑADIR DNI 
def generar_edad():
    return random.randint(18, 75)

def generar_cartera():
    return round(random.uniform(2, 100), 2)

def generar_mood():
    return random.choice(['majo', 'normal', 'antipático'])

def generar_persona(id):
    id_persona = generar_id_persona(id)
    nombre = generar_nombres()
    primer_apellido = generar_primer_apellido()
    segundo_apellido = generar_segundo_apellido()
    edad = generar_edad()
    mood = generar_mood()
    cartera = generar_cartera()
    
    peaton = {
        'ID_persona':id_persona,
        'Nombre':nombre,
        'Primer_apellido':primer_apellido,
        'Segundo_apellido':segundo_apellido,
        'Edad':edad,
        'Mood':mood,
        'Cartera':cartera,
        'Cartera_inicial': cartera
    }

    return peaton

# crea un array con los id de los peatones
def id_peaton_generator(n_peatones):
    array_id = [(i + 1) for i in range(n_peatones)]
    return array_id

# WRITE TO BIG QUERRY
def write_peaton_to_bigquery(project_id, dataset_id, table_peaton, n_peatones):
    options = PipelineOptions(streaming=True)
    with beam.Pipeline(options=options) as p:
        #crea los peatones a usar
        peaton = [generar_persona(i+1) for i in range(n_peatones)]

        # Crear un PCollection con los peatones
        peaton_pcollection = p | beam.Create(peaton)
 
        peaton_pcollection | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                table=f'{project_id}:{dataset_id}.{table_peaton}',
                schema = '{"ID_persona":"INTEGER", "Nombre":"STRING", "Primer_apellido":"STRING", "Segundo_apellido":"STRING","Edad":"INTEGER", "Cartera":"FLOAT", "CARTERA_INICIAL":"FLOAT", "Mood":"STRING"}',
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
# READ FROM BIG QUERRY
def read_peaton_from_bigquery(project_id, dataset_id, table_peaton, peaton_id):
    client = bigquery.Client(project=project_id)

    # Construye la consulta SQL para obtener el peaton por ID
    query = f"""
        SELECT *
        FROM `{project_id}.{dataset_id}.{table_peaton}`
        WHERE ID_persona = {peaton_id}
    """
    query_job = client.query(query)

    # Devuelve el resultado como un iterows
    results = query_job.result()

    for row in results:
        peaton = dict(row.items())   # Convierte el row en un diccionario
        return peaton

    return None

# CONVERTIR A JSON -> id, coordenadas, punto destino, cartera, mood

def convertir_a_json(id_persona, coordenadas, punto_destino, cartera):
    datos_peaton = {
        "id_persona": id_persona,
        "coordenadas": coordenadas,
        "punto_destino": punto_destino,
        "cartera": cartera
    }
    return datos_peaton


def generar_fecha_hora():
    fecha_hora = datetime.now()
    fecha_hora_str = fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
    return fecha_hora_str


def publicar_movimiento(coordenadas, project_id, topic_peaton, id_persona, cartera):
    hora_str = generar_fecha_hora()

    longitud_ruta = len(coordenadas)
    punto_destino = coordenadas[longitud_ruta - 1]
    
    for i in range(len(coordenadas) - 1):
        coord_actual = coordenadas[i]
        coord_siguiente = coordenadas[i + 1]

        velocidad = 2
        tiempo_inicio = time.time()

        punto_mapa_actual = {
            'hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'coordenada_actual': coord_actual,
        }

        try:
            peaton_publisher = PubSubPeatonMessage(project_id, topic_peaton)
            message_actual: dict = convertir_a_json(id_persona, punto_mapa_actual, punto_destino, cartera)
            peaton_publisher.publishPeatonMessage(message_actual)
        except Exception as e:
            logging.error("Error while inserting data into ruta_peaton Topic: %s", e)
        finally:
            peaton_publisher.__exit__()

        tiempo_inicio_duplicado = time.time() + velocidad

        punto_mapa_duplicado = {
            'hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'coordenada_duplicada': coord_actual,
        }

        while time.time() < tiempo_inicio_duplicado:
            time.sleep(2)  # Pequeño retardo entre la coordenada actual y duplicada

        try:
            peaton_publisher = PubSubPeatonMessage(project_id, topic_peaton)
            message_duplicado: dict = convertir_a_json(id_persona, punto_mapa_duplicado, punto_destino, cartera)
            peaton_publisher.publishPeatonMessage(message_duplicado)
        except Exception as e:
            logging.error("Error while inserting data into ruta_peaton Topic: %s", e)
        finally:
            peaton_publisher.__exit__()



def leer_coordenadas_desde_kml(ruta_archivo_kml):
    coordenadas_ruta = []
    tree = ET.parse(ruta_archivo_kml)
    root = tree.getroot()

    for coordinates_element in root.findall(".//{http://www.opengis.net/kml/2.2}coordinates"):
        coordinates_text = coordinates_element.text.strip()
        i = 0
        for coord in coordinates_text.split():
            cords = (tuple(map(float, coord.split(','))))
            cordenada1 = cords[1]
            cordenada2 = cords[0]
            coordenada = (cordenada1, cordenada2)            
            coordenadas_ruta.append(coordenada)

    return coordenadas_ruta


def leer_todas_las_rutas_en_carpeta(carpeta_kml):
    todas_las_rutas = []

    for archivo_kml in os.listdir(carpeta_kml):
        if archivo_kml.endswith(".kml"):
            ruta_completa = os.path.join(carpeta_kml, archivo_kml)
            coordenadas_ruta = leer_coordenadas_desde_kml(ruta_completa)
            todas_las_rutas.append(coordenadas_ruta)

    return todas_las_rutas


if __name__ == "__main__":

    project_id = args.project_id
    topic_peaton = args.peaton_topic_name
    dataset_id = args.dataset_id
    table_id = args.table_peaton

    n_peatones = int(args.n_peatones)

    # publicar en bigquery el num de peatones a usar
    #write_peaton_to_bigquery(project_id, dataset_id, table_id, n_peatones)
    id_peaton = id_peaton_generator(n_peatones)

    while(True):

        # HAY QUE VALIDAR QUE EL peaton NO ESTA EN RUTA (LUEGO)
        peaton_elegido = random.choice(id_peaton)

        ruta_rutas = "./ruta/ruta_peaton"
        archivos_rutas = os.listdir(ruta_rutas)
        archivos_rutas = [archivo for archivo in archivos_rutas if archivo.endswith(".kml")]


        ruta_aleatoria = random.choice(archivos_rutas)
        ruta_completa = os.path.join(ruta_rutas, ruta_aleatoria)

        coordenadas_ruta = leer_coordenadas_desde_kml(ruta_completa)
        # print de lo que publicamos en el topic
        logging.getLogger().setLevel(logging.INFO)

        peaton = read_peaton_from_bigquery(project_id, dataset_id, table_id, peaton_elegido)
        cartera = peaton.get('Cartera')

        #leemos de big query el peatones con sus datos
        publicar_movimiento(coordenadas_ruta, project_id, topic_peaton, peaton_elegido, cartera)
