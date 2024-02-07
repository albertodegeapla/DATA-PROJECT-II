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

# Obtener todos los IDs de coches disponibles
def get_available_car_ids():
    query = f"SELECT DISTINCT ID_coche FROM `{project_id}.{dataset_name}.coches_streamlit`"
    query_job = client.query(query)
    results = query_job.result()
    return [row['ID_coche'] for row in results]

# Obtener todos los IDs de personas disponibles
def get_available_person_ids():
    query = f"SELECT DISTINCT ID_persona FROM `{project_id}.{dataset_name}.personas`"
    query_job = client.query(query)
    results = query_job.result()
    return [row['ID_persona'] for row in results]

# Configuración de la aplicación Streamlit
st.title('Visualización en Tiempo Real')

# Obtener los IDs de coches y personas disponibles
car_ids = get_available_car_ids()
person_ids = get_available_person_ids()

# Widget de selección para elegir el ID del coche
selected_car_id = st.sidebar.selectbox("Selecciona un ID de coche:", car_ids)

# Obtener datos en tiempo real para el coche seleccionado
data_coches_streamlit = list(get_realtime_data('coches_streamlit', 'ID_coche', selected_car_id))

# Mostrar resumen de la tabla Coches en la parte superior derecha
st.sidebar.subheader('Resumen de Coches')
if data_coches_streamlit:
    row_coche = data_coches_streamlit[0]
    st.sidebar.write(f"ID_coche: {row_coche['ID_coche']}")
    st.sidebar.write(f"Marca: {row_coche['Marca']}")
    st.sidebar.write(f"Matricula: {row_coche['Matricula']}")
    st.sidebar.write(f"Plazas: {row_coche['Plazas']}")
    st.sidebar.write(f"N_viajes: {row_coche['N_viajes']}")
    st.sidebar.write(f"Cartera: {row_coche['Cartera']}")
else:
    st.sidebar.write("No hay datos disponibles en este momento para el ID_coche.")

# Widget de selección para elegir el ID de la persona
selected_person_id = st.sidebar.selectbox("Selecciona un ID de persona:", person_ids)

# Obtener datos en tiempo real para la persona seleccionada
data_personas = list(get_realtime_data('personas', 'ID_persona', selected_person_id))

# Mostrar resumen de la tabla Personas en la parte superior derecha
st.sidebar.subheader('Resumen de Personas')
if data_personas:
    row_persona = data_personas[0]
    st.sidebar.write(f"ID_persona: {row_persona['ID_persona']}")
    st.sidebar.write(f"Nombre: {row_persona['Nombre']} {row_persona['Primer_apellido']} {row_persona['Segundo_apellido']}")
    st.sidebar.write(f"Edad: {row_persona['Edad']}")
    st.sidebar.write(f"N_viajes: {row_persona['N_viajes']}")
    st.sidebar.write(f"Cartera: {row_persona['Cartera']}")
else:
    st.sidebar.write("No hay datos disponibles en este momento para el ID_persona.")

# Botón para actualizar manualmente
if st.button('Actualizar'):
    # Mostrar el mapa con las coordenadas del coche seleccionado
    if data_coches_streamlit:
        coordenadas_coche = data_coches_streamlit[0]['Coordenadas_coche']
        latitud, longitud = [float(coord.strip()) for coord in coordenadas_coche.split(',')]

        # Crear un DataFrame con las coordenadas
        df = pd.DataFrame({'LAT': [latitud], 'LON': [longitud]})

        # Mostrar el mapa con las coordenadas
        st.map(data=df, zoom=15)
    else:
        st.write(f"No hay datos disponibles en este momento para el ID_coche = {selected_car_id} en la tabla Coches Streamlit.")
