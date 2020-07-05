from WeatherData import WeatherData
from CurrentWeather import CurrentWeather
import sys
import os

weather = WeatherData('49.591', '8.646', 'bcdf63a0553e42805e8f1111bcbd94e5')

currentWeather = weather.getData()

print(str(currentWeather.currentTemp) + "°C min: " + str(currentWeather.minTemp) + "°C max: " + str(currentWeather.maxTemp) + "°C Wind Speed: " + str(currentWeather.windSpeed) + " km/h + Icon: " + str(currentWeather.currentIcon))