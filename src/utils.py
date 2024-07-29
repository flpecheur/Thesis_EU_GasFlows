################
#   Imports    #
################
from entsog import EntsogPandasClient, parsers, mappings
import pandas as pd
import requests
import plotly.graph_objects as go # TO BE MOVED
import math


################
#   Mappings   #
################
countries = ['Italy', 'Austria', 'Germany', 'Hungary', 'Slovakia', 'Slovenia', 
             'Belgium', 'France', 'Luxemburg', 'Netherlands', 'Norway', 
             'United Kingdom', 'Bulgaria', 'Greece', 'North Macedonia', 'Romania', 
             'Serbia', 'Turkey', 'Croatia', 'Czechia', 'Poland', 'Denmark', 
             'Estonia', 'Finland', 'Latvia', 'Russia', 'Spain', 'Switzerland', 
             'Ukraine', 'Ireland', 'Albania', 'Libya', 'San Marino', 'Lithuania', 
             'Belarus', 'Portugal', 'Moldavia', 'Morocco']
country_codes = {
    'Italy': 'IT', 'Austria': 'AT', 'Germany': 'DE', 'Hungary': 'HU', 'Slovakia': 'SK', 
    'Slovenia': 'SI', 'Belgium': 'BE', 'France': 'FR', 'Luxemburg': 'LU', 
    'Netherlands': 'NL', 'Norway': 'NO', 'United Kingdom': 'UK', 'Bulgaria': 'BG', 
    'Greece': 'GR', 'North Macedonia': 'MK', 'Romania': 'RO', 'Serbia': 'RS', 
    'Turkey': 'TR', 'Croatia': 'HR', 'Czechia': 'CZ', 'Poland': 'PL', 'Denmark': 'DK', 
    'Estonia': 'EE', 'Finland': 'FI', 'Latvia': 'LV', 'Russia': 'RU', 'Spain': 'ES', 
    'Switzerland': 'CH', 'Ukraine': 'UA', 'Ireland': 'IE', 'Albania': 'AL', 
    'Libya': 'LY', 'San Marino': 'SM', 'Lithuania': 'LT', 'Belarus': 'BY', 
    'Portugal': 'PT', 'Moldavia': 'MD', 'Morocco': 'MA'
}
country_names = {v: k for k, v in country_codes.items()}

