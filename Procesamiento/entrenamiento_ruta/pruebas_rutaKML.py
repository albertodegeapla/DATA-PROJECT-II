import re

# Load the KML file
kml_file_path = "Indicaciones de Gran Azul, Avenida de Aragón, Valencia a Colegio Guadalaviar, Avenida de Blasco Ibáñez, Valencia.kml"  # Replace with the actual filename

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

    # Print the formatted coordinates array
    print("Formatted Coordinates [y, x]:")
    for point in formatted_coordinates:
        print(point)
else:
    print("No coordinates found in the KML file.")
