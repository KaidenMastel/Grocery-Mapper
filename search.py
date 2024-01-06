import requests


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
            for place in data['elements']:
                print(place)
        else:
            print("No results found.")
            search_overpass(latitude,longitude,radius*1.5,store)

    else:
        print(f"Error: {response.status_code}")

# Example coordinates
latitude = 53.5269
longitude = -113.5

# Specify the radius (in meters) for the search
radius = 100000

# Call the function to search for Walmart within the specified radius using Overpass API
search(latitude, longitude, radius, "Safeway")
