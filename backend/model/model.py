import pickle
from pmdarima import ARIMA
from sklearn.metrics import mean_squared_error
import data.fetch_data as fetch_data
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet




dailyParameters = ["temperature_2m_max"]

hourlyParameters = ["temperature_2m"]


fd = fetch_data.FetchData(47.50, 9.5, "2020-01-01", "2024-01-01", hourlyParameters, dailyParameters)
df = fd.getData()

df[2]["date"] = pd.to_datetime(df[2]["date"])
#df[2].set_index('date', inplace=True)

df[2].to_csv("temperatures.csv")

test = df[2][-720:]

df = df[2][:-720]
print("--------------------------------")
print(df)


df.rename(columns={'date': 'ds', 'temperature_2m_max': 'y'}, inplace=True)

print(df)

model = Prophet()
model.fit(df)
future = model.make_future_dataframe(periods=720)  # z.B. für 1 Jahr in die Zukunft

# 5. Vorhersagen machen
forecast = model.predict(future)

print(forecast)


model.plot(forecast)
model.plot_components(forecast)

forecast_subset = forecast[['ds', 'yhat']]  # Selecting only 'ds' and 'yhat'
actual_data_renamed = test.rename(columns={'date': 'ds'})  # Renaming for alignment, if necessary

# Now, merge the two DataFrames on the 'ds' column
merged_df = pd.merge(forecast_subset, actual_data_renamed, on='ds', how='left')

merged_df.to_csv("fc.csv")









