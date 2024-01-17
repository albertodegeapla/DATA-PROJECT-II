import streamlit as st
import folium

def create_folium_map(location):
    m = folium.Map(location=location, zoom_start=10)
    return m

def main():
    st.title("Streamlit App with Folium Map")

    # User input for location
    location_input = st.text_input("Enter location (latitude, longitude):")

    # Convert user input to a list of floats
    try:
        location = [float(coord.strip()) for coord in location_input.split(",")]
    except ValueError:
        st.warning("Invalid input. Please enter latitude and longitude separated by a comma.")
        return

    # Create a Folium map
    folium_map = create_folium_map(location)

    # Convert Folium map to HTML
    folium_map_html = folium_map._repr_html_()

    # Display the map using st
    st.write(folium_map_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
