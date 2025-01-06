##############################################################
#   Purpose: This script processes the operational data and creates aggregated files for each month.
#   The aggregated files contain the total gas flow for each pair of countries and the total gas flow for each country.
#   The script processes the data for each month in the dataset.
#   The script uses the following datasets:
#       - op_data_{date}.csv
#       - points_data.csv
#       - operator_points_dir.csv
#       - interconnections_data.csv
#   The script saves the aggregated data to the 'perCountry' directory.
#   The script saves the following files:
#       - aggregated_data_{date}.csv
#       - agg_data_pairs_{date}.csv
#       - agg_data_countries_{date}.csv

# TODO : This actually builds data per pair of countries, not per country. The function names are misleading.
##############################################################


##################
#    Imports     #
##################
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px

current_dir = os.getcwd()
DIR = f"{current_dir}"
DATES_19 = ['2019_01','2019_02','2019_03','2019_04','2019_05', '2019_06', '2019_07', '2019_08', '2019_09', '2019_10', '2019_11', '2019_12']
DATES_23 = ['2023_01', '2023_02', '2023_03','2023_04','2023_05','2023_06','2023_07','2023_08','2023_09','2023_10','2023_11','2023_12' ]
 
##################
#   Load data    #
##################
def load_data(date):
    """Load operational, points, operator points directions, and interconnections data."""
    operational_df = pd.read_csv(f"{DIR}/data/opData/op_data_{date}.csv")
    points_df = pd.read_csv(f"{DIR}/data/points_data.csv")
    interconnections_df = pd.read_csv(f'{DIR}/data/interconnections_data.csv')
    return operational_df, points_df, [], interconnections_df
######################
#   Rename Columns   #
######################
def rename_columns(points_df, operational_df):
    """Rename columns to match the format of other datasets."""
    points_df.rename(columns={
        'point_key': 'pointKey',
        'point_label': 'pointLabel',
        'is_single_operator': 'isSingleOperator',
        'point_tooltip': 'pointTooltip',
        'point_eic_code': 'pointEicCode',
        'control_point_type': 'controlPointType',
        'tp_map_x': 'tpMapX',
        'tp_map_y': 'tpMapY',
        'point_type': 'pointType',
        'commercial_type': 'commercialType',
        'import_from_country_key': 'importFromCountryKey',
        'import_from_country_label': 'importFromCountryLabel',
        'has_virtual_point': 'hasVirtualPoint',
        'virtual_point_key': 'virtualPointKey',
        'virtual_point_label': 'virtualPointLabel',
        'has_data': 'hasData',
        'is_planned': 'isPlanned',
        'is_interconnection': 'isInterconnection',
        'is_import': 'isImport',
        'infrastructure_key': 'infrastructureKey',
        'infrastructure_label': 'infrastructureLabel',
        'is_cross_border': 'isCrossBorder',
        'eu_crossing': 'euCrossing',
        'is_invalid': 'isInvalid',
        'is_macro_point': 'isMacroPoint',
        'is_cam_relevant': 'isCamRelevant',
        'is_pipe_in_pipe': 'isPipeInPipe',
        'is_cmp_relevant': 'isCmpRelevant',
        'id': 'id',
        'data_set': 'dataSet',
        'url': 'url'
    }, inplace=True)

    operational_df.rename(columns={
        'direction_key': 'directionKey',
        'flow_status': 'flowStatus',
        'id_point_type': 'idPointType',
        'operator_key': 'operatorKey',
        'period_from': 'periodFrom',
        'period_to': 'periodTo',
        'period_type': 'periodType',
        'point_key': 'pointKey',
        'point_label': 'pointLabel',
        'tso_eic_code': 'tsoEicCode',
        'unit': 'unit',
        'value': 'value'
    }, inplace=True)


################
#   Methods    #
################

def merge_data(operational_df, points_df, interconnections_df):
    """Merge operational data with points and interconnections data."""
    merged_df = operational_df.merge(points_df[['pointKey', 'pointLabel']], on='pointKey', how='left')
    merged_df = merged_df.merge(interconnections_df[['pointKey', 'fromCountryLabel', 'toCountryLabel']], on='pointKey', how='left')
    return merged_df

