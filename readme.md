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


DISEÑO DE LA ARQUITECTURA

--> AÑADIR IMAGÉN QUE TENGO QUE CREAR DE LA ARQUITECTURA

Generador de datos (PUB/SUB)

Se generan datos tanto para peatones como para coches cada uno con sus repectivas rutas. 

Se utiliza Google Cloud para publicar mensajes sobre las rutas planificadas. 

Ambos generadores funcionan igual:  con una función se genera un ejemplo de ruta en forma de diccionario Python, incluyendo detalles diferentes dependiendo de si estamos en el generador de datos para los coches (la marca, la matrícula, el número de plazas, el precio, la hora de salida y una lista de coordenadas de la ruta)o en el generador de datos para personas (ID de la persona, el nombre, la cantidad de dinero en su cartera, la hora de salida y una lista de coordenadas de la ruta)

con la función run se crea una instancia de la clase PubSubCarMessage, se genera un mensaje de ruta utilizando la función gen_ruta_coche, y publica este mensaje utilizando el método publishCarMessage. 

Se crea un cliente de publicador de Pub/Sub y se almacenan el ID del proyecto y el nombre del tema. 

El método publishCarMessage toma un mensaje como entrada, lo convierte a formato JSON, y lo publica en el tema especificado. También registra información sobre el mensaje publicado.

En resumen, este código proporciona una forma de generar y publicar mensajes sobre rutas de coche y de peaton en un tema de Google Cloud Pub/Sub, utilizando argumentos de línea de comandos para especificar el proyecto y el nombre del tema.

"""REVISAR """

Para ejecutar el codigo del generador correctamente hay que realizar los siguientes pasos:

Construir la imagen Docker de ----- Para ello hay un script en la carpeta ..... que se llama 

Una vez construida la imagen, se puede ejecutar el siguiente código Python para enviar la info a Pub/Sub

python3 main.py --topcontainers <num_paneles> \
    --elapsedtime <t_delay> \
    --image solar_gen \
    --project_id <GCP project ID> \
    --topic_name <GCP pub/sub topic>

DATAFLOW

Dentro de la carpeta de dataflow, se encuentra el código Python escrito utilizando la librería Apache BEAM para consumir los datos generados mediante una subscripción al tópico de Pub/Sub. En Dataflow se realizan los siguientes pasos:

Primero se leen los mensajes escritos en formato JSON que se encuentran en el topic, creando una PColletion con el contenido de los mensajes

