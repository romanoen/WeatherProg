from matplotlib import pyplot as plt
import fetch_data
import pandas as pd
from pmdarima.arima import auto_arima
from pmdarima.arima import ADFTest



dailyParameters = ["weather_code"]

hourlyParameters = ["temperature_2m"]


fd = fetch_data.FetchData(47.50, 9.5, "1955-01-01", "2024-02-12", hourlyParameters, dailyParameters)
df = fd.getData()

df[1]["date"] = pd.to_datetime(df[1]["date"])
df[1].set_index('date', inplace=True)

df[1].to_csv()


train = df[1].iloc[:int(0.8*(len(df[1])))]
test = df[1].iloc[int(0.8*(len(df[1]))):]

print(train)
print(test)

model = auto_arima(train, start_p=0, d=1, start_q=0,
                    max_p = 5, max_d = 5, max_q = 5,
                    start_P = 0, D = 1, start_Q = 0,
                    max_P = 5, max_D = 5, max_Q = 5,
                    m=8, seasonal=True, error_action="warn",
                    trace=True, supress_warnings=True, 
                    stepwise=True, 
                    random_state=20,
                    n_fits=50)

print(model.summary())






