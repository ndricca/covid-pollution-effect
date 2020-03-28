import folium

from src.config import FOLIUM_CFG
from src.data.arpa.arpa_quality_raw_funcs import ArpaConnect, get_city_sensor_ids


def display_station_map(folium_map, sensor_registry):
    sensor_registry = sensor_registry[['idstazione','idsensore','nometiposensore', 'lat', 'lng']].reset_index(drop=True)
    sensor_registry['label'] = sensor_registry['idsensore'] + ": " + sensor_registry['nometiposensore']
    station_registry = sensor_registry.groupby(['idstazione', 'lat', 'lng'])['label'].apply(
        lambda x: "<b>sensori:</b><br>" + "<br>".join(list(x))).reset_index()
    station_registry.columns = ['idstazione', 'lat', 'lng', 'label']
    for _, row in station_registry.iterrows():
        test = folium.Html(row['label'], script=True)
        popup = folium.Popup(test, max_width=300, min_width=300)
        folium.Marker([row['lat'], row['lng']], popup=popup).add_to(folium_map)
    return folium_map





if __name__ == '__main__':
    arpa = ArpaConnect()
    sensor_data = get_city_sensor_ids(arpa=arpa, city='Milano')
    m = folium.Map(**FOLIUM_CFG)
    display_station_map(folium_map=m, sensor_registry=sensor_data)

