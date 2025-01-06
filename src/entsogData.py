
######################
#       Setup       #
#####################
# Imports
from entsog import EntsogPandasClient
import pandas as pd
import time
import os
import requests


UPDATE_POINTS = False # Set to True to update the points data

# Constants
current_dir = os.getcwd()
DATA_DIR = f"{current_dir}/data"
N_WEEKS = 4  # Length of the time period for data collection (in weeks)
BASE_OP_URL = "https://transparency.entsog.eu/api/v1/operationaldatas?limit=-1&timeZone=UCT"  # Base URL for the data collection
YEAR1 = 2019  # Start year for the data collection
YEAR2 = 2023  # Second year for the data collection
# Mapping from API fields to desired column names
COLUMN_MAPPING = {
    "directionKey": "direction_key",
    "flowStatus": "flow_status",
    "id": "id",
    "idPointType": "id_point_type",
    "operatorKey": "operator_key",
    "periodFrom": "period_from",
    "periodTo": "period_to",
    "periodType": "period_type",
    "pointKey": "point_key",
    "pointLabel": "point_label",
    "tsoEicCode": "tso_eic_code",
    "unit": "unit",
    "value": "value"
}

# Ensure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize the Entsog client
client = EntsogPandasClient()

######################
#    Points Data     #
######################
def collect_points_data(client, data_dir, to_csv=True):
    """
    Collects and saves the points data using the entsog-py client.
    """
    point_data = client.query_connection_points()
    if to_csv:
        point_data.to_csv(os.path.join(data_dir, "points_data.csv"))
    print("Points data collected")




################################
#    Interconnections Data     #
################################
def collect_interconnections_data(data_dir, to_csv=False):
    """
    Collects and saves the interconnections data using the entsog-py client.
    """

    # List of country codes
    countries = [
        "AL", "CH", "AT", "AZ", "BA", "BE", "BG", "BY", "CY", "CZ", "DE", "DK", "EE",
        "ES", "FI", "FR", "GR", "HR", "HU", "IE", "UK", "IT", "LT", "LU", "LV", "LY",
        "MD", "MK", "MT", "NL", "NO", "PL", "PT", "RO", "RS", "RU", "SE", "SI", "SK",
        "TN", "TR", "SM", "UA"
    ]
    countries = list(set(countries) - set(["AZ","BA","CY","MT","TN","SM"]))# Countries with no data

    base_url = "https://transparency.entsog.eu/api/v1/interconnections?fromCountryKey={}&offset=0"

    interconnections_data = {}

    # Loop making an API request to the TP for each CC
    for country in countries:
        response = requests.get(base_url.format(country))
        
        if response.status_code == 200:
            try:
                data = response.json()
                interconnections_data[country] = data['interconnections']
                # print(f"Data collected for {country}")
            except KeyError as e:
                print(f"KeyError for country {country}")
                print(e)
        else:
            print(f"Failed to collect data for {country}")
        
        # Sleep to avoid hitting the rate limit
        time.sleep(1)

    # Convert the data to a pandas DataFrame
    all_interconnections = []

    for country, interconnections in interconnections_data.items():
        cnt = 0
        for point in interconnections:
            all_interconnections.append({
            "country": country,
            "pointKey": point.get("pointKey"),
            "pointLabel": point.get("pointLabel"),
            "isSingleOperator": point.get("isSingleOperator"),
            "pointTpMapX": point.get("pointTpMapX"),
            "pointTpMapY": point.get("pointTpMapY"),
            "fromSystemLabel": point.get("fromSystemLabel"),
            "fromInfrastructureTypeLabel": point.get("fromInfrastructureTypeLabel"),
            "fromCountryKey": point.get("fromCountryKey"),
            "fromCountryLabel": point.get("fromCountryLabel"),
            "fromDirectionKey": point.get("fromDirectionKey"),
            "fromOperatorKey": point.get("fromOperatorKey"),
            "fromBzKey": point.get("fromBzKey"),
            "fromPointKey": point.get("fromPointKey"),
            "toSystemLabel": point.get("toSystemLabel"),
            "toInfrastructureTypeLabel": point.get("toInfrastructureTypeLabel"),
            "toCountryKey": point.get("toCountryKey"),
            "toCountryLabel": point.get("toCountryLabel"),
            "toOperatorKey": point.get("toOperatorKey"),
            "toOperatorLabel": point.get("toOperatorLabel"),
            "toBzKey": point.get("toBzKey"),
            "toPointKey": point.get("toPointKey"),
            "toPointLabel": point.get("toPointLabel"),
            "validFrom": point.get("validFrom"),
            "validto": point.get("validto"),
            "lastUpdateDateTime": point.get("lastUpdateDateTime"),
            "id": point.get("id")
        })

    df = pd.DataFrame(all_interconnections)
    # Save the data to a CSV file
    df.to_csv(f"{data_dir}/interconnections_data.csv", index=False)

    print("Data collection complete. Data saved to interconnections_data.csv.")


######################
#  Operational Data  #
######################
def process_operational_data(json_data):
    """Processes JSON data into a pandas DataFrame."""
    records = json_data['operationaldatas']
    df = pd.DataFrame(records)
    df = df.rename(columns=COLUMN_MAPPING)

    return df

def collect_operational_API(start_date, end_date):
    """
    Collects operational data using the public API.
    """
    url = f"{BASE_OP_URL}&from={start_date}&to={end_date}&periodType=day&indicator=Physical+Flow"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def collect_operational_data(client, year, month, data_dir, n_weeks):
    """
    Collects and saves the operational data for a given month and year using the entsog-py client.
    """
    start_date = pd.Timestamp(f'{year}-{month:02d}-01')
    end_date = start_date + pd.DateOffset(weeks=n_weeks)
    
    print(f"Data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} loading ...")
    # op_data = client.query_operational_data_all(start=start_date, end=end_date, indicators=['physical_flow']) # We use the API version for more control

    json_data = collect_operational_API(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    op_data = process_operational_data(json_data)    

    op_data_columns = [
        'direction_key', 'flow_status', 'id', 'id_point_type', 'operator_key',
        'period_from', 'period_to', 'period_type', 'point_key', 'point_label',
        'tso_eic_code', 'unit', 'value'
    ]
    
    op_data = op_data[op_data_columns]
    file_name = f"opData/op_data_{year}_{month:02d}.csv" 
    op_data.to_csv(os.path.join(data_dir, file_name))
    print(f"Operational data for {start_date.strftime('%Y-%m-%d')} collected")

def collect_yearly_operational_data(client, year, data_dir, n_weeks):
    """Collects operational data for each month of the specified year."""
    for month in range(1, 13): 
        collect_operational_data(client, year, month, data_dir, n_weeks)


# Collect the operational data for the specified years

if UPDATE_POINTS : 
    collect_points_data(client, DATA_DIR)
    collect_interconnections_data(DATA_DIR) 

collect_yearly_operational_data(client, YEAR1, DATA_DIR, N_WEEKS)
collect_yearly_operational_data(client, YEAR2, DATA_DIR, N_WEEKS)
print("-----------  Data Collected -----------")