def filter_data(merged_df,points_df=None):
    """
    Filter the operational data to keep only entry and exit records
    Additionally, filter the data to keep only the points that are in a given points_df
    In our case it is used to filter transmission points
    Add columns countryTo and countryFrom so that :
    - entry means gas enters "countryFrom" to "countryTo"
    - exit means gas exits "countryTo" to "countryFrom"
    Resulting in all pairs being considered as "entries" for the countryFrom
    """
    # print(f'Size before filtering: {merged_df.shape}')
    filtered_df = merged_df[(merged_df['directionKey'].isin(['entry', 'exit']))]
    filtered_df = filtered_df[filtered_df['value'].notna()]
    if points_df is not None:
        filtered_df = filtered_df[filtered_df['pointKey'].isin(points_df['point_key'])]
    # print(f'... Size after filtering: {filtered_df.shape}')

    return filtered_df

def normalize_direction(filtered_df):
    """
    UNUSED
    NOTE : THis might create some duplicates -> aggregate_entries_exits separates both
    Normalize the direction of the gas flow to have a common direction for all entries.
    Add columns countryTo and countryFrom so that :
    - entry means gas enters "countryFrom" to "countryTo"
    - exit means gas exits "countryTo" to "countryFrom"
    The direction is normalized so that all pairs are considered as "entries" for the countryFrom.
    """
    filtered_df['fromCountryLabel'] = filtered_df.apply(lambda row: row['fromCountryLabel'] if row['directionKey'] == 'entry' else row['toCountryLabel'], axis=1)
    filtered_df['toCountryLabel'] = filtered_df.apply(lambda row: row['toCountryLabel'] if row['directionKey'] == 'exit' else row['fromCountryLabel'], axis=1)
    return filtered_df

def aggregate_entries_exits(filtered_df):
    """
    Group data by pair of countries and direction key.
    Keep direction keys and compute total gas flow.
    Resulting in two dataframes : one for entries and one for exits
    """
    entries_df = filtered_df[filtered_df['directionKey'] == 'entry']
    exits_df = filtered_df[filtered_df['directionKey'] == 'exit']

    relevant_columns = ['fromCountryLabel', 'toCountryLabel', 'value']

    grouped_entries_df = entries_df[relevant_columns].groupby(['fromCountryLabel','toCountryLabel']).sum().reset_index()
    grouped_exits_df = exits_df[relevant_columns].groupby(['fromCountryLabel','toCountryLabel']).sum().reset_index()

    grouped_entries_df.rename(columns={'value': 'entryValue'}, inplace=True)
    grouped_exits_df.rename(columns={'value': 'exitValue'}, inplace=True)

    return grouped_entries_df, grouped_exits_df

def sankey_diagram(combined_df,selected_countries=None):
    """
    UNUSED
    Create a sankey diagram from the aggregated data.
    Pre : The dataframe should contain the following columns : fromCountryLabel, toCountryLabel, entryValue, exitValue

    This can be used as a tool to analyze the flow of gas between countries by analyzing all neighboring countries for example
    """
    selected_df = combined_df.copy()

    # List of unique country labels
    if selected_countries is not None:
        countries = selected_countries
        selected_df = combined_df[(combined_df['toCountryLabel'].isin(countries)) & (combined_df['fromCountryLabel'].isin(countries))]

    else:
        countries = list(set(combined_df['fromCountryLabel']).union(set(combined_df['toCountryLabel'])))


    # Create a dictionary for index mapping
    country_index = {country: i for i, country in enumerate(countries)}

    # Prepare source, target, and values for the Sankey diagram
    source_indices = [country_index[selected_df.loc[i, 'fromCountryLabel']] for i in selected_df.index]
    target_indices = [country_index[selected_df.loc[i, 'toCountryLabel']] for i in selected_df.index]
    entry_values = selected_df['entryValue']
    exit_values = selected_df['exitValue']

    # Prepare Sankey nodes and links
    nodes = dict(label=countries)

    links = dict(
        source=source_indices + target_indices,
        target=target_indices + source_indices,
        value=entry_values.tolist() + exit_values.tolist(),
        color=["blue"] * len(entry_values) + ["red"] * len(exit_values),
        customdata=["Entries"] * len(entry_values) + ["Exits"] * len(exit_values),
        hovertemplate='Flow Type: %{customdata}<br>Source: %{source.label}<br>Target: %{target.label}<br>Value: %{value}<extra></extra>'
    )

    # Create the Sankey diagram
    fig = go.Figure(go.Sankey(
        node=nodes,
        link=links
    ))

    # Update the layout
    fig.update_layout(
        title_text="Total Gas Flow Entries and Exits Between Countries",
        font_size=10
    )

    # Show the figure
    return dict,fig

