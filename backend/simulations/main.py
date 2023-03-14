import googlemaps
import os
import json
import requests
from dotenv import load_dotenv
import datetime
from dateutil.relativedelta import relativedelta
from SimulatedWorld import SimulatedWorld


load_dotenv()  # only relevant for local - P4 cleanup later

sample_request_file = open('sampleRequest.json')
sample_request_data = json.load(sample_request_file)
print(f'GMAP API = {os.getenv("GOOGLE_MAPS_API_KEY")}')

world_1 = SimulatedWorld(sample_request_data)
world_1.get_lat_long()
world_1.get_weather_data()


