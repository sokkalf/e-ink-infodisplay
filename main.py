# coding=utf-8

import epd7in5
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from yr import Yr

EPD_WIDTH = 640
EPD_HEIGHT = 384

def main():
    epd = epd7in5.EPD()
    epd.init()
    yr = Yr("https://www.yr.no/sted/Norge/Akershus/Asker/Heggedal/varsel.xml")

    weather_symbol = Image.open(yr.get_weather_symbol())
    image = Image.open('img/main.bmp')
    draw = ImageDraw.Draw(image)
    font_large = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 48)
    draw.text((20, 45), yr.get_temperature() + u'°C', font = font_large, fill = 0)
    font_small = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
    draw.text((10, 90), yr.get_weather_type(), font = font_small, fill = 0)
    image.paste(weather_symbol, (200, 21))
    image = image.rotate(90, False, True)
    epd.display_frame(epd.get_frame_buffer(image))

    image = Image.open('img/skrik.bmp')
    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    main()
