import numpy as np
import pandas as pd

# read in data
df = pd.read_csv('data/DataSample.csv', skipinitialspace=True)
pois = pd.read_csv('data/POIList.csv', skipinitialspace=True)

# 1. Cleanup
df = df.drop_duplicates(['TimeSt', 'Latitude', 'Longitude'])
pois = pois.drop_duplicates(['Latitude', 'Longitude'])
pois = pois.rename({'Latitude': 'Latitude_POI', 'Longitude':'Longitude_POI'}, axis=1)

# 2. Label
df_len = len(df.index)
pois_len = len(pois.index)
df = pd.concat([df] * pois_len, ignore_index=True)
pois = pd.concat([pois] * df_len, ignore_index=True)
df = df.sort_values(by=['_ID'])
df = df.reset_index(drop=True)
joined = df.join(pois)

# convert lat & long values to radians
joined['Latitude_Radian'] = np.radians(joined['Latitude'])
joined['Longitude_Radian'] = np.radians(joined['Longitude'])
joined['Latitude_POI_Radian'] = np.radians(joined['Latitude_POI'])
joined['Longitude_POI_Radian'] = np.radians(joined['Longitude_POI'])

# apply formula to calculate distance between each POI 
# and every location, vectorized
# 6367 is Earth's radius in km
joined['Distance'] = (
    np.arcsin(np.sqrt(
        np.sin((joined['Latitude_Radian'] - joined['Latitude_POI_Radian']) / 2) ** 2 + 
        np.cos(joined['Latitude_Radian']) * 
        np.cos(joined['Latitude_POI_Radian']) * 
        np.sin((joined['Longitude_Radian'] - joined['Longitude_POI_Radian']) / 2) ** 2
    )) * 6367 * 2
)

# groupby to find out the closest POI for every location
joined['Distance_Min'] = joined.groupby(['_ID'])['Distance'].transform('min')

# 3. Analysis
# groupby to find out the average and std for every POI
grouped = pd.DataFrame()
grouped['Distance_Avg'] = joined.groupby(['POIID'])['Distance'].min()
grouped['Distance_Std'] = joined.groupby(['POIID'])['Distance'].std()

# find the maximum distance for each POI, use it as
# radius. this will include
# all of its assigned locations
grouped['Distance_Max'] = joined.groupby(['POIID'])['Distance'].max()
grouped['Location_Count'] = joined.groupby(['POIID'])['Distance'].size()
grouped['Area'] = (grouped['Distance_Max'] ** 2) * np.pi
grouped['Density'] = grouped['Location_Count'] / grouped['Area']

# output data
joined.to_csv('joined.csv')
grouped.to_csv('grouped.csv')

