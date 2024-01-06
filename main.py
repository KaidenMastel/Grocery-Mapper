import folium


def main(inputs):
    # Create a folium map
    m = folium.Map(location=[0, -121.6972],
                   zoom_start=15, tiles=inputs['map_tile'])

    # Add markers to map
    folium.Marker(
        [45.372, -121.6972], popup="<i>Italic popup text</i>", tooltip="Click on Marker"
    ).add_to(m)
    folium.Marker(  # Marker with icon
        location=[45.371, -121.683],
        popup="<b>Bold popup text</b>",
        tooltip="Click on Marker",
        icon=folium.Icon(color=inputs['color'], icon="info-sign"),
    ).add_to(m)

    # Add line shape
    lat_lng_points = [[45.372, -121.6972],
                      [45.373, -121.6831],
                      [45.371, -121.683]]
    folium.PolyLine(lat_lng_points,
                    color=inputs['color'],
                    tooltip="PolyLine",
                    weight=5,  # line thickness
                    opacity=0.8  # transparency
                    ).add_to(m)

    # Add circle shape
    folium.Circle(
        radius=100,
        location=[45.372, -121.6972],
        tooltip="Click on Circle",
        popup="Circle",
        color=inputs['color'],
        fill=False,
    ).add_to(m)

    # Export folium map as HTML string
    map_html = m._repr_html_()

    return {"map": map_html}