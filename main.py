import folium


def main(inputs):
    
    start_location = [45.372, -121.6972]
    storename, store_location = get_best_store()

    # Create a folium map
    m = folium.Map(location=start_location,
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

    # # Add line shape
    # lat_lng_points = [[45.372, -121.6972],
    #                   [45.373, -121.6831],
    #                   [45.371, -121.683]]
    # folium.PolyLine(lat_lng_points,
    #                 color=inputs['color'],
    #                 tooltip="PolyLine",
    #                 weight=5,  # line thickness
    #                 opacity=0.8  # transparency
    #                 ).add_to(m)

    # # Add circle shape
    # folium.Circle(
    #     radius=100,
    #     location=[45.372, -121.6972],
    #     tooltip="Click on Circle",
    #     popup="Circle",
    #     color=inputs['color'],
    #     fill=False,
    # ).add_to(m)

    # Export folium map as HTML string
    map_html = m._repr_html_()

    return {"map": map_html}


def get_best_store():
    storename = "Costco"
    location = [45.371, -121.683]
    
    return storename, location