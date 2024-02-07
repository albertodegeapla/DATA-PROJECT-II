import argparse
import logging
import json
import time
from google.cloud import bigquery
from google.cloud.bigquery.job import WriteDisposition
from google.cloud import pubsub_v1

def update_streamlit_table(message, client, dataset_id, destination_table_id):
    message_data = json.loads(message.data)
    id_coche = message_data.get("id_coche")
    coordenadas = message_data.get("punto_destino")
    if id_coche is not None and coordenadas is not None:
        # Actualizar la tabla de destino con las coordenadas y el ID del coche
        table_ref = client.dataset(dataset_id).table(destination_table_id)
        table = client.get_table(table_ref)
        rows = client.list_rows(table, selected_fields=[table.schema[0]], where=f"ID_coche = {id_coche}", max_results=1)
        for row in rows:
            row["Coordenadas_coche"] = coordenadas
            client.update_rows([row], table, ["Coordenadas_coche"])
            logging.info(f"Tabla actualizada con coordenadas para el coche ID: {id_coche}")

def receive_messages(project_id, topic_name, client, dataset_id, destination_table_id):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = f"projects/{project_id}/subscriptions/ruta_coche-sub"


    while True:
        response = subscriber.pull(
            request={
                "subscription": subscription_path,
                "max_messages": 1,
            }
        )

        for message in response.received_messages:
            update_streamlit_table(message, client, dataset_id, destination_table_id)
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [message.ack_id]}
            )

        time.sleep(5)  # Espera 5 segundos antes de solicitar más mensajes

def main(project_id, topic_name, dataset_id, table_id):
    logging.getLogger().setLevel(logging.INFO)
    client = bigquery.Client(project=project_id)

    # Ejecuta la función para recibir y procesar mensajes
    receive_messages(project_id, topic_name, client, dataset_id, table_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Carga de coches a una tabla en BigQuery desde Pub/Sub")
    parser.add_argument("--project_id", help="ID del proyecto de GCP", required=True)
    parser.add_argument("--topic_name", help="Nombre del topic de Pub/Sub", required=True)
    parser.add_argument("--dataset_id", help="ID del dataset en BigQuery", required=True)
    parser.add_argument("--table_id", help="ID de la tabla en BigQuery", required=True)
    args = parser.parse_args()

    main(args.project_id, args.topic_name, args.dataset_id, args.table_id)