def merge_pairs_entries_exits(combined_df):
    """ 
    Compare entries and exits between countries.
    Pre : The dataframe should contain the following columns : fromCountryLabel, toCountryLabel, entryValue, exitValue
    Post : A dataframe containing the total entries and exits between countries and a bar chart px figure
    """
    # # Reverse the country pairs and append to the combined dataframe
    # reverse_exits_df = combined_df[['toCountryLabel', 'fromCountryLabel', 'exitValue']].rename(
    #     columns={'toCountryLabel': 'fromCountryLabel', 'fromCountryLabel': 'toCountryLabel'}
    # )
    # reverse_exits_df = reverse_exits_df.groupby(['fromCountryLabel', 'toCountryLabel']).sum().reset_index()
    grouped_entries_df, grouped_exits_df = aggregate_entries_exits(combined_df)
    merged_df = pd.merge(grouped_entries_df, grouped_exits_df, 
                     on=['fromCountryLabel', 'toCountryLabel'], 
                     how='outer').fillna(0)

    merged_df.rename(columns={'entryValue': 'Entries', 'exitValue': 'Exits'}, inplace=True)
    merged_df['Exits'] = -merged_df['Exits']    # Make exits negative for visualization

    return merged_df

def visualize_country_entries_exits(merged_df):
    """ 
    UNUSED
    Create a bar chart to visualize the total gas flow entries and exits between countries.
    Pre : The dataframe should contain the following columns : fromCountryLabel, toCountryLabel, Entries, Exits
    Post : A bar chart px figure
    """
    # Rename to match dataset as exported and the method
    merged_df.rename(columns={'entryValue':'Entries','exitValues':'Exits'})

    melted_df = merged_df.melt(id_vars=['fromCountryLabel', 'toCountryLabel'], 
                           value_vars=['Entries', 'Exits'], 
                           var_name='FlowType', 
                           value_name='Value')

    # Create the bar chart
    fig = px.bar(melted_df, 
                x='fromCountryLabel', 
                y='Value', 
                color='FlowType', 
                barmode='group',
                hover_data=['toCountryLabel'],
                labels={'fromCountryLabel': 'From Country', 'Value': 'Gas Flow (kWh/d)', 'FlowType': 'Flow Type'},
                title='Comparison of Total Gas Flow Entries and Exits Between Countries')

    # Update layout to make the chart more readable
    fig.update_layout(
        xaxis_title='From Country',
        yaxis_title='Gas Flow (kWh/d)',
        legend_title='Flow Type',
        yaxis=dict(tickformat='.2s')  # Format y-axis ticks for readability
    )

    return fig

def visualize_pairs_entries_exits(merged_df):
    """
    UNUSED
    Compare entries and exits between country pairs.
    Pre : The dataframe should contain the following columns : fromCountryLabel, toCountryLabel, entryValue, exitValue
    Post : a bar chart px figure containing the total entries and exits between country pairs
    """
    # Rename to match dataset as exported and the method
    merged_df.rename(columns={'entryValue':'Entries','exitValues':'Exits'})


    merged_df['countryPair'] = merged_df['fromCountryLabel'] + ' -> ' + merged_df['toCountryLabel']
    diff_df = merged_df.copy()
    # print(f"Size before filtering: {diff_df.shape}")
    diff_df = diff_df[['countryPair', 'Entries', 'Exits']]
    diff_df = diff_df[(diff_df['Entries'] != 0) | (diff_df['Exits'] != 0)]
    diff_df = diff_df[diff_df['countryPair'].apply(lambda x: x.split(' -> ')[0] != x.split(' -> ')[1])]
    # print(f"... Size after filtering: {diff_df.shape}")
    diff_df['Difference'] = diff_df['Entries'] + diff_df['Exits']

    # Create a long-form DataFrame suitable for Plotly Express
    long_df = pd.melt(diff_df, 
                    id_vars=['countryPair'], 
                    value_vars=['Entries', 'Exits','Difference'], 
                    var_name='FlowType', 
                    value_name='Value')

    # Define custom color mapping
    color_mapping = {
        'Entries': 'blue', 'Exits': 'red','Difference':'green'}

    # Create the bar chart
    fig = px.bar(long_df, 
                x='countryPair', 
                y='Value', 
                color='FlowType', 
                color_discrete_map=color_mapping,
                labels={'countryPair': 'Country Pair', 'Value': 'Gas Flow (kWh/d)','Difference':'Total diff' ,'FlowType': 'Flow Type'},
                title='Comparison of Total Gas Flow Entries and Exits Between Country Pairs')

    # Update layout for better readability
    fig.update_layout(
        barmode='group',
        xaxis_tickangle=-45,
        yaxis=dict(
            title='Gas Flow (kWh/d)',
            showgrid=True
        ),
        xaxis=dict(
            title='Country Pair',
            categoryorder='total descending'
        )
    )

    return fig
    

