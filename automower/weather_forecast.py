import os
import logging
import subprocess
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
        self._file_name =  "_".join([self._name, self._url_adress.split("/")[-1]])
        
    def download_xml_file(self):
        """ Get xml file from www.yr.no"""

        # If directory for xml files does not exist, create directory
        if not os.path.exists("data"):
            os.makedirs("data")

        # Download xml file
        err_code = subprocess.call(["wget", 
                                    self._url_adress, 
                                    "-O", 
                                    self._file_name])
        if err_code:
            raise WeatherException("Error during downloading {}".format(self._url_adress))
            
    def parse(self):

        try:
            self.download_xml_file()
        except WeatherException as e:
            logging.error(str(e))
            return
        
        tree = ET.parse("sondre_eik_varsel_time_for_time.xml")
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
                        average = time[1].attrib["value"]

                        self._hours.append(HourlyWeatherForecast(timestamp[0], timestamp[1], forecast, average))

        
    def debug_weather_forecast(self):
        for hour in self._hours:
            print("Date {}, Hour {}, Forecast {}, Rain {}".format(hour.date, hour.start_hour, hour.forecast, hour.rain))

if __name__ == "__main__":
    weather = WeatherForecast("sondre_eik", "https://www.yr.no/place/Norway/Akershus/Nannestad/S%C3%B8ndre_Eik/varsel_time_for_time.xml")
    weather.parse()
    weather.debug_weather_forecast()

