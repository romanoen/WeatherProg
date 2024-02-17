import pandas as pd
from prophet import Prophet

class Prediction:

    def __init__(
            self, data, periodss):
        self.data = data
        self.periods = periodss
        self.transformed_data = []
        self.transform()

    def transform(self):

        date_column = 'date'  
        feature_columns = self.data.columns.drop(date_column)
        
        for column in feature_columns:
            temp_df = self.data[[date_column, column]].copy()
            temp_df.rename(columns={date_column: 'ds', column: 'y'}, inplace=True) 
            self.transformed_data.append(temp_df)

    def predict(self):
        
        predictions = []

        for df in self.transformed_data:
            predictions.append(self.prophesy(df))

        return predictions

    def prophesy(self,df):
        prophet = Prophet()
        prophet.fit(df)
        prognosis = prophet.make_future_dataframe(periods=self.periods)
        forecast = prophet.predict(prognosis)
        return forecast[['ds', 'yhat']].tail(self.periods)


        
