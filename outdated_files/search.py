import requests
from math import radians, sin, cos, sqrt, atan2


def search(latitude, longitude, radius, store):
    # Overpass API query to find specific amenities (e.g., Walmart) within a radius
    overpass_query = f"""
        [out:json];
        (
            way["name"="{store}"](around:{radius},{latitude},{longitude});
        );
        out center;
    """

    # Make the Overpass API request
    overpass_url = "https://overpass-api.de/api/interpreter"
    response = requests.post(overpass_url, data={'data': overpass_query}, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        if data['elements']:
            # Process the data to extract information about each place
            return data['elements']
        else:
            print("No results found.")

    else:
        print(f"Error: {response.status_code}")

# Example coordinates
latitude = 53.5269
longitude = -113.5

# Specify the radius (in meters) for the search
radius = 100000

# Call the function to search for Walmart within the specified radius using Overpass API

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth specified by latitude and longitude in decimal degrees.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    radius_of_earth = 6371  # Radius of Earth in kilometers

    # Distance in kilometers
    distance = radius_of_earth * c

    return distance

def find_closest_store(json_list, lat_param, lon_param):
    """
    Find the JSON object with the smallest distance from specified latitude and longitude parameters
    in the list of JSON objects.

    Parameters:
    - json_list: List of JSON objects with 'lat' and 'lon' fields.
    - lat_param: Latitude parameter for distance calculation.
    - lon_param: Longitude parameter for distance calculation.

    Returns:
    - closest_object: JSON object with the smallest distance.
    """
    closest_object = None
    min_distance = float('inf')  # Initialize with a large value

    if json_list == None:
        return None

    for json_obj in json_list:
        if 'center' in json_obj:
            coords = json_obj['center']
            if 'lat' in coords and 'lon' in coords:
                lat = coords['lat']
                lon = coords['lon']
                distance = haversine(lat_param, lon_param, lat, lon)

                if distance < min_distance:
                    min_distance = distance
                    closest_object = json_obj

    return closest_object
    

def distance_and_price_to_score(distance, price):
    return price + distance * 0.00005

best_of_each_store = []
best_of_each_store.append(find_closest_store(search(latitude, longitude, radius, "Safeway"), latitude, longitude))
best_of_each_store.append(find_closest_store(search(latitude, longitude, radius, "Walmart"), latitude, longitude))
best_of_each_store.append(find_closest_store(search(latitude, longitude, radius, "Costco"), latitude, longitude))
best_of_each_store.append(find_closest_store(search(latitude, longitude, radius, "Loblaws"), latitude, longitude))
