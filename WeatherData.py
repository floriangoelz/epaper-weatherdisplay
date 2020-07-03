import requests
import json

class WeatherData:

    def __init__(self, latitude, longitude, key):
        self.longitude = longitude
        self.latitude = latitude
        self.key = key
    

    def getData():
        resp = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + self.latitude + '&lon=' + longitude + '&appid='+ key)

        with resp as json_file:
            data = json.load(json_file)
            print (data['current']['temp'])
    
