# coding=utf-8

import epd7in5
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from yr import Yr
from readcal import Readcal
import yaml
import time


EPD_WIDTH = 640
EPD_HEIGHT = 384


def display_info(display, yr, cal):
    weather_symbol = Image.open(yr.get_weather_symbol())
    image = Image.open('img/main.bmp')
    draw = ImageDraw.Draw(image)
    font_large = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 48)
    draw.text((20, 45), yr.get_temperature() + u'°C', font = font_large, fill = 0)
    font_small = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
    draw.text((10, 90), yr.get_weather_type(), font = font_small, fill = 0)
    image.paste(weather_symbol, (200, 21))
    base_calendar_text_pos = 180
    offset_calendar_text_pos = 0
    for calendar_event in cal.get_next_events():
        draw.text((10, base_calendar_text_pos+offset_calendar_text_pos), calendar_event, font = font_small, fill = 0)
        offset_calendar_text_pos = offset_calendar_text_pos + 25

    image = image.rotate(90, False, True)
    display.display_frame(display.get_frame_buffer(image))


def main():
    epd = epd7in5.EPD()
    epd.init()
    config = yaml.load(open('config.yml'))
    yr = Yr(config['weather']['url'])
    cal = Readcal(config['calendar']['url'], config['calendar']['username'], config['calendar']['password'])
    while(True):
        display_info(epd, yr, cal)
        time.sleep(60)
        yr.refresh()

    image = Image.open('img/skrik.bmp')
    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    main()