def add_country_info(filtered_df):
    """
    Add country information based on 'to' and 'from' country labels.
    Post : All pairs are considered as "entries". Dataset has added columns 'fromCountry', 'toCountry', 'operatorCountryCode'
    """
    filtered_df['fromCountry'] = filtered_df.apply(lambda row: row['fromCountryLabel'] if row['directionKey'] == 'entry' else row['toCountryLabel'], axis=1)
    filtered_df['toCountry'] = filtered_df.apply(lambda row: row['toCountryLabel'] if row['directionKey'] == 'exit' else row['fromCountryLabel'], axis=1)
    filtered_df['operatorCountryCode'] = filtered_df['operatorKey'].str[:2]
    return filtered_df

def aggregate_data(filtered_df):
    """ 
    Aggregate filtered operational data by pair of country and direction.
    POST : new attribute 'totalFlow' = entryValue - exitValue
    - entryValue : total gas flow with key 'entry' , countryFrom to countryTo
    - exitValue : total gas flow with key 'exit' , countryFrom to countryTo    
    """

    grouped_entries,grouped_exits = aggregate_entries_exits(filtered_df)
    # Merge entries and exits data for a given country pair
    # NOTE : 
    #   - exit means gas exits "countryFrom" to "countryTo" 
    #   - entry means gas enters "countryFrom" from "countryTo"

    aggregated_df = pd.merge(grouped_entries, grouped_exits, on=['fromCountryLabel', 'toCountryLabel'], how='outer').fillna(0)

    aggregated_df['totalFlow'] = aggregated_df['entryValue'] - aggregated_df['exitValue']
    aggregated_df = aggregated_df[(aggregated_df['fromCountryLabel'] != aggregated_df['toCountryLabel'])]
    # print(f"... Size after removing intra-country data : {aggregated_df.shape}")

    return aggregated_df , grouped_entries, grouped_exits

def aggregate_percountry(aggregated_df):
    """ 
    Pre : Aggregated_df contains the columns ['fromCountryLabel', 'toCountryLabel', 'entryValue', 'exitValue', 'totalFlow']
    Post : Returns dataset with the columns ['countryName', 'totalEntries', 'totalExits', 'totalFlow']
    Each country name is associated with the total gas flow entries, exits, and total flow.
    """
    # Aggregate the data per country
    entries_df = aggregated_df.groupby('toCountryLabel')['entryValue'].sum().reset_index()
    entries_df.columns = ['countryName', 'totalEntries']

    exits_df = aggregated_df.groupby('toCountryLabel')['exitValue'].sum().reset_index()
    exits_df.columns = ['countryName', 'totalExits']

    totalFlow_df = aggregated_df.groupby('fromCountryLabel')['totalFlow'].sum().reset_index()
    totalFlow_df.columns = ['countryName', 'totalFlow']

    percountry_flow_df = pd.merge(entries_df, exits_df, on='countryName', how='outer').fillna(0)
    percountry_flow_df = pd.merge(percountry_flow_df, totalFlow_df, on='countryName', how='outer').fillna(0)

    return percountry_flow_df



def save_data(aggregated_df, percountry_flow_df, date):
    """Save the aggregated data to CSV files."""
    output_dir = f"{DIR}/data/perCountry"
    os.makedirs(output_dir, exist_ok=True)

    aggregated_df.to_csv(f"{output_dir}/aggregated_data_{date}.csv", index=False)
    percountry_flow_df.to_csv(f'{output_dir}/agg_data_countries_{date}.csv', index=False)
    print(f"Data saved for {date}")

###############
#   Main      #
###############
def process_data(date):
    """Main function to process the operational data and create aggregated files."""
    # print(f"Processing data for {date}...")
    operational_df, points_df, _, interconnections_df = load_data(date)
    rename_columns(points_df, operational_df)
    merged_df = merge_data(operational_df, points_df, interconnections_df)
    filtered_df = filter_data(merged_df)
    filtered_df = add_country_info(filtered_df)
    aggregated_df,_,_ = aggregate_data(filtered_df)
    percountry_flow_df = aggregate_percountry(aggregated_df)
    save_data(aggregated_df, percountry_flow_df, date)
    # print(f"Processing complete for {date}")

if __name__ == "__main__":

    print("Aggregating data per country for 2019...")
    for date in DATES_19:
        process_data(date)
    print("Aggregating data per country for 2023...")
    for date in DATES_23:   
        process_data(date)

    print("Data aggregation complete. Files saved in 'perCountry' directory.")