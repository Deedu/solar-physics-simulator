from .CONSTANTS import SPECIFIC_HEAT_CAPACITY_OF_WATER


class SolarCollector:
    _surface_area: float = None  # m^2
    _water_temp_in: float = 0  # ºC
    _water_temp_out: float = 0  # ºC
    _water_flow_rate: float = 0  # L/min rate
    _energy_captured_by_solar: float = 0  # Watts
    _solar_efficiency: float = None  # give as a decimal, e.g. 0.05 for 5%

    def __init__(self, config):
        try:
            self._surface_area = config["length"] * config["width"]
            self._solar_efficiency = config["solar_efficiency"]
        except KeyError as e:
            raise KeyError("Incorrect config passed to SolarCollector", e)

    def add_one_hour_solar_energy(self, DNI_value_over_period: float, flow_rate, water_temp_in):
        """
        :param DNI_value_over_period: given in W/m^2 - proxy for energy given to panel.
                                      not actually correct since it is for 90º angle with sun, maximum absorption
                                      but you have to make some simplifying assumptions somehwere,
                                      and it is directionally right 🤷

        :param flow_rate: given in L/min - shows how much water is being moved
        :param water_temp_in: ºC, the temperature of water coming in
        :return: temperate_of_water_leaving

        Reasoning: We get DNI in, W/m^2, which is power per unit of area.
        This collector has a given efficiency of turning that solar energy into
        thermal energy in the water. I may not know that conversion rate very well
        (it changes over time with relative temperatures of water, condition of panels, etc.)
        but I could make a conservative assumption and run with it.

        I take the DNI in, multiply by efficiency of conversion, that gives me the
        energy that I am adding to the system, through the water.

        How I allocate that energy depends on the flow rate, i.e. slow moving water will get hotter
        and fast moving water will not get as hot, but a greater volume of water will be heated
        """

        watts_hitting_solar_collector = DNI_value_over_period * self._surface_area  # W/m^2 * m^2 = W
        watts_converted_to_energy = watts_hitting_solar_collector * self._solar_efficiency  # factor in losses from real world system

        energy_from_one_hour = watts_converted_to_energy * 60 * 60  # W = J/s, x 60s x 60m = J/hr and we look at 1hr periods, so just J

        volume_of_water_to_transfer_energy_to = flow_rate * 60  # L/min * 60min = L/hr, again 1 hr period so L

        num_degrees_celsius_temp_water_raised = \
            (energy_from_one_hour / volume_of_water_to_transfer_energy_to) / SPECIFIC_HEAT_CAPACITY_OF_WATER
        # (J / L ) / (J/L)ºC = ºC

        self._water_temp_in = water_temp_in
        self._water_temp_out = water_temp_in + num_degrees_celsius_temp_water_raised
        self._energy_captured_by_solar = energy_from_one_hour
        self._water_flow_rate = flow_rate

        return self._water_temp_out

    def get_loggable_metrics(self):
        """
        Returns JSON of what to log.

        NOTE - Json Keys must be unique - prefix with object name to be safe
        :return: Dictionary of metric names and metric values
        """
        return {"water_temp_into_solar": self._water_temp_in,
                "water_temp_out_of_solar": self._water_temp_out,
                "energy_captured_by_solar": self._energy_captured_by_solar,
                "solar_efficiency": self._solar_efficiency
                }

    def __hash__(self):
        """
        Just so I can use this obj as a key in dict
        :return:
        """
        return hash(self._surface_area)

    def __eq__(self, other):
        """
        Just so I can use this obj as a key in dict
        :return:
        """
        return self._surface_area == other._surface_area
