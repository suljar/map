import folium
import pandas

html = """<h4>Volcano information:</h4>
Height: %s m
"""
volcanoes = pandas.read_csv("Volcanoes.txt")
elev = list(volcanoes["ELEV"])
lat = list(volcanoes["LAT"])
lon = list(volcanoes["LON"])


def color_producer(elev):
    if elev < 1000:
        return "green"
    elif 1000 <= elev < 3000:
        return "orange"
    else:
        return "red"


# my map
map = folium.Map(location=[38.1041, -122.2566],
                 zoom_start=6, tiles="Stamen Terrain")

# creat featuregroup for volcanones
fgv = folium.FeatureGroup("VOLCANOES")
for ele, lat, lon in zip(elev, lat, lon):
    iframe = folium.IFrame(html=html % str(ele), width=200, height=100)
    # adding circles on the map using add_child
    fgv.add_child(folium.CircleMarker(
        [lat, lon], popup=folium.Popup(iframe), radius=8, fill_color=color_producer(ele), fill_apactiy=0.7, color='grey'))

# creat featuregroup for population
fgp = folium.FeatureGroup("POPULATION")
with open('world.json', 'r', encoding='utf-8-sig') as f:
    data = f.read()
    # categorize  countries based on population usin Geojson
    fgp.add_child(folium.GeoJson(data, style_function=lambda x: {
        'fillColor': "green" if x['properties']['POP2005'] < 10000000 else "orange" if 10000000 <= x['properties']['POP2005'] < 20000000 else "red"}))
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
