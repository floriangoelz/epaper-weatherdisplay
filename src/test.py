from ForecastData import ForecastData
from CurrentWeather import CurrentWeather
from WeatherData import WeatherData
from datetime import date
import json
import time

polution_levels_german = {
        0: 'keine',
        1: 'niedrig',
        2: 'mittel',
        3: 'hoch'
    }

for i in range(10):
    #read config data
    config = open('src/config.json', 'r')
    config = json.loads(config.read())

    #get current weather data
    weather_data = WeatherData(str(config['lat']), str(config['lon']), config['api_key'])
    current_weather = weather_data.get_current_weather()

    #get location name
    location = weather_data.get_location_name()

    #get air polution severeness
    air_polution = weather_data.get_air_polution()
    critical_air_polution = list()
    for pollutant, values in air_polution.items():
        if values['warning']:
            critical_air_polution += [pollutant + ': ' + str(values['value']) + ' ' + polution_levels_german[values['level']]]

    if len(critical_air_polution):
        critical_air_polution = ', '.join(critical_air_polution)
    

    print('current location: ' + location)
    print('current temperature: '+  str(current_weather.current_temp))
    print('Max: ' + str(current_weather.max_temp))
    print('Min: ' + str(current_weather.min_temp))
    print('Wind: ' + str(current_weather.wind_speed))
    print('air polution: ' + critical_air_polution + '\n')

    forecast = weather_data.get_forecast()

    for j in range(3):
        print("forecast day " + str(j))
        print(str(forecast[j].max_temp))
        print(str(forecast[j].min_temp))

    time.sleep(10)