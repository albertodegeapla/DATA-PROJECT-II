import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms import Map
from haversine import haversine, Unit

# Este script escucha de dos topics a la vez, coches y pasajeros, y dependiendo de ciertas reglas
# ...como son la distancia entre coordenadas, entre destinos, rango de alcance y precio, decidimos
# ...si el coche recoge o no al pasajero. Una vez hecho, actualiza en la base de datos.

class ProcessData(beam.DoFn):
    def process(self, element):
        datos_coche, datos_pasajero = element
        # El mood, que tendremos en cuenta a la hora de recoger, lo hardcodeamos
        distancia_rangos = {'mood_1': 500, 'mood_2': 750, 'mood_3': 1000}

        # Calcular la distancia entre el coche y el pasajero, usando la librería Haversine
        distancia = haversine((datos_coche['coordenadas']['latitud'], datos_coche['coordenadas']['longitud']),
                             (datos_pasajero['coordenadas']['latitud'], datos_pasajero['coordenadas']['longitud']),
                             unit=Unit.METERS)

        # Check si la distancia en metros esta dentro del rango del mood
        for mood, rango in distancia_rangos.items():
            if distancia <= rango:
                # Check distancia entre destinos
                destinos_distancia = haversine((datos_coche['punto_destino']['latitud'], datos_coche['punto_destino']['longitud']),
                                          (datos_pasajero['punto_destino']['latitud'], datos_pasajero['punto_destino']['longitud']),
                                          unit=Unit.METERS)

                # Check destinos_distancia menor a 500 metros (podemos cambiarlo)
                if destinos_distancia <= 500:
                    # Check dinero en la wallet
                    if datos_pasajero['cartera'] >= datos_coche['precio']:
                        # Recoger al pasajero
                        datos_coche['plazas'] -= 1
                        picked_up = {'coche': datos_coche, 'pasajero': datos_pasajero}
                        yield picked_up

                        # Write en BigQuery (cambiar con código de BigQuery)
                        yield picked_up

def run():
    # Set up PipelineOptions / To be defined por Pepe
    pipeline_options = PipelineOptions() # To be defined por Pepe

    # Leemos de las pipelines de coche y pasajero (to be defined por Pepe)
    with beam.Pipeline(options=pipeline_options) as p:
        datos_coche = p | "Read Car Data" >> beam.io.ReadFromPubSub(subscription="coche_sub") | beam.Map(lambda x: json.loads(x))
        datos_pasajero = p | "Read Passenger Data" >> beam.io.ReadFromPubSub(subscription="pasajero_sub") | beam.Map(lambda x: json.loads(x))

        # Join datos de coche y pasajero por key comun, en este caso tiempo
        joined_data = ({'coche': datos_coche, 'pasajero': datos_pasajero}
                       | "Join Data" >> beam.CoGroupByKey()
                       | Map(lambda x: x[1])
                       | "Process Data" >> beam.ParDo(ProcessData()))
        
        for data in joined_data:
            # Reemplazar por los datos de BigQuery de Pepe
            data | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                table="your_project_id.your_dataset_id.your_table_id",
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )

if __name__ == "__main__":
    run()