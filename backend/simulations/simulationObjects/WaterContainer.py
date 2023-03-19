from .CONSTANTS import SPECIFIC_HEAT_CAPACITY_OF_WATER


class WaterContainer:
    _water_capacity: float = None  # capacity in L
    _current_average_water_temp: float = 50  # 50ºC is # considered safe temp to prevent bacteria growth - start value
    _current_thermal_energy: float = None
    _percent_of_thermal_energy_absorbed_from_pipes: float = None  # % expressed as float, e.g. 5% is 0.05
    _percent_of_thermal_energy_lost_to_waste_per_hour: float = None  # % expressed as float, e.g. 5% is 0.05
    _temperature_of_external_water_source: float = None  # ºC
    outgoing_water_temperature = _current_average_water_temp

    _consumption_pattern: dict = None  # dict of time of day as key, value is another dict with water temp (ºC) and water volume (L)
    #                                    e.g. {"01:00":{"water_used":10, "average_temperature_of_water_used":50}}

    def __init__(self, config):
        try:
            self._water_capacity = config["water_capacity"]
            self._percent_of_thermal_energy_lost_to_waste = config["percent_of_thermal_energy_lost_to_waste_per_hour"]
            self._percent_of_thermal_energy_absorbed_from_pipes = config[
                "percent_of_thermal_energy_absorbed_from_pipes"]
            self._temperature_of_external_water_source = config["temperature_of_external_water_source"]
            self._current_thermal_energy = SPECIFIC_HEAT_CAPACITY_OF_WATER * self._water_capacity * self._current_average_water_temp
        except KeyError as e:
            raise KeyError("Incorrect config passed to WaterContainer", e)

    def get_loggable_metrics(self):
        return {"current_average_water_temp_in_water_container": self._current_average_water_temp,
                "current_thermal_energy_in_water_container": self._current_thermal_energy,
                }

    def run_hour_of_usage(self, temp_in_pipes, flow_rate_in_pipes, current_hour_of_day):

        # TODO finish this
        #  take difference between temp_in_pipes and average temp to get ºC difference
        #  multiply by flow rate to get total energy difference flowed over water container
        #  multiply energy by % absorption
        #  multiply absorbed eenergy by (1-loss%)
        #  increase temp as appropriate
        # factor in water usage and that temp change (energy loss by giving out hot water and replacing with cold)
        #  factor in external heater system

        raise NotImplementedError
    def __hash__(self):
        """
        Just so I can use this obj as a key in dict
        :return:
        """
        return hash(self._water_capacity)

    def __eq__(self, other):
        """
        Just so I can use this obj as a key in dict
        :return:
        """
        return self._water_capacity == other._water_capacity
