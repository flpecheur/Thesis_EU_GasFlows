import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

from utils import compute_bearing
from buildPairs import COUNTRY_COORDS, build_dict

app = dash.Dash(__name__)

DATES = ['2019_01','2019_02','2019_03','2019_04','2019_05', '2019_06', '2019_07', '2019_08', '2019_09', '2019_10', '2019_11', '2019_12']
DATES_23 = ['2023_01', '2023_02', '2023_03','2023_04','2023_05','2023_06','2023_07','2023_08','2023_09','2023_10','2023_11','2023_12' ]
DICT = build_dict(DATES)
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

    for pair, data in input_dict.items():
        # Add arrows using px shapes
        # TODO : create method
        # lon=[data['fromCoords']['lon'], data['toCoords']['lon']]
        # lat=[data['fromCoords']['lat'], data['toCoords']['lat']]
        # mid_lon = lon[0] + (lon[1]-lon[0]) / 2
        # mid_lat = lat[0] + (lat[1]-lat[0]) / 2

        # # TODO : modify direction and color if needed
        # fig.add_shape(
        #     type="line",
        #     x0=mid_lon, y0=mid_lat, 
        #     x1=mid_lon+0.5, y1=mid_lat+0.5,
        #     line=dict(color="black", width=30)
        #     # arrowhead=2
        #     )


        # DOES NOT WORK
        # annotations.append(dict(
        #     x=mid_lon,
        #     y=mid_lat,
        #     ax=mid_lon+0.5,
        #     ay=mid_lat+0.5,
        #     xref='geo',
        #     yref='geo',
        #     showarrow=False,
        #     arrowhead=4,
        #     arrowsize=2,
        #     arrowcolor='black',
        #     font=dict(size=10),
        # ))

        # Create traces
        text=f"{pair[0]} -> {pair[1]} : {sum(data['totalFlow']):.3e} (kWh/d)",
        color='blue' if sum(data['totalFlow']) > 0 else 'red' if sum(data['totalFlow']) < 0 else 'black'
        angle = compute_bearing((data['fromCoords']['lat'], data['fromCoords']['lon']), (data['toCoords']['lat'], data['toCoords']['lon']))
        mid_lon, mid_lat = interpolate_coords((data['fromCoords']['lon'], data['fromCoords']['lat']), (data['toCoords']['lon'], data['toCoords']['lat']))
        fig.add_trace(go.Scattergeo(
            lon=[data['fromCoords']['lon'], data['toCoords']['lon']],
            lat=[data['fromCoords']['lat'], data['toCoords']['lat']],
            mode='lines',
            marker=dict(size=10, color=color,symbol='arrow'),
            # text=text,
            # hovertext=text,
            hoverinfo='none',
            name=f"{pair[0]} -> {pair[1]}",
            line=dict(width=max(1, sum(data['totalFlow']) / 5e10), color=color),
            showlegend=False
        ))
        # # Add marker on the `fromCoords` side
        # fig.add_trace(go.Scattergeo(
        #     lon=[data['fromCoords']['lon']],
        #     lat=[data['fromCoords']['lat']],
        #     mode='markers',
        #     marker=dict(size=5, color=color, symbol='diamond'),
        #     text=text,
        #     hovertext=text,
        #     hoverinfo='text',
        #     showlegend=False
        # ))
        # # Add marker on the `toCoords` side
        # fig.add_trace(go.Scattergeo(
        #     lon=[data['toCoords']['lon']],
        #     lat=[data['toCoords']['lat']],
        #     mode='markers',
        #     marker=dict(size=5, color=color, symbol='diamond-dot'),
        #     text=text,
        #     hovertext=text,
        #     hoverinfo='text',
        #     showlegend=False
        # ))
        # Add marker on the centrer of the line
        fig.add_trace(go.Scattergeo(
            lon=[mid_lon],
            lat=[mid_lat],
            mode='markers',
            marker=dict(size=5, color=color, symbol='arrow-wide', angle=angle),
            text=text,
            hovertext=text,
            hoverinfo='text',
            showlegend=False
        ))
        # fig.add_trace(go.Scattergeo(
        #     lon=[data['fromCoords']['lon'], data['toCoords']['lon']],
        #     lat=[data['fromCoords']['lat'], data['toCoords']['lat']],
        #     mode='lines+markers',
        #     text = text,
        #     line=dict(width=max(1, sum(data['entries']) / 5e10),dash="dash", color='blue'),
        #     marker=dict(symbol='arrow-wide', color='blue',angleref='previous'),
        #     showlegend=False
        # ))
        # fig.add_trace(go.Scattergeo(
        #     lon=[data['fromCoords']['lon'], data['toCoords']['lon']],
        #     lat=[data['fromCoords']['lat'], data['toCoords']['lat']],
        #     mode='lines+markers',
        #     text=text,
        #     line=dict(width=max(1, sum(data['exits']) / 5e10), color='red',dash="dash"),
        #     marker=dict(symbol='arrow-wide', color='red',angleref='previous'),
        #     showlegend=False
        # ))

    fig.update_layout(
        title='Gas Flow Network in Europe (2019)',
        geo=dict(
            projection_type='mercator',
            showland=True,
            showcountries=True,
            showocean=True,
            landcolor='lightgrey',
            subunitwidth=1,
            countrywidth=1,
            center={"lat": 50.5, "lon": 15.2551},  # Updated center coordinates
            projection_scale=5,  # Zoom level (adjust as necessary)
            subunitcolor='rgb(255, 255, 255)',
            countrycolor='rgb(255, 255, 255)',
        ),
        autosize=True,
        # annotations=annotations
    )
    return fig

