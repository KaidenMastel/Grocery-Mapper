import folium
import matplotlib.pyplot as plt
import pandas as pd

def main(inputs):
    start_location = [inputs['lat'], inputs['lon']] #[45.372, -121.6972]
    item = inputs['item']
    storename, store_location = get_best_store(item)

    # Create a folium map
    bounds = [start_location, store_location]
    m = folium.Map(location=get_center(start_location, start_location),
                   zoom_start=15, tiles=inputs['map_tile'])
    

    # Add markers to map

    folium.Marker(
        start_location, popup="<i>Your Location</i>", tooltip="You are here"
    ).add_to(m)
    folium.Marker(  # Marker with icon
        location=store_location,
        popup="The best store found",
        tooltip=storename,
        icon=folium.Icon(color=inputs['color'], icon="info-sign"),
    ).add_to(m)

    m.fit_bounds(bounds)

#     # # Add line shape
#     # lat_lng_points = [[45.372, -121.6972],
#     #                   [45.373, -121.6831],
#     #                   [45.371, -121.683]]
#     # folium.PolyLine(lat_lng_points,
#     #                 color=inputs['color'],
#     #                 tooltip="PolyLine",
#     #                 weight=5,  # line thickness
#     #                 opacity=0.8  # transparency
#     #                 ).add_to(m)

#     # # Add circle shape
#     # folium.Circle(
#     #     radius=100,
#     #     location=[45.372, -121.6972],
#     #     tooltip="Click on Circle",
#     #     popup="Circle",
#     #     color=inputs['color'],
#     #     fill=False,
#     # ).add_to(m)

    # Export folium map as HTML string
    map_html = m._repr_html_()

    return {"map": map_html}


def get_best_store(item):
    storename = "Costco"
    location = [45.371, -121.683]
    
    return storename, location

def get_center(start_location, store_location):
    center_lat = (start_location[0] + store_location[0]) / 2
    center_lon = (start_location[1] + store_location[1]) / 2
    return [center_lat, center_lon]