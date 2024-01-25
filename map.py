import folium
from geopy.distance import geodesic

coordinates = [(47.9959368, 2.7633018), (47.967906, 3.018118), (47.9480331, 2.8704895),(47.9980331, 3.2704895), ]

latitudes = [coord[0] for coord in coordinates]
longitudes = [coord[1] for coord in coordinates]
centre = (sum(latitudes) / len(coordinates), sum(longitudes) / len(coordinates))

rayon_max = max(geodesic(centre, coord).meters for coord in coordinates)

ma_carte = folium.Map(location=centre, zoom_start=12)

folium.Circle(
    location=centre,
    radius=rayon_max,
    color='red',
    fill=True,
    fill_color='red'
).add_to(ma_carte)

ma_carte.save('ma_carte_cercle_englobant.html')