Los datos recibidos se guardan en una tabla de BigQuery que tiene el siguiente schema:

 [{
  "ID_persona": "1",
  "Nombre": "Rebeca",
  "Primer_apellido": "Durán",
  "Segundo_apellido": "Ibáñez",
  "Edad": "20",
  "Cartera": "88.45",
  "Cartera_inicial": "88.45",
  "Mood": "antipático"
}, {
  "ID_persona": "2",
  "Nombre": "Isaac",
  "Primer_apellido": "Esteban",
  "Segundo_apellido": "Durán",
  "Edad": "67",
  "Cartera": "60.18",
  "Cartera_inicial": "60.18",
  "Mood": "majo"
}, {
  "ID_persona": "3",
  "Nombre": "Leonardo",
  "Primer_apellido": "Gallardo",
  "Segundo_apellido": "Ramírez",
  "Edad": "24",
  "Cartera": "59.15",
  "Cartera_inicial": "59.15",
  "Mood": "antipático"
}, {
  "ID_persona": "4",
  "Nombre": "Borja",
  "Primer_apellido": "Lorenzo",
  "Segundo_apellido": "Velasco",
  "Edad": "39",
  "Cartera": "91.46",
  "Cartera_inicial": "91.46",
  "Mood": "majo"
}, {
  "ID_persona": "5",
  "Nombre": "Virgilio",
  "Primer_apellido": "Suárez",
  "Segundo_apellido": "Arias",
  "Edad": "26",
  "Cartera": "54.45",
  "Cartera_inicial": "54.45",
  "Mood": "majo"
}, {
  "ID_persona": "6",
  "Nombre": "Norberto",
  "Primer_apellido": "Delgado",
  "Segundo_apellido": "Giménez",
  "Edad": "56",
  "Cartera": "79.13",
  "Cartera_inicial": "79.13",
  "Mood": "antipático"
}, {
  "ID_persona": "7",
  "Nombre": "Bonifacio",
  "Primer_apellido": "Domínguez",
  "Segundo_apellido": "Román",
  "Edad": "56",
  "Cartera": "51.38",
  "Cartera_inicial": "51.38",
  "Mood": "antipático"
}, {
  "ID_persona": "8",
  "Nombre": "Urbano",
  "Primer_apellido": "Fuentes",
  "Segundo_apellido": "García",
  "Edad": "63",
  "Cartera": "75.47",
  "Cartera_inicial": "75.47",
  "Mood": "majo"
}, {
  "ID_persona": "9",
  "Nombre": "Leonardo",
  "Primer_apellido": "Marín",
  "Segundo_apellido": "Hernández",
  "Edad": "43",
  "Cartera": "26.87",
  "Cartera_inicial": "26.87",
  "Mood": "majo"
}, {
  "ID_persona": "10",
  "Nombre": "Norberto",
  "Primer_apellido": "Vega",
  "Segundo_apellido": "López",
  "Edad": "68",
  "Cartera": "54.03",
  "Cartera_inicial": "54.03",
  "Mood": "majo"
}]
[20:57, 5/2/2024] Alberto Edem: [{
  "ID_coche": "1",
  "Marca": "Citroen",
  "Matricula": "4378LIW",
  "Plazas": "4",
  "Precio_punto": "0.01",
  "Cartera": "0.0"
}, {
  "ID_coche": "2",
  "Marca": "Ford",
  "Matricula": "8644AKU",
  "Plazas": "4",
  "Precio_punto": "0.02",
  "Cartera": "0.0"
}, {
  "ID_coche": "3",
  "Marca": "BMW",
  "Matricula": "4802EAI",
  "Plazas": "4",
  "Precio_punto": "0.02",
  "Cartera": "0.0"
}, {
  "ID_coche": "4",
  "Marca": "Honda",
  "Matricula": "9628MIH",
  "Plazas": "4",
  "Precio_punto": "0.01",
  "Cartera": "0.0"
}, {
  "ID_coche": "5",
  "Marca": "Honda",
  "Matricula": "4537KWQ",
  "Plazas": "4",
  "Precio_punto": "0.02",
  "Cartera": "0.0"
}, {
  "ID_coche": "6",
  "Marca": "Infiniti",
  "Matricula": "4699LSF",
  "Plazas": "4",
  "Precio_punto": "0.01",
  "Cartera": "0.0"
}, {
  "ID_coche": "7",
  "Marca": "Ford",
  "Matricula": "5450MUR",
  "Plazas": "4",
  "Precio_punto": "0.01",
  "Cartera": "0.0"
}, {
  "ID_coche": "8",
  "Marca": "Opel",
  "Matricula": "5962CYP",
  "Plazas": "4",
  "Precio_punto": "0.01",
  "Cartera": "0.0"
}, {
  "ID_coche": "9",
  "Marca": "Daihatsu",
  "Matricula": "3795DPO",
  "Plazas": "4",
  "Precio_punto": "0.01",
  "Cartera": "0.0"
}, {
  "ID_coche": "10",
  "Marca": "Ford",
  "Matricula": "1921IVB",
  "Plazas": "4",
  "Precio_punto": "0.02",
  "Cartera": "0.0"
}]

DESCRIBIR LO QUE SUCEDE EN EL DATAFLOW --> 
EJEMPLO QUE HAY QUE CAMBIAR Y ADAPTAR A NUESTRO PROYECTO --> 

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






STREAMLIT


TABLEAU

En la parte de visualización, se ha creado un dashboard para análizar los resultados que se muestra ...... 



Si deseas ver cómo funciona el código puedes consultar el siguiente vídeo:

---





