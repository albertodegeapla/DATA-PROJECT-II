import streamlit as st
import pandas as pd
from google.cloud import bigquery
from datetime import datetime

# Configuración del proyecto de BigQuery
project_id = 'blablacar2-413422'
client = bigquery.Client(project=project_id)

# Configuración del nombre de tu conjunto de datos en BigQuery
dataset_name = 'blablacar2'

# Función para obtener datos de BigQuery en tiempo real
def get_realtime_data(table_name, id_column, id_value):
    query = f"SELECT * FROM `{project_id}.{dataset_name}.{table_name}` WHERE {id_column} = {id_value} ORDER BY {id_column} DESC LIMIT 1"
    query_job = client.query(query)
    results = query_job.result()
    return results

# Configuración de la aplicación Streamlit
st.title('Visualización en Tiempo Real')

# Widget de selección para elegir el ID del coche
selected_car_id = st.sidebar.selectbox("Selecciona un ID de coche:", [1])

# Obtener datos en tiempo real para el coche seleccionado
data_coches = list(get_realtime_data('coches', 'ID_coche', selected_car_id))

# Mostrar información lateral de la tabla coches
if data_coches:
    row_coche = data_coches[0]
    st.sidebar.subheader('Resumen de Coches')
    st.sidebar.write(f"ID_coche: {row_coche['ID_coche']}")
    st.sidebar.write(f"Marca: {row_coche['Marca']}")
    st.sidebar.write(f"Matricula: {row_coche['Matricula']}")
    st.sidebar.write(f"Plazas: {row_coche['Plazas']}")
    st.sidebar.write(f"N_viajes: {row_coche['N_viajes']}")
    st.sidebar.write(f"Cartera: {row_coche['Cartera']}")
else:
    st.sidebar.write("No hay datos disponibles en este momento para el ID_coche.")

# Widget de selección para elegir el ID de la persona
selected_person_id = st.sidebar.selectbox("Selecciona un ID de persona:", [1])

# Obtener datos en tiempo real para la persona seleccionada
data_personas = list(get_realtime_data('personas', 'ID_persona', selected_person_id))

# Mostrar información lateral de la tabla personas
if data_personas:
    row_persona = data_personas[0]
    st.sidebar.subheader('Resumen de Personas')
    st.sidebar.write(f"ID_persona: {row_persona['ID_persona']}")
    st.sidebar.write(f"Nombre: {row_persona['Nombre']} {row_persona['Primer_apellido']} {row_persona['Segundo_apellido']}")
    st.sidebar.write(f"Edad: {row_persona['Edad']}")
    st.sidebar.write(f"N_viajes: {row_persona['N_viajes']}")
    st.sidebar.write(f"Cartera: {row_persona['Cartera']}")
else:
    st.sidebar.write("No hay datos disponibles en este momento para el ID_persona.")

# Botón para actualizar manualmente
if st.button('Actualizar'):
    # Obtener datos en tiempo real para el coche seleccionado desde la tabla coches_streamlit
    data_coches_streamlit = list(get_realtime_data('coches_streamlit', 'ID_coche', selected_car_id))
    # Obtener datos en tiempo real para la persona seleccionada desde la tabla personas_streamlit
    data_personas_streamlit = list(get_realtime_data('personas_streamlit', 'ID_persona', selected_person_id))
    # Mostrar el mapa con las coordenadas del coche y de la persona seleccionados
    if data_coches_streamlit and data_personas_streamlit:
        coordenadas_coche = data_coches_streamlit[0]['Coordenada_coche']
        latitud_coche, longitud_coche = [float(coord.strip()) for coord in coordenadas_coche.split(',')]
        
        coordenadas_persona = data_personas_streamlit[0]['Coordenadas_persona']
        latitud_persona, longitud_persona = [float(coord.strip()) for coord in coordenadas_persona.split(',')]
        
        # Crear un DataFrame con las coordenadas
        df = pd.DataFrame({'LAT': [latitud_coche, latitud_persona], 'LON': [longitud_coche, longitud_persona]})
        
        # Mostrar el mapa con las coordenadas
        st.map(data=df, zoom=15)
    else:
        st.write(f"No hay datos disponibles en este momento para el ID_coche = {selected_car_id} y/o ID_persona = {selected_person_id}.")