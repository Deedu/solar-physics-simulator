import os
import json
from dotenv import load_dotenv
from simulationObjects.SimulatedWorld import SimulatedWorld

load_dotenv()  # only relevant for local - P4 cleanup later


def create_app():
    raise NotImplementedError


def make_world():
    sample_request_file = open('sampleData/sampleCorrectClientRequest.json')
    sample_request_data = json.load(sample_request_file)
    print(f'GMAP API = {os.getenv("GOOGLE_MAPS_API_KEY")}')

    world_1 = SimulatedWorld(sample_request_data)
    world_1.generate_lat_long()
    world_1.get_weather_data()
    # world_1.write_out_simulation_results()
    print("STARTING SIMULATION")
    world_1.start_simulation()
    world_1.upload_results_to_bigquery()

def write_results():
    sample_request_file = open('sampleData/sampleCorrectClientRequest.json')
    sample_request_data = json.load(sample_request_file)
    world_1 = SimulatedWorld(sample_request_data)
    world_1.upload_results_to_bigquery()

if __name__ == "__main__":
    make_world()
    # write_results()
