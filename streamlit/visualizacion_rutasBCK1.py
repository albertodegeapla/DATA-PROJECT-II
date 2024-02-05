import streamlit as st
import pandas as pd
from google.cloud import bigquery
from datetime import datetime

# Configuración del proyecto de BigQuery
project_id = 'deductive-span-411710'
client = bigquery.Client(project=project_id)

# Configuración del nombre de tu conjunto de datos y tabla en BigQuery
dataset_name_peaton = 'dataset'
table_name_peaton = 'Peaton'

dataset_name_coche = 'dataset'
table_name_coche = 'Coche'

# Función para obtener datos de BigQuery en tiempo real
def get_realtime_data(table_name, id_column, id_value):
    query = f"SELECT * FROM `{project_id}.{dataset_name_peaton}.{table_name}` WHERE {id_column} = {id_value} ORDER BY {id_column} DESC LIMIT 1"
    query_job = client.query(query)
    results = query_job.result()
    return results

# Configuración de la aplicación Streamlit
st.title('Visualización en Tiempo Real')

# Botón para actualizar manualmente
if st.button('Actualizar'):
    # Obtener el tiempo actual
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Mostrar la hora actual
    st.write(f'Hora actual: {current_time}')

    # Obtener datos en tiempo real para la tabla Coche
    data_coche = list(get_realtime_data(table_name_coche, 'ID_Coche', 1))

    # Mostrar resumen de la tabla Coche en la parte superior derecha
    st.sidebar.subheader('Resumen de Coche')
    if data_coche:
        row_coche = data_coche[0]
        st.sidebar.write(f"ID_Coche: {row_coche['ID_Coche']}")
        st.sidebar.write(f"Matricula: {row_coche['Matricula']}")
        st.sidebar.write(f"Plazas: {row_coche['Plazas']}")
        st.sidebar.write(f"Cartera: {row_coche['Cartera']}")
    else:
        st.sidebar.write("No hay datos disponibles en este momento para la tabla Coche.")

    # Obtener datos en tiempo real para la tabla Peaton
    data_peaton = list(get_realtime_data(table_name_peaton, 'ID_Peaton', 1))

    # Mostrar resumen de la tabla Peaton en la parte superior derecha
    st.sidebar.subheader('Resumen de Peaton')
    if data_peaton:
        row_peaton = data_peaton[0]
        st.sidebar.write(f"ID_Peaton: {row_peaton['ID_Peaton']}")
        st.sidebar.write(f"Nombre: {row_peaton['Nombre']} {row_peaton['Apellidos']}")
        st.sidebar.write(f"Wallet: {row_peaton['Wallet']}")
    else:
        st.sidebar.write("No hay datos disponibles en este momento para la tabla Peaton.")

    # Crear un DataFrame de Pandas con las coordenadas
    df_map = pd.DataFrame({
        'latitude': [float(row_peaton['coordenada_peaton'].split(',')[0]), float(row_coche['coordenada_coche'].split(',')[0])],
        'longitude': [float(row_peaton['coordenada_peaton'].split(',')[1]), float(row_coche['coordenada_coche'].split(',')[1])]
    })

    # Agregar un mapa con los datos del DataFrame
    st.map(df_map)
