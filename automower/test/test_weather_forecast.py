import pytest
from automower.weather_forecast import WeatherException, WeatherForecast
class TestWeatherForecast(object):

    def test_download_xml_file_from_yr(self):
        forecast = WeatherForecast("test", "https://www.yr.no/place/Norway/Oslo/Oslo/Oslo/varsel_time_for_time.xml")
        forecast.download_xml_file()

    def test_download_xml_file_with_file_that_cant_be_downloaded__should_raise_exception(self):
        forecast = WeatherForecast("test", "invalidurladress")
        with pytest.raises(WeatherException):
            forecast.download_xml_file()