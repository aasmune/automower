from weather_forecast import WeatherForecast
from state_machine import AutomowerStateMachine
from common import config_section
from configparser import ConfigParser

class Automower(object):

    def __init__(self):
        config_parser = ConfigParser()
        config_parser.read("config.ini")
        name = config_section(config_parser, "Weather")["name"]
        url = config_section(config_parser, "Weather")["url"]
        self._weather = WeatherForecast(name, url)
        self.state_machine = AutomowerStateMachine()

    def execute(self):
        self._weather.parse()
        if self._weather.get_latest_weather_data().rain > 5:
            self.state_machine.rain()
        else:
            self.state_machine.clear()

if __name__ == "__main__":
    a = Automower()
    a.execute()