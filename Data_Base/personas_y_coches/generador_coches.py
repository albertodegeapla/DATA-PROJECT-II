import random
from datetime import datetime, timedelta
import xml. etree.ElementTree as ET
import os
import time

### librerias para el publisher
from google.cloud import pubsub_v1
import argparse
import json
import logging

### librerias para el bigQuery
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.runners.interactive.interactive_runner import InteractiveRunner
import apache_beam.runners.interactive.interactive_beam as ib
from apache_beam.transforms import window
import apache_beam as beam
from google.cloud import bigquery

# Flags para llamar al arcvhivo desde el terminal
# Para llamar a este codiog de python hay que llamarlo desde el terminal así : 
# python .\generador_coches.py --project_id <TU_PROYECT_ID> --car_topic_name <NOMBRE_DEL_TOPIC_COCHE>
# python .\generador_coches.py --project_id genuine-essence-411713 --car_topic_name ruta_coche --dataset_id blablacar2 --table_car coches --n_coches 10
# RECOMENDACIÓN, llamad todos al topic con el mismo nombre ejemplo: (ruta_coche).

parser = argparse.ArgumentParser(description=("Generador de Rutas de coche y publicadas en pub/sub"))
parser.add_argument(
    "--project_id",
    required=True,
    help="Project ID de GCloud"
)
parser.add_argument(
    "--car_topic_name",
    required=True,
    help="Topic de GCloud del coche"
)
parser.add_argument(
    "--dataset_id",
    required=True,
    help="Dataset de GCloud"
)
parser.add_argument(
    "--table_car",
    required=True,
    help="Table de coches GCloud"
)
parser.add_argument(
    "--n_coches",
    required=True,
    help="Numero de coches a generar"
)

args, opts = parser.parse_known_args()


# Clase para publicar en el topic
class PubSubCarMessage:

    def __init__(self, project_id, topic_car):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = project_id
        self.topic_name = topic_car

    def publishCarMessage(self, message):
        json_str = json.dumps(message)
        topic_path = self.publisher.topic_path(self.project_id, self.topic_name)
        publish_future = self.publisher.publish(topic_path, json_str.encode("utf-8"))
        publish_future.result()
        logging.info(f"El coche {message['id_coche']}, va a esta hora y en estas coordenadas: {message['coordenadas']}, a {message['punto_destino']} con {message['plazas']} plazas y cuesta {message['precio']} €")

    def __exit__(self):
        self.publisher.transport.close()
        logging.info("Cerrando car Publisher") 


# Funciones
def generar_id_coche(id):
    return id

