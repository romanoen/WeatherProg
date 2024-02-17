import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry


class FetchData:

    cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://archive-api.open-meteo.com/v1/archive"

    
    def __init__(
        self,  startdate, enddate, latitude, longitude, hourlyParameters, dailyParameters
    ):
        self.lat = latitude
        self.long = longitude
        self.startdate = startdate
        self.enddate = enddate
        self.hourlyParameters = hourlyParameters
        self.dailyParameters = dailyParameters
    

    def getData(self):

        params = {
            "latitude": self.lat,
            "longitude": self.long,
            "start_date": self.startdate,
            "end_date": self.enddate,
            "daily": self.dailyParameters,
            "hourly": self.hourlyParameters,
        }

        responses = self.openmeteo.weather_api(self.url, params=params)
        response = responses[0]

        metadata = {
            "latidute": [response.Latitude()],
            "longitude": [response.Longitude()],
            "elevation": [response.Elevation()],
        }

        daily = response.Daily()
        hourly = response.Hourly()

        dailycontentdata = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s"),
                end=pd.to_datetime(daily.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left",
            )
        }

        hourlycontentdata = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s"),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            )
        }
        
        for index, element in enumerate(self.dailyParameters):
            dailycontentdata[element] = daily.Variables(index).ValuesAsNumpy()

        for index, element in enumerate(self.hourlyParameters):
            hourlycontentdata[element] = hourly.Variables(index).ValuesAsNumpy()


        
        return [pd.DataFrame(data=metadata).head(), pd.DataFrame(data=hourlycontentdata), pd.DataFrame(data=dailycontentdata)]


