import pandas as pd 
import folium
from folium.plugins import MarkerCluster

cycleincidences = pd.read_csv('/users/charlotte1/documents/cfgproject/finaldata.csv')

cyclemap = folium.Map(location = [51.5074, -0.1278],
                      tiles='CartoDB positron',
                      zoom_start = 11, 
                      width = 800, height = 600)

marker_cluster = MarkerCluster().add_to(cyclemap)

for each in cycleincidences.iterrows():
     folium.Marker(
        location = [each[1]['X'],each[1]['Y']]
        ).add_to(marker_cluster)
     
cyclemap.save('cyclesmap4.html')