def cargar_txt(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def generar_marca():
    marca = cargar_txt('./marcas_coche.txt')
    return random.choice(marca)

def generar_matricula():
    numeros = random.randint(0000, 9999)
    letra1 = random.choice('ABCDEFGHIJKLM')
    letra2 = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    letra3 = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return f"{numeros}{letra1+letra2+letra3}"

def generar_edad_coche():
    return random.randint(0, 25)

def generar_plazas():
    return 4

def generar_kilometraje():
    return random.randint(1000, 200000)

def generar_precio_compra():
    return random.randint(10000, 80000)


#### en base a los km y el precio de compra y edad del coche generar un dato de 0,005 a 0,05 max y un min
#def generar_cobro_km(kilometraje, precio_compra):
    #descuento_por_kilometraje = 0.05  # Descuento del 5% por cada 10000km
    #descuento = (kilometraje // 10000) * descuento_por_kilometraje
    #precio_final = precio_compra - descuento

    #return max(precio_final, 0)

def generar_precio_inicial():
    return random.uniform(0.5, 1.5)

def generar_coche(id):
    id_coche = generar_id_coche(id)
    marca = generar_marca()
    matricula = generar_matricula()
    plazas = generar_plazas()
    kilometraje = generar_kilometraje()
    precio_compra = generar_precio_compra()
    precio_x_punto = generar_precio_inicial()
    

    coche = {
        'ID_coche':id_coche,
        'Marca':marca,
        'Matricula':matricula,
        'Plazas':plazas,
        'Precio_punto':precio_x_punto,
        'Cartera': 0.0
    }
    
    return coche

# crea un array con los id de los coches
def id_car_generator(n_coches):
    array_id = [(i + 1) for i in range(n_coches)]
    return array_id

# Escribe en bigQuerry los coches que se van a usar  
def write_car_to_bigquery(project_id, dataset_id, table_id, n_coches):
    options = PipelineOptions(streaming=True)
    with beam.Pipeline(options=options) as p:
        #crea los coches a usar
        coches = [generar_coche(i+1) for i in range(n_coches)]

        # Crear un PCollection con los coches
        coches_pcollection = p | beam.Create(coches)
 
        coches_pcollection | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                table=f'{project_id}:{dataset_id}.{table_id}',
                schema = '{"ID_coche":"INTEGER", "Marca":"STRING", "Matricula":"STRING", "Plazas":"INTEGER","Precio_punto":"FLOAT", "Cartera":"FLOAT"}',
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
          
def read_car_from_bigquery(project_id, dataset_id, table_id, car_id):
    client = bigquery.Client(project=project_id)

    # Construye la consulta SQL para obtener el coche por ID
    query = f"""
        SELECT *
        FROM `{project_id}.{dataset_id}.{table_id}`
        WHERE ID_coche = {car_id}
    """
    query_job = client.query(query)

    # Devuelve el resultado como un iterows
    results = query_job.result()

    for row in results:
        coche = dict(row.items())   # Convierte el row en un diccionario
        return coche

    return None

def convertir_a_json(id_coche, coordenadas, punto_destino, plazas, precio):
    # Construye un diccionario con la información
    datos_coche = {
        "id_coche": id_coche,
        "coordenadas": coordenadas,
        "punto_destino": punto_destino,
        "plazas": plazas,
        "precio": precio
    }
    return datos_coche


def generar_fecha_hora():
    fecha_hora = datetime.now()
    fecha_hora_str = fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
    return fecha_hora_str


# introducir el id de coche que toque por parametro
def publicar_movimiento(coordenadas, project_id, topic_car, dataset_id, table_id, id_coche):
    hora_str = generar_fecha_hora()

    longitud_ruta = len(coordenadas)
    #punto_inicial = coordenadas_ruta[0]
    punto_destino = coordenadas[longitud_ruta-1]
    precio =  generar_precio_inicial()

    for i in range(len(coordenadas)-1):
        
        coche = read_car_from_bigquery(project_id, dataset_id, table_id, id_coche)
        plazas = coche.get('Plazas')
        precio_x_coord = coche.get('Precio_punto')
        coord_restantes = longitud_ruta - i - 1
        precio = round(precio_x_coord * coord_restantes,2)

        coord_actual = coordenadas[i]
        coord_siguiente = coordenadas[i + 1]

        velocidad = 2
        tiempo_inicio = time.time()       

        while time.time() - tiempo_inicio < velocidad:
            hora_actual = datetime.strptime(hora_str, "%d/%m/%Y %H:%M:%S") + timedelta(seconds=i * 2)
            punto_mapa = (hora_actual.strftime("%Y-%m-%d %H:%M:%S"), coord_siguiente, precio)
            precio_subida = round(random.uniform(0.01, 0.1), 2)
            precio += precio_subida
            
            try:
                car_publisher = PubSubCarMessage(project_id, topic_car)
                message: dict = convertir_a_json(id_coche, punto_mapa, punto_destino, plazas, precio)
                car_publisher.publishCarMessage(message)
                
            except Exception as e:
                logging.error("Error while inserting data into ruta_coche Topic: %s", e)
            finally:
                car_publisher.__exit__()
            
            time.sleep(5)
      

def leer_coordenadas_desde_kml(file_path):
    coordenadas_ruta = []
    tree = ET.parse(file_path)
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
    topic_car = args.car_topic_name
    dataset_id = args.dataset_id
    table_id = args.table_car

    n_coches = int(args.n_coches)

    # publicar en bigquery el num de coches a usar
    #write_car_to_bigquery(project_id, dataset_id, table_id, n_coches)
    id_coches = id_car_generator(n_coches)
     
    while(True):

        # HAY QUE VALIDAR QUE EL COCHE NO ESTA EN RUTA (LUEGO)
        coche_elegido = random.choice(id_coches)        


        ruta_rutas = "./ruta/ruta_coche"
        archivos_rutas = os.listdir(ruta_rutas)
        archivos_rutas = [archivo for archivo in archivos_rutas if archivo.endswith(".kml")]


        ruta_aleatoria = random.choice(archivos_rutas)
        ruta_completa = os.path.join(ruta_rutas, ruta_aleatoria)

        coordenadas_ruta = leer_coordenadas_desde_kml(ruta_completa)
        
        # print de lo que publicamos en el topic
        logging.getLogger().setLevel(logging.INFO)

        #leemos de big query el coche con sus datos
        # ESTO NO SERIA NECESARIO 
        
        '''coche = read_car_from_bigquery(project_id, dataset_id, table_id, coche_elegido)
        #print(coche)
        plazas = coche.get('Plazas')'''
        project_id = args.project_id
        topic_car = args.car_topic_name

        publicar_movimiento(coordenadas_ruta, project_id, topic_car, dataset_id, table_id, coche_elegido)
        # run(args.project_id, args.car_topic_name)

