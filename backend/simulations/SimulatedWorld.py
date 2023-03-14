import googlemaps
import os

import requests
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

class SimulatedWorld:
    gmaps = None
    _num_solar_panels = None
    _width_solar_panels = None
    _height_solar_panels = None
    _current_direct_normal_irradiance = None
    _latitude = None
    _longitude = None
    _address_of_system = None

    def __init__(self, configuration):
        """
        This initializes the world with params given and does some basic checks
        :param configuration:
        :return:
        """
        try:
            self._address_of_system = configuration["address"]
            self.gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
        except:
            raise ValueError("Incorrect config passed in")

    def start_simulation(self):
        # TODO - kick off iterative version of model
        raise NotImplementedError

    def get_weather_data(self):
        # TODO - fetch from METEO API - sample in sampleGeoData.json
        today_date_formatted = datetime.now().strftime('%Y-%m-%d')
        twenty_years_ago_formatted = (datetime.now() - relativedelta(years=20)).strftime('%Y-%m-%d')
        meteo_api_url = f'https://archive-api.open-meteo.com/v1/archive?latitude={self._latitude}&longitude={self._longitude}&start_date={twenty_years_ago_formatted}&end_date={today_date_formatted}&hourly=direct_normal_irradiance&timezone=America%2FNew_York'
        meteo_response = requests.get(meteo_api_url)
        print(meteo_response.text)
        # raise NotImplementedError

    def get_lat_long(self):
        try:
            result = self.gmaps.geocode(self._address_of_system)[0] # Returns multiple results, pick first by default
            print(result)
            geo_data = result["geometry"]["location"]
            self._latitude = geo_data["lat"]
            self._longitude = geo_data["lng"]
        except:
            raise LookupError