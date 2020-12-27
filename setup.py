# -*- coding: utf-8 -*-
"""
This script is used to retrieve and transform weather data into single csv.
example API explorer: https://www.worldweatheronline.com/developer/premium-api-explorer.aspx

input: api_key, location_list, start_date, end_date, frequency

output: location_name.csv'

@author: Ekapope Viriyakovithya
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wwo_hist",
    version="0.0.7",
    author="Ekapope Viriyakovithya",
    author_email="ekapope.v@gmail.com",
    description="This package is used to retrieve and transform historical weather data from www.worldweatheronline.com into pandas dataframe and csv.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ekapope/WorldWeatherOnline",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
