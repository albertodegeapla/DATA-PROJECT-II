import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms import Map
from haversine import haversine, Unit

import argparse
import json
import logging

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

class ProcessData(beam.DoFn):
    def process(self, element):
        datos_coche, datos_pasajero = element
        # El mood, que tendremos en cuenta a la hora de recoger, lo hardcodeamos
        distancia_rangos = {'antipatico': 50000, 'normal': 75000, 'majo': 100000}

        # Calcular la distancia entre el coche y el pasajero, usando la librería Haversine
        distancia = haversine((datos_coche['coordenadas'][1][0], datos_coche['coordenadas'][1][1]),
                             (datos_pasajero['coordenadas'][1][0], datos_pasajero['coordenadas'][1][1]),
                             unit=Unit.METERS)

        # Check si la distancia en metros esta dentro del rango del mood
        for mood, rango in distancia_rangos.items():
            if distancia <= rango:
                # Check distancia entre destinos
                destinos_distancia = haversine((datos_coche['punto_destino'][0], datos_coche['punto_destino'][1]),
                                          (datos_pasajero['punto_destino'][0], datos_pasajero['punto_destino'][1]),
                                          unit=Unit.METERS)

                # Check destinos_distancia menor a 500 metros (podemos cambiarlo)
                if destinos_distancia <= 500:
                    # Check dinero en la wallet
                    if datos_pasajero['cartera'] >= datos_coche['precio']:
                        # Recoger al pasajero y pasajero paga
                        datos_pasajero['cartera'] -= datos_coche['precio']
                        datos_coche['plazas'] -= 1
                        # El dinero del pasajero se suma a la cartera del conductor
                        datos_coche['cartera'] += datos_coche['precio'] / 1.25

                        picked_up = {'coche': datos_coche, 'pasajero': datos_pasajero}
                        print(picked_up)
                        yield picked_up
                        

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
                         | "WindowIntoCar" >> beam.WindowInto(beam.window.FixedWindows(2)) 
                         | "print car" >> beam.Map(print)
        )
        datos_pasajero = (p | "Read Passenger Data" >> beam.io.ReadFromPubSub(subscription=f'projects/{project_id}/subscriptions/{topic_person}') 
                            | "decode person message" >> beam.Map(lambda x: json.loads(x)) 
                            | "WindowIntoPeaton" >> beam.WindowInto(beam.window.FixedWindows(2)) 
                            | "print person" >> beam.Map(print)
        )

        #   Part 02: Get the aggregated data of the vehicle within the section.

        datos_coche_procesados = (

            datos_coche 
                | "Process car Data" >> beam.ParDo(ProcessData())
                #| "Encode cars to Bytes" >> beam.Map(lambda x: json.dumps(x).encode("utf-8"))
                | "Write to BigQuery Car" >> beam.io.WriteToBigQuery(
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                        table=f"{project_id}:{dataset_id}.{table_car}",
                        schema="id_coche:INTEGER,coordenadas:RECORD,punto_destino:RECORD,plazas:INTEGER,precio:FLOAT,cartera:FLOAT",
                        rows=lambda x: x['coche']
                    )
        )

        datos_pasajero_procesados = (

            datos_pasajero 
                | "Process passenger Data" >> beam.ParDo(ProcessData())
                #| "Encode pasajeros to Bytes" >> beam.Map(lambda x: json.dumps(x).encode("utf-8"))
                | "Write to BigQuery Passenger" >> beam.io.WriteToBigQuery(
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                        table=f"{project_id}:{dataset_id}.{table_person}",
                        schema="id_persona:INTEGER,coordenadas:RECORD,punto_destino:RECORD,cartera:FLOAT,mood:STRING",
                        rows=lambda x: x['pasajero']
                    )
        )





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