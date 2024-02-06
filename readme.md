DATA PROJECT 2

DESCRIPCIÓN

La empresa Bla Ba Car, está decidida a revolucionar la forma en que nos movemos en distancias cortas. Han decidido dar el salto hacia la reserva en tiempo real de desplazamientos dentro de las ciudades. ¿Qué significa esto? Significa que podrías reservar un viaje dentro de tu ciudad justo cuando lo necesites, sin esperar mucho tiempo o depender de un horario fijo.

Y adivina qué ciudad ha elegido Bla Ba Car como su pionera en esta audaz iniciativa: ¡Valencia! Sí, la vibrante y hermosa ciudad de Valencia se convertirá en el campo de pruebas para esta nueva forma de moverse en la urbe.

Pero, ¿por qué Valencia? ¿Qué tiene de especial esta ciudad que la hace perfecta para este piloto? Bueno, para empezar, Valencia es un centro de actividad constante. Con sus calles llenas de vida, sus puntos de interés turístico y sus habitantes siempre en movimiento, Valencia ofrece el escenario ideal para probar la efectividad de este sistema de reserva en tiempo real.

Además, Valencia cuenta con una infraestructura vial diversa y bien desarrollada, lo que facilita la navegación y la logística del transporte urbano. Desde sus amplias avenidas hasta sus estrechas callejuelas llenas de encanto, Valencia desafía a Bla Ba Car a demostrar que su sistema puede adaptarse a cualquier entorno urbano.

Así que prepárate, Valencia, porque el futuro del transporte en la ciudad está a punto de cambiar. Con Bla Ba Car liderando el camino, pronto podrías estar reservando tus viajes dentro de la ciudad con solo unos pocos clics en tu teléfono. Es un salto emocionante hacia adelante, y Valencia está a la vanguardia de esta revolución en movimiento urbano


Equipo

José Aguilar Van Der Hofstadt:Licenciado en administración y dirección de empresas Encargado de la parte de Data Engineering relativa a la cola de mensajes en Pub/Sub, diseño de arquitectura y desarrollo de código para el Dataflow.

Pablo Pérez Álvarez: Licenciado en Negocios Internacionales y Marketing. Parte del equipo de Data Engineering del proyecto. Desarrollo de la lógica para la recogida de pasajeros. 

Lucía Esteve Domínguez: Licenciada en administración y dirección de empresas. Desarrollo de código para la generación de los datos del proyecto. Diseño de la arquitectura, y Bussines Inteligence.

Ándrés Cervera Beneyto:Ingeniero informático.Encargado de la parte del desarrollo de la creación de la interfaz de usuario para visualizar el  modelo utilizando Streamlit y apoyo en la parte de desarrollo de código para Dataflow.

Álberto De Gea Pla:Licenciado en administración y dirección de empresas. Desarrollo de código para la generación de los datos del proyecto y el Dataflow. Encargado del análisis y visualización de los datos y resultados del negocio. 


En este repositorio, se encuentra la solución en Google Cloud que hemos diseñado. Consta de las siguientes partes:

Generador de datos con envío a Pub/Sub

Dataflow para transformación de los mensajes

BigQuery como almacenamiento

Streamlit para visualización de la interfaz 

Tableau para el análisis y visualización de los datos del negocio


DISEÑO DE LA ARQUITECTURA

--> AÑADIR IMAGÉN QUE TENGO QUE CREAR DE LA ARQUITECTURA

Generador de datos (PUB/SUB)

Se generan datos tanto para peatones como para coches cada uno con sus respectivas rutas. 

Se utiliza Pub/sup para publicar mensajes en directo sobre las rutas que esta utilizando el usuario. 

Ambos generadores funcionan igual:  con una función se genera un ejemplo de ruta en forma de diccionario Python, incluyendo detalles diferentes dependiendo de si estamos en el generador de datos para los coches (la marca, la matrícula, el número de plazas, el precio, la hora de salida y una lista de coordenadas de la ruta)o en el generador de datos para personas (ID de la persona, el nombre, la cantidad de dinero en su cartera, la hora de salida y una lista de coordenadas de la ruta)

