import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# List of coordinates (latitude, longitude)
coordinates = [
    [39.46939, -0.35902],
    [39.46949, -0.35889],
    [39.46958, -0.35876],
    [39.46962, -0.35871],
    [39.46969, -0.35865],
    [39.4698, -0.35858],
    [39.46992, -0.35849],
    [39.47013, -0.35842],
    [39.47014, -0.3584],
    [39.47015, -0.35839],
    [39.47018, -0.35837],
    [39.47019, -0.35836],
    [39.47021, -0.35835],
    [39.47024, -0.35834],
    [39.47027, -0.35834],
    [39.4703, -0.35834],
    [39.47033, -0.35837],
    [39.47035, -0.35839],
    [39.47038, -0.35834],
    [39.47043, -0.35827],
    [39.47048, -0.35822],
]

# Convert the coordinates to a DataFrame
df = pd.DataFrame(coordinates, columns=["LATITUDE", "LONGITUDE"])

# Display the DataFrame using st.dataframe
st.dataframe(df)

# Create a Folium map to add markers
m = folium.Map(location=[coordinates[0][0], coordinates[0][1]], zoom_start=15)

# Add markers to the Folium map using the DataFrame
for index, row in df.iterrows():
    folium.Marker(location=[row["LATITUDE"], row["LONGITUDE"]]).add_to(m)

# Display the Folium map using st_folium
st_folium(m)