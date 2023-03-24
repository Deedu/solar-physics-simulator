import os

import pytest
import json
# noinspection PyUnresolvedReferences
from simulationObjects.SimulatedWorld import SimulatedWorld
import json
from collections import namedtuple
from types import SimpleNamespace




def customWorldDecoder(inputDict):
    return namedtuple('X', inputDict.keys())(*inputDict.values())


class TestSimulatedWorld:
    def test_init(self):
        sample_request_file = open('sampleData/sampleCorrectClientRequest.json')
        sample_request_data = json.dumps(json.load(sample_request_file))
        sample_request_data = json.loads(sample_request_data, object_hook=lambda d: SimpleNamespace(**d))
        # Parse JSON into an object with attributes corresponding to dict keys.
        # worldInputFormatted = json.loads(sample_request_data, object_hook=customWorldDecoder)
        world = SimulatedWorld(sample_request_data)
        assert world._address_of_system == sample_request_data.address

    def test_lat_lon(self):
        sample_request_file = open('sampleData/sampleCorrectClientRequest.json')
        sample_request_data = json.dumps(json.load(sample_request_file))
        sample_request_data = json.loads(sample_request_data, object_hook=lambda d: SimpleNamespace(**d))
        world = SimulatedWorld(sample_request_data)
        world.generate_lat_long()
        assert world._latitude == 43.6443398
        assert world._longitude == -79.3836206

    def test_meteo_data_pull(self):
        sample_request_file = open('sampleData/sampleCorrectClientRequest.json')
        sample_request_data = json.dumps(json.load(sample_request_file))
        sample_request_data = json.loads(sample_request_data, object_hook=lambda d: SimpleNamespace(**d))
        world = SimulatedWorld(sample_request_data)
        world.generate_lat_long()

        sample_correct_meteo_data = json.load(open('sampleData/sampleCorrectMeteoData.json'))

        world.get_weather_data()

        # assert world._meteo_weather_data["DNI_data"] == sample_correct_meteo_data["hourly"]["direct_normal_irradiance"]
        assert len(world._meteo_weather_data["timestamps"]) >= len(sample_correct_meteo_data["hourly"]["time"])
