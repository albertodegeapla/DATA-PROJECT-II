import folium
import streamlit as st
from streamlit_folium import st_folium

# Center on Liberty Bell, add markers
m = folium.Map(location=[39.46939,-0.35902], zoom_start=16)

# Marker for Liberty Bell
folium.Marker(
    [39.46939,-0.35902], popup="01", tooltip="Localización"
).add_to(m)

second_location = [39.46949,-0.35889]
folium.Marker(
    second_location, popup="02", tooltip="Localización"
).add_to(m)

third_location = [39.46958,-0.35876,]
folium.Marker(
    third_location, popup="03", tooltip="Localización"
).add_to(m)

# Call to render Folium map in Streamlit
# Don't get any data back from the map (so that it won't rerun the app when the user interacts)
st_folium(m, width=725, returned_objects=[])
