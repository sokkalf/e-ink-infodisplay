# coding=utf-8

import epd7in5
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

EPD_WIDTH = 640
EPD_HEIGHT = 384

def main():
    epd = epd7in5.EPD()
    epd.init()

    sun = Image.open('img/cloud_snow.bmp')
    image = Image.open('img/main.bmp')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 48)
    draw.text((20, 25), u'-2°C', font = font, fill = 0)
    image.paste(sun, (200, 21))
    image = image.rotate(90, False, True)
    epd.display_frame(epd.get_frame_buffer(image))

    image = Image.open('img/skrik.bmp')
    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    main()
