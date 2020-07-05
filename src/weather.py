import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from 'waveshare_epd' import epd5in83
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
    
    # Drawing on the Vertical image
    logging.info("2.Drawing on the Vertical image...")
    Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    
    logging.info("3.read bmp file")
    Himage = Image.open(os.path.join(picdir, '5in83.bmp'))
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in83.epdconfig.module_exit()
    exit()