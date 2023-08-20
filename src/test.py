from ForecastData import ForecastData
from CurrentWeather import CurrentWeather
from WeatherData import WeatherData
from datetime import date
import json
import time

for i in range(10):
    #read config data
    config = open('src/config.json', 'r')
    config = json.loads(config.read())

    #get current weather data
    weatherdata = WeatherData(str(config['lat']), str(config['lon']), config['api_key'])
    currentWeather = weatherdata.getCurrentWeather()

    #get location name
    location = weatherdata.getLocationName()

    print("current location: " + location)
    print("current temperature: "+  str(currentWeather.currentTemp))
    print("Max: " + str(currentWeather.maxTemp))
    print("Min: " + str(currentWeather.minTemp))
    print("Wind: " + str(currentWeather.windSpeed) + "\n")

    forecast = weatherdata.getForecast()

    for j in range(3):
        print("forecast day " + str(j))
        print(str(forecast[j].maxTemp))
        print(str(forecast[j].minTemp))

    time.sleep(10)