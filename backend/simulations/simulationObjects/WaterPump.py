from .ConfigurationInputs import WaterPumpInput


class WaterPump:
    _min_flow_rate: float = 0
    _max_flow_rate: float = None
    _current_flow_rate: float = None
    _percent_of_maximum_flow_rate: float = 0
    _minimum_temp_difference_between_water_incoming_and_outgoing_solar = 2
    _maximum_temp_difference_between_water_incoming_and_outgoing_solar = 15  # ºC, a proxy for how fast the pump should work
    _flow_rate_increase_factor: float = 1.20  # how much to increase flow rate over 1 hour, e.g. 15% faster is 1.15
    _flow_rate_decrease_factor: float = 0.7  # how much to decrease flow rate over 1 hour, e.g. 30% slower is 0.7

    def __init__(self, config: WaterPumpInput):
        try:
            self._min_flow_rate = 0.5  # 0.5 L/min hardcoded because I have no idea if this is a real thing
            self._max_flow_rate = config.max_flow_rate
            self._current_flow_rate = self._min_flow_rate
            self._maximum_temp_difference_between_water_incoming_and_outgoing_solar = config.maximum_temp_difference_between_water_incoming_and_outgoing_solar
            self._minimum_temp_difference_between_water_incoming_and_outgoing_solar = config.minimum_temp_difference_between_water_incoming_and_outgoing_solar
        except KeyError as e:
            raise KeyError("Incorrect config passed to WaterPump", e)

    def get_flow_rate(self):
        return self._current_flow_rate

    def adjust_flow_to_current_state(self, incoming_solar_water_temperature, outgoing_solar_water_temperature):
        """
        Uses a simple scaling formula to increase or decrease pump speed based on difference in water temperature
        :param incoming_solar_water_temperature:
        :param outgoing_solar_water_temperature:
        :return:
        """
        temp_difference_between_incoming_and_outgoing = outgoing_solar_water_temperature - incoming_solar_water_temperature

        temp_diff_too_high = temp_difference_between_incoming_and_outgoing > self._maximum_temp_difference_between_water_incoming_and_outgoing_solar
        temp_diff_too_low = temp_difference_between_incoming_and_outgoing < self._minimum_temp_difference_between_water_incoming_and_outgoing_solar

        if temp_diff_too_low:  # slow down pump
            self._current_flow_rate = max(self._current_flow_rate * self._flow_rate_decrease_factor,
                                          self._min_flow_rate)
        elif not temp_diff_too_low and not temp_diff_too_high:
            pass  # leave pump in same state
        elif temp_diff_too_high:  # speed up pump
            self._current_flow_rate = min(self._current_flow_rate * self._flow_rate_increase_factor,
                                          self._max_flow_rate)
        self._percent_of_maximum_flow_rate = self._current_flow_rate / self._max_flow_rate

    def get_loggable_metrics(self):
        """
        Returns JSON of what to log.

        NOTE - Json Keys must be unique - prefix with object name to be safe
        :return: Dictionary of metric names and metric values
        """
        return {
            "water_flow_rate": self._current_flow_rate,
            "percent_water_pump_flow_rate_used": self._percent_of_maximum_flow_rate
        }

    def __hash__(self):
        """
        Just so I can use this obj as a key in dict
        :return:
        """
        return hash(self._max_flow_rate)

    def __eq__(self, other):
        """
        Just so I can use this obj as a key in dict
        :return:
        """
        return self._max_flow_rate == other._max_flow_rate
