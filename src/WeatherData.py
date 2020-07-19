import requests
import json
from CurrentWeather import CurrentWeather
from ForecastData import ForecastData

class WeatherData:

    def __init__(self, latitude, longitude, key):
        self.longitude = longitude
        self.latitude = latitude
        self.key = key
    

    def getCurrentWeather(self):
        resp = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + self.latitude + '&lon=' + self.longitude + '&appid='+ self.key)

        data = json.loads(resp.text)
        currentData = data['current']

        currentTemp = currentData['temp']
        currentTemp = round(currentTemp - 273.15, 1)

        currentIcon = currentData['weather'][0]['icon']

        dailyData = data['daily'][0]

        maxTemp = dailyData['temp']['max']
        maxTemp = round(maxTemp - 273.15, 1)

        minTemp = dailyData['temp']['min']
        minTemp = round(minTemp - 273.15, 1)

        windSpeed = round(dailyData['wind_speed'], 1)

        weather = CurrentWeather(currentTemp, windSpeed, maxTemp, minTemp, currentIcon)
        return weather

    def getForecast(self):
        resp = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + self.latitude + '&lon=' + self.longitude + '&appid='+ self.key)

        data = json.loads(resp.text)
        forecastData = data['daily']

        forecast = [ForecastData(round(forecastData[1]['wind_speed'], 1), round(forecastData[1]['temp']['max'] - 273.15, 1), round(forecastData[1]['temp']['min'] - 273.15, 1), forecastData[1]['weather'][0]['icon']),
                    ForecastData(round(forecastData[2]['wind_speed'], 1), round(forecastData[2]['temp']['max'] - 273.15, 1), round(forecastData[2]['temp']['min'] - 273.15, 1), forecastData[2]['weather'][0]['icon']),
                    ForecastData(round(forecastData[3]['wind_speed'], 1), round(forecastData[3]['temp']['max'] - 273.15, 1), round(forecastData[3]['temp']['min'] - 273.15, 1), forecastData[3]['weather'][0]['icon'])]

        return forecast

        
        
    
