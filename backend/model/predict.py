import pandas as pd
from prophet import Prophet

class Prediction:

    def __init__(
            self, data, periodss):
        self.data = data
        self.periods = periodss
        self.transformedData = []
        self.origColNames = []
        self.transform()

    def transform(self):

        date_column = 'date'  
        feature_columns = self.data.columns.drop(date_column)
        
        for column in feature_columns:
            temp_df = self.data[[date_column, column]].copy()
            temp_df.rename(columns={date_column: 'ds', column: 'y'}, inplace=True) 
            self.transformedData.append(temp_df)
            self.origColNames.append(column)

    def predict(self):
        
        predictions = []

        for idx, df in enumerate(self.transformedData):
            predictions.append(self.prophesy(df, self.origColNames[idx]))

        return predictions

    def prophesy(self,df,origColnames):
        prophet = Prophet()
        prophet.fit(df)
        prognosis = prophet.make_future_dataframe(periods=self.periods)
        forecast = prophet.predict(prognosis)
        forecast.rename(columns={'yhat': origColnames}, inplace=True)  
        return forecast[['ds', origColnames]].tail(self.periods)


        
