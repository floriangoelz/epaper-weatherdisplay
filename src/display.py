#!/usr/bin/python
# -*- coding:utf-8 -*-

from WeatherData import WeatherData
from CurrentWeather import CurrentWeather
from datetime import date
import sys
import os
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
    logging.info("epd5in83 Demo")
    
    epd = epd5in83.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    font24 = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Medium.ttf'), 24)
    font28 = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Medium.ttf'), 28)
    font32 = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Medium.ttf'), 32)
    font55b = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Bold.ttf'), 55)
    font32b = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Bold.ttf'), 32)

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

    while(1):
        
        # Drawing on the Horizontal image
        Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        
        #get current weather data
        weatherdata = WeatherData('49.591', '8.646', 'bcdf63a0553e42805e8f1111bcbd94e5')
        currentWeather = weatherdata.getCurrentWeather()

        #date
        today = date.today()
        draw.text((20, 10), "Hemsbach        " + weekdays[today.weekday()] + " " + str(today.day) + "." + str(today.month) + "." + str(today.year), font = font32b, fill = 0)

        #icon
        logging.info("read icon bmp file")
        iconbmp = Image.open(os.path.join(iconsdir, icons[currentWeather.currentIcon] + '.bmp'))
        Limage.paste(iconbmp, (5, 90))

        #temperatures
        draw.text((250, 100), str(currentWeather.currentTemp) + u" °C", font = font55b, fill = 0)
        draw.text((250, 190), "Max: " + str(currentWeather.maxTemp) + u" °C", font = font24, fill = 0)
        draw.text((250, 220), "Min: " + str(currentWeather.minTemp) + u" °C", font = font24, fill = 0)
        draw.text((250, 250), "Wind: " + str(currentWeather.windSpeed) + " km/h", font = font24, fill = 0)

        #layout lines
        draw.line((0, 350, 448, 350), fill = 0)
        draw.line((149, 350, 149, 600), fill = 0)
        draw.line((298, 350, 298, 600), fill = 0)

        #forecast
        forecast = weatherdata.getForecast()

        #weekdays
        draw.text((12, 10), weekdays[today.weekday() + 1 % 7], font = font32b, fill = 0)
        draw.text((161, 10), weekdays[today.weekday() + 2 % 7], font = font32b, fill = 0)
        draw.text((310, 10), weekdays[today.weekday() + 3 % 7], font = font32b, fill = 0)

        #icons
        forecastIcon0 = Image.open(os.path.join(smalliconsdir, icons[forecast[0].icon] + '.bmp'))
        forecastIcon1 = Image.open(os.path.join(smalliconsdir, icons[forecast[1].icon] + '.bmp'))
        forecastIcon2 = Image.open(os.path.join(smalliconsdir, icons[forecast[2].icon] + '.bmp'))
        Limage.paste(forecastIcon0, (12, 370))
        Limage.paste(forecastIcon0, (161, 370))
        Limage.paste(forecastIcon0, (310, 370))

        #temperatures
        draw.text((12, 495), str(forecast[0].maxTemp) + u" °C", font = font32b, fill = 0)
        draw.text((12, 525), str(forecast[0].minTemp) + u" °C", font = font28, fill = 0)
        draw.text((12, 555), str(forecast[0].windSpeed) + u" km/h", font = font28, fill = 0)

        draw.text((161, 495), str(forecast[1].maxTemp) + u" °C", font = font32b, fill = 0)
        draw.text((161, 525), str(forecast[1].minTemp) + u" °C", font = font28, fill = 0)
        draw.text((161, 555), str(forecast[1].windSpeed) + u" km/h", font = font28, fill = 0)

        draw.text((310, 495), str(forecast[2].maxTemp) + u" °C", font = font32b, fill = 0)
        draw.text((310, 525), str(forecast[2].minTemp) + u" °C", font = font28, fill = 0)
        draw.text((310, 555), str(forecast[2].windSpeed) + u" km/h", font = font28, fill = 0)

        epd.display(epd.getbuffer(Limage))
        time.sleep(900)
    
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in83.epdconfig.module_exit()
    exit()
