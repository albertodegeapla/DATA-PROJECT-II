from google.cloud import pubsub_v1
import argparse
import json
import logging

'''
Para llamar a este codiog de python hay que llamarlo desde el terminal así : python --project_id ...
'''

parser = argparse.ArgumentParser(description=("Generador de Rutas y publicadas en pub/sub"))
parser.add_argument(
    "--project_id",
    required=True,
    help="Project ID de GCloud"
)
parser.add_argument(
    "--person_topic_name",
    required=True,
    help="Topic de GCloud de la persona"
)
parser.add_argument(
    "--car_topic_name",
    required=True,
    help="Topic de GCloud del coche"
)

args, opts = parser.parse_known_args()

class PubSubPersonMessage:

    def __init__(self, project_id, topic_person):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = project_id
        self.topic_name = topic_person
    
    def publishPersonMessage(self, message): 
        json_str = json.dumps(message)
        topic_path = self.publisher.topic_path(self.project_id, self.topic_name)
        publish = self.publisher.publish(topic_path, json_str.encode("utf-8"))
        publish.result()
        logging.info(f"{message['Nombre']} quiere realizar un viaje a las {message['hora_salida']}")

    def __exit__(self):
        self.publisher.transport.close()
        logging.info("Cerrando perosn Publisher")

class PubSubCarMessage:

    def __init__(self, project_id, topic_car):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = project_id
        self.topic_name = topic_car

    def publishCarMessage(self, message):
        json_str = json.dumps(message)
        topic_path = self.publisher.topic_path(self.project_id, self.topic_name)
        publish = self.publisher.publish(topic_path, json_str.encode("utf-8"))
        publish.result()
        logging.info(f"El coche {message['ID_coche']}, matricula {message['Matricula']} va ha realizar un viaje a las {message['hora_salida']} por {message['Precio']}€. Hay {message['Plazas']} plazas")

    def __exit__(self):
        self.publisher.transport.close()
        logging.info("Cerrando car Publisher") 


def gen_ruta_persona():

    ruta_persona = {
        'ID_persona': 1000,
        'Nombre': "Pedro",
        'Cartera': 10.00,
        'hora_salida': "17:25",
        'ruta_persona': [
            (-0.37927, 39.46897, 0),
            (-0.3792, 39.46905, 0),
            (-0.37913, 39.46915, 0),
            (-0.37896, 39.46938, 0),
            (-0.37889, 39.46947, 0),
            (-0.37882, 39.46956, 0),
            (-0.37864, 39.46981, 0),
            (-0.37805, 39.46962, 0),
            (-0.37769, 39.46951, 0),
            (-0.37684, 39.46925, 0),
            (-0.3767, 39.46923, 0),
            (-0.37609, 39.46923, 0),
            (-0.37589, 39.46917, 0),
            (-0.37579, 39.46916, 0),
            (-0.3757, 39.46915, 0),
            (-0.37554, 39.46914, 0),
            (-0.3755, 39.46915, 0),
            (-0.37483, 39.46914, 0),
            (-0.37432, 39.46915, 0),
            (-0.37408, 39.46916, 0),
            (-0.3739, 39.46916, 0),
            (-0.37234, 39.46917, 0),
            (-0.37229, 39.46917, 0),
            (-0.37224, 39.46916, 0),
            (-0.37221, 39.46916, 0),
            (-0.37218, 39.46916, 0),
            (-0.37216, 39.46915, 0),
            (-0.37211, 39.46914, 0),
            (-0.37202, 39.46909, 0),
            (-0.37178, 39.46925, 0),
            (-0.37142, 39.46951, 0),
            (-0.37112, 39.46973, 0),
            (-0.37105, 39.46979, 0),
            (-0.37037, 39.47033, 0),
            (-0.37002, 39.47026, 0),
            (-0.36855, 39.47026, 0),
            (-0.36819, 39.47025, 0),
            (-0.36705, 39.47024, 0),
            (-0.36534, 39.47021, 0),
            (-0.36523, 39.47021, 0),
            (-0.36547, 39.47061, 0),
            (-0.36529, 39.47066, 0),
            (-0.36523, 39.4707, 0),
            (-0.36517, 39.47072, 0),
            (-0.36512, 39.47075, 0),
            (-0.36433, 39.4711, 0),
            (-0.36355, 39.47144, 0),
            (-0.36345, 39.47148, 0),
            (-0.36336, 39.47152, 0),
            (-0.36333, 39.47154, 0),
            (-0.36329, 39.47155, 0),
            (-0.36319, 39.4716, 0),
            (-0.36308, 39.47167, 0),
            (-0.36297, 39.47174, 0),
            (-0.36271, 39.47186, 0),
            (-0.36294, 39.4723, 0),
            (-0.36301, 39.4724, 0),
            (-0.36311, 39.47254, 0)
            ]
    }

    return ruta_persona
    
