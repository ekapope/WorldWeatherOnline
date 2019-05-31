# -*- coding: utf-8 -*-
"""
This script is used to retrieve and transform weather data into single csv.
example API exploror: https://www.worldweatheronline.com/developer/premium-api-explorer.aspx

input: api_key, location_list, start_date, end_date, frequency

output: location_name.csv'

@author: Ekapope Viriyakovithya
"""

from setuptools import setup

setup(name='wwo_hist',
      version='0.1',
      description='Retrieve historical weather data and save into single csv',
      url='https://github.com/ekapope/WorldWeatherOnline/',
      author='Flying Circus',
      author_email='ekapope.v@gmail.com',
      license='MIT',
      packages=['wwo_hist'],
      zip_safe=False)


