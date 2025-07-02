import pandas as pd
from dataclasses import dataclass
import requests

@dataclass
class API_Params:
    lat = 0
    lon = 0
    start = 0
    end = 0
    appid = 0
    API_key = "933ff313f244e5161b4df88393c24201"

location = input("Location: ")

API_KEY = "933ff313f244e5161b4df88393c24201"

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 52.52,
	"longitude": 13.41,
	"end_date": "2025-06-09",
	"start_date": "2025-05-26",
	"hourly": "temperature_2m"
}

# API_Params = f"""
# http://api.openweathermap.org/data/2.5/air_pollution/history?\
# lat={lat}&lon={lon}&start={start}&end={end}&appid={API_key}
# """

# print(API_URI)
r = requests.get(url, params=params)

json = dict(r.json())

df = pd.DataFrame(json)

print(df.head())
