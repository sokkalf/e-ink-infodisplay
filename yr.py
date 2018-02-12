# coding=utf-8
import urllib2
import xmltodict
from mlstripper import MLStripper
from datetime import datetime
from datetime import timedelta

class Yr:
    weather_symbols = {
        1:  'img/sun_clear.bmp',
        2:  'img/sun_small_cloud.bmp',
        3:  'img/sun_large_cloud.bmp',
        4:  'img/cloudy.bmp',
        13: 'img/cloud_snow.bmp',
    }

    def __init__(self, url):
        self.last_refreshed_at = None
        self.weather_url = url
        self.weather_data = self.get_weather()

    def get_weather(self):
        if self.last_refreshed_at is not None and self.last_refreshed_at > datetime.now()-timedelta(minutes=10):
            print "using cached yr data"
            return self.weather_data

        file = urllib2.urlopen(self.weather_url)
        print "fetching data from yr"
        data = file.read()
        file.close()
        data = xmltodict.parse(data)
        self.weather_data = data
        self.last_refreshed_at = datetime.now()
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