import streamlit as st
import folium

def main():
    st.title("Streamlit App with Folium Map")

    # Create a Folium map centered on Liberty Bell
    m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)

    # Add a marker for Liberty Bell
    folium.Marker(
        location=[39.949610, -75.150282],
        popup="Liberty Bell",
        tooltip="Liberty Bell"
    ).add_to(m)

    # Display the Folium map using st
    folium_static(m)

if __name__ == "__main__":
    main()