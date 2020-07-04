import requests
import json

class WeatherData:

    def __init__(self, latitude, longitude, key):
        self.longitude = longitude
        self.latitude = latitude
        self.key = key
    

    def getData(self):
        resp = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + self.latitude + '&lon=' + self.longitude + '&appid='+ self.key)

        data = json.loads(resp.text)
        current = data['current']['temp']
        print(current - 273.15)
    
