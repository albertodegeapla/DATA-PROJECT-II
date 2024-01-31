import logging
import apache_beam as beam
from apache_beam.runners.interactive.interactive_runner import InteractiveRunner
import apache_beam.runners.interactive.interactive_beam as ib
import json

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms import window


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

def run_local():
    options = PipelineOptions(streaming=True)
    with beam.Pipeline(options=options) as p:
        p_peaton = (p
                        | "ReadFromPubSubPeaton" >> beam.io.ReadFromPubSub(subscription='projects/genuine-essence-411713/subscriptions/ruta_persona-sub')
                        | "DecodeMessagePeaton" >> beam.Map(decode_message)
                        | "addTuplePeaton" >> beam.Map(lambda x: ("peaton", x))
                        | "WindowIntoPeaton" >> beam.WindowInto(beam.window.FixedWindows(10)) 
                    )
        p_coche =   (p 
                        | "ReadFromPubSubCoche" >> beam.io.ReadFromPubSub(subscription='projects/genuine-essence-411713/subscriptions/ruta_coche-sub')
                        | "DecodeMessageCoche" >> beam.Map(decode_message)
                        | "addTupleCoche" >> beam.Map(lambda x: ("coche", x))
                        | "WindowIntoCoche" >> beam.WindowInto(beam.window.FixedWindows(10)) 
                    )
        
        data = ((p_peaton, p_coche)
                        | "groupByKey" >> beam.CoGroupByKey()
                        | "print" >> beam.Map(print))
        
'''
class PlazaState(beam.DoFn):
    def process(self, element, state=beam.DoFn.StateParam(beam.DoFn.StateSpec("plazas", beam.BagCombineFn(sum)))):
        coche = element['coche']
        coche_id = coche['ID_coche']

        # Recupera el estado actual de las plazas para el coche
        current_plazas = list(state.read()[coche_id]) if state.contains_key(coche_id) else 0

        # Resta una plaza al coche
        coche['Plazas'] -= 1
        current_plazas = coche['Plazas']

        # Actualiza el estado de las plazas
        state.write({coche_id: current_plazas})

        yield coche


def change_plazas():
    options = PipelineOptions(streaming=True)
    with beam.Pipeline(options=options) as p:
        (p  | "ReadFromPubSubCoche" >> beam.io.ReadFromPubSub(subscription='projects/genuine-essence-411713/subscriptions/ruta_coche-sub')
            | "DecodeMessageCoche" >> beam.Map(decode_message)
            | "windowInto1sec" >> beam.WindowInto(window.FixedWindows(1)) 
            | "plazaState" >> beam.ParDo(PlazaState())
           
        )

'''
'''                     | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                            table='genuine-essence-411713:blablacar2.ruta_coche',
                            schema='{"ID_coche":"STRING", "Marca":"STRING", "Matricula":"STRING", "Plazas":"INTEGER","Precio":"FLOAT","hora_salida":"STRING", "ruta_coche":"STRING"}',
                            create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
                        )

                        | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                            table='genuine-essence-411713:blablacar2.ruta_persona',
                            schema='{"ID_persona":"STRING", "Nombre":"STRING", "Cartera":"FLOAT","hora_salida":"STRING", "ruta_perosna":"STRING"}',
                            create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
                        )                     
'''
        
    
'''def run_GCP():
    with beam.Pipeline(options=PipelineOptions(
        streaming=True,
        # save_main_session=True
        project=project_id,
        runner="DataflowRunner",
        temp_location=f"gs://{bucket_name}/tmp",
        staging_location=f"gs://{bucket_name}/staging",
        region="europe-west1"
    )) as p:
        (p 
            | "ReadFromPubSub" >> beam.io.ReadFromPubSub(subscription='projects/genuine-essence-411713/subscriptions/ruta_persona-sub')
            | "DecodeMessage" >> beam.Map(decode_message)
            | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                table='genuine-essence-411713:blablacar2.ruta_persona',
                schema = '{"ID_persona":"STRING", "Nombre":"STRING", "Cartera":"FLOAT","hora_salida":"STRING", "ruta_perosna":"STRING"}',
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )  '''


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    logging.info("The process started")
    
    run_local()
