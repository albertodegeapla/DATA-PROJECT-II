import streamlit as st
from google.cloud import bigquery

# Configuración del proyecto de BigQuery
project_id = 'deductive-span-411710'
client = bigquery.Client(project=project_id)

# Configuración del nombre de tu conjunto de datos y tabla en BigQuery
dataset_name = 'dataset'  # Reemplaza 'tu-conjunto-de-datos' con el nombre real
table_name = 'ruta_coche'  # Reemplaza 'tu-tabla' con el nombre real

# Función para obtener datos de BigQuery en tiempo real
def get_realtime_data():
    query = f"SELECT * FROM `{project_id}.{dataset_name}.{table_name}` ORDER BY timestamp_column DESC LIMIT 10"
    query_job = client.query(query)
    results = query_job.result()
    return results

# Configuración de la aplicación Streamlit
st.title('Visualización en Tiempo Real de Rutas')

# Obtener datos en tiempo real
data = get_realtime_data()

# Mostrar datos en Streamlit
if data:
    for row in data:
        st.write(f"ID: {row['ID']}, Latitud: {row['Latitud']}, Longitud: {row['Longitud']}, Hora: {row['Hora']}")
else:
    st.write("No hay datos disponibles en este momento.")
