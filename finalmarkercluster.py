import pandas as pd 
import folium
from folium.plugins import MarkerCluster
import os
import glob 
from convertbng.util import convert_lonlat

path =r'/users/charlotte1/documents/cfgproject/vehicleaccidents' 
allFiles = glob.glob(path + '/*.csv')
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_)
    df['filename'] = os.path.basename(file_)
    list_.append(df)
frame = pd.concat(list_)

frame.to_csv('cyclingdataframe.csv')

frame2 = frame[['Accident Ref.','Borough', 'Easting', 'Northing', 'Vehicle Type']].copy() 
df = frame2
onlypedals = df[df['Vehicle Type'].str.contains('Pedal')]

onlypedals.to_csv('datanew.csv')

eastings = onlypedals['Easting']
northings = onlypedals['Northing']
converted_coords = convert_lonlat(eastings, northings)

df = pd.DataFrame(list(converted_coords), index=['Y', 'X'])
df2 = df.T    
df2.to_csv('convertedcoords.csv')

a = pd.read_csv('/users/charlotte1/documents/datanew.csv')
b = pd.read_csv('/users/charlotte1/documents/convertedcoords.csv')
data2 = pd.concat([a, b], axis =1)
data2.to_csv('finaldata.csv')

cycleincidences = pd.read_csv('/users/charlotte1/documents/finaldata.csv')

cyclemap = folium.Map(location = [51.5074, -0.1278],
                      tiles='CartoDB positron',
                      zoom_start = 11, 
                      width = 800, height = 600)

marker_cluster = MarkerCluster().add_to(cyclemap)


for each in cycleincidences.iterrows():
     folium.Marker(
        location = [each[1]['X'],each[1]['Y']]
        ).add_to(marker_cluster)
     
cyclemap.save('cylesmap4.html')
