# e-ink infodisplay

## Hardware

- Raspberry Pi
- Waveshare 7.5" e-ink display (SPI)

## Software

- Python (not my favourite, but easiest to get going with available libs)
- On raspbian, install packages wiringpi, python-spidev and python-pil
- Package fonts-freefont-ttf is needed for the font rendering
- Package python-xmltodict is needed for parsing data from Yr
- python-yaml for config
- python-caldav for calendar, install with "pip install git+https://github.com/python-caldav/caldav.git"
- ImageMagick for simulate mode

## Usage

Run with `python main.py`

For simulate mode, `python main.py --simulate` (Requires X forwarding if running in an SSH session)
