import requests
import json
from CurrentWeather import CurrentWeather
from ForecastData import ForecastData

class WeatherData:

    def __init__(self, latitude, longitude, key):
        self.longitude = longitude
        self.latitude = latitude
        self.key = key

    def __request_data(self, url):
        resp = requests.get(url + '?lat=' + self.latitude + '&lon=' + self.longitude + '&appid='+ self.key)
        return json.loads(resp.text)
    

    def get_current_weather(self):
        data = self.__request_data('https://api.openweathermap.org/data/3.0/onecall')
        current_data = data['current']

        current_temp = current_data['temp']
        current_temp = round(current_temp - 273.15, 1)

        current_icon = current_data['weather'][0]['icon']

        daily_data = data['daily'][0]

        max_temp = daily_data['temp']['max']
        max_temp = round(max_temp - 273.15, 1)

        min_temp = daily_data['temp']['min']
        min_temp = round(min_temp - 273.15, 1)

        wind_speed = round(daily_data['wind_speed'], 1)

        weather = CurrentWeather(current_temp, wind_speed, max_temp, min_temp, current_icon)
        return weather

    def get_forecast(self):
        data = self.__request_data('https://api.openweathermap.org/data/3.0/onecall')
        forecast_data = data['daily']

        forecast = [ForecastData(round(forecast_data[1]['wind_speed'], 1), round(forecast_data[1]['temp']['max'] - 273.15, 1), round(forecast_data[1]['temp']['min'] - 273.15, 1), forecast_data[1]['weather'][0]['icon']),
                    ForecastData(round(forecast_data[2]['wind_speed'], 1), round(forecast_data[2]['temp']['max'] - 273.15, 1), round(forecast_data[2]['temp']['min'] - 273.15, 1), forecast_data[2]['weather'][0]['icon']),
                    ForecastData(round(forecast_data[3]['wind_speed'], 1), round(forecast_data[3]['temp']['max'] - 273.15, 1), round(forecast_data[3]['temp']['min'] - 273.15, 1), forecast_data[3]['weather'][0]['icon'])]

        return forecast
    
    def get_location_name(self):
        data = self.__request_data('https://api.openweathermap.org/geo/1.0/reverse')
        return data[0]['name']

    def get_air_polution(self):
        data = self.__request_data('https://api.openweathermap.org/data/2.5/air_pollution')
        return self.get_air_polution_severeness(data)
    
    def get_air_polution_severeness(self, air_polution_data):
        warning_threshold = 'medium'
        air_polution_data = air_polution_data['list'][0]['components']

        air_quality_scale = {
            'no2': {
                'low': 50,
                'medium': 100,
                'high': 200
            },
            'pm10': {
                'low': 25,
                'medium': 50,
                'high': 90
            },
            'o3': {
                'low': 60,
                'medium': 120,
                'high': 180
            },
            'pm2_5': {
                'low': 15,
                'medium': 30,
                'high': 55
            }
        }

        air_quality_levels = {
            'none': 0,
            'low': 1,
            'medium': 2,
            'high': 3
        }
        
        relevant_pollutants = [pollutant for pollutant, _ in air_quality_scale.items()]

        current_values = dict((pollutant, air_polution_data[pollutant]) for pollutant in air_polution_data.keys() if pollutant in relevant_pollutants)

        result = dict()

        current_air_polution_levels = self.__get_air_polution_levels(current_values, air_quality_scale)
        for pollutant, level in current_air_polution_levels.items():
            if level >= air_quality_levels[warning_threshold]:
                result[pollutant] = {
                    'warning': True,
                    'level': level,
                    'value': current_values[pollutant]
                }
            else:
                result[pollutant] = {
                    'warning': False,
                    'level': level,
                    'value': current_values[pollutant]
                }
        
        return result
                
    def __get_air_polution_levels(self, air_quality_values, air_quality_scale):
        air_polution_level_result = dict()

        for pollutant, value in air_quality_values.items():
            if value >= air_quality_scale[pollutant]['high']:
                air_polution_level_result[pollutant] = 3
            elif value >= air_quality_scale[pollutant]['medium']:
                air_polution_level_result[pollutant] = 2
            elif value >= air_quality_scale[pollutant]['low']:
                air_polution_level_result[pollutant] = 1
            else:
                air_polution_level_result[pollutant] = 0

        return air_polution_level_result

    

        
        
    
