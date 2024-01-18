import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import re

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
m = folium.Map(location=[df["LATITUDE"].iloc[0], df["LONGITUDE"].iloc[0]], zoom_start=15)

# Create a FeatureGroup for markers
markers_feature_group = folium.FeatureGroup(name="Markers")

# Add markers to the FeatureGroup
for index, row in df.iterrows():
    marker = folium.CircleMarker(location=[row["LATITUDE"], row["LONGITUDE"]], radius=5, color='#3498db', fill=True, fill_color='#3498db', fill_opacity=1)
    markers_feature_group.add_child(marker)

# Add the FeatureGroup to the Folium map
m.add_child(markers_feature_group)

# Display the Folium map using st_folium
st_folium(m)