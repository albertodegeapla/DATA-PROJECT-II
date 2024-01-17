from math import radians, sin, cos, sqrt, atan2

def haversine_distance(point1, point2):
    """
    Calculate the Haversine distance between two GPS points in meters.

    Parameters:
        point1 (list): Latitude and longitude of the first point, e.g., [lat1, lon1].
        point2 (list): Latitude and longitude of the second point, e.g., [lat2, lon2].

    Returns:
        float: Haversine distance in meters.
    """
    # Radius of the Earth in meters
    R = 6371000.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = radians(point1[1]), radians(point1[0])
    lat2, lon2 = radians(point2[1]), radians(point2[0])

    # Calculate differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate distance
    distance = R * c

    return distance

# Example usage
point1 = [-0.35902, 39.46939]
point2 = [-0.35569, 39.47562]

distance = haversine_distance(point1, point2)
print(f"The distance between Point 1 and Point 2 is approximately {distance:.2f} meters.")