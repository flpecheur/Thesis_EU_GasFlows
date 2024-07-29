import pandas as pd
import plotly.express as px
from plotly.colors import sequential

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# DOES NOT WORK ANYMOREEEE

DATE = "2019_01"


# Load the Agg dataset : source : FINAL/data/perCountry/agg_data_pairs_{DATE}.csv
agg_pairs_df = pd.read_csv(f'FINAL/data/perCountry_V2/aggregated_data_{DATE}.csv')

# MAPPINGS
# TODO : Source
# Cfr perplexity
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

agg_pairs_df.rename(columns={'fromCountryLabel': 'countryA', 'toCountryLabel': 'countryB'}, inplace=True)
agg_pairs_df.rename(columns={'entryValue':'totalEntries','exitValue':'totalExits','totalFlow':'totalFlow_init' })
# Adding coordinates to the aggregated dataframe
agg_pairs_df['LatA'] = agg_pairs_df['countryA'].map(lambda x: country_coords.get(x, {}).get('lat'))
agg_pairs_df['LonA'] = agg_pairs_df['countryA'].map(lambda x: country_coords.get(x, {}).get('lon'))
agg_pairs_df['LatB'] = agg_pairs_df['countryB'].map(lambda x: country_coords.get(x, {}).get('lat'))
agg_pairs_df['LonB'] = agg_pairs_df['countryB'].map(lambda x: country_coords.get(x, {}).get('lon'))

################
#  Helpers     #
################
# Helper function to create the flow data for plotly express
def create_flow_data(df, flow_column):
    flow_data = []
    for idx, row in df.iterrows():
        if pd.notnull(row['LatA']) and pd.notnull(row['LatB'])and row[flow_column] > 0:
            flow_data.append({
                'countryA': row['countryA'],
                'countryB': row['countryB'],
                'flow': row[flow_column],
                'lat': [row['LatA'], row['LatB']],
                'lon': [row['LonA'], row['LonB']]
            })
    return flow_data

# Function to normalize flow values to a 0-1 range
def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

# Adding a dummy trace for the color scale
def add_color_scale(fig, min_flow, max_flow):
    color_bar_trace = go.Scattergeo(
        lon=[None],
        lat=[None],
        mode='markers',
        marker=dict(
            colorscale=color_scale,
            cmin=min_flow,
            cmax=max_flow,
            colorbar=dict(
                title="Flow (kWh/d)",
                titleside="right",
                tickmode="array",
                tickvals=[min_flow, (min_flow + max_flow) / 2, max_flow],
                ticktext=[str(min_flow), str((min_flow + max_flow) / 2), str(max_flow)]
            ),
        ),
        hoverinfo='none'
    )
    fig.add_trace(color_bar_trace)

def build_total_flow_df(df):
    """ 
    Input: A dataframe with information about country, entries and exits
    
    """
    new_df = df.copy()
    # new_df.rename(columns={'country': 'countryCode','total_entries':'totalEntries','total_exits':'totalExits'}, inplace=True)

    # Add information about the total flow and country name
    new_df['totalFlow'] = new_df['totalEntries'] - new_df['totalExits']
    # new_df['countryName'] = new_df['countryCode'].map(country_names)
    new_df['countryISO'] = new_df['countryName'].map(country_iso)

    return new_df

def info_per_country(country,total_flow_df):
    
    """
    This function takes a country name as input and returns the total entries, total exits, and total flow for that country.
    """
    country_data = total_flow_df[total_flow_df['countryName'] == country]
    total_entries = country_data['totalEntries'].values
    total_exits = country_data['totalExits'].values
    total_flow = country_data['totalFlow'].values

    print(f'Total entries for {country}: {total_entries}')
    print(f'Total exits for {country}: {total_exits}')
    print(f'Total flow for {country}: {total_flow}')
################
#  MAPS        #
################

##### MAP 1 #####
# Define color scale
color_scale = sequential.Viridis

entry_flow_data = create_flow_data(agg_pairs_df, 'entryFlow')
exit_flow_data = create_flow_data(agg_pairs_df, 'exitFlow')

