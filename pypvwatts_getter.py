# -*- coding: utf-8 -*-
"""Script to get the AC output of a solar installation in a given location
from the NREL PVWatts caluclator API and add it to a csv file. Script reads in
a csv with township locations in Myanmar, makes request to PVWatts API to get
yearly AC output at that lattitude and longitude under certain assumptions and
then rewrites the data to a new csv

The assumptions used are:
* 1kw capacity
* standard module type (not premium or thin film)
* 14% loss
* Fixed roof array
* Tilt = latitude
* Azimuth = 0

"""

from pypvwatts import PVWatts
import pandas as pd
import pickle

def setup_api_connection():
    with open('api_key.txt') as api_file:
        key = api_file.readline()
    PVWatts.api_key = key

def load_candidates(filename):
    all_grids = pd.read_csv(filename)
    return all_grids

def make_requests(df, system_cap):
    ac_output = []
    latitude_index = 3
    longitude_index = 2
    for i, item in enumerate(df.itertuples()):
        result = PVWatts.request(system_capacity=system_cap, module_type=0, array_type=1,
                azimuth=0, tilt=item[latitude_index], dataset='intl',
                losses=0.14, lat=item[latitude_index], lon=item[longitude_index]).ac_annual
        ac_output.append(result)
    return ac_output

def group_by_township(df):
    grouped_pop = df.groupby('Township').sum()['Population']
    average_lon = df.groupby('Township').mean()['Longitude']
    average_lat = df.groupby('Township').mean()['Latitude']
    grouped_pop = grouped_pop.to_frame()
    average_lon = average_lon.to_frame()
    average_lat = average_lat.to_frame()
    new_df = grouped_pop.join([average_lon, average_lat])
    return new_df

def main():
    input_grid_file = 'allgrids2014.csv'
    setup_api_connection()
    df = load_candidates(input_grid_file)
    only_minigrids = df[df['System']=='mini-grid']

    only_minigrids = group_by_township(only_minigrids)

    ac_list = make_requests(only_minigrids, 1)

    only_minigrids['AC_output_yearly'] = ac_list
    minigrid_pickle = open('mini_grid.pickle', 'wb')
    pickle.dump(only_minigrids, minigrid_pickle)
    minigrid_pickle.close()

    only_minigrids.to_csv('minigrids_w_ac.csv')

if __name__ == '__main__':
    main()
