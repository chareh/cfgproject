import pandas as pd 
import folium
from folium.plugins import HeatMap
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

onlypedals.to_csv('/users/charlotte1/documents/cfgproject/datanew.csv')

eastings = onlypedals['Easting']
northings = onlypedals['Northing']
converted_coords = convert_lonlat(eastings, northings)

df = pd.DataFrame(list(converted_coords), index=['Y', 'X'])
df2 = df.T    
df2.to_csv('convertedcoords.csv')

a = pd.read_csv('/users/charlotte1/documents/cfgproject/datanew.csv')
b = pd.read_csv('/users/charlotte1/documents/cfgproject/convertedcoords.csv')
data2 = pd.concat([a, b], axis =1)
data2.to_csv('finaldata.csv')

cyclemap = folium.Map(location = [51.5074, -0.1278],
                  tiles='CartoDB positron',
                  zoom_start = 11, 
                  width = 600, height = 400)

cycleincidences = pd.read_csv('/users/charlotte1/documents/cfgproject/finaldata.csv')

heat_map = HeatMap(zip(cycleincidences.X.values, cycleincidences.Y.values), 
                   min_opacity=0.2,
                   radius=10, blur=15, 
                   max_zoom=10, 
                 )
cyclemap.add_child(heat_map)
cyclemap.save('cyclesmap43.html')