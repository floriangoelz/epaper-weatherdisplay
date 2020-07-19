from ForecastData import ForecastData
from CurrentWeather import CurrentWeather
from WeatherData import WeatherData
from datetime import date
import sys
import os
import json 
import requests

today = date.today()
print((today.weekday() + 3) % 7)