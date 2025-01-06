import pandas as pd
from buildDataPerCountry import aggregate_data, load_data, rename_columns,merge_data
from buildDataPerCountry import visualize_pairs_entries_exits

samples = ['2019_01', '2019_02', '2019_03', '2019_04', '2019_05', '2019_06', '2019_07', '2019_08', '2019_09', '2019_10', '2019_11', '2019_12','2023_01', '2023_02', '2023_03', '2023_04', '2023_05', '2023_06', '2023_07', '2023_08', '2023_09', '2023_10', '2023_11', '2023_12']

def compare_nans():
    to_country_nans = []
    from_country_nans = []

    for DATE in samples:
        op_df, points_df, point_dir_df, interco_df = load_data(DATE)

        rename_columns(points_df,op_df)
        merged_df = merge_data(op_df, points_df, interco_df)

        to_country_nans.append(merged_df['toCountryLabel'].isna().sum())
        from_country_nans.append(merged_df['fromCountryLabel'].isna().sum())


    print(f" toCountryLabel NaNs: {to_country_nans} , mean: {sum(to_country_nans)/len(to_country_nans)}")
    print(f" fromCountryLabel NaNs: {from_country_nans}, mean: {sum(from_country_nans)/len(from_country_nans)}")

def compare_total_entries_exits():

    year_total = pd.DataFrame(columns=['fromCountryLabel','toCountryLabel','Entries','Exits'])

    for DATE in samples:
        op_df, points_df, point_dir_df, interco_df = load_data(DATE)

        rename_columns(points_df,op_df)
        merged_df = merge_data(op_df, points_df, interco_df)
        merged_df = aggregate_data(merged_df)
        print(merged_df)
        merged_df['countryPair'] = merged_df['fromCountryLabel'] + ' -> ' + merged_df['toCountryLabel']

        for idx,row in merged_df.iterrows():
            year_total = pd.concat([year_total, row], ignore_index=True)
            
    year_total = year_total.groupby(['fromCountryLabel','toCountryLabel']).sum().reset_index()
    visualize_pairs_entries_exits(year_total)

compare_total_entries_exits()