AÑADIR REDACCIÓN! 


Se crea un cliente de publicador de Pub/Sub y se almacenan el ID del proyecto y el nombre del tema. 

El método publishCarMessage toma un mensaje como entrada, lo convierte a formato JSON, y lo publica en el tema especificado. También registra información sobre el mensaje publicado.

En resumen, este código proporciona una forma de generar y publicar mensajes sobre rutas de coche y de peaton en un tema de Google Cloud Pub/Sub, utilizando argumentos de línea de comandos para especificar el proyecto y el nombre del tema.

"""REVISAR """

Para ejecutar el codigo del generador correctamente hay que realizar los siguientes pasos:

FALTA RELLENAR 

DATAFLOW

Dentro de la carpeta de dataflow, se encuentra el código Python escrito utilizando la librería Apache BEAM para consumir los datos generados tanto de pasajeros como de vehiculos  mediante dos subscripciones de cada topic de Pub/Sub. En Dataflow se realizan los siguientes pasos:

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
}]
[{
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
}]

DESCRIBIR LO QUE SUCEDE EN EL DATAFLOW --> 

LÓGICA DEL DATAFLOW. LA RECOGIDA DEL PASAJERO.

Una vez nuestro código ha leido los mensajes de dos topics diferentes a la vez - por una parte, "coche" y por otra "persona" -, los juntamos para poder procesarlos con un DoFn donde desarrollamos la lógica de nuestro proyecto.

Cómo se puede comprobar en el formato de los mensajes que anteriormente hemos puesto de ejemplo, la información que llega en esos mensajes contiene, entre otras cosas, las ubicaciones de cada coche y/o persona, en un determinado momento - tiempo real, streaming - y el punto geográfico hasta el cual se dirige.

La función empieza calculando la distancia entre el coche y el pasajero, usando la librería "Haversine", que nos ayuda a calcular las distancias entre dos puntos por GPS - en formato Latitud, Longitud - en metros. Se ha elegido esta librería porque, inicialmente, utilizamos la librería "math" donde utilizábamos una fórmula muy interesante con cosenos, senos, tangentes y radianes, ya que las coordenadas en GPS están en radianes y esta fórmula, que tiene en cuenta el radio del planeta Tierra, nos convertía esas distancias en el formato que necesitábamos. Por tal de simplificar y optar por un formato más minimalista, hemos reducido líneas de código con esta librería.

Una vez ya tenemos la distancia, en tiempo real, entre el coche y el pasajero, nos basamos en el "mood" para definir un rango de acción. En nuestra lógica, si alguien es "majo", "normal" o "antipático" debería de definir cuán lejos se va a desplazar para hacer match. Si la distancia es menor que el rango del mood, entonces esta condición se cumple.

La siguiente y no menos importante condición, es si ambos, coche y persona, se dirigen al mismo punto. Para ello, hemos cogido las coordenadas del final de la ruta de cada uno, y hemos vuelto a calcular la distancia, para ver si entra dentro de un determinado rango, para que tenga sentido ir en el mismo coche y a un punto relativamente cercano. Si la distancia entre los destinos es menor al rango definido, entonces esta condición se cumple.

A continuación, tenemos una situación en la cuál el coche y la persona no solo están lo suficientemente cerca como para recoger a la persona, sino que además van a un sitio relativamente cercano el uno del otro, pero tenemos que comprobar si quedan plazas disponibles en el coche. Si quedan plazas disponibles, entonces realizamos la comprobación del pago y vemos si la persona tiene suficiente dinero para pagar el viaje, y si es así, entonces se realiza el match, se realiza el pago y se resta la plaza disponible en dicho coche.

Una vez estas condiciones se cumplen y obtenemos un match, entonces realizamos el update en la base de datos, para poder almacenarlo y visualizarlo posteriormente.



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





