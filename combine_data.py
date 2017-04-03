# -*- coding: utf-8 -*-
"""Quick script to combine multiple csv files to match up data about townships
in Myanmar using township postal code to join on"""

import pandas as pd
from sklearn import preprocessing

minigrid_csv_name = 'semi_matched_minigrid.csv'
minigrid_df = pd.read_csv(minigrid_csv_name)

demand_csv_name = 'HouseholdPopulationbaseddataset_energydemand.csv'
demanddf = pd.read_csv(demand_csv_name)
mergeddf = minigrid_df.merge(demanddf, on='pcode_ts', how='left')

pay_csv_name = 'HouseholdPopulationbaseddataset_abilitytopay.csv'
paydf = pd.read_csv(pay_csv_name)
keep_cols = ['name_ts', 'pcode_ts', 'Total_Score']
paydf = paydf[keep_cols]
mergeddf = mergeddf.merge(paydf, on='pcode_ts', how='left')
final_cols = ['Township', 'Population','Longitude','Latitude','AC_output_yearly', 'pcode_ts', 'hh_t', 'YR 1', 'YR 2', 'YR 3','YR 4','YR 5','YR 6', 'Total_Score']
final_df = mergeddf[final_cols]
final_df['Total_yearly_demand'] = final_df['YR 1'] + final_df['YR 2'] + final_df['YR 3'] + final_df['YR 4'] + final_df['YR 5'] + final_df['YR 6']
final_df = final_df.dropna(axis=0, how='any')


to_normalize = final_df[['AC_output_yearly', 'Total_Score', 'Total_yearly_demand']]
to_normalize_values = to_normalize.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(to_normalize_values)
ac_output_index = 0
pay_index = 1
demand_index = 2
final_df['Normalized AC output'] = x_scaled[:, ac_output_index]
final_df['Normalized Ability to Pay'] = x_scaled[:, pay_index]
final_df['Normalized demand'] = x_scaled[:, demand_index]
final_df.to_csv('all_data.csv')
