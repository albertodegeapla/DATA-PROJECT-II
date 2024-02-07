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

Generador de datos, tanto estáticos como dinámicos, los dinámicos se envian como mensaje a traves de Pub/Sub de GCP

Dataflow para transformación de los mensajes y procesamiento de la información (gestión del match)

BigQuery como almacenamiento

Streamlit para visualización de la interfaz 

Tableau para el análisis y visualización de los datos del negocio


DISEÑO DE LA ARQUITECTURA

--> AÑADIR IMAGÉN QUE TENGO QUE CREAR DE LA ARQUITECTURA

Generador de datos.

[Estáticos]

Se generan datos tanto para peatones como para coches y se almacenan en Big Query.

Estos datos son los datos son las propiedades de cada uno.

En el caso de los coches: ID, Marca, Matricula, nº plazas disponibles, Precio por coordenada(€), Cartera, nº viajes realizados y nº pasajeros recogidos.

En el caso de las personas: ID, Nombre, Apellidos, Edad, Cartera, Cartera inicial, Mood*, nº viajes, en_ruta**.

*Esta variable en un entorno productivo real no exisitiría, pero en esta simulación queriamos simular el comportamiento de diferentes tipos de personas.
**Esta variable hace referencia a si en este preciso momento el peaton se encuentra dentro de un coche o no, ayuda en el procesamiento.

[Dinámicos] Pub/Sub

Se selecciona a un peaton/coche y se le asigna una ruta al azar. Esta, se desglosa por coordenadas y se envia un mensaje con el estado del coche/peaton.

Se utiliza Pub/sup para publicar mensajes en directo del estado del ususario en cada coordenada. 

El contenido de los mensajes es el siguiente:

- Coches: ID, (hora actual, (coordeanda1, coordenada 2), coordenadas del destino, nº plazas disponibles, precio del viaje

El precio del viaje se calcula segun el número de coordenadas que faltan para llegar al destino, de esta forma un viaje al principio del trayecto será más caro que un viajes a mitad de trayecto.

Para actualizar las plazas se lee de Big Query (esta disminuye cuando hay un match en el procesamiento)

- Peatones: ID, (hora actual, (coordeanda1, coordenada 2), coordenadas del destino, Cartera, mood

Cada mensaje se envia a un topic, todos los mensajes del coche a un topic. Ej: ruta_coche y todos los mensajes del peaton se envian a otro topic, ej. ruta_peaton.

Los mensajes enviados estan en formato JSON por lo que se codifican antes de ser enviados y se deberan decodificar una vez llegan.
 
En resumen, este código proporciona una forma de generar y publicar mensajes sobre rutas de coche y de peaton en un topic de Google Cloud Pub/Sub, utilizando argumentos de línea de comandos para especificar el proyecto y el nombre del tema.

Para ejecutar el codigo del generador correctamente hay que realizar los siguientes pasos:

python <GENERADOR_X.py> --project_id <TU_PROYECTO> --peaton_topic_name <NOMBRE_TOPIC_X> --dataset_id <NOMBRE_DATASET> --table_peaton <NOMBRE_TABLA_X> --n_peatones <INT. nº de datos estáticos que quieres generar>   

Aclaracion IMPORTANTE. los datos estáticos solo se deben ejecutar una vez. Por lo que cada vez que lances el generador te hará escribir una palabra 'n' para que no generes nuevos peatones. Si fuese la primera vez que quieres generar peatones, deberás escribir 'peatones' o 'coches'

DATAFLOW

Dentro de la carpeta de dataflow, se encuentra el código Python escrito utilizando la librería Apache BEAM para consumir los datos generados tanto de pasajeros como de vehiculos mediante dos subscripciones de cada topic de Pub/Sub. En Dataflow se realizan los siguientes pasos:

Primero se leen los mensajes escritos del topic y se decodifican para acceder al formato JSON, creando una PColletion con el contenido de los mensajes. a cada mensaje se le agrega una key que será la hora a la que se envia el mensaje. Importante alclarar que para que funcione correctamente los datos de tiempo están modificados para que los segunod sean siempre par y sea más facil la agrupacion posterior

Para delimitar el número de mensajes que llegan y poder trabajar correctamente se ha ajustado una ventana de 2 segundos para las dos pcollections que recojen los datos (los datos se generan aproximadamente cada 1-2 segunods)

Una vez leidos se juntan en la misma p colection agrupandose por key (la hora) y se envian al proceso de match con una funcion ParDo.

LÓGICA DEL DATAFLOW. LA RECOGIDA DEL PASAJERO.

Una vez nuestro código ha leido los mensajes de dos topics diferentes a la vez - por una parte, "coche" y por otra "persona" -, los juntamos para poder procesarlos con un DoFn donde desarrollamos la lógica de nuestro proyecto.

Cómo se puede comprobar en el formato de los mensajes que anteriormente hemos puesto de ejemplo, la información que llega en esos mensajes contiene, entre otras cosas, las ubicaciones de cada coche y/o persona, en un determinado momento - tiempo real, streaming - y el punto geográfico hasta el cual se dirige.

La función empieza calculando la distancia entre el coche y el pasajero, usando la librería "Haversine", que nos ayuda a calcular las distancias entre dos puntos por GPS - en formato Latitud, Longitud - en metros. 

Una vez ya tenemos la distancia, en tiempo real, entre el coche y el pasajero, nos basamos en el "mood" para definir un rango de acción. En nuestra lógica, si alguien es "majo", "normal" o "antipático" debería de definir cuán lejos se va a desplazar para hacer match. Si la distancia es menor que el rango del mood, entonces esta condición se cumple.

La siguiente y no menos importante condición, es si ambos, coche y persona, se dirigen al mismo punto. Para ello, hemos cogido las coordenadas del final de la ruta de cada uno, y hemos vuelto a calcular la distancia, para ver si entra dentro de un determinado rango, para que tenga sentido ir en el mismo coche y a un punto relativamente cercano. Si la distancia entre los destinos es menor al rango definido, entonces esta condición se cumple.

A continuación, tenemos una situación en la cuál el coche y la persona no solo están lo suficientemente cerca como para recoger a la persona, sino que además van a un sitio relativamente cercano el uno del otro, pero tenemos que comprobar si quedan plazas disponibles en el coche. Si quedan plazas disponibles, entonces realizamos la comprobación del pago y vemos si la persona tiene suficiente dinero para pagar el viaje, y si es así, entonces se realiza el match, se realiza el pago y se resta la plaza disponible en dicho coche.

Una vez estas condiciones se cumplen y obtenemos un match, entonces realizamos el update en la base de datos de Big Query, para poder almacenarlo y visualizarlo posteriormente.



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

En la parte de visualización, se ha creado un dashboard para análizar los resultados sobre el conjunto de viajes de los coches, con la finalidad de ver a cuantos pasajeros han transportado y como ha aumentado su cartera.

Por otra parte, también se ha empleado esta herramienta para visualizar como ha variado la cartera de las personas durante el transcurso del proyecto.



Si deseas ver cómo funciona el código puedes consultar el siguiente vídeo:

---






