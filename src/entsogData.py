
######################
#       Setup       #
#####################
# Imports
from entsog import EntsogPandasClient
import pandas as pd
import os
import requests

# Constants
current_dir = os.getcwd()
DATA_DIR = f"{current_dir}/data"
# COUNTRY_CODE = 'BE'  # Parameter for the data collection (UNUSED)
N_WEEKS = 4  # Length of the time period for data collection (in weeks)
BASE_OP_URL = "https://transparency.entsog.eu/api/v1/operationaldatas?limit=10000&timeZone=UCT"  # Base URL for the data collection
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
def collect_points_data(client, data_dir):
    """
    Collects and saves the points data using the entsog-py client.
    """
    point_data = client.query_connection_points()
    # point_data.to_csv(os.path.join(data_dir, "points_data.csv"))
    print("Points data collected")

collect_points_data(client, DATA_DIR)


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
    """Collects operational data using the public API."""
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
    # op_data = client.query_operational_data_all(start=start_date, end=end_date, indicators=['physical_flow'])

    json_data = collect_operational_API(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    op_data = process_operational_data(json_data)    

    op_data_columns = [
        'direction_key', 'flow_status', 'id', 'id_point_type', 'operator_key',
        'period_from', 'period_to', 'period_type', 'point_key', 'point_label',
        'tso_eic_code', 'unit', 'value'
    ]
    
    op_data = op_data[op_data_columns]
    file_name = f"op_data_{year}_{month:02d}.csv"
    # op_data.to_csv(os.path.join(data_dir, file_name))
    print(f"Operational data for {start_date.strftime('%Y-%m-%d')} collected")

def collect_yearly_operational_data(client, year, data_dir, n_weeks):
    """Collects operational data for each month of the specified year."""
    for month in range(1, 13):
        collect_operational_data(client, year, month, data_dir, n_weeks)


# Collect the operational data for the specified years
collect_yearly_operational_data(client, YEAR1, DATA_DIR, N_WEEKS)
collect_yearly_operational_data(client, YEAR2, DATA_DIR, N_WEEKS)
print("-----------  Data Collected -----------")
