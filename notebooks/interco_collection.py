from entsog import EntsogPandasClient
import pandas as pd 
import os

current_dir = os.getcwd()
DATA_DIR = f"{current_dir}"

client = EntsogPandasClient()
interconnections_df = client.query_interconnections()
interconnections_df.to_csv(f'{DATA_DIR}/notebooks/interconnections_data.csv',index=False)