app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in COUNTRY_COORDS.keys()],
        value='All Countries',
        clearable=False
    ),
    dcc.Graph(id='global-map', figure=create_global_map(), style={'height': '80vh','width':'100%'}),
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

    country_data = {pair: data for pair, data in DICT.items() if pair[0] == selected_country or pair[1] == selected_country}
    print(f"Country data size for {selected_country}: {len(country_data)}")

    fig = go.Figure()

    for pair, data in country_data.items():
        text=f"{pair[0]} -> {pair[1]} : {sum(data['totalFlow']):.3e} (kWh/d)",
        fig.add_trace(go.Scattergeo(
            lon=[data['fromCoords']['lon'], data['toCoords']['lon']],
            lat=[data['fromCoords']['lat'], data['toCoords']['lat']],
            mode='lines',
            text=text,
            name=f"{pair[0]} -> {pair[1]}",
            line=dict(width=max(1, sum(data['totalFlow']) / 5e10), color='blue' if sum(data['totalFlow']) > 0 else 'red'),
            showlegend=True
        ))

    fig.update_layout(
        title=f'Gas Flow Network for {selected_country}',
        geo=dict(
            projection_type='mercator',
            showland=True,
            showcountries=True,
            showocean=True,
            landcolor='lightgrey',
            subunitwidth=1,
            countrywidth=1,
            center={"lat": 50.5, "lon": 15.2551},  # Updated center coordinates
            projection_scale=5,  # Zoom level (adjust as necessary)
            subunitcolor='rgb(255, 255, 255)',
            countrycolor='rgb(255, 255, 255)',
        )
    )

    # Create pie charts for entries and exits
    entries = {pair[1]: sum(data['entries']) for pair, data in country_data.items() if pair[0] == selected_country}
    exits = {pair[0]: sum(data['exits']) for pair, data in country_data.items() if pair[1] == selected_country}

    fig_pie_entries = px.pie(values=list(entries.values()), names=list(entries.keys()), title='Total Entries')
    fig_pie_exits = px.pie(values=list(exits.values()), names=list(exits.keys()), title='Total Exits')

    # Create line graph for flow evolution over the year
    monthly_flows = []

    for pair, data in country_data.items():
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for i, month in enumerate(DATES):
            monthly_flows.append({
                'Month': months[i],
                'Entries': data['entries'][i],
                'Exits': -data['exits'][i],
                'Total Flow': data['totalFlow'][i],
                'Pair': f"{pair[0]} -> {pair[1]}"
            })

    monthly_flows_df = pd.DataFrame(monthly_flows)

    fig_line = go.Figure()
    for pair in monthly_flows_df['Pair'].unique():
        pair_data = monthly_flows_df[monthly_flows_df['Pair'] == pair]
        fig_line.add_trace(go.Scatter(x=pair_data['Month'], y=pair_data['Total Flow'], mode='lines+markers',hoverinfo=f"y+name", stackgroup='one'))
        fig_line.add_trace(go.Scatter(x=pair_data['Month'], y=pair_data['Entries'], mode='lines+markers', hoverinfo=f"y+name",stackgroup='one'))
        fig_line.add_trace(go.Scatter(x=pair_data['Month'], y=pair_data['Exits'], mode='lines+markers', hoverinfo=f"y+name",stackgroup='one'))
    # fig_line = px.line(monthly_flows_df, x='Month', y=['Entries', 'Exits', 'Total Flow'], color='Pair', title='Flow Evolution Over the Year')
    # # fig_line['data'][0]['line']['dash'] = 'dash'
    # # fig_line['data'][1]['line']['dash'] = 'longdash'
    # fig_line.update_traces(
    #     # patch=dict(line=dict(dash='dash')), selector=dict(name='Entries'),
    #     # hovertemplate=" Total Entries: %{y:.3e}"
    # )
    fig_line.update_layout(
        hovermode='x unified'
    )

    return fig, [
        dcc.Graph(figure=fig_pie_entries),
        dcc.Graph(figure=fig_pie_exits),
        dcc.Graph(figure=fig_line)]


if __name__ == "__main__":
    app.run_server(debug=True)
