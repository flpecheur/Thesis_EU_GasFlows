############################################
# INTRO 
# This script creates an interactive map of the world with the LNG points.
# The map is created using the Dash library and the Plotly graphing library.
# The map displays the total entries for each LNG point in the dataset.
# The user can select a country from a dropdown menu to see the total entries for each LNG point in that country.
# The map is updated based on the selected country, and a table and line chart are displayed with the total entries for each LNG point in the selected country.

# The script uses the following data files:
# - data/points/lng_points.csv: Contains information about the LNG points, including the point label, coordinates, country, and operational status.
# - data/opData/op_data_YYYY_MM.csv: Contains operational data for each LNG point for a specific month (YYYY_MM).

# Upcoming TODO ideas for improvement:
# - Refactor for better readability and maintainability (methods descr. + comment)
# - Add a pie chart for all countries showing the total entries for each country.
# - Add a slider to select the month for which to display the data.
# - Add a heatmap to show the total entries for each country over time.
# - Add a dropdown menu to select the type of data to display (entries, exits, etc.).
# - Add a column to the table with the LNG point status (operational or non-operational).


############################################

import dash
import numpy as np
import os
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils import process_total_data, initialize_lng_dict
from utils import create_initial_map

current_dir = os.getcwd()
DIR = f"{current_dir}"

# Initialize the Dash app
app = dash.Dash(__name__)

### Data Initialization ###
lng_points_df = pd.read_csv(f'{DIR}/data/points/lng_points.csv')
lng_keys = lng_points_df['point_key'].unique()
lng_dict = initialize_lng_dict(lng_points_df)
process_total_data(lng_dict, ['2023_01', '2023_02', '2023_03','2023_04','2023_05','2023_06','2023_07','2023_08','2023_09','2023_10','2023_11','2023_12' ], lng_keys, f'{DIR}/data/opData')

### Layout Definition ###
app.layout = html.Div([
    html.H1(children ='LNG Points Map (2023)', style={'text-align': 'center'}),
    dcc.Graph(
        id='main-map',
        figure=create_initial_map(lng_dict),
        style={'width': '75%', 'display': 'inline-block'}
    ),
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': 'All Countries', 'value': 'All Countries'}]+[
                {'label': country, 'value': country} for country in lng_points_df['Country'].unique()
            ],
            placeholder='Select a country',
            style={'width': '50%'}
        ),
        html.Div(id='sidebar',
             style={'width': '90%'}),
        dcc.Graph(id='entries-graph',
                  style={'width': '100%', 'display': 'inline-block'})
    ],style={'margin-top': '40px'})
    
])

### Callbacks ###
@app.callback(
    Output('sidebar', 'children'),
    Output('entries-graph', 'figure'),
    Input('country-dropdown', 'value')
)
def update_on_country(selected_country):
    """
    Update sidebar and entries graph based on the selected country.
    """
    if selected_country is None:
        return html.Div('Select a country to see related data'),go.Figure()
    
    print(f"Selected: {selected_country}")
    # lng_points = {k: v for k, v in lng_dict.items() if v['Country'] == selected_country}

    if selected_country == 'All Countries':
        
        return generate_AllCountries_view(lng_dict)
    
    else : 
        return generate_Country_view(selected_country,lng_dict)

    
@app.callback(
    Output('main-map', 'figure'),
    Input('country-dropdown', 'value')
)
def update_map(selected_country,lng_dict=lng_dict):
    """
    Update the map based on the selected country.
    """
    return create_initial_map(lng_dict, selected_country)

### Helper Functions ###

def generate_AllCountries_view(lng_dict):
    """
    Generate view for all countries with a pie chart and a line graph.
    """
    country_data = aggregate_country_data(lng_dict)
    df = create_country_data_df(country_data)

    # Generate line plot
    line_fig = px.line(
        df,
        x='month',
        y='entries',
        color='Country',
        title='Total LNG Entries by Country (2023)',
        labels={'entries': 'Entries (kWh)'}
    )
    line_fig.update_traces(hovertemplate=" Total Entries: %{y:.2e}")
    line_fig.update_layout(
        hovermode='x unified',
        height=800
        )

    # Generate pie chart
    total_entries = sum([np.nansum(entries) for entries in country_data.values()])
    pie_chart = px.pie(
        values=[sum(entries) for entries in country_data.values()],
        names=[f"{country}:{sum(entries):3e}" for country,entries in country_data.items()],
        title=f'Total Entries by Country in 2023 - Total Entries: {total_entries:.2e} (kWh)'
    )
    pie_chart.update_traces(hovertemplate="Total Entries: %{value:.2e}")

    # Generate table
    table = generate_country_table(country_data)

    return html.Div([
        html.H2('All Countries', style={'text-align': 'center'}),
        dcc.Graph(figure=pie_chart, style={'width': '90%', 'display': 'inline-block'}),
        table
    ]), line_fig


