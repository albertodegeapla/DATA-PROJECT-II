# Cómo hemos ido entrenando el script de la ruta.
*...cuando digo "entrenar" me refiero a ir aprendiendo a hacer que el script funcione de una forma u otra. No es realmente entrenar ningún algoritmo pero me hace ilusión utilizar la expresión de esa forma :)*

## ¿Qué es lo que queremos lograr?
Lo que queremos **lograr** con este directorio es aprender a hacer, paso a paso, script por script, las reglas de negocio que queremos aplicar al funcionamiento de la aplicación. Por ejemplo, hacer funcionar streamlit para que muestre por pantalla un único punto definido, o una ruta (un array hard-codeado de coordenadas) o un cambio de color/formato en un icono. O de forma más avanzada, que los pasajeros tengan un rango máximo de 1000 metros a la ruta más cercana, para que no tengan que dedicar mucho tiempo a andar.

### Cómo hacer funcionar Streamlit.
Streamlit es una librería de Python que podemos instalar con:
```
pip install streamlit
```
Para comprobar si está bien instalado, puedes hacer:
```
streamlit --version
```
Si te aparecen unas líneas rojas, cómo me ha pasado a mí, que básicamente dice que no sabe de qué les estás hablando, que _streamlit_ no es un comando, entonces tienes un problema con el PATH donde se ha instalado Streamlit. Para solucionarlo, le puedes pedir a ChatGPT que te lo instale en una ruta específica. Si no te funciona, puedes preguntarme cómo lo he solucionado y lo vemos.

Siguiente paso es crear un script de Python y ponerse a picar código.
Las librerías que vamos a tener que importar son las siguientes:
```
import streamlit as st
```
Además, para poder utilizar el mapa de forma visual, hemos encontrado la librería de Folium, que es bastante completa. Para instalarla:
```
import folium
from streamlit_folium import st_folium
```
Y por otra parte, también vamos a utilizar Pandas:
```
import pandas as pd
```
Ya que estamos, añadimos también la librería Math, que utilizaremos para calcular la distancia entre 2 coordenadas, con una fórmula que luego más adelante explicaré. Instalamos Math con:
```
from math import radians, sin, cos, sqrt, atan2
```
### Quiero ver el mapa.
Ahora viene la hora de la verdad. Para poder ver el mapa en el último navegador que hayas usado, tienes que situarte en la carpeta _entrenamiento_ruta_ y meter el siguiente comando en la terminal:
```
streamlit run .\pruebas_streamlit.py
```
Aparecerán unas letras azules y automáticamente se te abrirá el navegador, para visualizar el mapa.
> Si quieres parar el código, simplemente pulsa **CNTRL + C** y se parará.
## Vamos a ver el código.
> Para explorar las posibilidades que tenemos con Streamlit, puedes ver la documentación aquí: https://folium.streamlit.app/

En el script de _pruebas_streamlit.py_ nos hemos basado en el código disponible en el primer ejemplo de _Stremlit app_, que es este:
```
import folium
import streamlit as st

from streamlit_folium import st_folium

# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)
```
Aquí realmente solo hay 3 partes, vamos a verla una a una:
### Parte 1: Ubicar la pantalla del mapa.
En Streamlit, tenemos que ayudarle a ubicar dónde está la pantalla por default, definiéndole unas coordenadas geográficas y un Zoom (cuanto más grande el número más cerca, cuanto más pequeño, más lejos):
```
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
```
Las coordenadas geográficas que podemos utilizar pueden ser las mismas que el punto que queremos visualizar.
```
[39.949610, -75.150282]
```
### Parte 2: Marcar un punto en el mapa.
Es una expresión muy sencilla que únicamente nos pide las coordenadas, y a la que podemos poner títulos:
```
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)
```
### Parte 3: Renderizar la información en el mapa.
Al final de nuestro script, tendremos que añadir lo siguiente, para que Streamlit ejecute el código en el mapa de nuestro navegador:
```
st_data = st_folium(m, width=725)
```
# pruebas_streamlit.py
Ahora voy a proceder a explicar lo que hay en concreto en el script _pruebas_streamlit.py_
## Objetivo: visualizar la ruta en el mapa.
Cuando descargamos la ruta que hemos creado con Google Maps en formato .KML, encontramos que, entre otras cosas, hay un array de coordenadas geográficas que indican **la longitud, la latitud y la altura**. El problema viene cuando vemos que en Streamlit, el formato que se requiere es **[Latitud,Longitud]**, por lo que debemos cambiar el orden de las variables, y eliminar la altura de la ecuación, ya que sino aparecerá un error.
> Lo que he hecho yo es, ya que vivimos en tiempos de ChatGPT, le he pedido que me lo haga, pero para 20 coordenadas de la ruta, ya que no necesito más.
El resultado es el siguiente:
```
coordinates = [
    [39.46939, -0.35902],
    [39.46949, -0.35889],
    [39.46958, -0.35876],
    [39.46962, -0.35871],
    [39.46969, -0.35865],
    [39.4698, -0.35858],
    [39.46992, -0.35849],
    [39.47013, -0.35842],
    [39.47014, -0.3584],
    [39.47015, -0.35839],
    [39.47018, -0.35837],
    [39.47019, -0.35836],
    [39.47021, -0.35835],
    [39.47024, -0.35834],
    [39.47027, -0.35834],
    [39.4703, -0.35834],
    [39.47033, -0.35837],
    [39.47035, -0.35839],
    [39.47038, -0.35834],
    [39.47043, -0.35827],
    [39.47048, -0.35822],
]
```
A diferencia del ejemplo anterior, lo que necesitamos aquí es crear un loop _for_ que haga el trabajo por nosotros y nos evite tener que meter cada punto a mano.
> DISCLAIMER: Ya que queremos evitar que nos resten puntos por hard-codear, la idea es volcar las coordenadas de un .CSV o de una BBDD en SQL.

Lo primero que hemos hecho es definir un Dataframe, indicando la LATITUD y la LONGITUD:
```
df = pd.DataFrame(coordinates, columns=["LATITUDE", "LONGITUDE"])
```
Después, y para comprobar que las coordenadas se cargan correctamente, hemos visualizado el Dataframe en el navegador:
```
st.dataframe(df)
```
Para posteriormente, ejecutar el script e ir creando marcadores en el mapa:
```
for index, row in df.iterrows():
    folium.Marker(location=[row["LATITUDE"], row["LONGITUDE"]]).add_to(m)
```
Lo único que hace es, con el Dataframe definido, y usando iterrows, ir creando un marcador con **folium.Marker(location=[X,Y])** con las coordenadas del array **row["LATITUDE"], row["LONGITUDE"]** y luego añadirlas al mapa con **.add_to(m)**.
