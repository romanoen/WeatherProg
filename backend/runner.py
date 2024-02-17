import model.predict as predict
import data.fetch_data as fetch_data
import pandas as pd

class Runner:

    def __init__(self, startdate, enddate, periods, latitude, longitude, hourlyParameters, dailyParameters, dataSelector):
        self.startdate = startdate
        self.enddate = enddate
        self.periods = periods
        self.latitude = latitude
        self.longitude = longitude
        self.hourlyParameters = hourlyParameters
        self.dailyParameters = dailyParameters
        self.dataSelector = dataSelector

    def run(self):
        fetchedData = self.fetchData(self.startdate, self.enddate, self.latitude, self.longitude, self.hourlyParameters, self.dailyParameters)
        prognosis = self.predict(fetchedData[self.dataSelector])
        dataframes = [df.set_index('ds') for df in prognosis]
        merged_df = pd.concat(dataframes, axis=1)
        merged_df.reset_index(inplace=True)
        return merged_df
    
    def fetchData(self, startdate, enddate, latitude, longitude, hourlyParameters, dailyParameters):
        fd = fetch_data.FetchData(startdate, enddate, latitude, longitude, hourlyParameters, dailyParameters)
        return fd.getData()

    def predict(self, fetchedData):
        ph = predict.Prediction(fetchedData, self.periods)
        return ph.predict()