def generate_Country_view(selected_country,lng_dict):
    """
    Generate view for a specific country with a pie chart and a line graph.
    """
    points = {k: v for k, v in lng_dict.items() if v['Country'] == selected_country}
    
    df = create_point_data_df(points)

    # Generate line plot
    line_fig = px.line(
        df,
        x='month',
        y='entries',
        color='point_label',
        title=f'LNG entries in {selected_country} (2023)',
        labels={'entries': 'Entries (kWh)', 'point_label': 'LNG Point'},
    )
    line_fig.update_traces(hovertemplate=" Total Entries: %{y:.2e}")
    line_fig.update_layout(hovermode='x unified')


    # Generate pie chart
    total_entries = sum([np.nansum(point['total_entries']) for point in points.values()]) #nansum to avoid nan values in found in UK data 2023
    pie_chart = px.pie(
        values=[sum(point['total_entries']) for point in points.values()],
        names=[point['point_label'] for point in points.values()],
        title=f'LNG Entries in {selected_country} - Total Entries: {total_entries:.2e} (kWh)'
    )
    pie_chart.update_traces(hovertemplate="Total Entries: %{value:.2e}")

    # Generate table
    table = generate_point_table(points)

    return html.Div([
        html.H2(f'LNG Points in {selected_country}', style={'text-align': 'center'}),
        dcc.Graph(figure=pie_chart, style={'width': '60%', 'display': 'inline-block'}),
        table
    ]), line_fig


def aggregate_country_data(lng_dict):
    """
    Aggregate data for all countries.
    Post : return a dictionary with the list of total entries per month for each country.
    """
    country_data = {}
    for point_data in lng_dict.values():
        country = point_data['Country']
        if country not in country_data:
            country_data[country] = [0] * 12
        for month in range(12):
            country_data[country][month] += point_data['total_entries'][month]
    return country_data

def create_country_data_df(country_data):
    """
    Create a dataframe for country data.
    Post : return a dataframe with the total entries for each country for each month.
    """
    data = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for country, entries in country_data.items():
        for i in range(12):
            data.append({'Country': country, 'entries': entries[i], 'month': months[i]})
    return pd.DataFrame(data)

def create_point_data_df(points):
    """
    Create a dataframe for point data.
    """
    data = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for point_data in points.values():
        for i in range(12):
            data.append({'point_label': point_data['point_label'], 'entries': point_data['total_entries'][i], 'month': months[i]})
    return pd.DataFrame(data)

def generate_country_table(country_data):
    """
    Generate HTML table for country data.
    """
    return html.Table(
        children=[
            html.Tr([html.Th('Country'), html.Th('Total Entries (kWh)')]),
            *[html.Tr([html.Td(country, style={'whiteSpace': 'nowrap', 'maxWidth': '150px'}), html.Td(f"{sum(entries):.3e}")]) for country, entries in country_data.items()]
        ],
        style={
            'display': 'inline-block', 'vertical-align': 'top',
            'border': '1px solid black',
            'margin-top': '60px',
            'maxHeight': '400px', 'overflowY': 'scroll',
            'tableLayout': 'fixed',
                        'width': '30%'

        }
    )

def generate_point_table(points):
    """
    Generate HTML table for point data.
    """
    return html.Table(
        children=[
            html.Tr([html.Th("Point Label"), html.Th("Tot Entries (kWh)")]),
            *[html.Tr([html.Td(point_data['point_label'], style={'whiteSpace': 'nowrap', 'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': '150px'}), html.Td(f"{sum(point_data['total_entries']):.3e}")]) for point_data in points.values()]
        ],
        style={
            'display': 'inline-block', 'vertical-align': 'top',
            'border': '1px solid black',
            'margin-top': '30px',
            'maxHeight': '400px', 'overflowY': 'scroll',
            'tableLayout': 'fixed',
            'width': '30%'

        }
    )


### RUN APP ###
if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)