def gen_ruta_coche():

    ruta_coche = {
        'ID_coche':2000,
        'Marca':"Nieto",
        'Matricula':"0000AAA",
        'Plazas':2,
        'Precio': 1.55,
        'hora_salida': "17:28",
        'ruta_coche': [
            (-0.37927, 39.46897, 0),
            (-0.3792, 39.46905, 0),
            (-0.37913, 39.46915, 0),
            (-0.37896, 39.46938, 0),
            (-0.37889, 39.46947, 0),
            (-0.37882, 39.46956, 0),
            (-0.37864, 39.46981, 0),
            (-0.37805, 39.46962, 0),
            (-0.37769, 39.46951, 0),
            (-0.37684, 39.46925, 0),
            (-0.3767, 39.46923, 0),
            (-0.37609, 39.46923, 0),
            (-0.37589, 39.46917, 0),
            (-0.37579, 39.46916, 0),
            (-0.3757, 39.46915, 0),
            (-0.37554, 39.46914, 0),
            (-0.3755, 39.46915, 0),
            (-0.37483, 39.46914, 0),
            (-0.37432, 39.46915, 0),
            (-0.37408, 39.46916, 0),
            (-0.3739, 39.46916, 0),
            (-0.37234, 39.46917, 0),
            (-0.37229, 39.46917, 0),
            (-0.37224, 39.46916, 0),
            (-0.37221, 39.46916, 0),
            (-0.37218, 39.46916, 0),
            (-0.37216, 39.46915, 0),
            (-0.37211, 39.46914, 0),
            (-0.37202, 39.46909, 0),
            (-0.37178, 39.46925, 0),
            (-0.37142, 39.46951, 0),
            (-0.37112, 39.46973, 0),
            (-0.37105, 39.46979, 0),
            (-0.37037, 39.47033, 0),
            (-0.37002, 39.47026, 0),
            (-0.36855, 39.47026, 0),
            (-0.36819, 39.47025, 0),
            (-0.36705, 39.47024, 0),
            (-0.36534, 39.47021, 0),
            (-0.36523, 39.47021, 0),
            (-0.36547, 39.47061, 0),
            (-0.36529, 39.47066, 0),
            (-0.36523, 39.4707, 0),
            (-0.36517, 39.47072, 0),
            (-0.36512, 39.47075, 0),
            (-0.36433, 39.4711, 0),
            (-0.36355, 39.47144, 0),
            (-0.36345, 39.47148, 0),
            (-0.36336, 39.47152, 0),
            (-0.36333, 39.47154, 0),
            (-0.36329, 39.47155, 0),
            (-0.36319, 39.4716, 0),
            (-0.36308, 39.47167, 0),
            (-0.36297, 39.47174, 0),
            (-0.36271, 39.47186, 0),
            (-0.36294, 39.4723, 0),
            (-0.36301, 39.4724, 0),
            (-0.36311, 39.47254, 0)
            ]
    }
    return ruta_coche




def run(project_id, topic_person, topic_car):

    try:
        person_publisher = PubSubPersonMessage(project_id, topic_person)
        message1: dict = gen_ruta_persona()
        person_publisher.publishPersonMessage(message1)
    except Exception as e:
        logging.error("Error while inserting data into ruta_persona Topic: %s", e)
    finally:
        person_publisher.__exit__()

    try:
        car_publisher = PubSubCarMessage(project_id, topic_car)
        message2: dict = gen_ruta_coche()
        car_publisher.publishCarMessage(message2)
    except Exception as e:
        logging.error("Error while inserting data into ruta_coche Topic: %s", e)
    finally:
        car_publisher.__exit__()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run(args.project_id, args.person_topic_name, args.car_topic_name)