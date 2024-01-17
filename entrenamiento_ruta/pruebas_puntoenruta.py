import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# Formula to calculate the distance between two GPS points
def haversine_distance(point1, point2):
    R = 6371000.0  # Radius of the Earth in meters

    lat1, lon1 = radians(point1[0]), radians(point1[1])
    lat2, lon2 = radians(point2[0]), radians(point2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

# Formula to know if a point is inside the range or not
def is_point_within_range(meeting_point, coordinates, range_meters):
    for coord in coordinates:
        distance = haversine_distance(meeting_point, coord)
        if distance <= range_meters:
            return True
    return False


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

meeting_point = [39.470286, -0.365151]

range_meters = 100

# Convert the coordinates to a DataFrame
df = pd.DataFrame(coordinates, columns=["LATITUDE", "LONGITUDE"])

# Display the DataFrame using st.dataframe
st.dataframe(df)

# Create a Folium map to add markers
m = folium.Map(location=[coordinates[0][0], coordinates[0][1]], zoom_start=15)

# Add markers to the Folium map using the DataFrame
for index, row in df.iterrows():
    folium.Marker(location=[row["LATITUDE"], row["LONGITUDE"]]).add_to(m)

# Check if the meeting point is within range of any coordinate
result = is_point_within_range(meeting_point, coordinates, range_meters)

# Print the result
if result:
    folium.Marker(
    location=meeting_point,
    popup="Meeting Point is in the route",
    icon=folium.Icon(color="green"),
).add_to(m)
else:
    folium.Marker(
    location=meeting_point,
    popup="Meeting Point is not in the route",
    icon=folium.Icon(color="red"),
).add_to(m)

# Display the Folium map using st_folium
st_folium(m)