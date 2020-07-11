#!/usr/bin/python
# -*- coding:utf-8 -*-

from WeatherData import WeatherData
from CurrentWeather import CurrentWeather
from datetime import date
import sys
import os
iconsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'icons')
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
    font55 = ImageFont.truetype(os.path.join(fontdir, 'Roboto-Medium.ttf'), 55)

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

    while(1):
        
        # Drawing on the Horizontal image
        Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        
        #get current weather data
        weatherdata = WeatherData('49.591', '8.646', 'bcdf63a0553e42805e8f1111bcbd94e5')
        currentWeather = weatherdata.getData()

        #date
        today = date.today()
        draw.text((20, 10), str(today.day) + "." + str(today.month) + "." + str(today.year), font = font28, fill = 0)

        #icon
        logging.info("read icon bmp file")
        iconbmp = Image.open(os.path.join(iconsdir, icons[currentWeather.currentIcon] + '.bmp'))
        Limage.paste(iconbmp, (5, 30))

        #temperatures
        draw.text((250, 40), str(currentWeather.currentTemp) + " C", font = font55, fill = 0)
        draw.text((250, 100), "Max: " + str(currentWeather.maxTemp) + " C", font = font24, fill = 0)
        draw.text((250, 130), "Min: " + str(currentWeather.minTemp) + " C", font = font24, fill = 0)
        draw.text((250, 160), "Wind: " + str(currentWeather.windSpeed) + " km/h", font = font24, fill = 0)


        epd.display(epd.getbuffer(Limage))
        time.sleep(300)
    
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in83.epdconfig.module_exit()
    exit()
