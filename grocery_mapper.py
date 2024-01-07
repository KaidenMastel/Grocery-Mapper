import folium
import matplotlib.pyplot as plt
import pandas as pd
import mecsimcalc as msc
import requests
import numpy

def main(inputs):
    #get input variables
    start_location = [inputs['lat'], inputs['lon']]
    latitude = start_location[0]
    longitude = start_location[1]
    item = inputs['item']
    radius = inputs['radius']

    #Find closest store of each brand
    best_of_each_store = {}
    best_of_each_store["Safeway"] = find_closest_store(search(latitude, longitude, radius, "Safeway"), latitude, longitude)
    best_of_each_store["Walmart"] = find_closest_store(search(latitude, longitude, radius, "Walmart"), latitude, longitude)
    best_of_each_store["Costco"] = find_closest_store(search(latitude, longitude, radius, "Costco"), latitude, longitude)
    best_of_each_store["Loblaws"] = find_closest_store(search(latitude, longitude, radius, "Loblaws"), latitude, longitude)

    #Get the input file
    input_file = inputs['file']
    df = msc.input_to_dataframe(input_file)
    x = -1
    #1: costco, 2: Walmart, 3: Safeway, 4: Loblaws
    cols = [1, 2, 3, 4]
    df = df[df.columns[cols]]

    #Calculate which of the 4 brands has the best score
    min_score = float("inf") 
    stores = ["Costco", "Walmart", "Safeway", "Loblaws"]
    foods = {"Eggs": 0, "Chicken": 1, "Tomatoes": 2, "Rice": 3, "Bread": 4,
                "Milk": 5, "Fish": 6, "Broccoli": 7, "Apples": 8}
    best_store = ""
    for store in stores:
        if best_of_each_store[store] == None:
            continue
        #Gets the price for the store
        current_price = df.iloc[foods[item]][store]
        current_price = current_price.item()
        #Uses a combination of distance and price
        current_score = distance_and_price_to_score(best_of_each_store[store][1], current_price)
        if  current_price < min_score:
            min_score = current_score
            best_store = store
    #create the map
    m = folium.Map(location=get_center(start_location, start_location),
                   zoom_start=15, tiles=inputs['map_tile'])
    
    #If no store was found, kill the program early
    if best_store == "":
        folium.Marker(
        start_location, popup="<i>Your Location</i>", tooltip="Failed to find grocery store, use larger radius or different location"
        ).add_to(m)

        map_html = m._repr_html_()
        return {"map": map_html, "table": None, "plot": None}
    
    #Get the location of the best store
    store_location = [best_of_each_store[best_store][0]['center']['lat'], best_of_each_store[best_store][0]['center']['lon']]
    storename = best_store
    bounds = [start_location, store_location]

    # Add markers to map
    folium.Marker(
        start_location, popup="<i>Your Location</i>", tooltip="You are here"
    ).add_to(m)
    folium.Marker(
        location=store_location,
        popup="The best store found",
        tooltip=storename,
        icon=folium.Icon(color=inputs['color'], icon="info-sign"),
    ).add_to(m)

    m.fit_bounds(bounds)

    # Add line shape
    lat_lng_points = [start_location, store_location]
    folium.PolyLine(lat_lng_points,
                    color=inputs['color'],
                    tooltip="PolyLine",
                    weight=5,  # line thickness
                    opacity=0.8  # transparency
                    ).add_to(m)

    # Add circle shape
    folium.Circle(
        radius=radius,
        location=start_location,
        tooltip="Click on Circle",
        popup="Circle",
        color=inputs['color'],
        fill=False,
    ).add_to(m)

    # Export folium map as HTML string
    map_html = m._repr_html_()

    x = plot_data(inputs, best_store)

    return {"map": map_html, "table": x['table'], "plot": x['plot']}

#Gets the center of two locations
def get_center(start_location, store_location):
    center_lat = (start_location[0] + store_location[0]) / 2
    center_lon = (start_location[1] + store_location[1]) / 2
    return [center_lat, center_lon]


def plot_data(inputs, best):

    # get the input file
    input_file = inputs['file']

    # convert the input file to a dataframe
    df = msc.input_to_dataframe(input_file)
    x = -1
    if best == "CostCo":
        x = 1
    elif best == "Walmart":
        x = 2
    elif best == "Safeway":
        x = 3
    elif best == "Loblaws":
        x = 4
    #1: costco, 2: Walmart, 3: Safeway, 4: Loblaws
    print(df)
    cols = [0, x]
    df = df[df.columns[cols]]
    # covert the dataframe to an HTML table and generate a download link
    html_table, download_link = msc.print_dataframe(df, download=True)

    x=df["Food"]
    y=df[best]
    #plt.plot(x, y)
    plt.rcParams.update({'font.size': 5})
    plt.bar(x, y, width=0.3)
    # plt.bar(x, "Walmart", width=0.3)
    plt.xlabel("Food")
    plt.ylabel("Prices")
    plot_html = msc.print_plot(plt)

    return {
        # Return the HTML table
        "table": html_table,
        # Returns the HTML download link
        "download": download_link,"plot": plot_html
    }

from math import radians, sin, cos, sqrt, atan2


def search(latitude, longitude, radius, store):
    # Overpass API query to find retail stores within a radius
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

#Calculates distances from lattitude and longitude
def haversine(lat1, lon1, lat2, lon2):
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
    closest_object = None
    min_distance = float('inf') 
    #Make sure at least 1 store was found
    if json_list == None:
        return None
    
    #Loop to find closest store
    for json_obj in json_list:
        if 'center' in json_obj:
            coords = json_obj['center']
            if 'lat' in coords and 'lon' in coords:
                lat = coords['lat']
                lon = coords['lon']
                #Calculates distance using latitude and longitude
                distance = haversine(lat_param, lon_param, lat, lon)

                #find min distance
                if distance < min_distance:
                    min_distance = distance
                    closest_object = json_obj

    return [closest_object, distance]

#Formula for weights of price and distance
def distance_and_price_to_score(distance, price):
    return price + distance * 0.1