import _io
import csv
import uuid

import googlemaps
import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from google.cloud import bigquery

from .SolarCollector import SolarCollector
from .WaterPump import WaterPump
from .WaterContainer import WaterContainer
from .CONSTANTS import BIGQUERY_TABLE_ID, OUTPUT_METRICS_FILE_PATH, BIGQUERY_SCHEMA
import time
from .ConfigurationInputs import SimulationIncomingRequest


class SimulatedWorld:
    gmaps: googlemaps.Client = None
    _num_solar_panels: int = None
    _width_solar_panels: int = None
    _height_solar_panels: int = None
    _current_direct_normal_irradiance: float = 0
    _latitude: float = None
    _longitude: float = None
    _address_of_system: str = None
    _meteo_weather_data: dict = None
    _pandas_data: pd.DataFrame = None
    _date_of_simulation_start: datetime = None
    _current_time_in_simulation: str = None
    _num_hours_to_simulate: int = 24 * 14  # 1 year default 24hrs * 14 days
    _solar_collector: SolarCollector = None
    _water_container: WaterContainer = None
    _water_pump: WaterPump = None
    _loggable_parts_of_system: list = None  # list of all the objects, will be solar, water pump and water container once created
    _output_csv_file: _io.FileIO = None
    _output_csv_file_writer: csv.writer = None
    _written_output_header: bool = False
    _header_for_output_file: dict = None
    _header_as_list_for_output_file: list = None
    _num_metrics_logged: int = None
    _simulation_uuid: uuid = None
    _bigquery_client: bigquery = None

    def __init__(self, configuration: SimulationIncomingRequest):
        """
        This initializes the world with params given and does some basic checks
        :param configuration:
        :return:
        """
        try:
            # Geo Data
            self._address_of_system = configuration.address
            self.gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
            self._meteo_weather_data = {"DNI_data": None, "timestamps": None}

            # BigQuery Connection
            self._bigquery_client = bigquery.Client()

            # Decide Start Date
            if configuration.optional_date_of_simulation:
                self._date_of_simulation_start = datetime.strptime(configuration.optional_date_of_simulation,
                                                                   "%d-%B-%Y")
            else:
                self._date_of_simulation_start = datetime.strptime(datetime.now().strftime("%d-%B-%Y"), "%d-%B-%Y")

            # Decide uuid
            if configuration.simulation_uuid:
                self._simulation_uuid = configuration.simulation_uuid
            else:
                self._simulation_uuid = uuid.uuid4()

            # Get num hours to simulate, defaults to 1 year (24*365)
            if configuration.num_hours_to_simulate:
                self._num_hours_to_simulate = configuration.num_hours_to_simulate

            # Setup logging metrics locally
            self._output_csv_file = open(OUTPUT_METRICS_FILE_PATH, 'w')
            self._output_csv_file_writer = csv.writer(self._output_csv_file)

            # Solar Setup
            self._solar_collector = SolarCollector(configuration.solar)

            # Pump Setup
            self._water_pump = WaterPump(configuration.water_pump)

            # Water Container Setup
            self._water_container = WaterContainer(configuration.water_container)

            # Logging Setup
            self._loggable_parts_of_system = []
            self._loggable_parts_of_system.append(
                self._solar_collector)
            self._loggable_parts_of_system.append(self._water_pump)
            self._loggable_parts_of_system.append(self._water_container)

            # Logging Output setup
            self._header_for_output_file = {"uuid": 0, "Timestamp": 1, "DNI_Value": 2}
            self._header_as_list_for_output_file = ["uuid", "Timestamp", "DNI_Value"]

        except KeyError as e:
            print("Error here")
            print(e)
            raise KeyError("Incorrect config passed in to SimulatedWorld", e)

    def run_entire_simulation(self):
        # Prep - fetching external data
        self.generate_lat_long()
        self.get_weather_data()

        # Computation
        self.start_simulation()

        # Output results for analysis
        self.upload_results_to_bigquery()

    def start_simulation(self):

        start_time = time.time()

        self.calculate_output_file_header()

        for i in range(self._num_hours_to_simulate):
            current_time = time.time()
            print(
                f"Simulation running for: {round(current_time - start_time, 3)} seconds on iteration {i}/{self._num_hours_to_simulate},"
                f" avg speed per iteration: {round((current_time - start_time) / (i + 1), 7)}")

            self._current_time_in_simulation = self._meteo_weather_data["timestamps"][i]
            self.write_out_simulation_results()
            self.run_one_hourly_iteration_of_simulation()

        completion_time = time.time()
        minutes_elapsed = round((completion_time - start_time) / 60, 2)
        print(f"Simulation took: {minutes_elapsed} mins")

    def run_one_hourly_iteration_of_simulation(self):
        # Filter Historical Dataset to get an average to use today
        # print(self._current_time_in_simulation)
        current_hour_of_day = self._current_time_in_simulation[-5:]  # e.g. 01:00
        month_day_hour_formatted = self._current_time_in_simulation[5:]  # e.g. 03-10T22:00
        same_day_time_all_years_in_dataset_mask = self._pandas_data.index.str.contains(month_day_hour_formatted)
        same_day_time_all_years_in_dataset = self._pandas_data[same_day_time_all_years_in_dataset_mask]
        dni_value_for_hour_in_simulation = same_day_time_all_years_in_dataset.loc[:, 'DNI_value'].mean()
        self._current_direct_normal_irradiance = dni_value_for_hour_in_simulation

        # Update timestamp to be today, hardcoded to take 2000's date and make it in the 2020's by adding 20 years
        self._current_time_in_simulation = self._current_time_in_simulation.replace("200", "202")

        # note, pump uses retroactive data - it uses temperature for the previous hour to determine flow rate for
        # the current hour. This feedback loop is faster in real life, but again, directionally right.
        flow_rate_for_the_hour = self._water_pump.get_flow_rate()

        # Add in solar energy from the hour
        starting_temperature_into_solar = self._water_container.outgoing_water_temperature
        temperature_of_water_in_pipes = self._solar_collector.add_one_hour_solar_energy(
            self._current_direct_normal_irradiance, flow_rate_for_the_hour,
            starting_temperature_into_solar
        )

        # Add solar energy to water container through pipes, remove energy from water usage
        self._water_container.run_hour_of_usage(temperature_of_water_in_pipes, flow_rate_for_the_hour,
                                                current_hour_of_day=current_hour_of_day)

        # Adjust water flow from temperature difference between what is in pipes and what is in solar panel.
        # print(
        #     f"Starting flow rate: {flow_rate_for_the_hour}, starting temp into solar {starting_temperature_into_solar}, ending temp in pipes {temperature_of_water_in_pipes}, ending temp water container {self._water_container.outgoing_water_temperature}")
        # self._water_pump.adjust_flow_to_current_state(self._water_container.outgoing_water_temperature,
        #                                               temperature_of_water_in_pipes)

        # print(same_day_time_all_years_in_dataset)
        # print(f"Mean DNI for {month_day_hour_formatted} is: {dni_value_for_hour_in_simulation}")

    def get_weather_data(self):
        """
        Gets weather data from Open Meteo API
        Docs here: https://open-meteo.com/en/docs/historical-weather-api
        :return:
        """
        print("Fetching weather data")
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

        self._meteo_weather_data["DNI_data"] = meteo_response["hourly"]["direct_normal_irradiance"]
        self._meteo_weather_data["timestamps"] = meteo_response["hourly"]["time"]

        holding_dict = {
            "DNI_value": pd.Series(self._meteo_weather_data["DNI_data"], index=self._meteo_weather_data["timestamps"])

        }
        self._pandas_data = pd.DataFrame(
            holding_dict)

        print("Fetched Weather Data")

        # raise NotImplementedError # Decide what to do with data, how to process

    def generate_lat_long(self):
        try:
            result = self.gmaps.geocode(self._address_of_system)[0]  # Returns multiple results, pick first by default
            geo_data = result["geometry"]["location"]
            # print(f"geo data - {geo_data}")
            self._latitude = geo_data["lat"]
            self._longitude = geo_data["lng"]
            print("Fetched Coordinates from address input")
        except:
            raise LookupError

    def calculate_output_file_header(self):
        """
        Dynamically generate header based on logging metrics set at object level
        :return:
        """

        print("writing output header")
        if not self._written_output_header:
            self._num_metrics_logged = len(self._header_as_list_for_output_file)  # based on two existing headers

            for loggableObject in self._loggable_parts_of_system:
                loggableJSONResponse = loggableObject.get_loggable_metrics()
                loggableJSONResponseKeys = loggableJSONResponse.keys()
                for key in loggableJSONResponseKeys:
                    if not self._header_for_output_file.get(loggableObject, False):
                        self._header_for_output_file[loggableObject] = {}
                        print(self._header_for_output_file)
                    self._header_for_output_file[loggableObject][key] = self._num_metrics_logged
                    self._header_as_list_for_output_file.append(key)
                    self._num_metrics_logged += 1

                    # Header
            # self._output_csv_file_writer.writerow(self._header_as_list_for_output_file)
            self._written_output_header = True
            if (len(self._header_as_list_for_output_file) > 16):
                pass

    def write_out_simulation_results(self):

        # TODO - fix hardcoded
        row_of_data = [self._simulation_uuid, self._current_time_in_simulation, self._current_direct_normal_irradiance]
        for i in range(len(row_of_data), self._num_metrics_logged + 1):
            row_of_data.append(0)

        for loggableObject in self._loggable_parts_of_system:
            loggableJSONResponse = loggableObject.get_loggable_metrics()
            for key in loggableJSONResponse.keys():
                value = loggableJSONResponse[key]
                row_of_data[self._header_for_output_file[loggableObject][key]] = value

        print(f"Simulation Results Intermediate - {self._header_for_output_file}")
        print(row_of_data)

        self._output_csv_file_writer.writerow(row_of_data)

    def delete_existing_bigquery_results_with_same_uuid(self):
        """
        This function deletes bigquery rows with same uuid - used to make demo live and update to new values instead of
        averaging past values
        :return:
        """
        table_id = BIGQUERY_TABLE_ID

        table_original = self._bigquery_client.get_table(table_id)  # Make an API request.

        # TODO - Modify to sanitize input, protect from sql injection
        sql_statement = f"""
                    DELETE {table_id} t WHERE t.uuid IN
                    (SELECT uuid FROM {table_id}
                    WHERE uuid = '{self._simulation_uuid}');
                    """
        query_job = self._bigquery_client.query(query=sql_statement)
        print("Bigquery cleanup started")
        results = query_job.result()  # Waits for job to complete.
        table_new = self._bigquery_client.get_table(table_id)  # Make an API request.

        print(
            f"Deleted {table_original.num_rows - table_new.num_rows} rows to clean bq table {table_id} for new simulation {self._simulation_uuid}")

    def upload_results_to_bigquery(self):

        table_id = BIGQUERY_TABLE_ID
        self.delete_existing_bigquery_results_with_same_uuid()

        # close existing temp file
        self._output_csv_file.close()

        job_config = bigquery.LoadJobConfig(
            schema=BIGQUERY_SCHEMA
        )

        with open(OUTPUT_METRICS_FILE_PATH, "rb") as source_file:
            job = self._bigquery_client.load_table_from_file(source_file, table_id, job_config=job_config)

        job.result()

        table = self._bigquery_client.get_table(table_id)  # Make an API request.
        print(
            "Total of {} rows and {} columns in {}".format(
                table.num_rows, len(table.schema), table_id
            )
        )