country_iso = {
    'Italy': 'ITA', 'Austria': 'AUT', 'Germany': 'DEU',
    'Hungary': 'HUN', 'Slovakia': 'SVK', 'Slovenia': 'SVN',
    'Belgium': 'BEL', 'France': 'FRA', 'Luxemburg': 'LUX',
    'Netherlands': 'NLD', 'Norway': 'NOR', 'United Kingdom': 'GBR',
    'Bulgaria': 'BGR', 'Greece': 'GRC', 'North Macedonia': 'MKD',
    'Romania': 'ROU', 'Serbia': 'SRB', 'Turkey': 'TUR',
    'Croatia': 'HRV', 'Czechia': 'CZE', 'Poland': 'POL',
    'Denmark': 'DNK', 'Estonia': 'EST', 'Finland': 'FIN',
    'Latvia': 'LVA', 'Russia': 'RUS', 'Spain': 'ESP',
    'Switzerland': 'CHE', 'Ukraine': 'UKR', 'Ireland': 'IRL',
    'Albania': 'ALB', 'Libya': 'LBY', 'San Marino': 'SMR',
    'Lithuania': 'LTU', 'Belarus': 'BLR', 'Portugal': 'PRT',
    'Moldavia': 'MDA', 'Morocco': 'MAR'
}
# Mapping country names to coordinates (latitude and longitude)
country_coords = {
    'Italy': {'lat': 41.8719, 'lon': 12.5674},
    'Austria': {'lat': 47.5162, 'lon': 14.5501},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'Hungary': {'lat': 47.1625, 'lon': 19.5033},
    'Slovakia': {'lat': 48.6690, 'lon': 19.6990},
    'Slovenia': {'lat': 46.1512, 'lon': 14.9955},
    'Belgium': {'lat': 50.5039, 'lon': 4.4699},
    'France': {'lat': 46.6034, 'lon': 1.8883},
    'Luxemburg': {'lat': 49.8153, 'lon': 6.1296},
    'Netherlands': {'lat': 52.1326, 'lon': 5.2913},
    'Norway': {'lat': 60.4720, 'lon': 8.4689},
    'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
    'Bulgaria': {'lat': 42.7339, 'lon': 25.4858},
    'Greece': {'lat': 39.0742, 'lon': 21.8243},
    'North Macedonia': {'lat': 41.6086, 'lon': 21.7453},
    'Romania': {'lat': 45.9432, 'lon': 24.9668},
    'Serbia': {'lat': 44.0165, 'lon': 21.0059},
    'Turkey': {'lat': 38.9637, 'lon': 35.2433},
    'Croatia': {'lat': 45.1, 'lon': 15.2},
    'Czechia': {'lat': 49.8175, 'lon': 15.4730},
    'Poland': {'lat': 51.9194, 'lon': 19.1451},
    'Denmark': {'lat': 56.2639, 'lon': 9.5018},
    'Estonia': {'lat': 58.5953, 'lon': 25.0136},
    'Finland': {'lat': 61.9241, 'lon': 25.7482},
    'Latvia': {'lat': 56.8796, 'lon': 24.6032},
    'Russia': {'lat': 55.4521, 'lon': 37.372}, # Moscow coordinates
    'Spain': {'lat': 40.4637, 'lon': -3.7492},
    'Switzerland': {'lat': 46.8182, 'lon': 8.2275},
    'Ukraine': {'lat': 48.3794, 'lon': 31.1656},
    'Ireland': {'lat': 53.1424, 'lon': -7.6921},
    'Albania': {'lat': 41.1533, 'lon': 20.1683},
    'Libya': {'lat': 26.3351, 'lon': 17.2283},
    'San Marino': {'lat': 43.9424, 'lon': 12.4578},
    'Lithuania': {'lat': 55.1694, 'lon': 23.8813},
    'Belarus': {'lat': 53.7098, 'lon': 27.9534},
    'Portugal': {'lat': 39.3999, 'lon': -8.2245},
    'Moldavia': {'lat': 47.4116, 'lon': 28.3699},
    'Morocco': {'lat': 31.7917, 'lon': -7.0926}
}

################
#   Methods    #
################

###### API tools ######

def my_query_operator_point_directions():
    base_url = "https://transparency.entsog.eu/api/v1/operatorpointdirections?limit=-1&timeZone=UCT"

    response = requests.get(base_url)
    # print(response.text)
    json, url = response.text, response.url
    data = parsers.parse_operator_points_directions(json)

    data['url'] = url

    return data

###### Data tools ######

def pairs_per_country(country,agg_df):
    """
    This function takes a country name as input and returns the number of pairs from that country in the dataset.
    """
    countA = agg_df[agg_df['countryA'] == country].shape[0]
    countB = agg_df[agg_df['countryB'] == country].shape[0]

    print(f'There are {countA} pairs from {country} as A.')
    print(f'There are {countB} pairs from {country} as B.')


###### buildDataPerPointType Tools ######
def filter_point_type(keyword,df,column):
    return df[df[column].str.contains(keyword)]

def initialize_lng_dict(lng_points_df):
    lng_dict={}
    process_point_data(lng_points_df,lng_dict)
    return lng_dict

def process_point_data(points_df,dict):
    """ 
    Pre : The points_df should contain the following coluns : point_label,coordinates,is_operational,Country
    """
    # Populate the dictionary
    for _, row in points_df.iterrows():
        point_key = row['point_key']
        dict[point_key] = {
            'point_label': row['point_label'],
            'coordinates': (row['lat'], row['lon']),
            'is_operational': row['is_operational'],
            'Country': row['Country'],
            'total_entries': [0] * 12,  # 12 months, initialized to 0
            'total_exits': [0] * 12     # 12 months, initialized to 0
        }

