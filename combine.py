import requests
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
import pandas as pd


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
radius = 50000

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

    return [closest_object, distance]

def distance_and_price_to_score(distance, price):
    return price + distance * 0.1

best_of_each_store = {}
best_of_each_store["Safeway"] = find_closest_store(search(latitude, longitude, radius, "Safeway"), latitude, longitude)
best_of_each_store["Walmart"] = find_closest_store(search(latitude, longitude, radius, "Walmart"), latitude, longitude)
best_of_each_store["Costco"] = find_closest_store(search(latitude, longitude, radius, "Costco"), latitude, longitude)
best_of_each_store["Loblaws"] = find_closest_store(search(latitude, longitude, radius, "Loblaws"), latitude, longitude)

data_name = "data\grocery_prices.xlsx"
data = pd.read_excel('data\grocery_prices.xlsx')

#print(data)

result = data[data['Food'] == 'eggs']

# for column in result:
#     #print(column)
#     print(result[column])

# print(data.iloc[0]['Costco'])

# 0 = Costco, 1 = Walmart, 2 = Safeway, 3 = Loblaws

# set an arbitrary minimum pruce
min_score = float("inf") #1000.0
stores = ["Costco", "Walmart", "Safeway", "Loblaws"]
best_store = ""
for store in stores:
    if best_of_each_store[store] == None:
        continue
    current_price = data.iloc[0][store]
    current_price = current_price.item()
    print(store)
    print(current_price)
    current_score = distance_and_price_to_score(best_of_each_store[store][1], current_price)
    print(best_of_each_store[store][1])
    print(current_score)
    if  current_price < min_score:
        min_score = current_score
        best_store = store

print(best_of_each_store[best_store])