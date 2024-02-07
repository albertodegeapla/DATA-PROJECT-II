import argparse
import json
from google.cloud import pubsub_v1
from google.cloud import bigquery

def update_coordenadas_persona(project_id, persona_topic_name, subscription_name, dataset_id, table_persona):
    subscriber = pubsub_v1.SubscriberClient()
    bigquery_client = bigquery.Client(project=project_id)

    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        data = json.loads(message.data.decode("utf-8"))
        id_persona = data["id_persona"]
        coordenadas = data["coordenadas"][1]

        table_ref = bigquery_client.dataset(dataset_id).table(table_persona)
        table = bigquery_client.get_table(table_ref)

        query = f"""
            UPDATE `{project_id}.{dataset_id}.{table_persona}`
            SET Coordenadas_persona = ST_GEOGPOINT({coordenadas[0]}, {coordenadas[1]})
            WHERE ID_persona = {id_persona}
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
    parser.add_argument("--persona_topic_name", required=True, help="Pub/Sub topic name for person messages")
    parser.add_argument("--subscription_name", required=True, help="Pub/Sub subscription name for person messages")
    parser.add_argument("--dataset_id", required=True, help="BigQuery dataset ID")
    parser.add_argument("--table_persona", required=True, help="BigQuery table name for persons")
    args = parser.parse_args()

    update_coordenadas_persona(args.project_id, args.persona_topic_name, args.subscription_name, args.dataset_id, args.table_persona)
