import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

from utils import compute_bearing
from buildPairs import COUNTRY_COORDS, build_dict

app = dash.Dash(__name__)

YEAR = 2019 # 2019 or 2023
DATES_19 = ['2019_01','2019_02','2019_03','2019_04','2019_05', '2019_06', '2019_07', '2019_08', '2019_09', '2019_10', '2019_11', '2019_12']
DATES_23 = ['2023_01', '2023_02', '2023_03','2023_04','2023_05','2023_06','2023_07','2023_08','2023_09','2023_10','2023_11','2023_12' ]

dates = DATES_19 if YEAR == 2019 else DATES_23

DICT = build_dict(dates)
# print(DICT)

def interpolate_coords(coord1, coord2, ratio=2/3):
    """Interpolates coordinates between coord1 and coord2 based on the given ratio."""
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    lon = lon1 + (lon2 - lon1) * ratio
    lat = lat1 + (lat2 - lat1) * ratio
    return (lon, lat)


def create_global_map(input_dict=DICT):
    fig = go.Figure()

    # annotations = []
    max_total_flow = max(abs(sum(data['totalFlow'])) for data in input_dict.values())
    gradient_colors = px.colors.sequential.haline_r

    for pair_dict, data in input_dict.items():

        total_flow = sum(data['totalFlow'])
        pair = (pair_dict[0], pair_dict[1])
        total_flow_data = [data['totalFlow']]
        fromCoords, toCoords = data['toCoords'], data['fromCoords']

        if total_flow < 0:
            # Invert the countries and make the flow positive
            pair = (pair_dict[1], pair_dict[0])
            total_flow_data = [-flow for flow in data['totalFlow']]
            fromCoords,toCoords = data['toCoords'], data['fromCoords']
            total_flow = -total_flow

        normalized_flow = total_flow / (max_total_flow * 1.5)  # Slightly above the max value
        color_index = int(normalized_flow * (len(gradient_colors) - 1))
        color = 'black' if total_flow==0 else gradient_colors[color_index]

        text=f"{pair[0]} - {pair[1]} : {total_flow:.3e} (kWh/d)",
        angle = compute_bearing((fromCoords['lat'], fromCoords['lon']), (toCoords['lat'], toCoords['lon']))
        mid_lon, mid_lat = interpolate_coords((fromCoords['lon'], fromCoords['lat']), (toCoords['lon'], toCoords['lat']))

        # Create traces
        fig.add_trace(go.Scattergeo(
            lon=[fromCoords['lon'], toCoords['lon']],
            lat=[fromCoords['lat'], toCoords['lat']],
            mode='lines',
            hoverinfo='none',
            name=f"{pair[0]} - {pair[1]} : {total_flow:.3e} (kWh/d)",
            line=dict(color=color),
            showlegend=True
        ))

        # Add marker on the centrer of the line
        fig.add_trace(go.Scattergeo(
            lon=[mid_lon],
            lat=[mid_lat],
            mode='markers',
            marker=dict(size=10, color=color, symbol='arrow-wide', angle=angle),
            text=text,
            hovertext=text,
            hoverinfo='text',
            showlegend=False
        ))


    fig.update_layout(
        title='Gas Flow Network in Europe (2019)',
        geo=dict(
            projection_type='mercator',
            showland=True,
            showcountries=True,
            landcolor='darkgrey',
            subunitwidth=1,
            countrywidth=1,
            center={"lat": 50.5, "lon": 15.2551},  # Updated center coordinates
            projection_scale=5,  # Zoom level (adjust as necessary)
            subunitcolor='rgb(255, 255, 255)',
            countrycolor='rgb(255, 255, 255)',
        ),
        showlegend=True,
        # dict1={'colorscale':gradient_colors}
        # annotations=annotations
    )
    return fig

