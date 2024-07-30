import pandas as pd
import pandas as pd
import os
import json
from buildDataPerCountry import add_country_info, filter_data, merge_data, rename_columns

YEAR = 2019

current_dir = os.getcwd()
DIR = f"{current_dir}"
DATA_DIR = f"{DIR}/data"
DATA_DICT = {}
DATES_2019 = ["2019_01",'2019_02','2019_03','2019_04','2019_05','2019_06','2019_07','2019_08','2019_09','2019_10','2019_11','2019_12']
DATES_2023 = ["2023_01",'2023_02','2023_03','2023_04','2023_05','2023_06','2023_07','2023_08','2023_09','2023_10','2023_11','2023_12']

dates = DATES_2019 if YEAR == 2019 else DATES_2023

###############
#   MAPPINGS  #
###############
COUNTRY_COORDS = {
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


##################
# Import data   # NO MORE NEEDED
##################
# agg_pairs_df = pd.read_csv(f'FINAL/data/perCountry_V2/aggregated_data_{DATE}.csv')
# agg_pairs_df = agg_pairs_df.rename(columns={'Unnamed: 0': 'pairID','entryValue':'Entries','exitValue':'Exits'})


################
#   Helpers    #
# ##############
def load_op_data(date):
    """
    Load the operator data for a given date
    """
    op_df = pd.read_csv(f'{DATA_DIR}/opData/op_data_{date}.csv')
    return op_df

def load_points_data():
    points_df = pd.read_csv(f"{DATA_DIR}/points_data.csv")
    operator_points_directions_df = pd.read_csv(f"{DATA_DIR}/operator_points_dir.csv")
    interconnections_df = pd.read_csv(f'{DATA_DIR}/interconnections_data.csv')
    return points_df, operator_points_directions_df,interconnections_df

def filter_keyword(keyword,df,column):
    return df[df[column].str.contains(keyword)]

def get_coords(country):
    """ 
    Return (lat,lon) based on the country coords dictionnary (arbitrary centrer per country)
    """
    return COUNTRY_COORDS[country]['lat'], COUNTRY_COORDS[country]['lon'] 

def aggregate_data(filtered_df):
    """ 
    Aggregate filtered operational data by pair of country and direction
    """
    entries_df = filtered_df[filtered_df['directionKey'] == 'entry']
    exits_df = filtered_df[filtered_df['directionKey'] == 'exit']

    # Group by Pair of countries
    relevant_columns = ['fromCountryLabel', 'toCountryLabel', 'value']

    grouped_entries_df = entries_df[relevant_columns].groupby(['fromCountryLabel','toCountryLabel']).sum().reset_index()
    grouped_exits_df = exits_df[relevant_columns].groupby(['fromCountryLabel','toCountryLabel']).sum().reset_index()

    grouped_entries_df.rename(columns={'value': 'entryValue'}, inplace=True)
    grouped_exits_df.rename(columns={'value': 'exitValue'}, inplace=True)

    # Merge entries and exits data
    combined_df = pd.merge(grouped_entries_df, grouped_exits_df, 
                        on=['fromCountryLabel', 'toCountryLabel'], 
                        how='outer').fillna(0)

    combined_df['totalFlow'] = combined_df['entryValue'] - combined_df['exitValue']

    return combined_df

def combine_pairs(aggregated_df):
    """ 
    Args : aggregated_df is a dataframe with the columns formCountryLabel, toCountryLabel, entryValue, exitValue
    Remove inter-country pairs (country A to country A)
    """
    df = aggregated_df.copy()
    df['pairKey'] = df.apply(lambda row: tuple(sorted([row['fromCountryLabel'],row['toCountryLabel']])), axis=1)

    # Group by the pair_key and compute aggregated values
    aggregated_df = df.groupby('pairKey').agg({
        'entryValue': 'sum',
        'exitValue': 'sum',
        'totalFlow': 'sum'
    }).reset_index()

    # Split the pair_key back into fromCountry and toCountry
    aggregated_df[['fromCountryLabel', 'toCountryLabel']] = pd.DataFrame(aggregated_df['pairKey'].tolist(), index=aggregated_df.index)
    aggregated_df.drop(columns='pairKey', inplace=True)

    aggregated_df = aggregated_df[['fromCountryLabel', 'toCountryLabel', 'entryValue', 'exitValue', 'totalFlow']]
    filtered_df = aggregated_df[aggregated_df['fromCountryLabel'] != aggregated_df['toCountryLabel']]

    return filtered_df

def get_data_for_country(aggregated_df,country):
    """" 
    Pre : Aggregated_df contains the columns ['fromCountryLabel', 'toCountryLabel', 'entryValue', 'exitValue', 'totalFlow']
    Post : Returns the data for the given country
    """
    return aggregated_df[(aggregated_df['fromCountryLabel'] == country) | (aggregated_df['toCountryLabel'] == country)]

def process_data(date,points_df,interconnections_df):
    """ 
    Main function to process the operational data and create aggregated files.
    Final dataset contains the columns ['fromCountryLabel', 'toCountryLabel', 'entryValue', 'exitValue', 'totalFlow']
    """
    # print(f"Processing data for {date}...")
    operational_df = load_op_data(date)
    rename_columns(points_df, operational_df)
    merged_df = merge_data(operational_df, points_df, interconnections_df)
    filtered_df = filter_data(merged_df)
    # filtered_df = add_country_info(filtered_df) # NOT NECESSARY
    aggregated_df = aggregate_data(filtered_df)
    # percountry_flow_df = aggregate_percountry(aggregated_df)
    agg_pairs_df = combine_pairs(aggregated_df)
    # save_data(aggregated_df, percountry_flow_df, date)
    # print(f"Processing complete for {date}")

    return agg_pairs_df

def interpolate_coords(coord1, coord2, ratio=2/3):
    """Interpolates coordinates between coord1 and coord2 based on the given ratio."""
    lon1, lat1 = coord1['lon'], coord1['lat']
    lon2, lat2 = coord2['lon'], coord2['lat']
    # print(f"Interpolating between {coord1} and {coord2}")
    lon = lon1 + (lon2 - lon1) * ratio
    lat = lat1 + (lat2 - lat1) * ratio
    return dict(lon=lon, lat=lat)

def fill_dict(date,agg_pairs_df,data_dict):
    """ 
    Given the final operational aggregated data,
    For each pair of 'fromCountryLabel', 'toCountryLabel' encountered,
    if not already in the dict:
    - you must itinialize the key pair (a tuple of both labels)
    and create 3 parameters for total entries, exits and flow that each contain an array of 
    size 12.
    - Add the longitude and latitude of the two countries in the pair as 'fromCoords' and 'toCoords'
    For example, for month X we must set ['entries'][X] to agg_pairs_df['entriesValue']

    """
    month_index = int(date[-2:])-1
    print(f"... Saving data for {date} to data_dict")
    for _, row in agg_pairs_df.iterrows():
        from_country = row['fromCountryLabel']
        to_country = row['toCountryLabel']
        pair_key = (from_country, to_country)
        
        if pair_key not in data_dict:
            from_coords = COUNTRY_COORDS[from_country]
            to_coords = COUNTRY_COORDS[to_country]
            from_coords_adj = interpolate_coords(from_coords, to_coords, 5/6)
            to_coords_adj = interpolate_coords(to_coords, from_coords, 5/6)


            data_dict[pair_key] = {
                'entries': [0] * 12,
                'exits': [0] * 12,
                'totalFlow': [0] * 12,
                'fromCoords': from_coords_adj,
                'toCoords': to_coords_adj
            }
        
        data_dict[pair_key]['entries'][month_index] = row['entryValue']
        data_dict[pair_key]['exits'][month_index] = row['exitValue']
        data_dict[pair_key]['totalFlow'][month_index] = row['entryValue'] - row['exitValue']

def build_dict(dates):
    points_df, _, interconnections_df = load_points_data()
    trans_points = filter_keyword('Transmission',points_df,'point_type')

    data_dict = {}
    for date in dates:
        agg_pairs_df = process_data(date,trans_points,interconnections_df)

        fill_dict(date,agg_pairs_df,data_dict)
    return data_dict

if __name__ == "__main__":
    points_df, _, interconnections_df = load_points_data()
    trans_points = filter_keyword('Transmission',points_df,'point_type')
    
    data_dict = {}
    for date in dates:
        agg_pairs_df = process_data(date,trans_points,interconnections_df)

        fill_dict(date,agg_pairs_df,data_dict)
        



# # Expanded example data
# data = {
#     'fromCountryLabel': ['Estonia', 'Finland', 'Latvia', 'Russia', 'Russia', 'Russia', 'Russia', 'Russia', 'Ukraine',
#                          'Germany', 'Germany', 'France', 'France', 'Italy', 'Italy', 'Spain', 'Spain'],
#     'toCountryLabel': ['Russia', 'Russia', 'Russia', 'Estonia', 'Finland', 'Latvia', 'Lithuania', 'Ukraine', 'Russia',
#                        'France', 'Poland', 'Germany', 'Italy', 'Germany', 'France', 'France', 'Italy'],
#     'Entries': [2.270703e+08, 0.000000e+00, 7.496338e+07, 2.270703e+08, 1.087223e+09, 7.496338e+07, 0.000000e+00, 2.923028e+10, 0.000000e+00,
#                 5.000000e+09, 2.000000e+09, 6.000000e+09, 4.000000e+09, 3.500000e+09, 2.500000e+09, 4.500000e+09, 3.000000e+09],
#     'Exits': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -6.36912274e+08, 0.0, 0.0,
#               -4.500000e+09, -1.500000e+09, -5.500000e+09, -3.500000e+09, -3.000000e+09, -2.000000e+09, -4.000000e+09, -2.500000e+09]
# }
# df = pd.DataFrame(data)

# # Compute the total flow
# df['totalFlow'] = df['Entries'] + df['Exits']

# # Country coordinates
# country_coords = {
#     'Estonia': {'lat': 58.5953, 'lon': 25.0136},
#     'Finland': {'lat': 61.9241, 'lon': 25.7482},
#     'Latvia': {'lat': 56.8796, 'lon': 24.6032},
#     'Russia': {'lat': 61.5240, 'lon': 105.3188},
#     'Lithuania': {'lat': 55.1694, 'lon': 23.8813},
#     'Ukraine': {'lat': 48.3794, 'lon': 31.1656},
#     'Germany': {'lat': 51.1657, 'lon': 10.4515},
#     'France': {'lat': 46.6034, 'lon': 1.8883},
#     'Poland': {'lat': 51.9194, 'lon': 19.1451},
#     'Italy': {'lat': 41.8719, 'lon': 12.5674},
#     'Spain': {'lat': 40.4637, 'lon': -3.7492}
# }

# # Function to add flow arrows
# def add_flow_arrows(df, fig, country_coords):
#     for i in range(len(df)):
#         from_country = df['fromCountryLabel'][i]
#         to_country = df['toCountryLabel'][i]
#         fig.add_trace(go.Scattergeo(
#             locationmode='country names',
#             lon=[country_coords[from_country]['lon'], country_coords[to_country]['lon']],
#             lat=[country_coords[from_country]['lat'], country_coords[to_country]['lat']],
#             mode='lines+markers',
#             line=dict(width=2, color='blue' if df['Entries'][i] > 0 else 'red'),
#             marker=dict(size=5),
#             name=f"{from_country} to {to_country}"
#         ))


# # Create the base map
# fig = go.Figure()

# # Function to add flow arrows
# def add_flow_arrows(df, fig):
#     for i in range(len(df)):
#         fig.add_trace(go.Scattergeo(
#             locationmode='country names',
#             lon=[df['fromCountryLabel'][i], df['toCountryLabel'][i]],
#             lat=[df['fromCountryLabel'][i], df['toCountryLabel'][i]],
#             mode='lines+markers',
#             line=dict(width=2, color='blue' if df['totalFlow'][i] > 0 else 'red'),
#             marker=dict(size=5),
#             name=f"{df['fromCountryLabel'][i]} to {df['toCountryLabel'][i]}"
#         ))

# # Add flow arrows
# add_flow_arrows(df, fig)

# # Add the color scale for total flow
# fig.update_traces(marker=dict(color=df['totalFlow'], colorscale='Viridis', cmin=df['totalFlow'].min(), cmax=df['totalFlow'].max()))

# # Update layout to center the map and position the color scale
# fig.update_geos(
#     visible=True,
#     resolution=50,
#     showcoastlines=True,
#     showcountries=True,
#     coastlinecolor="Black",
#     countrywidth=0.5,
#     showland=True,
#     landcolor="white",
#     showocean=True,
#     oceancolor="lightblue",
#     projection_type="mercator",
#     center=dict(lat=50.5, lon=15.2551),
#     projection_scale=5
# )

# # Adjust the color bar position
# fig.update_layout(
#     title_text="Gas Flow Exchanges Between Countries",
#     coloraxis_colorbar=dict(
#         title="Total Flow",
#         tickvals=[df['totalFlow'].min(), df['totalFlow'].max()],
#         ticks="outside",
#         # lenmode="fraction",
#         # len=0.75,
#         # yanchor="middle",
#         # y=0.5,
#         # xanchor="left",
#         # x=1.05
#     )
# )

# # Show the figure
# fig.show()
