# -*- coding: utf-8 -*-
"""
Quick script to add postal codes to a csv file based on another csv file that
contains townships in Myanmar and their postal code
"""

import pandas as pd
import pickle


def make_township_dict(df):
    ts_directory = df.groupby('name_ts').agg(lambda x: x.value_counts().index[0])['pcode_ts']
    ts_dir_dict = ts_directory.to_dict()
    return ts_dir_dict


def main():
    demanddf = pd.read_csv('HouseholdPopulationbaseddataset_energydemand.csv')
    ts_dir_dict = make_township_dict(demanddf)

    minigrid_pickle = open('mini_grid.pickle')
    minigrid_df = pickle.load(minigrid_pickle)
    minigrid_pickle.close()
    postal_codes = []
    township_name_index = 0
    for row in minigrid_df.itertuples():
        name_ts = row[township_name_index]
        postal_codes.append(ts_dir_dict.get(name_ts, "NA"))

    minigrid_df['Postal_code'] = postal_codes
    minigrid_df.to_csv('minigrid_ac_with_pcode.csv')

if __name__ == '__main__':
    main()