# Get the min and max values for entry and exit flows
min_flow = min(min([d['flow'] for d in entry_flow_data]), min([d['flow'] for d in exit_flow_data]))
max_flow = max(max([d['flow'] for d in entry_flow_data]), max([d['flow'] for d in exit_flow_data]))

# Create a Plotly Express scatter_geo figure for entry flows
fig_entry = px.scatter_geo(
    lat=[d['lat'][0] for d in entry_flow_data],
    lon=[d['lon'][0] for d in entry_flow_data],
    size=[d['flow'] for d in entry_flow_data],
    hover_name=[f"{d['countryA']} to {d['countryB']:} (entry)" for d in entry_flow_data],
    title='Total Gas Flow Entry in Europe'
)

# Add the flow lines for entry with color scaling
for d in entry_flow_data:
    norm_flow = normalize(d['flow'], min_flow, max_flow)
    color = color_scale[int(norm_flow * (len(color_scale) - 1))]
    fig_entry.add_trace(go.Scattergeo(
        locationmode='country names',
        lon=d['lon'],
        lat=d['lat'],
        mode='lines',
        line=dict(width=2, color=color),
        opacity=0.6,
        name=f"{d['countryA']} to {d['countryB']} : {d['flow']:.2e}(entry)",
        text=f"{d['countryA']} to {d['countryB']} Entry Flow: {d['flow']:.2e} kWh/d",
        hoverinfo='text'
    ))

# add_color_scale(fig_entry, min_flow, max_flow)

# Create a Plotly Express scatter_geo figure for exit flows
fig_exit = px.scatter_geo(
    lat=[d['lat'][0] for d in exit_flow_data],
    lon=[d['lon'][0] for d in exit_flow_data],
    size=[d['flow'] for d in exit_flow_data],
    hover_name=[f"{d['countryB']} to {d['countryA']} (exit)" for d in exit_flow_data],
    title='Total Gas Flow Exit in Europe'
)

# Add the flow lines for exit with color scaling
for d in exit_flow_data:
    norm_flow = normalize(d['flow'], min_flow, max_flow)
    color = color_scale[int(norm_flow * (len(color_scale) - 1))]
    fig_exit.add_trace(go.Scattergeo(
        locationmode='country names',
        lon=d['lon'],
        lat=d['lat'],
        mode='lines',
        line=dict(width=2, color=color),
        opacity=0.6,
        name=f"{d['countryB']} to {d['countryA']} : {d['flow']:.2e}(exit)",
        text=f"{d['countryB']} to {d['countryA']} Exit Flow: {d['flow']:.2e} kWh/d",
        hoverinfo='text'
    ))

# Customize the layout to show country borders and coastlines
for fig in [fig_entry, fig_exit]:
    fig.update_layout(
        geo=dict(
            scope='europe',
            projection_type='natural earth',
            showland=True,
            landcolor='whitesmoke',
            countrycolor='black',
            coastlinecolor='black',
            showcoastlines=True,
            showcountries=True,
            countrywidth=0.5,
        ),
        height=800,
        width=1000,
    )

fig_entry.show()
fig_exit.show()

fig_combined1 = make_subplots(rows=1, cols=1)
# Add all traces to the combined figure
for trace in fig_entry.data:
    fig_combined1.add_trace(trace)
for trace in fig_exit.data:
    fig_combined1.add_trace(trace)

fig_combined1.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="down",
            buttons=[
                dict(
                    args=["visible", [True] * len(fig_entry.data) + [False] * len(fig_exit.data)],
                    label="Entries",
                    method="restyle"
                ),
                dict(
                    args=["visible", [False] * len(fig_entry.data) + [True] * len(fig_exit.data)],
                    label="Exits",
                    method="restyle"
                ),
            ],
        )
    ],
    title="Gas Flow exchanges in Europe",
    geo=dict(
        showcountries=True,
        countrycolor="black",
        center={"lat": 50.5, "lon": 15.2551},  # Updated center coordinates
        projection_scale=2.5  # Zoom level (adjust as necessary)
    ),
)
# Set the initial view to Total Entries
fig_combined1.update_traces(visible=False)
for trace in fig_combined1.data[:len(fig_entry.data)]:
    trace.visible = True
fig_combined1.show()

###############
#   MAP 2     #
###############

