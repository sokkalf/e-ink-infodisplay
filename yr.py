# coding=utf-8
import urllib2
import xmltodict
from mlstripper import MLStripper

class Yr:
    weather_symbols = {
        1:  'img/sun_clear.bmp',
        13: 'img/cloud_snow.bmp',
    }

    def __init__(self, url):
        self.weather_url = url
        self.weather_data = self.get_weather()

    def get_weather(self):
        file = urllib2.urlopen(self.weather_url)
        print "fetching data from yr"
        data = file.read()
        file.close()
        data = xmltodict.parse(data)
        self.weather_data = data
        return data

    def get_temperature(self):
        return self.weather_data['weatherdata']['forecast']['tabular']['time'][0]['temperature']['@value']

    def get_weather_symbol(self):
        symbol = int(self.weather_data['weatherdata']['forecast']['tabular']['time'][0]['symbol']['@number'])
        return Yr.weather_symbols[symbol]

    def get_weather_type(self):
        return self.weather_data['weatherdata']['forecast']['tabular']['time'][0]['symbol']['@name']

    def get_forecast(self):
        m = MLStripper()
        return m.strip_tags(self.weather_data['weatherdata']['forecast']['text']['location']['time'][0]['body'])

    def refresh(self):
        self.weather_data = self.get_weather()

if __name__ == '__main__':
    yr = Yr("https://www.yr.no/sted/Norge/Akershus/Asker/Heggedal/varsel.xml")
    print yr.get_temperature()
    print yr.get_weather_symbol()