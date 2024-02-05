import streamlit as st
import pandas as pd  # Añade esta línea para usar DataFrames de Pandas
from google.cloud import bigquery
from datetime import datetime
import time
import random

# Configuración del proyecto de BigQuery
project_id = 'deductive-span-411710'
client = bigquery.Client(project=project_id)

# Configuración del nombre de tu conjunto de datos y tabla en BigQuery
dataset_name_peaton = 'dataset'
table_name_peaton = 'Peaton'

dataset_name_coche = 'dataset'
table_name_coche = 'Coche'

# Función para obtener datos de BigQuery en tiempo real
def get_realtime_data(table_name):
    query = f"SELECT * FROM `{project_id}.{dataset_name_peaton}.{table_name}` ORDER BY ID_{table_name} DESC LIMIT 1"
    query_job = client.query(query)
    results = query_job.result()
    return results

# Configuración de la aplicación Streamlit
st.title('Visualización en Tiempo Real de Datos')

# Botón para actualizar manualmente
if st.button('Actualizar'):
    # Obtener el tiempo actual
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Mostrar el reloj
    st.text(current_time)

    # Obtener datos en tiempo real para la tabla Peaton
    data_peaton = get_realtime_data('Peaton')

    # Mostrar resumen de la tabla Peaton en la parte superior derecha
    if data_peaton:
        st.sidebar.subheader('Resumen de Peaton')
        for row in data_peaton:
            st.sidebar.write(f"ID_Peaton: {row['ID_Peaton']}")
            st.sidebar.write(f"Nombre: {row['Nombre']} {row['Apellidos']}")
            st.sidebar.write(f"Wallet: {row['Wallet']}")
    else:
        st.sidebar.write("No hay datos disponibles en este momento para la tabla Peaton.")

    # Obtener datos en tiempo real para la tabla Coche
    data_coche = get_realtime_data('Coche')

    # Mostrar resumen de la tabla Coche en la parte superior derecha
    if data_coche:
        st.sidebar.subheader('Resumen de Coche')
        for row in data_coche:
            st.sidebar.write(f"ID_Coche: {row['ID_Coche']}")
            st.sidebar.write(f"Matricula: {row['Matricula']}")
            st.sidebar.write(f"Plazas: {row['Plazas']}")
            st.sidebar.write(f"Cartera: {row['Cartera']}")
    else:
        st.sidebar.write("No hay datos disponibles en este momento para la tabla Coche.")

    # Crear un DataFrame de Pandas con dos puntos aleatorios
    df_map = pd.DataFrame({'latitude': [random.uniform(-90, 90), random.uniform(-90, 90)],
                           'longitude': [random.uniform(-180, 180), random.uniform(-180, 180)]})

    # Agregar un mapa con los datos del DataFrame
    st.subheader('Mapa con Puntos Aleatorios')
    st.map(df_map)