def process_monthly_data(dict,op_data, date_idx):
    """ 
    Pre : Month index is a two-digit string starting from 01 to 12.
    Post : Add operational data entries to the corresponding point_key entry in 
    the dictionnary
    """
    # Aggregate the entries and exits
    for _, row in op_data.iterrows():
        point_key = row['point_key']
        value = row['value']
        
        # Check flow direction and update accordingly
        if row['direction_key'] == 'entry':
            dict[point_key]['total_entries'][date_idx] += value
        elif row['direction_key'] == 'exit':
            dict[point_key]['total_exits'][date_idx] += value

def process_total_data(dict,dates,point_keys,directory="../data/opData"):
    """
    Pre : Dates is a list of dates following the same format used when encoding
    the csv files (ex : 2019_01, 2019,02,...)
    point_keys is the list of keys we want to process the data of
    Post : A dictionnary with point_key as keys containing point info and tha total 
    entries and exits for each month in the dates input
    """
    for date in dates:
        op_data = pd.read_csv(f'{directory}/op_data_{date}.csv')
        # print(op_data.columns)
        filtered_op_data = op_data[op_data['point_key'].isin(point_keys)]

        process_monthly_data(dict,filtered_op_data,int(date[-2:])-1)

def initialize_lng_dict(points_df):
    lng_dict = {}
    for _, row in points_df.iterrows():
        point_key = row['point_key']
        lng_dict[point_key] = {
            'point_label': row['point_label'],
            'coordinates': (row['lat'], row['lon']),
            'is_operational': row['is_operational'],
            'Country': row['Country'],
            'total_entries': [0] * 12,  # 12 months, initialized to 0
            'total_exits': [0] * 12     # 12 months, initialized to 0
        }
    return lng_dict

### Map Tools ### 
# TO BE MOVED

# Main map for country information
def create_initial_map(lng_dict, selected_country=None):
    fig = go.Figure()

    for point_key, point_data in lng_dict.items():
        color = 'blue' if point_data['is_operational'] else 'red'
        lat, lon = point_data['coordinates']
        opacity = 0.8 if selected_country is None or point_data['Country'] == selected_country else 0.3
        fig.add_trace(go.Scattergeo(
            lon=[lon],
            lat=[lat],
            text=point_data['point_label'],
            marker=dict(size=10, color=color, opacity=opacity),
            name=point_data['point_label'],
            customdata=[point_data['Country']]
        ))
    fig.update_layout(
        geo=dict(
            projection_type='mercator',
            showland=True,
            showcountries=True,
            landcolor='grey',
            subunitwidth=1,
            countrywidth=1,
            center={"lat": 50.5, "lon": 15.2551},  # Updated center coordinates
            projection_scale=5,  # Zoom level (adjust as necessary)
            subunitcolor='rgb(255, 255, 255)',
            countrycolor='rgb(255, 255, 255)',
        ),
        # width = 600,
        # height = 600
    )
    return fig

#### mapPairs tools ####

import math

def compute_bearing(fromCoords, toCoords):
    """
    Compute the bearing from `fromCoords` to `toCoords`.

    Parameters:
    - fromCoords: tuple of (longitude, latitude) for the starting point
    - toCoords: tuple of (longitude, latitude) for the destination point

    Returns:
    - bearing: angle in degrees from the starting point to the destination point
    """
    # lon1, lat1 = map(math.radians, fromCoords)
    # lon2, lat2 = map(math.radians, toCoords)

    # dlon = lon2 - lon1

    # x = math.sin(dlon) * math.cos(lat2)
    # y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)

    # bearing = math.atan2(x, y)
    # bearing = math.degrees(bearing)
    # bearing = (bearing + 360) % 360  # Normalize to 0-360 degrees
    # bearing = bearing - 90  # Adjust for the starting point (0 degrees is North)
    lon1, lat1 = fromCoords
    lon2, lat2 = toCoords
    
    # Compute differences
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    
    # Calculate the angle in radians
    angle_rad = math.atan2(delta_lat, delta_lon)
    
    # Convert the angle to degrees
    angle_deg = math.degrees(angle_rad)
    
    # Add a 90-degree rotation to the left
    adjusted_angle_deg = (angle_deg - 180) % 360
    bearing = adjusted_angle_deg

    return bearing
