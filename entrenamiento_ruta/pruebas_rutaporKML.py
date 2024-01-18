import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import re
import time

# Load the KML file
kml_file_path = "Indicaciones de Restaurante Marina Beach Club, Valencia a Plaza de España, Valencia.kml"  # Replace with the actual filename

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
    formatted_coordinates = [[point[0], point[1]] for point in reordered_coordinates]

# Convert the coordinates to a DataFrame
df = pd.DataFrame(formatted_coordinates, columns=["LATITUDE", "LONGITUDE"])

# Display the DataFrame using st.dataframe
st.dataframe(df)

# Create a Folium map to add markers
m = folium.Map(location=[formatted_coordinates[0][0], formatted_coordinates[0][1]], zoom_start=15)

# Add markers to the Folium map using the DataFrame
for index, row in df.iterrows():
    folium.Marker(location=[row["LATITUDE"], row["LONGITUDE"]]).add_to(m)

# Add the car moving through the route each second
for index, row in df.iterrows():
    time.sleep(5)
    marker = folium.Marker(location=[row["LATITUDE"], row["LONGITUDE"]], icon=folium.Icon(color='green'))
    m._children = {}
    m.add_child(marker)

st_folium(m)