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
