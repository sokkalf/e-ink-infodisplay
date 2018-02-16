# coding=utf-8

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageShow
from datetime import datetime
from datetime import timedelta
from dateutil import tz

from yr import Yr
from readcal import Readcal
import yaml
import time
import argparse
import os

EPD_WIDTH = 640
EPD_HEIGHT = 384

prev_image_hash = None
fortune = os.popen("fortune -n 80 -s | fold -w 40").read()

def show_image(display, image):
    if display==None:
        image.show()
    else:
        display.display_frame(display.get_frame_buffer(image))


def display_info(display, yr, cal):
    global prev_image_hash
    global fortune
    weather_symbol = Image.open(yr.get_weather_symbol())
    image = Image.open('img/main.bmp')
    draw = ImageDraw.Draw(image)
    font_large = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 48)
    font_small = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
    font_small_bold = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 20)
    draw.text((20, 45), yr.get_temperature() + u'°C', font = font_large, fill = 0)
    draw.text((10, 90), yr.get_weather_type(), font = font_small_bold, fill = 0)
    image.paste(weather_symbol, (200, 21))
    base_calendar_text_pos = 180
    offset_calendar_text_pos = 0
    for calendar_event in cal.get_next_events():
        if calendar_event[0].replace(tzinfo=None).date() == datetime.today().date():
            None
        elif calendar_event[0].replace(tzinfo=None).date() == (datetime.today()+timedelta(days=1)).date():
            draw.text((125, base_calendar_text_pos+offset_calendar_text_pos), u"— I morgen —", font=font_small_bold, fill=0)
            offset_calendar_text_pos = offset_calendar_text_pos + 25
        elif calendar_event[0].replace(tzinfo=None).date() > (datetime.today()+timedelta(days=1)).date() and \
                calendar_event[0].replace(tzinfo=None).date() < (datetime.today()+timedelta(days=6)).date():
            draw.text((125, base_calendar_text_pos+offset_calendar_text_pos), u"— " + Readcal.weekdays[calendar_event[0].isoweekday()] + u" —", font=font_small_bold, fill=0)
            offset_calendar_text_pos = offset_calendar_text_pos + 25
        else:
            draw.text((125, base_calendar_text_pos+offset_calendar_text_pos), u"— " + calendar_event[0].strftime('%d.%m.%Y') + u" —", font=font_small_bold, fill=0)
            offset_calendar_text_pos = offset_calendar_text_pos + 25
        draw.text((10, base_calendar_text_pos+offset_calendar_text_pos), calendar_event[0].strftime('%H:%M') + " "+ calendar_event[1], font = font_small, fill = 0)
        offset_calendar_text_pos = offset_calendar_text_pos + 25

    draw.text((5, 580), fortune, font=font_small, fill=0)

    if display != None:
        image = image.rotate(90, False, True)

    image_hash = hash(image.tobytes())
    print image_hash
    if prev_image_hash != image_hash:
        show_image(display, image)

    prev_image_hash = image_hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--simulate', help='Simulate e-ink display', action='store_true')
    args = parser.parse_args()

    if args.simulate:
        epd = None
    else:
        import epd7in5
        epd = epd7in5.EPD()
        epd.init()

    config = yaml.load(open('config.yml'))
    yr = Yr(config['weather']['url'])
    cal = Readcal(config['calendar']['url'], config['calendar']['username'], config['calendar']['password'])
    while(True):
        display_info(epd, yr, cal)
        time.sleep(60)
        yr.refresh()


if __name__ == '__main__':
    main()