def create_selected_map(country):
    country_data = {pair: data for pair, data in DICT.items() if pair[0] == country or pair[1] == country}
    print(f"Country data size for {country}: {len(country_data)}")

    fig = create_global_map(country_data)

    color_map = px.colors.qualitative.Plotly
    pair_colors = {pair: color_map[i % len(color_map)] for i, pair in enumerate(country_data.keys())}
    print(f"Pair colors : {pair_colors}")

    # Create pie charts for entries and exits
    entries = {pair[1]: sum(data['entries']) for pair, data in country_data.items() if pair[0] == country}
    exits = {pair[0]: sum(data['exits']) for pair, data in country_data.items() if pair[1] == country}

    fig_pie_entries = px.pie(values=list(entries.values()),
                             color=[pair for pair in entries.keys()],
                             color_discrete_map=pair_colors,
                              names=[f"{key} : {value:.3e}" for key,value in entries.items()], title=f'Total Entries : {sum(entries.values()):.3e} (kWh/d)')
    fig_pie_exits = px.pie(values=list(exits.values()),
                            color=[pair for pair in exits.keys()],
                            color_discrete_map=pair_colors,
                            names=[f"{key} : {value:.3e}" for key,value in exits.items()], title=f'Total Exits : {sum(exits.values()):3e} (kWh/d)')

    # Create line graph for flow evolution over the year
    monthly_flows = []

    for pair, data in country_data.items():
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for i in range(12):
            monthly_flows.append({
                'Month': months[i],
                'Entries': data['entries'][i],
                'Exits': -data['exits'][i],
                'Total Flow': data['totalFlow'][i],
                'Pair': f"{pair[0]} - {pair[1]}"
            })

    monthly_flows_df = pd.DataFrame(monthly_flows)

    fig_bar = go.Figure()

    for pair in monthly_flows_df['Pair'].unique():
    #     pair_data = monthly_flows_df[monthly_flows_df['Pair'] == pair]
    #     fig_line.add_trace(go.Scatter(x=pair_data['Month'], y=pair_data['Total Flow'], mode='lines+markers',hoverinfo=f"y+name", stackgroup='one'))
    #     fig_line.add_trace(go.Scatter(x=pair_data['Month'], y=pair_data['Entries'], mode='lines+markers', hoverinfo=f"y+name",stackgroup='one'))
    #     fig_line.add_trace(go.Scatter(x=pair_data['Month'], y=pair_data['Exits'], mode='lines+markers', hoverinfo=f"y+name",stackgroup='one'))

    # fig_line.update_layout(
    #     hovermode='x unified'
    # )
        pair_data = monthly_flows_df[monthly_flows_df['Pair'] == pair]
        pair_key = (pair.split(' - ')[0], pair.split(' - ')[1])
        color = pair_colors[pair_key]
        fig_bar.add_trace(go.Bar(
            x=pair_data['Month'], 
            y=pair_data['Entries'], 
            name=f"{pair} Entries", 
            hovertemplate=": %{y:.2e}%",
            marker=dict(color=color)
        ))
        fig_bar.add_trace(go.Bar(
            x=pair_data['Month'], 
            y=pair_data['Exits'], 
            name=f"{pair} Exits", 
            hovertemplate=": %{y:.2e}%",
            marker=dict(color=color)
        ))
        fig_bar.update_layout(
        barmode='relative',  # This stacks the bars on top of each other
        title='Flow Evolution Over the Year',
        hovermode='x unified',
        xaxis_title='Month',
        yaxis_title='Flow (kWh/d)'
    )


    return fig, fig_pie_entries, fig_pie_exits, fig_bar


app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in COUNTRY_COORDS.keys()]+[{'label': 'All Countries', 'value': 'All Countries'}],
        value='All Countries',
        clearable=False
    ),
    dcc.Graph(id='global-map', figure=create_global_map()),
    html.Div(id='country-details')
])


@app.callback(
    [Output('global-map', 'figure'),
     Output('country-details', 'children')],
    [Input('country-dropdown', 'value')]
)
def update_output(selected_country):
    if not selected_country or selected_country == 'All Countries':
        return create_global_map(), []


    fig,fig_pie_entries,fig_pie_exits,fig_line = create_selected_map(selected_country)
    
    return fig, [
        dcc.Graph(figure=fig_pie_entries),
        dcc.Graph(figure=fig_pie_exits),
        dcc.Graph(figure=fig_line)]


if __name__ == "__main__":
    app.run_server(debug=True)
