import pandas as pd
import plotly.express as px
from plotly.colors import sequential
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



current_dir = os.getcwd()
DIR = f"{current_dir}"


# # Load the Agg dataset
# agg_pairs_df = pd.read_csv(f'{DIR}/data/perCountry/agg_data_pairs_{DATE}.csv')

# MAPPINGS
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
def add_color_scale(fig, min_flow, max_flow,color_scale="Viridis"):
    color_bar_trace = go.Scattergeo(
        lon=[None],
        lat=[None],
        mode='markers',
        marker=dict(
            colorscale=color_scale,
            cmin=min_flow,
            cmax=max_flow,
            colorbar=dict(
                title="Flow (kWh)",
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



def create_choropleth(data, column,min_value,max_value, title,default_color_scale="Viridis",zero_color="grey"):
    fig = px.choropleth(
        data,
        locations="countryISO",
        locationmode="ISO-3",
        color=column,
        hover_name="countryName",
        range_color=(min_value, max_value),
        color_continuous_scale=default_color_scale,
        title=title,
        projection="natural earth"
    )

    # Manually set zero-value countries to grey
    zero_value_indices = data.index[data[column] == 0].tolist()
    for idx in zero_value_indices:
        country_code = data.loc[idx, "countryISO"]
        fig.add_trace(go.Choropleth(
            locations=[country_code],
            z=[0],
            showscale=False,
            colorscale=[[0, zero_color], [1, zero_color]],
            hoverinfo='none'
        ))
        
    fig.update_geos(
        showcountries=True,
        countrycolor="black",
        center={"lat": 50.5, "lon": 15.2551},  # Centered around Europe
        projection_scale=4.3  # Zoom level (adjust as necessary)
    )

    return fig

def update_combined(title,fig_combined,length_data,min,max):
    # Update the layout with buttons
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    buttons = [
            dict(
            args=["visible",[i == month for i in range(12)] * length_data],
            label=f"Month {months[month]}",
            method="restyle"
    ) for month in range(12)
    ]
    fig_combined.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="down",
                buttons=buttons,
            )
        ],
        title=title,
        geo=dict(
            showcountries=True,
            countrycolor="black",
            center={"lat": 50.5, "lon": 15.2551},  # Updated center coordinates
            projection_scale=2.5  # Zoom level (adjust as necessary)
        ),
        coloraxis=dict(
            colorscale="Inferno",
            cmin=min,
            cmax=max,
            colorbar=dict(title="Flow (kWh/d)")
        )
    )
    # Set the initial view to Total Entries
    fig_combined.update_traces(visible=False)
    for trace in fig_combined.data[:length_data]:
        trace.visible = True
        

def combined_maps(year):
    """ 
    Input : Year is the array of dates considered 
    """
    fig_entries_comb = make_subplots(rows=1, cols=1)
    fig_exits_comb = make_subplots(rows=1, cols=1)
    fig_total_comb = make_subplots(rows=1, cols=1)

    global_min = 0
    global_max = 0

    for date in year:
        df = pd.read_csv(f'{DIR}/data/PerCountry/agg_data_countries_{date}.csv')
        total_flow_df = build_total_flow_df(df)

        # Get the maximum value of total entries
        max_entries = total_flow_df['totalEntries'].max()
        max_exits = total_flow_df['totalExits'].max()
        max_flow = total_flow_df['totalFlow'].max()

        global_min = min(global_min, total_flow_df['totalFlow'].min())
        global_max = max(global_max, max_entries, max_exits, max_flow)

        default_color_scale = "Viridis"
        zero_color = "grey"

        fig_entries = create_choropleth(total_flow_df, "totalEntries", title="Total Gas Flow Entries in Europe",max_value=global_max,min_value=global_min)
        fig_exits = create_choropleth(total_flow_df, "totalExits", title="Total Gas Flow Exits in Europe",max_value=global_max,min_value=global_min)
        fig_total = create_choropleth(total_flow_df, "totalFlow", title="Total Gas Flow in Europe",max_value=global_max,min_value=global_min)

        # print(f"Len fig entries : {len(fig_entries.data)}")
        # print(f"Len fig exits : {len(fig_exits.data)}")
        # print(f"Len fig total : {len(fig_total.data)}")

        # Add all traces to the combined figure
        for trace in fig_entries.data:
            fig_entries_comb.add_trace(trace)
        for trace in fig_exits.data:
            fig_exits_comb.add_trace(trace)
        for trace in fig_total.data:
            fig_total_comb.add_trace(trace)

    update_combined(f"Total entries flow {year}",fig_entries_comb,len(fig_entries.data),global_min,global_max)
    update_combined(f"Total exits flow {year}",fig_exits_comb,len(fig_exits.data),global_min,global_max)
    update_combined(f"Total flow {year}",fig_total_comb,len(fig_total.data),global_min,global_max)

    return fig_entries_comb, fig_exits_comb, fig_total_comb


if __name__ == "__main__":
    # Define the year array
    year_19 = ["2019_01", "2019_02", "2019_03", "2019_04", "2019_05", "2019_06", "2019_07", "2019_08", "2019_09", "2019_10", "2019_11", "2019_12"]
    year_23 = ["2023_01", "2023_02", "2023_03", "2023_04", "2023_05", "2023_06", "2023_07", "2023_08", "2023_09", "2023_10", "2023_11", "2023_12"]

    # Generate the combined maps
    fig_entries_comb_19, fig_exits_comb_19, fig_total_comb_19 = combined_maps(year_19)
    fig_entries_comb_23, fig_exits_comb_23, fig_total_comb_23 = combined_maps(year_23)

    # Show the combined maps
    fig_entries_comb_19.show()
    fig_exits_comb_19.show()
    fig_total_comb_19.show()
    fig_entries_comb_23.show()
    fig_exits_comb_23.show()
    fig_total_comb_23.show()

