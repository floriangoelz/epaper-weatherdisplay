import requests
import json
from CurrentWeather import CurrentWeather

class WeatherData:

    def __init__(self, latitude, longitude, key):
        self.longitude = longitude
        self.latitude = latitude
        self.key = key
    

    def getData(self):
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

        
        
    
