import os
import logging
import subprocess
import urllib.request
from urllib.error import URLError
import shutil
import xml.etree.ElementTree as ET


class HourlyWeatherForecast(object):
    # FORECAST_CLEAR_SKY = "CLEAR_SKY"
    # FORECAST_FAIR = "FAIR"
    # FORECAST_PARTLY_CLOUDY = "PARTLY_CLOUDY"
    # FORECAST_CLOUDY = "CLOUDY"
    # FORECAST_LIGHT_RAIN_SHOWERS = "LIGHT_RAIN_SHOWERS"
    # FORECAST_RAIN_SHOWERS = "RAIN_SHOWERS"
    # FORECAST_HEAVY_RAIN_SHOWERS = "HEAVY_RAIN_SHOWERS"
    # FORECAST_LIGHT_RAIN_SHOWERS_AND_THUNDER = "LIGHT RAIN_SHOWERS_AND_THUNDER"
    # FORECAST_LIGHT_RAIN = "LIGHT_RAIN"

    def __init__(self, date, start_hour, forecast, rain):
        self._date = date
        self._start_hour = start_hour
        self._forecast = forecast
        self._rain = rain

    @property
    def date(self):
        return self._date

    @property
    def start_hour(self):
        return self._start_hour

    @property
    def forecast(self):
        return self._forecast

    @property
    def rain(self):
        """ Get average rain value in mm."""
        return self._rain


class WeatherException(Exception):
    """Class to be passed in case of WeatherException"""
    pass


class WeatherForecast(object):
    def __init__(self, name, url_adress):
        self._name = name
        self._url_adress = url_adress
        self._hours = []
        self._file_name =  "_".join([self._name, "forecast_hour_by_hour.xml"])

    @property
    def name(self):
        return self._name

    @property
    def url_adress(self):
        return self._url_adress

    @property
    def hours(self):
        return self._hours

    @property
    def file_name(self):
        return self._file_name
        
    def download_xml_file(self):
        """ Get xml file from www.yr.no"""

        if not self.url_adress.endswith("varsel_time_for_time.xml") and \
           not self.url_adress.endswith("forecast_hour_by_hour.xml"):
            self._url_adress = ("/" if not self.url_adress.endswith("/") else "") \
                              .join([self.url_adress, "forecast_hour_by_hour.xml"])

        # # Download xml file
        # err_code = subprocess.call(["wget", 
        #                             self._url_adress, 
        #                             "-O", 
        #                             self._file_name])

        try:
            with urllib.request.urlopen(self.url_adress) as response, open(self._file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except ValueError as err:
            raise WeatherException("Error during downloading {}: {}".format(self._url_adress, str(err)))

    def parse(self):

        try:
            self.download_xml_file()
        except WeatherException as e:
            logging.error(str(e))
            return
        
        tree = ET.parse(self.file_name)
        root = tree.getroot()

        for attribute in root:
            for forecast in attribute.iter("forecast"):
                for tabular in forecast.iter("tabular"):
                    for time in tabular.iter("time"):

                        # attrib format
                        # {'from': '2017-08-19T23:00:00', 'to': '2017-08-20T00:00:00'}

                        # timestamp format
                        # [2017-08-19, 23:00:00]
                        timestamp = time.attrib["from"].split("T")
                        forecast = time[0].attrib["name"]
                        average = float(time[1].attrib["value"])

                        self._hours.append(HourlyWeatherForecast(timestamp[0], timestamp[1], forecast, average))

        os.remove(self.file_name)

    def get_latest_weather_data(self):
        return self.hours[0]

        
    def debug_weather_forecast(self):
        for hour in self._hours:
            print("Date {}, Hour {}, Forecast {}, Rain {}".format(hour.date, hour.start_hour, hour.forecast, hour.rain))

if __name__ == "__main__":
    weather = WeatherForecast("sondre_eik", "https://www.yr.no/place/Norway/Akershus/Nannestad/S%C3%B8ndre_Eik/")
    weather.parse()
    weather.debug_weather_forecast()

#

