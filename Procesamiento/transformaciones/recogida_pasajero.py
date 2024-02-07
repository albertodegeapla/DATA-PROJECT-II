import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms import Map
from haversine import haversine, Unit

import argparse
import json
import logging
from google.cloud import bigquery

# Este script escucha de dos topics a la vez, coches y pasajeros, y dependiendo de ciertas reglas
# ...como son la distancia entre coordenadas, entre destinos, rango de alcance y precio, decidimos
# ...si el coche recoge o no al pasajero. Una vez hecho, actualiza en la base de datos.


# añadimos flags para que funcione
# añadirimaos el porject ID, los subscribers y el bucket


# ejemplo de correrlo python .\recogida_pasajero.py --project_id genuine-essence-411713 --person_topic_sub ruta_persona-sub --car_topic_sub ruta_coche-sub --dataset_id blablacar2 --car_table coches --person_table perosnas

parser = argparse.ArgumentParser(description=("Procesamiento de los topics de GCloud SUBSCRIBER"))
parser.add_argument(
    "--project_id",
    required=True,
    help="Project ID de GCloud"
)
parser.add_argument(
    "--person_topic_sub",
    required=True,
    help="Topic del subscriber GCloud de la persona"
)
parser.add_argument(
    "--car_topic_sub",
    required=True,
    help="Topic del subscriber GCloud del coche"
)
parser.add_argument(
    "--dataset_id",
    required=True,
    help="Dataset de GCloud"
)
parser.add_argument(
    "--car_table",
    required=True,
    help="Tabla de coches en GCloud"
)
parser.add_argument(
    "--person_table",
    required=True,
    help="Tabla de pasajeros en GCloud"
)
'''parser.add_argument(
    "--bucket_name",
    required=True,
    help="Bucket de GCloud"
)'''

args, opts = parser.parse_known_args()

pasajeros_en_coche = []

def car_select(coche):
    client = bigquery.Client()

    query = f"SELECT Cartera, N_viajes, N_pasajeros FROM `{args.project_id}.{args.dataset_id}.{args.car_table}` WHERE ID_coche = {coche['id_coche']}"
    result = client.query(query).result()
    
    # Assuming there is only one row in the result
    for row in result:
        return row.Cartera, row.N_viajes, row.N_pasajeros if hasattr(row, 'Cartera') else (0, 0, 0)

    return 0, 0, 0

def car_update_bigquery(coche):
    client = bigquery.Client()

    coche['plazas'] = int(coche['plazas']) - 1
    coche['id_coche'] = int(coche['id_coche'])

    cartera_value, n_viajes, n_pasajeros = car_select(coche)
    ganancia_pasajero = cartera_value + coche['precio'] / 1.25
    n_pasajeros = n_pasajeros + 1
   
    query = f"UPDATE `{args.project_id}.{args.dataset_id}.{args.car_table}` SET Plazas = {coche['plazas']}, Cartera = {ganancia_pasajero}, N_pasajeros = {n_pasajeros} WHERE ID_coche = {coche['id_coche']}"
    client.query(query).result()

def person_select(persona):
    client = bigquery.Client()

    query = f"SELECT Cartera, N_viajes FROM `{args.project_id}.{args.dataset_id}.{args.person_table}` WHERE ID_persona = {persona['id_persona']}"
    result = client.query(query).result()

    for row in result:
        cartera_value = row.Cartera if hasattr(row, 'Cartera') else 0
        n_viajes_value = row.N_viajes if hasattr(row, 'N_viajes') else 0
        return cartera_value, n_viajes_value

    return 0, 0

def person_update_bigquery(persona, coche):
    client = bigquery.Client()

    cartera_value, n_viajes_value = person_select(persona)

    persona['cartera'] = cartera_value - int(coche['precio'])
    n_viajes = n_viajes_value + 1
    persona['id_persona'] = int(persona['id_persona'])

    query = f"UPDATE `{args.project_id}.{args.dataset_id}.{args.person_table}` SET Cartera = {persona['cartera']}, N_viajes = {n_viajes}, En_ruta = {True} WHERE ID_persona = {persona['id_persona']}"
    client.query(query).result()


def person_update_en_ruta(id):
    client = bigquery.Client()
    query = f"UPDATE `{args.project_id}.{args.dataset_id}.{args.person_table}` SET En_ruta = {False} WHERE ID_persona = {id}"
    client.query(query).result()

def car_update_n_viajes(coche):
    client = bigquery.Client()
    cartera_value, n_viajes, n_pasajeros = car_select(coche)
    viajes = n_viajes + 1
    query = f"UPDATE `{args.project_id}.{args.dataset_id}.{args.car_table}` SET N_viajes = {viajes}, Plazas = 4 WHERE ID_coche = {coche['id_coche']}"
    client.query(query).result()

