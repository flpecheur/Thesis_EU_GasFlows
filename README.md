# EU Gas flow between 2019 and 2023

This project processes and visualizes data related to LNG points, country interconnections, and flow dynamics before the invasion of Ukraine bu Russia. Follow the instructions below to set up and run the project.


## Setup Instructions

1. **Clone the Repository**
   ```sh
   git clone <repository_url>
   cd FINAL
   ```

2. **Install Dependencies**
This code relies on the following packages : 
* entsog-py (optional, only used to run the entsogData script which's data is already present in the data directory). However, if you want to install this package you should check the entsog-py git for more precise instructions. 
* plotly
* pandas
* numpy

3. **(OPTIONAL) Build datasets**

All datasets are already loaded in the data directory   

(OPTIONAL) Run the entsogData.py script to collect data from the ENTSOG transparency platform and store it in the data and data/opData directories.
```sh
python src/entsogData.py
```
Combine information about LNG points
```sh
python src/buildDataPerPointType.py
```
Aggregate data per country.    
Set the desired year at the top of the file in the YEAR constant.
```sh
python src/buildDataPerCountry.py
```
(OPTIONAL) Prepare data for country interconnection pairs. Note that the map directly calls a method so running this script is not necessary for the map to work.    
Set the desired year at the top of the file in the YEAR constant.
```sh
python src/buildPairs.py
```
4. **Run maps**

  * mapCountryTotals : Run the mapCountryTotals.py script to create maps for total entries, exits, and overall flows for each year.
  * mapCountryInterractive : Run the mapCountryInterractive_YEAR.py script to create an interactive map of LNG entry points (replace YEAR with the specific year, e.g., mapCountryInterractive_2019.py).
  * mapPairs : Run the mapPairs_FINAL.py script to display total connection flows between countries. Set the desired year at the top of the file in the YEAR constant.

## Maps descriptions
### mapCountryTotals.py: 
This script generates maps that display total entries, total exits, and overall flow for each year. Each map can be viewed by month, allowing for a detailed analysis of the flow dynamics over time. These maps provide a comprehensive overview of the flow patterns and are useful for identifying trends and anomalies in the data.

### mapCountryInterractive_YEAR.py: 
This script (where YEAR is replaced with the specific year, e.g., mapCountryInterractive_2019.py) creates an interactive map using Dash. It shows active and non-active LNG plants, and users can select a country from a dropdown menu to highlight the associated points and view the flow evolution throughout the year. Currently, it displays total entries, with plans to add graphs for total exits.

### mapPairs_FINAL.py:
This script visualizes the total connection flows between countries over a specified year. When a country is selected, the map shows the total contribution from each connected country and the flow evolution during the year. This tool helps in understanding the flow relationships and dependencies between different countries.

# Additional Notes : 
* In buildPairs.py, the DATA_DICT constant contains the final initialized dictionary. The YEAR constant can be set to choose the year for data processing.
* In buildDataPerCountry.py, the YEAR constant should be set at the top of the file. This script aggregates data per country to display total entries/exits/flow per country. Note that some methods in this file are for visualization and may need to be checked for compatibility with recent code and data modifications.
* mapCountryTotals.py creates maps for each year's total entries, total exits, and overall flows, with the possibility to display each month. Future improvements plan to combine all three maps for each year into a single layout.
mapCountryInterractive_YEAR.py provides a Dash layout showing active and non-active LNG plants. * Selecting a country in the dropdown highlights associated points and flow evolution during the year. Currently, this only displays total entries, but graphs for total exits will be added shortly.
* mapPairs_FINAL.py displays total connection flows between countries over the year. Selecting a specific country shows total contributions per connected country and the flow evolution during the year. The YEAR parameter at the top of the file should be set accordingly. Some inconsistencies in flow direction have been found and will be investigated further, but the data is consistent.





6. 

