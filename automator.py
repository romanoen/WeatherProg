from numpy import mean
import numpy as np
import openmeteo_requests
import seaborn as sns
import matplotlib.pyplot as plt
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in daily or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 39.50,
	"longitude": 32.5,
	"start_date": "2009-01-01",
	"end_date": "2024-02-12",
    "temp": "temperature_2m_max",
	"daily": ["temperature_2m_max",
             "weather_code",
              "temperature_2m_min",
             "precipitation_sum",
             "precipitation_hours",
             "sunshine_duration",
             "daylight_duration",
    ],
    "hourly": ["temperature_2m",
               "wind_speed_10m"]

}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]


print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()

temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
weather_code = daily.Variables(1).ValuesAsNumpy()
temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
hourly_precipitation_sum = daily.Variables(3).ValuesAsNumpy()
precipitation_hours = daily.Variables(4).ValuesAsNumpy()
sunshine_duration = daily.Variables(5).ValuesAsNumpy()
daylight_duration = daily.Variables(6).ValuesAsNumpy()


daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s"),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

hourly = response.Hourly()
averageTemp = hourly.Variables(0).ValuesAsNumpy()
averageWind = hourly.Variables(1).ValuesAsNumpy()
averageTemp = averageTemp.reshape(-1, 24)
averageWind = averageWind.reshape(-1, 24)

daily_data["year"] = daily_data["date"].year
daily_data["daysSinceYearStart"] = daily_data["date"].dayofyear
#daily_data["temperature_2m_max"] = temperature_2m_max
#daily_data["temperature_2m_min"] = temperature_2m_min
daily_data["hourly_precipitation_sum"] = hourly_precipitation_sum
#daily_data["weather_code"] = weather_code
daily_data["precipitation_hours"] = precipitation_hours
daily_data["sunshine_duration"] = sunshine_duration
daily_data["daylight_duration"] = daylight_duration
daily_data["averageTemp"] = averageTemp.mean(axis=1)
daily_data["averageWind"] = averageWind.mean(axis=1)


dataframe = pd.DataFrame(data = daily_data)
dataframe = dataframe.drop(columns = "date")
dataframe.to_csv('data.csv')

cor = dataframe.corr(method='spearman')
cor.to_csv('correlation.csv')








