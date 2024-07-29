######################
#    Imports & cst   #
######################

import pandas as pd
import os 
from utils import filter_point_type

DATE = '2019_01'
DIR = 'FINAL'
        

######################
#    Data Loading    #
######################
points_df = pd.read_csv(f'{DIR}/data/points_data.csv')
# op_data = pd.read_csv(f'../data/opData/op_data_{DATE}.csv')
lng_points_info = pd.read_excel(f'{DIR}/data/points/LNG_points_info.xlsx')
lng_points_info.rename(columns={'points_label':'point_label','LNG Entry Point':'mapped_name','Longitude':'lon','Latitude':'lat'},inplace=True)


######################
#    Data Processing #
######################

 ### Filtering LNG and Transmission points
trans_points_df = filter_point_type("Transmission",points_df,'point_type')
lng_points_df = filter_point_type("LNG",points_df,'point_type')

print(f"Total points : {len(points_df)}")
print(f"Transmission points : {len(trans_points_df)}")
print(f"LNG points : {len(lng_points_df)}")

### Add LNG points information
# Fix lon,lat from faulty excel file
lng_points_info['lat'] = lng_points_info['lat'].apply(lambda x: x/1000 if x>=0 else x)
lng_points_info['lon'] = lng_points_info['lon'].apply(lambda x: x/1000 if x>=0 else x)

lng_points_df = lng_points_df.merge(lng_points_info[['point_label','mapped_name','Country', 'lat', 'lon','is_operational']], on='point_label', how='left')
lng_points_df = lng_points_df[lng_points_df['Country'].notna()]

### LNG Operational data
# lng_keys = lng_points_df['point_key'].unique()
# lng_op_data = op_data[op_data['point_key'].isin(lng_keys)]
# op_lng_keys = lng_op_data['point_key'].unique()

### Save data
lng_points_df.to_csv(f'{DIR}/data/points/lng_points.csv',index=False)
print("lng_points_df saved in DIR/data/points/lng_points.csv")
