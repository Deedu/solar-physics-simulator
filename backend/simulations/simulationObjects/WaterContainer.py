from .CONSTANTS import SPECIFIC_HEAT_CAPACITY_OF_WATER
from .ConfigurationInputs import WaterContainerInput
from types import SimpleNamespace

class WaterContainer:
    _water_capacity: float = None  # capacity in L
    _current_average_water_temp: float = 50  # 50ºC is # considered safe temp to prevent bacteria growth - start value
    _current_thermal_energy: float = None
    _percent_of_thermal_energy_absorbed_from_pipes: float = None  # % expressed as float, e.g. 5% is 0.05
    _percent_of_thermal_energy_lost_to_waste_per_hour: float = None  # % expressed as float, e.g. 5% is 0.05
    _temperature_of_external_water_source: float = None  # ºC
    outgoing_water_temperature = _current_average_water_temp
    _volume_of_water_sent_out_of_water_container: float = 0  # L
    _average_temp_of_water_sent_out_of_water_container: float = 0  # ºC
    _energy_sent_out_of_water_container: float = 0  # ºC
    _efficiency_of_traditional_boiler: float = None  # % expressed as float, e.g. 5% is 0.05
    _energy_consumed_by_heater: float = 0  # J used over last hour
    _minimum_average_water_temp: float = 50  # ºC floor temp of water to prevent bacteria growth
    _energy_absorbed_from_pipes: float = 0  # J energy over last hour

    _consumption_pattern: dict = None  # dict of time of day as key, value is another dict with water temp (ºC) and water volume (L)

    #                                    e.g. {"01:00":{"water_used":10, "average_temperature_of_water_used":50}}

    def __init__(self, config: WaterContainerInput):
        try:
            self._water_capacity = config.water_capacity
            self._percent_of_thermal_energy_lost_to_waste_per_hour = config.percent_of_thermal_energy_lost_to_waste_per_hour
            self._percent_of_thermal_energy_absorbed_from_pipes = config.percent_of_thermal_energy_absorbed_from_pipes
            self._temperature_of_external_water_source = config.temperature_of_external_water_source
            self._current_thermal_energy = SPECIFIC_HEAT_CAPACITY_OF_WATER * self._water_capacity * self._current_average_water_temp
            self._efficiency_of_traditional_boiler = config.efficiency_of_traditional_boiler
            self._minimum_average_water_temp = config.minimum_average_water_temperature
            self._consumption_pattern = config.consumption_pattern
        except KeyError as e:
            raise KeyError("Incorrect config passed to WaterContainer", e)

    def set_current_thermal_energy(self):
        self._current_thermal_energy = self._water_capacity * self._current_average_water_temp * SPECIFIC_HEAT_CAPACITY_OF_WATER

    def get_loggable_metrics(self):
        return {
            "current_average_water_temp_in_water_container": self._current_average_water_temp,
            "current_thermal_energy_in_water_container": self._current_thermal_energy,
            "average_temp_of_water_sent_out_of_water_container": self._average_temp_of_water_sent_out_of_water_container,
            "energy_sent_out_of_water_container": self._energy_sent_out_of_water_container,
            "volume_of_water_sent_out_of_water_container": self._volume_of_water_sent_out_of_water_container,
            "energy_consumed_by_heater": self._energy_consumed_by_heater,
            "energy_absorbed_from_pipes":self._energy_absorbed_from_pipes
        }

    def process_energy_outflow_for_hour_of_day(self, current_hour_of_day):
        try:
            # print(f"current hour usage info {self._consumption_pattern.current_hour_of_day}")

            # typecheck below to get around differences between test and real request
            current_hour_usage_info = None
            if isinstance(self._consumption_pattern, SimpleNamespace):
                current_hour_usage_info = vars(self._consumption_pattern)[current_hour_of_day]
            else:
                current_hour_usage_info = self._consumption_pattern.current_hour_of_day

            print(current_hour_usage_info)


            if current_hour_usage_info is None:
                    raise KeyError()
            self._volume_of_water_sent_out_of_water_container = current_hour_usage_info.water_used
            self._average_temp_of_water_sent_out_of_water_container = current_hour_usage_info.average_temperature_of_water_used
        except AttributeError as e:
            AttributeError(f"Consumption pattern of WaterContainer not defined for {current_hour_of_day}", e)

        litres_of_hot_water_lost = self.process_hot_water_leaving_water_container(
            self._volume_of_water_sent_out_of_water_container, self._average_temp_of_water_sent_out_of_water_container)

    def process_hot_water_leaving_water_container(self, outgoing_water_amount, outgoing_water_temp):

        if (outgoing_water_temp <= self._temperature_of_external_water_source):
            self._average_temp_of_water_sent_out_of_water_container = 0
            self._volume_of_water_sent_out_of_water_container = 0
            self._energy_sent_out_of_water_container = 0
            return 0  # demand for water will be filled exclusively by tap/external source

        else:
            self._energy_sent_out_of_water_container = outgoing_water_amount * outgoing_water_temp * SPECIFIC_HEAT_CAPACITY_OF_WATER

            self._average_temp_of_water_sent_out_of_water_container = outgoing_water_temp
            self._volume_of_water_sent_out_of_water_container = outgoing_water_amount

            # This next step assumes that all thermal energy from the water container can be transferred to
            # the outgoing water as needed. This isn't perfectly true, but it assumes zero time to mix in external water.
            # That greatly simplifies my modelling process and is still approximately correct.

            energy_incoming_from_water_replacement = outgoing_water_amount * self._temperature_of_external_water_source * SPECIFIC_HEAT_CAPACITY_OF_WATER

            target_energy_level = self._minimum_average_water_temp * SPECIFIC_HEAT_CAPACITY_OF_WATER * self._water_capacity

            energy_surplus = ((self._current_thermal_energy + energy_incoming_from_water_replacement)
                              - self._energy_sent_out_of_water_container) - target_energy_level

            if energy_surplus < 0:  # need to kick in boiler
                print("Kicked in boiler this hour")
                self._energy_consumed_by_heater = energy_surplus / self._efficiency_of_traditional_boiler
                self._current_average_water_temp = self._minimum_average_water_temp
                self.set_current_thermal_energy()
            else:  # no heater needed and still above optimal temp
                self._energy_consumed_by_heater = 0

    def run_hour_of_usage(self, temp_in_pipes, flow_rate_in_pipes, current_hour_of_day):

        difference_in_temp = temp_in_pipes - self._current_average_water_temp

        if difference_in_temp < 0:
            raise EnvironmentError(
                "Water coming back to water container colder than when it left... wrong since heat loss not yet factored in on pipes")

        # ºC * Joules/(L*ºC) * L/Min * Min/Hour = Joules/Hour and we only need one hour
        total_energy_flowed_over_water_container = difference_in_temp * SPECIFIC_HEAT_CAPACITY_OF_WATER * flow_rate_in_pipes * 60

        # Factoring in that pipes won't perfectly transfer energy, some energy lost
        self._energy_absorbed_from_pipes = total_energy_flowed_over_water_container * self._percent_of_thermal_energy_absorbed_from_pipes

        # Calculate increase in temp to heater, assumes tank always full - J / ( (J/LºC) * L ) = ºC
        temp_increase = self._energy_absorbed_from_pipes / (SPECIFIC_HEAT_CAPACITY_OF_WATER * self._water_capacity)

        # Update internal temperature based on energy from solar panels coming in through pipes
        self._current_average_water_temp += temp_increase
        self.set_current_thermal_energy()

        # Update internal temp to reflect loss
        new_thermal_energy = self._current_thermal_energy * (1 - self._percent_of_thermal_energy_lost_to_waste_per_hour)
        self._current_average_water_temp = (new_thermal_energy / self._water_capacity) / SPECIFIC_HEAT_CAPACITY_OF_WATER
        self.set_current_thermal_energy()

        # Apply usage pattern and rules (e.g. minimum temperature of the tank
        self.process_energy_outflow_for_hour_of_day(current_hour_of_day=current_hour_of_day)

        # At the end of the hour, outgoing and current average sync up
        self.outgoing_water_temperature = self._current_average_water_temp


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
