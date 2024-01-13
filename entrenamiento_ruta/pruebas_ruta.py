import os
import ogr
import geopandas as gpd
from shapely.geometry import Point, LineString

def load_kml(file_path):
    # Load KML file into a GeoDataFrame
    driver = ogr.GetDriverByName("KML")
    data_source = driver.Open(file_path, 0)
    
    # Read the first layer from the KML file
    layer = data_source.GetLayerByIndex(0)
    
    # Create a GeoDataFrame from the layer
    gdf = gpd.GeoDataFrame.from_features([feature for feature in layer])
    
    # Close the data source
    data_source = None
    
    return gdf

def create_meeting_point(lat, lon):
    # Create a Shapely Point for the meeting location
    meeting_point = Point(lon, lat)
    return meeting_point

def modify_route(driver_route, meeting_point):
    # Extract LineString geometry from the driver's route
    route_line = driver_route.geometry.iloc[0]

    # Find the nearest point on the route to the meeting point
    nearest_point = route_line.interpolate(route_line.project(meeting_point))

    # Split the route into two segments: before and after the meeting point
    route_before = LineString(route_line.coords[:route_line.coords.index(nearest_point.coords[0]) + 1])
    route_after = LineString(route_line.coords[route_line.coords.index(nearest_point.coords[0]):])

    # Create a new route including the meeting point
    new_route = route_before.union(LineString([nearest_point, meeting_point, nearest_point]))
    new_route = new_route.union(route_after)

    return new_route

if __name__ == "__main__":
    # Get the current working directory
    current_dir = os.getcwd()

    # Define the file name
    kml_file_name = "Indicaciones de Gran Azul, Avenida de Aragón, Valencia a Colegio Guadalaviar, Avenida de Blasco Ibáñez, Valencia.kml"

    # Construct the full path to the KML file
    kml_file_path = os.path.join(current_dir, kml_file_name)

    # Load driver's route from KML file
    driver_route = load_kml(kml_file_path)

    # Extract meeting point coordinates from the second Point geometry
    meeting_point_coordinates = (
        driver_route.geometry[2].x,  # longitude
        driver_route.geometry[2].y   # latitude
    )
    meeting_point = create_meeting_point(*meeting_point_coordinates)

    # Modify the driver's route to include the meeting point
    new_route = modify_route(driver_route, meeting_point)

    # Save the modified route to a new KML file
    new_route_gdf = gpd.GeoDataFrame(geometry=[new_route])
    
    # Construct the full path for the new KML file
    new_kml_file_name = "modified_driver_route.kml"
    new_kml_file_path = os.path.join(current_dir, new_kml_file_name)

    new_route_gdf.to_file(new_kml_file_path, driver="KML")

    print(f"Modified route saved to: {new_kml_file_path}")