# -*- coding: utf-8 -*-
"""
This script is used to retrieve and transform weather data into single csv.
example API explorer: https://www.worldweatheronline.com/developer/premium-api-explorer.aspx

input: api_key, location_list, start_date, end_date, frequency

output: location_name.csv'

@author: Ekapope Viriyakovithya
"""

import urllib.request
import urllib.parse
import json
import pandas as pd
from datetime import datetime
import os


##################################
# function to unnest json for each month
def extract_monthly_data(data):
    num_days = len(data)
    # initialize df_month to store return data
    df_month = pd.DataFrame()
    for i in range(num_days):
        # extract this day
        d = data[i]
        # astronomy data is the same for the whole day
        astr_df = pd.DataFrame(d['astronomy'])
        # hourly data; temperature for each hour of the day
        hourly_df = pd.DataFrame(d['hourly'])
        # this wanted_key will be duplicated and use 'ffill' to fill up the NAs
        wanted_keys = ['date', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour', 'uvIndex']  # The keys you want
        subset_d = dict((k, d[k]) for k in wanted_keys if k in d)
        this_df = pd.DataFrame(subset_d, index=[0])
        df = pd.concat([this_df.reset_index(drop=True), astr_df], axis=1)
        # concat selected astonomy columns with hourly data
        df = pd.concat([df, hourly_df], axis=1)
        df = df.fillna(method='ffill')
        # make date_time columm to proper format
        # fill leading zero for hours to 4 digits (0000-2400 hr)
        df['time'] = df['time'].apply(lambda x: x.zfill(4))
        # keep only first 2 digit (00-24 hr) 
        df['time'] = df['time'].str[:2]
        # convert to pandas datetime
        df['date_time'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        # keep only interested columns
        col_to_keep = ['date_time', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour', 'uvIndex',
                       'moon_illumination', 'moonrise', 'moonset', 'sunrise', 'sunset',
                       'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC', 'WindGustKmph',
                       'cloudcover', 'humidity', 'precipMM', 'pressure', 'tempC', 'visibility',
                       'winddirDegree', 'windspeedKmph']
        df = df[col_to_keep]
        df = df.loc[:,~df.columns.duplicated()]
        df_month = pd.concat([df_month, df])
    return (df_month)


##################################
# function to retrive data by date range and location
# default frequency = 1 hr
# each month costs 1 request (free trial 500 requests/key, as of 30-May-2019)
def retrieve_this_location(api_key, location, start_date, end_date, frequency, response_cache_path):
    start_time = datetime.now()

    # create list of first day of month for range between start and end dates non-inclusive (open)
    list_mon_begin = pd.date_range(start_date, end_date, freq='MS', closed='right')
    # convert to Series and add start_date at beginning
    list_mon_begin = pd.concat([pd.Series(pd.to_datetime(start_date)), pd.Series(list_mon_begin)], ignore_index=True)

    # create list of month end dates for range between start and end dates non-inclusive (open)
    list_mon_end = pd.date_range(start_date, end_date, freq='M', closed='left')
    # convert to Series and add end_date at end
    list_mon_end = pd.concat([pd.Series(list_mon_end), pd.Series(pd.to_datetime(end_date))], ignore_index=True)

    # count number of months to be retrieved
    total_months = len(list_mon_begin)

    # initialize df_hist to store return data
    df_hist = pd.DataFrame()
    for m in range(total_months):
        start_d = str(list_mon_begin[m])[:10]
        end_d = str(list_mon_end[m])[:10]
        file_path = f'{response_cache_path}/{location}_{start_d}_{end_d}'
        if response_cache_path and os.path.exists(file_path):
            print('Reading cached data for ' + location + ': from ' + start_d + ' to ' + end_d)
            with open(f'{response_cache_path}/{location}_{start_d}_{end_d}', 'r') as f:
                json_data = json.load(f)
        else:
            print('Currently retrieving data for ' + location + ': from ' + start_d + ' to ' + end_d)
            url_page = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=' + api_key + '&q=' + location + '&format=json&date=' + start_d + '&enddate=' + end_d + '&tp=' + str(
                frequency)
            json_page = urllib.request.urlopen(url_page, timeout=10)
            json_data = json.loads(json_page.read().decode())

        if response_cache_path:
            with open(f'{response_cache_path}/{location}_{start_d}_{end_d}', 'w') as f:
                json.dump(json_data, f)
        data = json_data['data']['weather']
        # call function to extract json object
        df_this_month = extract_monthly_data(data)
        df_this_month['location'] = location
        df_hist = pd.concat([df_hist, df_this_month])

        time_elapsed = datetime.now() - start_time
        print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
    return (df_hist)


##################################
# main function to retrive the data by location list
def retrieve_hist_data(api_key, location_list, start_date, end_date, frequency, location_label=False, export_csv=True,
                       store_df=False, response_cache_path=None):
    result_list = []
    for location in location_list:
        print('\n\nRetrieving weather data for ' + location + '\n\n')
        df_this_city = retrieve_this_location(api_key, location, start_date, end_date, frequency, response_cache_path)

        if (location_label == True):
            # add city name as prefix to the colnames
            df_this_city = df_this_city.add_prefix(location + '_')
            df_this_city.columns.values[0] = 'date_time'

        if (export_csv == True):
            df_this_city.to_csv('./' + location + '.csv', header=True, index=False)
            print('\n\nexport ' + location + ' completed!\n\n')

        if (store_df == True):
            # save result as object in the work space
            result_list.append(df_this_city)

    return (result_list)
##################################
