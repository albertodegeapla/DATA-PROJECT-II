import re
import os

# Load the KML file
kml_file_path = "rutas\Indicaciones de Restaurante Marina Beach Club, Valencia a Plaza de España, Valencia.kml"  # Replace with the actual filename

with open(kml_file_path, 'r', encoding='utf-8') as file:
    kml_content = file.read()

# Extract coordinates using regular expression
coordinates_match = re.search(r'<coordinates>\s*([\s\S]*?)\s*</coordinates>', kml_content)

if coordinates_match:
    coordinates_text = coordinates_match.group(1)
    coordinates_list = [tuple(map(float, point.split(','))) for point in coordinates_text.split()]

    # Reorder and remove the third dimension (z)
    reordered_coordinates = [(point[1], point[0]) for point in coordinates_list]

    # Format coordinates with square brackets
    formatted_coordinates = [f"[{point[0]}, {point[1]}]" for point in reordered_coordinates]

else:
    print("No coordinates found in the KML file.")

# Open the file with an incrementing number in the filename
file_number = 1
file_path = f'ruta_{file_number:03d}.txt'

# Find the next available filename
while os.path.exists(file_path):
    file_number += 1
    file_path = f'ruta_{file_number:03d}.txt'

# Open the file in write mode, creating it
with open(file_path, 'w') as file:
    # Write each array element to a new line in the file
    for item in formatted_coordinates:
        file.write(f"{item}\n")