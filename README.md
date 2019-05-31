# WorldWeatherOnline historical weather data python

This package is used to retrieve and transform historical weather data from www.worldweatheronline.com into pandas dataframe and csv.

You can get API key for free (free trial 500 requests/key for 60 days, as of 30-May-2019).

example API explorer: https://www.worldweatheronline.com/developer/premium-api-explorer.aspx


#### Install the package:
```
pip install wwo-hist
```

#### import package 
```python
from wwo_hist import retrieve_hist_data
```

#### set working directory to store csv file output
```python
import os
os.chdir(".\YOUR_PATH")
```


input: api_key, location_list, start_date, end_date, frequency
output: location_name.csv'

#### Example code
```python
frequency=3
start_date = '11-dec-2018'
end_date = '11-mar-2019'
api_key = 'YOUR_API_KEY'
location_list = ['singapore','california']

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = False)
```