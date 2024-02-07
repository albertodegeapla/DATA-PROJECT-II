import argparse
import json
from google.cloud import pubsub_v1
from google.cloud import bigquery

def update_coordenadas_coche(project_id, car_topic_name, subscription_name, dataset_id, table_car):
    subscriber = pubsub_v1.SubscriberClient()
    bigquery_client = bigquery.Client(project=project_id)

    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        data = json.loads(message.data.decode("utf-8"))
        id_coche = data["id_coche"]
        coordenadas = data["coordenadas"][1]

        table_ref = bigquery_client.dataset(dataset_id).table(table_car)
        table = bigquery_client.get_table(table_ref)

        query = f"""
            UPDATE `{project_id}.{dataset_id}.{table_car}`
            SET Coordenada_coche = ST_GEOGPOINT({coordenadas[0]}, {coordenadas[1]})
            WHERE ID_coche = {id_coche}
        """
        bigquery_client.query(query)

        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    print(f"Listening for messages on {subscription_path}")
    # Mantener el programa en ejecución para recibir mensajes
    try:
        while True:
            pass
    except KeyboardInterrupt:
        subscriber.close(subscription_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", required=True, help="Google Cloud Project ID")
    parser.add_argument("--car_topic_name", required=True, help="Pub/Sub topic name for car messages")
    parser.add_argument("--subscription_name", required=True, help="Pub/Sub subscription name for car messages")
    parser.add_argument("--dataset_id", required=True, help="BigQuery dataset ID")
    parser.add_argument("--table_car", required=True, help="BigQuery table name for cars")
    args = parser.parse_args()

    update_coordenadas_coche(args.project_id, args.car_topic_name, args.subscription_name, args.dataset_id, args.table_car)
