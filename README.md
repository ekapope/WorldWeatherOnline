# WorldWeatherOnline historical weather data API wrapper

This package is used to retrieve and transform historical weather data from www.worldweatheronline.com into pandas dataframe and csv.

You can get API key for free (free trial 500 requests/key for 60 days, as of 30-May-2019).

example API explorer: https://www.worldweatheronline.com/developer/premium-api-explorer.aspx


#### Install the package:
```
pip install wwo-hist
```

#### Import package
```python
from wwo_hist import retrieve_hist_data
```

#### Set working directory to store output csv file(s)
```python
import os
os.chdir(".\YOUR_PATH")
```

Input: api_key, location_list, start_date, end_date, frequency

Output: location_name.csv


#### Example code
```python
frequency=3
start_date = '11-DEC-2018'
end_date = '11-MAR-2019'
api_key = 'YOUR_API_KEY'
location_list = ['singapore','california']

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)
```

#### Parameters:
```
api_key: string
(Premium/ free trial) API key from worldweatheronline.com

location_list: list of string
US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name

start_date: string
Preferred date format: 'dd-mmm-yyyy'

end_date: string
Preferred date format: 'dd-mmm-yyyy'

frequency: integer
1, 3, 6, 12, 24
1 hourly, 3 hourly, 6 hourly, 12 hourly (day/night) or 24 hourly (day average)

location_label: bool, default = False
If True, all column names will have city name as prefix.

export_csv: bool, default = True
If False, no csv file will be exported to current directory.

store_df: bool, default = False
If True, retrieved dataframe(s) will be stored as list in the work space.

```