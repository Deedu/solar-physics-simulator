import pytest
import json
# noinspection PyUnresolvedReferences
from SimulatedWorld import SimulatedWorld


class TestSimulatedWorld:
    def test_init(self):
        sample_request_file = open('sampleData/sampleCorrectClientRequest.json')
        sample_request_data = json.load(sample_request_file)
        world = SimulatedWorld(sample_request_data)
        assert world._address_of_system == sample_request_data["address"]

    def test_lat_lon(self):
        sample_request_file = open('sampleData/sampleCorrectClientRequest.json')
        sample_request_data = json.load(sample_request_file)
        world = SimulatedWorld(sample_request_data)
        world.generate_lat_long()
        assert world._latitude == 43.6443398
        assert world._longitude == -79.3836206

    def test_meteo_data_pull(self):
        sample_request_file = open('sampleData/sampleCorrectClientRequest.json')
        sample_request_data = json.load(sample_request_file)
        world = SimulatedWorld(sample_request_data)
        world.generate_lat_long()

        sample_correct_meteo_data = json.load(open('sampleData/sampleCorrectMeteoData.json'))

        world.get_weather_data()

        assert world._meteo_weather_data["DNI_data"] == sample_correct_meteo_data["hourly"]["direct_normal_irradiance"]
        assert world._meteo_weather_data["timestamps"] == sample_correct_meteo_data["hourly"]["time"]


