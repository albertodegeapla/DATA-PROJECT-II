
import xml.etree.ElementTree as ET
import json

file_path = "ruta_1.kml"

def cargar_coordenadas_desde_kml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    coordinates = []

    for coordinates_tag in root.findall('.//{http://www.opengis.net/kml/2.2}coordinates'):
        coordinates_text = coordinates_tag.text.strip()

        for coord_set in coordinates_text.split('\n'):
            lat, lon, _ = map(float, coord_set.split(','))
            coordinates.append((lat, lon))  

    return coordinates

coordenadas = cargar_coordenadas_desde_kml(file_path)

print("Coordenadas extraídas:")
for lat, lon in coordenadas:
    print(f"Latitud: {lat}, Longitud: {lon}")

#función convertir a json (id_coche etc .... )

def convertir_a_json(id_coche, coordenadas):
    # Construye un diccionario con la información
    datos_coche = {
        "id_coche": id_coche,
        "coordenadas": coordenadas,
    }

    # Convierte el diccionario a JSON
    json_coche = json.dumps(datos_coche, indent=2)  # indent para una salida más legible

    return json_coche

# Supongamos que tienes un identificador de coche (id_coche) y las coordenadas
id_coche =  str = string.ascii_letters + string.digits
vehicle_id = ''.join(secrets.choice(str) for _ in range(6))
coordenadas = cargar_coordenadas_desde_kml(file_path)

# Llama a la función para convertir a JSON
json_coche = convertir_a_json(id_coche, coordenadas)

# Muestra el JSON resultante
print("Datos del coche en formato JSON:")
print(json_coche)

#función pub_sub 