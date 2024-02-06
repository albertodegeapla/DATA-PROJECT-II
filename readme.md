DATA PROJECT 2

DESCRIPCIÓN

La empresa Bla Ba Car, está decidida a revolucionar la forma en que nos movemos en distancias cortas. Han decidido dar el salto hacia la reserva en tiempo real de desplazamientos dentro de las ciudades. ¿Qué significa esto? Significa que podrías reservar un viaje dentro de tu ciudad justo cuando lo necesites, sin esperar mucho tiempo o depender de un horario fijo.

Y adivina qué ciudad ha elegido Bla Ba Car como su pionera en esta audaz iniciativa: ¡Valencia! Sí, la vibrante y hermosa ciudad de Valencia se convertirá en el campo de pruebas para esta nueva forma de moverse en la urbe.

Pero, ¿por qué Valencia? ¿Qué tiene de especial esta ciudad que la hace perfecta para este piloto? Bueno, para empezar, Valencia es un centro de actividad constante. Con sus calles llenas de vida, sus puntos de interés turístico y sus habitantes siempre en movimiento, Valencia ofrece el escenario ideal para probar la efectividad de este sistema de reserva en tiempo real.

Además, Valencia cuenta con una infraestructura vial diversa y bien desarrollada, lo que facilita la navegación y la logística del transporte urbano. Desde sus amplias avenidas hasta sus estrechas callejuelas llenas de encanto, Valencia desafía a Bla Ba Car a demostrar que su sistema puede adaptarse a cualquier entorno urbano.

Así que prepárate, Valencia, porque el futuro del transporte en la ciudad está a punto de cambiar. Con Bla Ba Car liderando el camino, pronto podrías estar reservando tus viajes dentro de la ciudad con solo unos pocos clics en tu teléfono. Es un salto emocionante hacia adelante, y Valencia está a la vanguardia de esta revolución en movimiento urbano


Equipo

Pablo Pérez Álvarez: Licenciado en ----. Parte del equipo de Data Engineering del proyecto. Desarrollo de código Python para Dataflow. 

José Aguilar Van Der Hofstadt: -----. Encargado de la parte de Data Engineering relativa a la cola de mensajes en Pub/Sub, diseño de arquitectura y desarrollo de código para el Dataflow.

Lucía Esteve Domínguez: Licenciada en Administración y direcció de empresas. Desarrollo de código para la generación de los datos del proyecto. Diseño de la arquitectura, y Bussines Inteligence.

Ándrés Cervera Beneyto:----------.Encargado de la parte del desarrollo de la creación de la interfaz de usuario para visualizar el  modelo utilizando Streamlit y apoyo en la parte de desarrollo de código para Dataflow.

Álberto De Gea Pla: ------. Desarrollo de código para la generación de los datos del proyecto. Encargado del análisis y visualización de los datos y resultados del negocio. 


En este repositorio, se encuentra la solución en Google Cloud que hemos diseñado. Consta de las siguientes partes:

Generador de datos con envío a Pub/Sub

Dataflow para transformación de los mensajes

BigQuery como almacenamiento

Streamlit para visualización de la interfaz 

Tableau para el análisis y visualización de los datos del negocio


Diseño de Arquitectura

--> AÑADIR IMAGÉN QUE TENGO QUE CREAR DE LA ARQUITECTURA

Generador de datos (PUB/SUB)



Para ejecutar el codigo del generador correctamente hay que realizar los siguientes pasos:

Construir la imagen Docker de solar_gen. Para ello hay un script en la carpeta solar_panel que se llama init.sh

Una vez construida la imagen, se puede ejecutar el siguiente código Python para enviar la info a Pub/Sub

python3 main.py --topcontainers <num_paneles> \
    --elapsedtime <t_delay> \
    --image solar_gen \
    --project_id <GCP project ID> \
    --topic_name <GCP pub/sub topic>

DATAFLOW

Dentro de la carpeta de dataflow, se encuentra el código Python escrito utilizando la librería Apache BEAM para consumir los datos generador por los paneles solares mediante una subscripción al tópico de Pub/Sub. En Dataflow se realizan los siguientes pasos:

Primero se leen los mensajes escritos en formato JSON que se encuentran en el tópico, creando una PColletion con el contenido de los mensajes

Los datos recibidos se guardan en una tabla de BigQuery que tiene el siguiente schema:

{
    "fields": [
    {
      "mode": "NULLABLE",
      "name": "Panel_id",
      "type": "STRING"
    },
    {
      "mode": "NULLABLE",
      "name": "power_panel",
      "type": "FLOAT64"
    },
    {
      "mode": "NULLABLE",
      "name": "current_status",
      "type": "INT64"
    },
    {
      "mode": "NULLABLE",
      "name": "current_time",
      "type": "TIMESTAMP"
    }
    ]
}
Mediante el uso de una ventana, se obtiene la potencia total instantánea generada por los paneles, y se escribe en un tópico de Pub/Sub para utilizar luego en las Cloud Functions como disparador de una aviso.

Se calcula otra ventana para sacar en franjas de 30 segundos la potencia media generada por los paneles, y se escribe el resultado de la PCollection en otra tabla de BigQuery

Para ejecutar este código se puede hacer de 2 formas:

Ejecutando el siguiente comando desde la terminal:

python3 dataflow.py \
    --project_id <project_id> \
    --input_subscription <topic_name>-sub \
    --output_bigquery <dataset_bigquery>.Panel_Data \
    --runner DataflowRunner \
    --job_name dataflow-solar \
    --region <GCP region> \
    --temp_location gs://<bucket(project_id)>/tmp \
    --staging_location gs://<bucket(project_id)/stg
A partir de GitHub actions usando el archivo de Terraform main.tf que se encuentra también en esta carpeta.

Para este segundo caso, primero se tiene que construir la Flex-Template, que será almacenada en el Bucket storage de Google Cloud. Esto se consigue ejecutando los siguientes comandos:

gcloud builds submit --tag 'gcr.io/<Bucket ID>/dataflow/data-project2:latest' .

gcloud dataflow flex-template \
         build "gs://<Bucket ID>/data-project2-flowtemplate.json" \
        --image 'gcr.io/<Bucket ID>/dataflow/data-project2:latest' \
        --sdk-language "PYTHON"
Una vez que se ha construido la Flex Template dentro del proyecto de Google Cloud, se tiene que subir el repositorio a GitHub. Dentro de la carpeta .github/workflows existen dos archivos yaml, que sirven para ejecutar las GitHub actions de despliegue y parada de Dataflow. La siguiente imagen muestra una captura de pantalla de como se realiza el despliegue:

STREAMLIT


TABLEAU

En la parte de visualización, se ha creado un dashboard para análizar los resultados que se muestra ...... 
















## DESCRIPCIÓN DEL PROYECTO

## EJECUCIÓN DEL PROYECTO

1. Clona el repositorio: 
   
   ```bash
   git clone 
   
2. Ejecuta los siguientes comandos para levantar todos los contenedores, asignar volúmenes y puertos:
   
   ```bash
   docker-compose up -d

Si deseas ver cómo funciona el código puedes consultar el siguiente vídeo:

---





