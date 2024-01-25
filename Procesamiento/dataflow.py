import logging
import apache_beam as beam
from apache_beam.runners.interactive.interactive_runner import InteractiveRunner
import apache_beam.runners.interactive.interactive_beam as ib
import json

from apache_beam.options.pipeline_options import PipelineOptions


#### IMPORTANTE
# Este escript escucha un topic de GCloud y lo publica en BigQuery
# Para ello, habrá un generador de archivos que vaya publicando mensajes en GCloud en dos topics diferentes
# Aqui escuchamos los topics de gcloud y para publicarlos en BigQuery hay que crear previamente una tabla alli
# antes de correr este script hay que crear el topic en GCloud

# chquea los nombres de los topics, proyecto, tabla etc y ajustalos a los tuyos personales

# decodificador del JSON 
def decode_message(message):
   if message is not None:
        try:
            output = message.decode('utf-8')
            return json.loads(output) 
        except Exception as e:
            print(f"Error decoding message: {e}")
            return None

with beam.Pipeline(options=PipelineOptions(streaming=True)) as p:
    data = (p 
            | "ReadFromPubSub" >> beam.io.ReadFromPubSub(subscription='projects/genuine-essence-411713/subscriptions/ruta_persona-sub')
            | "DecodeMessage" >> beam.Map(decode_message)
            | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                table='genuine-essence-411713:blablacar2.ruta_persona',
                schema = '{"ID_persona":"STRING", "Nombre":"STRING", "Cartera":"FLOAT","hora_salida":"STRING", "ruta_perosna":"STRING"}',
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
    )    

