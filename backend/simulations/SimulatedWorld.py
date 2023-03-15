import googlemaps
import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SimulatedWorld:
    gmaps: googlemaps.Client = None
    _num_solar_panels: int = None
    _width_solar_panels: int = None
    _height_solar_panels: int = None
    _current_direct_normal_irradiance: float = None
    _latitude: float = None
    _longitude: float = None
    _address_of_system: str = None
    _meteo_weather_data: dict = {"DNI_data": None, "timestamps": None}
    _date_of_simulation_start: datetime = None

    def __init__(self, configuration):
        """
        This initializes the world with params given and does some basic checks
        :param configuration:
        :return:
        """
        try:
            self._address_of_system = configuration["address"]
            self.gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
            if configuration.get("optional-date-of-simulation", False):
                self._date_of_simulation_start = datetime.strptime(configuration["optional-date-of-simulation"],
                                                                   "%d-%B-%Y")
        except:
            raise ValueError("Incorrect config passed in")

    def start_simulation(self):
        # TODO - kick off iterative version of model
        raise NotImplementedError

    def get_weather_data(self):

        if self._date_of_simulation_start is None:
            self._date_of_simulation_start = datetime.now()
        today_date_formatted = (self._date_of_simulation_start - relativedelta(days=7)).strftime(
            '%Y-%m-%d')  # one week back to ensure they have the data
        twenty_years_ago_formatted = (
                    self._date_of_simulation_start - relativedelta(years=20) - relativedelta(days=7)).strftime(
            '%Y-%m-%d')  # 20 year lookback, TODO - can make lookback window param in future
        meteo_api_url = f'https://archive-api.open-meteo.com/v1/archive?latitude={self._latitude}&longitude={self._longitude}&start_date={twenty_years_ago_formatted}&end_date={today_date_formatted}&hourly=direct_normal_irradiance&timezone=America%2FNew_York'
        meteo_response = requests.get(meteo_api_url)
        meteo_response = meteo_response.json()
        # meteo_response_formmated = json.dumps(json.load(meteo_response), indent=4)
        # with open("sampleData/sampleCorrectMeteoData.json", "w") as outfile:
        #     json.dump(meteo_response, outfile, indent=4)
        # print(meteo_response)
        self._meteo_weather_data["DNI_data"] = meteo_response["hourly"]["direct_normal_irradiance"]
        self._meteo_weather_data["timestamps"] = meteo_response["hourly"]["time"]
        # raise NotImplementedError # Decide what to do with data, how to process

    def generate_lat_long(self):
        try:
            result = self.gmaps.geocode(self._address_of_system)[0]  # Returns multiple results, pick first by default
            geo_data = result["geometry"]["location"]
            # print(f"geo data - {geo_data}")
            self._latitude = geo_data["lat"]
            self._longitude = geo_data["lng"]
        except:
            raise LookupError
