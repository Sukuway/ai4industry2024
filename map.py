import folium
from geopy.distance import geodesic

def generate_map(points: list, map_name: str = 'map.html'):
    latitudes = [coord[0] for coord in points]
    longitudes = [coord[1] for coord in points]
    center = (sum(latitudes) / len(points), sum(longitudes) / len(points))

    max_radius = max(geodesic(center, coord).meters for coord in points)

    map = folium.Map(location=center, zoom_start=12)

    folium.Circle(
        location=center,
        radius=max_radius,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(map)

    map.save(map_name)