# df = pd.read_csv(f'FINAL/data/PerCountry/agg_data_countries_{DATE}.csv')
# total_flow_df = build_total_flow_df(df)

# # Get the maximum value of total entries
# max_entries = total_flow_df['totalEntries'].max()
# max_exits = total_flow_df['totalExits'].max()
# max_flow = total_flow_df['totalFlow'].max()

# global_max = max(max_entries, max_exits, max_flow)
# print(f"Global Max: {global_max} kWh/d")
# global_min = total_flow_df['totalFlow'].min()
# print(f"Global Min: {global_min} kWh/d")

# default_color_scale = "Viridis"
# zero_color = "grey"

# def create_choropleth(data, column,min_value,max_value, title):
#     fig = px.choropleth(
#         data,
#         locations="countryISO",
#         locationmode="ISO-3",
#         color=column,
#         hover_name="countryName",
#         range_color=(min_value, max_value),
#         color_continuous_scale=default_color_scale,
#         title=title,
#         projection="natural earth"
#     )

#     # Manually set zero-value countries to grey
#     zero_value_indices = data.index[data[column] == 0].tolist()
#     for idx in zero_value_indices:
#         country_code = data.loc[idx, "countryISO"]
#         fig.add_trace(go.Choropleth(
#             locations=[country_code],
#             z=[0],
#             showscale=False,
#             colorscale=[[0, zero_color], [1, zero_color]],
#             hoverinfo='none'
#         ))
        
#     fig.update_geos(
#         showcountries=True,
#         countrycolor="black",
#         center={"lat": 50.5, "lon": 15.2551},  # Centered around Europe
#         projection_scale=4.3  # Zoom level (adjust as necessary)
#     )

#     return fig


# fig_entries = create_choropleth(total_flow_df, "totalEntries", title="Total Gas Flow Entries in Europe",max_value=global_max,min_value=global_min)
# fig_exits = create_choropleth(total_flow_df, "totalExits", title="Total Gas Flow Exits in Europe",max_value=global_max,min_value=global_min)
# fig_total = create_choropleth(total_flow_df, "totalFlow", title="Total Gas Flow in Europe",max_value=global_max,min_value=global_min)

# # COMBINED MAP
# # Create a combined figure with buttons to toggle between views
# fig_combined = make_subplots(rows=1, cols=1)
# # Add all traces to the combined figure
# for trace in fig_entries.data:
#     fig_combined.add_trace(trace)
# for trace in fig_exits.data:
#     fig_combined.add_trace(trace)
# for trace in fig_total.data:
#     fig_combined.add_trace(trace)

# # Update the layout with buttons
# fig_combined.update_layout(
#     updatemenus=[
#         dict(
#             type="buttons",
#             direction="down",
#             buttons=[
#                 dict(
#                     args=["visible", [True] * len(fig_entries.data) + [False] * len(fig_exits.data) + [False] * len(fig_total.data)],
#                     label="Total Entries",
#                     method="restyle"
#                 ),
#                 dict(
#                     args=["visible", [False] * len(fig_entries.data) + [True] * len(fig_exits.data) + [False] * len(fig_total.data)],
#                     label="Total Exits",
#                     method="restyle"
#                 ),
#                 dict(
#                     args=["visible", [False] * len(fig_entries.data) + [False] * len(fig_exits.data) + [True] * len(fig_total.data)],
#                     label="Total Flow",
#                     method="restyle"
#                 )
#             ],
#         )
#     ],
#     title="Gas Flow in Europe",
#     geo=dict(
#         showcountries=True,
#         countrycolor="black",
#         center={"lat": 50.5, "lon": 15.2551},  # Updated center coordinates
#         projection_scale=2.5  # Zoom level (adjust as necessary)
#     ),
#     coloraxis=dict(
#         colorscale="Inferno",
#         cmin=global_min,
#         cmax=global_max,
#         colorbar=dict(title="Flow (kWh/d)")
#     )
# )
# # Set the initial view to Total Entries
# fig_combined.update_traces(visible=False)
# for trace in fig_combined.data[:len(fig_entries.data)]:
#     trace.visible = True



# # Show the combined map
# fig_combined.show()