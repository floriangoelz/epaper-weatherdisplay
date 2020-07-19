from ForecastData import ForecastData
from CurrentWeather import CurrentWeather
from WeatherData import WeatherData
import sys
import os
import json 
import requests

resp = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=49.591&lon=8.646&appid=bcdf63a0553e42805e8f1111bcbd94e5')
data = json.loads(resp.text)
forecastData = data['daily']
print(forecastData[1]['weather'][0]['icon'])