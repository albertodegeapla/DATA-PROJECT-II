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

def car_update_bigquery(coche):
    client = bigquery.Client()

    coche['plazas'] = int(coche['plazas']) - 1
    coche['id_coche'] = int(coche['id_coche'])
    ganancia_pasajero = coche['cartera'] + coche['precio'] / 1.25
    #print(type(row['id_coche']))
   
    query = f"UPDATE `{args.project_id}.{args.dataset_id}.{args.car_table}` SET Plazas = {coche['plazas']}, Cartera = {ganancia_pasajero} WHERE ID_coche = {coche['id_coche']}"
    client.query(query).result()

def person_update_bigquery(persona, coche):
    client = bigquery.Client()

    persona['cartera'] = int(persona['cartera']) - int(coche['precio'])
    persona['id_persona'] = int(persona['id_persona'])

    query = f"UPDATE `{args.project_id}.{args.dataset_id}.{args.car_table}` SET Cartera = {persona['cartera']} WHERE ID_persona = {persona['id_persona']}"
    client.query(query).result()
    #print(type(row['id_coche']))

class ProcessData(beam.DoFn):
    def process(self, element):

        hora, datos = element
        coches = [dato for dato in datos if 'id_coche' in dato]
        personas = [dato for dato in datos if 'id_persona' in dato]

        # si no hay coches o personas, no hacemos nada
        if len(coches) == 0 or len(personas) == 0:
            return None
            
        try:
            for coche in coches:
                for pasajero in personas:
                    # Calcula la distancia entre los puntos
                    distancia_recogida = haversine((coche['coordenadas'][1][0], coche['coordenadas'][1][1]),
                                    (pasajero['coordenadas'][1][0], pasajero['coordenadas'][1][1]),
                                    unit=Unit.METERS)
                    
                    # selecciona la distancia a la que el pasajero está dispuesto a desplazarse segun su mood
                    distancia_maxima = 0
                    if pasajero['mood'] == 'antipatico':
                        distancia_maxima = 250
                    elif pasajero['mood'] == 'normal':
                        distancia_maxima = 600
                    elif pasajero['mood'] == 'majo':
                        distancia_maxima = 1000
                    # si la posicion actual esta a x distancia entraga a recoger
                    if distancia_recogida <= distancia_maxima:
                        # calcula la distancia entre los destinos
                        destinos_distancia = haversine((coche['punto_destino'][0], coche['punto_destino'][1]),
                                              (pasajero['punto_destino'][0], pasajero['punto_destino'][1]),
                                              unit=Unit.METERS)
                        # si la distancia del putno de destino a x distancia entraga a recoger
                        if destinos_distancia <= distancia_maxima:
                            # si no hay plazas en el coche no hacemos nada
                            if coche['plazas'] == 0:
                                logging.info(f'El coche {coche["id_coche"]} ya no tiene plazas!!')
                                return None
                            # Check dinero en la wallet
                            if pasajero['cartera'] < coche['precio']:
                                logging.info(f'El pasajero {pasajero["id_persona"]} no tiene suficiente cartera!!')
                                return None
                            # Si hay plazas y dinero hay match!!
                            logging.info(f'¡MATCH! El coche {coche["id_coche"]} ha recogido al pasajero {pasajero["id_persona"]}')
                            #car_update_bigquery(coche, pasajero)
                            coche['plazas'] -= 1
                            pasajero['cartera'] -= coche['precio']


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
        
        

        #   Part 02: Get the aggregated data of the vehicle within the section.

        '''datos_coche_procesados = (

            data 
                | "Process car Data" >> beam.ParDo(ProcessData())
                #| "Encode cars to Bytes" >> beam.Map(lambda x: json.dumps(x).encode("utf-8"))
                
                )'''
        '''| "Write to BigQuery Car" >> beam.io.WriteToBigQuery(
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                        table=f"{project_id}:{dataset_id}.{table_car}",
                        schema="id_coche:INTEGER,coordenadas:RECORD,punto_destino:RECORD,plazas:INTEGER,precio:FLOAT,cartera:FLOAT",
                        rows=lambda x: x['coche']
                    )'''

        '''datos_pasajero_procesados = (

            datos_pasajero 
                | "Process passenger Data" >> beam.ParDo(ProcessData())
                #| "Encode pasajeros to Bytes" >> beam.Map(lambda x: json.dumps(x).encode("utf-8"))
                
        )'''
        '''| "Write to BigQuery Passenger" >> beam.io.WriteToBigQuery(
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                        table=f"{project_id}:{dataset_id}.{table_person}",
                        schema="id_persona:INTEGER,coordenadas:RECORD,punto_destino:RECORD,cartera:FLOAT,mood:STRING",
                        rows=lambda x: x['pasajero']
                    )'''





        # Join datos de coche y pasajero por key comun, en este caso tiempo
        '''joined_data = ({'coche': datos_coche, 'pasajero': datos_pasajero}
                       | "Join Data" >> beam.CoGroupByKey()
                       | "pabl0" >> beam.Map(lambda x: x[1])
                       | "Process Data" >> beam.ParDo(ProcessData())
                       | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                           table=f"{project_id}:{dataset_id}.{table_car}",
                           write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                           create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
                       ))'''
        
        '''for data in joined_data:
            # Aqui no se que quieres hacer, te hago la conexion a la tabla coches, la conexion a la tabla peatones es la misma
            data | "Write car to BigQuery" >> beam.io.WriteToBigQuery(
                table=f"{project_id}:{dataset_id}.{table_car}",
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER
            )'''

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