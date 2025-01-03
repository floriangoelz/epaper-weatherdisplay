#!/usr/bin/python
# -*- coding:utf-8 -*-

from WeatherData import WeatherData
from CurrentWeather import CurrentWeather
from datetime import date
import sys
import os
import json

iconsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'icons')
smalliconsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'small_icons')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd5in83
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    #initiate logging
    logging.basicConfig(filename='log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

    logging.info("Starting Weather Display")
    epd = epd5in83.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    roboto_medium = 'Roboto-Medium.ttf'
    roboto_bold = 'Roboto-Bold.ttf'

    font24 = ImageFont.truetype(os.path.join(fontdir, roboto_medium), 24)
    font28 = ImageFont.truetype(os.path.join(fontdir, roboto_medium), 28)
    font32 = ImageFont.truetype(os.path.join(fontdir, roboto_medium), 32)
    font55b = ImageFont.truetype(os.path.join(fontdir, roboto_bold), 55)
    font32b = ImageFont.truetype(os.path.join(fontdir, roboto_bold), 32)

    height = 600
    width = 448

    icons = {
        "01d": "clear",
        "01n": "clear",
        "02d": "few_clouds",
        "02n": "few_clouds",
        "03d": "scattered_clouds",
        "03n": "scattered_clouds",
        "04d": "broken_clouds",
        "04n": "broken_clouds",
        "09d": "shower_rain",
        "09n": "shower_rain",
        "10d": "rain",
        "10n": "rain",
        "11d": "thunderstorm",
        "11n": "thunderstorm",
        "13d": "snow",
        "13n": "snow",
        "50d": "mist",
        "50n": "mist"
    }

    weekdays = {
        0: "Mo",
        1: "Di",
        2: "Mi",
        3: "Do",
        4: "Fr",
        5: "Sa",
        6: "So"
    }

    pollutants = {
        'no2': 'NO2',
        'pm10': 'PM10',
        'o3': 'O3',
        'pm2_5': 'PM2.5'
    }

    polution_levels_german = {
        0: '',
        1: '(L)',
        2: '(M)',
        3: '(H)'
    }

    #read config data
    config = open('/home/pi/epaper-weatherdisplay/src/config.json', 'r')
    config = json.loads(config.read())

    #get location name
    weather_data = WeatherData(str(config['lat']), str(config['lon']), config['api_key'])
    location = weather_data.get_location_name()

    while(1):
        
        #Drawing on the Horizontal image
        Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        
        #get current weather data
        weather_data = WeatherData(str(config['lat']), str(config['lon']), config['api_key'])
        current_weather = weather_data.get_current_weather()

        #print location and date
        today = date.today()
        day = str(today.day) if today.day > 9 else "0" + str(today.day)
        month = str(today.month) if today.month > 9 else "0" + str(today.month)
        draw.text((20, 10), location, font = font32b, fill = 0)
        draw.text((width/2, 10), weekdays[today.weekday()] + " " + day + "." + month + "." + str(today.year), font = font32b, fill = 0)

        #print air polution warning
        air_polution = weather_data.get_air_polution()
        critical_air_polution = list()
        for pollutant, values in air_polution.items():
            if values['warning']:
                #critical_air_polution += [pollutants[pollutant] + ': ' + str(values['value']) + u'\u03bcg/m\u00b3' + polution_levels_german[values['level']]]
		critical_air_polution += [pollutants[pollutant] + ': ' + polution_levels_german[values['level']]]

        if len(critical_air_polution):
            critical_air_polution_text = ', '.join(critical_air_polution)
            draw.text((20, 55), critical_air_polution_text, font = font24, fill = 0)


        #print icons
        logging.info("read icon bmp file")
        iconbmp = Image.open(os.path.join(iconsdir, icons[current_weather.current_icon] + '.bmp'))
        Limage.paste(iconbmp, (5, 90))

        #print temperatures
        draw.text((250, 100), str(current_weather.current_temp) + u" °C", font = font55b, fill = 0)
        draw.text((250, 190), "Max: " + str(current_weather.max_temp) + u" °C", font = font24, fill = 0)
        draw.text((250, 220), "Min: " + str(current_weather.min_temp) + u" °C", font = font24, fill = 0)
        draw.text((250, 250), "Wind: " + str(current_weather.wind_speed) + " km/h", font = font24, fill = 0)

        #print layout lines
        draw.line((0, 340, width, 340), fill = 0)
        draw.line((149, 350, 149, height), fill = 0)
        draw.line((298, 350, 298, height), fill = 0)

        #get forecast
        forecast = weather_data.get_forecast()

        #print weekdays
        draw.text((12, 345), weekdays[(today.weekday() + 1) % 7], font = font32b, fill = 0)
        draw.text((161, 345), weekdays[(today.weekday() + 2) % 7], font = font32b, fill = 0)
        draw.text((310, 345), weekdays[(today.weekday() + 3) % 7], font = font32b, fill = 0)

        #print icons
        forecast_icon_0 = Image.open(os.path.join(smalliconsdir, icons[forecast[0].icon] + '.bmp'))
        forecast_icon_1 = Image.open(os.path.join(smalliconsdir, icons[forecast[1].icon] + '.bmp'))
        forecast_icon_2 = Image.open(os.path.join(smalliconsdir, icons[forecast[2].icon] + '.bmp'))
        Limage.paste(forecast_icon_0, (12, 380))
        Limage.paste(forecast_icon_1, (161, 380))
        Limage.paste(forecast_icon_2, (310, 380))

        #print temperatures
        draw.text((12, 505), str(forecast[0].max_temp) + u" °C", font = font32b, fill = 0)
        draw.text((12, 545), str(forecast[0].min_temp) + u" °C", font = font28, fill = 0)

        draw.text((161, 505), str(forecast[1].max_temp) + u" °C", font = font32b, fill = 0)
        draw.text((161, 545), str(forecast[1].min_temp) + u" °C", font = font28, fill = 0)

        draw.text((310, 505), str(forecast[2].max_temp) + u" °C", font = font32b, fill = 0)
        draw.text((310, 545), str(forecast[2].min_temp) + u" °C", font = font28, fill = 0)

        epd.display(epd.getbuffer(Limage))
        time.sleep(900)
    
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in83.epdconfig.module_exit()
    exit()