class ProcessData(beam.DoFn):
    def process(self, element):
        #logging.info(element)
        hora, datos = element
        coches = [dato for dato in datos if 'id_coche' in dato]
        personas = [dato for dato in datos if 'id_persona' in dato]
        
        for coche in coches:
            if coche['coordenadas'][1] == coche['punto_destino']:
                logging.info(f'El coche {coche["id_coche"]} ha llegado a su destino')
                car_update_n_viajes(coche)
                pasajeros_en_coche_copy = list(pasajeros_en_coche)
                for viaje in pasajeros_en_coche_copy:
                    if coche['id_coche'] == viaje[0]:
                        logging.info(f'La persona {viaje[1]} se ha bajado del coche {coche["id_coche"]}')
                        person_update_en_ruta(viaje[1])
                        pasajeros_en_coche.remove(viaje)
        
        # si no hay coches o personas, no hacemos nada
        if len(coches) == 0 or len(personas) == 0:
            return None

        try:
            for coche in coches:
                id_coche = coche['id_coche']
                for pasajero in personas:
                    id_pasajero = pasajero['id_persona']

                    #Comprueba que el pasajero no este en un coche
                    try:
                        if any(id_pasajero == viaje[1] for viaje in pasajeros_en_coche):
                            print(f'El pasajero {id_pasajero} ya se encuentra en un coche.')
                            return None
                    except Exception as e:
                        logging.error(f"Error CR7: {e}")

                    # Calcula la distancia entre los puntos
                    distancia_recogida = haversine((coche['coordenadas'][1][0], coche['coordenadas'][1][1]),
                                    (pasajero['coordenadas'][1][0], pasajero['coordenadas'][1][1]),
                                    unit=Unit.METERS)
                    #print(distancia_recogida)
                    # selecciona la distancia a la que el pasajero está dispuesto a desplazarse segun su mood
                    distancia_maxima = 0
                    if pasajero['mood'] == 'Antipatico':
                        distancia_maxima = 5000
                    elif pasajero['mood'] == 'Normal':
                        distancia_maxima = 10000
                    elif pasajero['mood'] == 'Majo':
                        distancia_maxima = 15000
                    # si la posicion actual esta a x distancia entraga a recoger
                    if distancia_recogida <= distancia_maxima:
                        # calcula la distancia entre los destinos
                        destinos_distancia = haversine((coche['punto_destino'][0], coche['punto_destino'][1]),
                                              (pasajero['punto_destino'][0], pasajero['punto_destino'][1]),
                                              unit=Unit.METERS)
                        # si la distancia del putno de destino a x distancia entraga a recoger
                        if destinos_distancia <= distancia_maxima:
                            # si no hay plazas en el coche no hacemos nada
                            if coche['plazas'] <= 0:
                                logging.info(f'El coche {coche["id_coche"]} ya no tiene plazas!!')
                                return None
                            # Check dinero en la wallet
                            if pasajero['cartera'] < coche['precio']:
                                logging.info(f'El pasajero {pasajero["id_persona"]} no tiene suficiente cartera!!')
                                return None
                            # Si hay plazas y dinero hay match!!
                            logging.info(f'¡MATCH! El coche {coche["id_coche"]} ha recogido al pasajero {pasajero["id_persona"]}')

                            ####### MIRAR CHECKEO DE PASAJEROS EN COCHE ################
                            #print(pasajeros_en_coche)
                            car_update_bigquery(coche)
                            person_update_bigquery(pasajero, coche)
                            pasajeros_en_coche.append((id_coche, id_pasajero))
                            
                            

        except Exception as e:
            logging.error(f"Error procesando datos: {e}")

                        
def add_key(element):
    key = element['coordenadas'][0]
    return key, element

def run_local():
    # Este es el Set up para correrlo en local, abajo esta el set up para la nube
    # que primero funcione aqui y depsues lo lanzamos a la nube 
    pipeline_options = PipelineOptions(streaming=True) 

    project_id = args.project_id
    dataset_id = args.dataset_id

    topic_person = args.person_topic_sub
    table_person = args.person_table
    topic_car = args.car_topic_sub
    table_car = args.car_table

    # Leemos de las pipelines de coche y pasajero 
    # ya esta la config

    with beam.Pipeline(options=pipeline_options) as p:
        datos_coche = (p | "Read Car Data" >> beam.io.ReadFromPubSub(subscription=f'projects/{project_id}/subscriptions/{topic_car}') 
                     | "decode car message" >> beam.Map(lambda x: json.loads(x)) 
                     | "addKeyCar" >> beam.Map(add_key)
                     | "WindowIntoCar" >> beam.WindowInto(beam.window.FixedWindows(2)) 
        )
        datos_pasajero = (p | "Read Passenger Data" >> beam.io.ReadFromPubSub(subscription=f'projects/{project_id}/subscriptions/{topic_person}') 
                        | "decode person message" >> beam.Map(lambda x: json.loads(x)) 
                        | "addKeyPassenger" >> beam.Map(add_key)
                        | "WindowIntoPeaton" >> beam.WindowInto(beam.window.FixedWindows(2)) 
        )
        data = ((datos_coche, datos_pasajero)
            | "Flatten" >> beam.Flatten()
            | "groupByKey" >> beam.GroupByKey()
            | "processData" >> beam.ParDo(ProcessData())
        )
        
if __name__ == "__main__":

    logging.getLogger().setLevel(logging.INFO)
    logging.info("The process started")

    run_local()





'''def run_GCP():
    with beam.Pipeline(options=PipelineOptions(
        streaming=True,
        # save_main_session=True
        project=project_id,
        runner="DataflowRunner",
        temp_location=f"gs://{bucket_name}/tmp",
        staging_location=f"gs://{bucket_name}/staging",
        region="europe-west1"
    )) '''