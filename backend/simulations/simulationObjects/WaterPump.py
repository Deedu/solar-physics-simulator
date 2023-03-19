class WaterPump:
    _min_flow_rate: float = 0
    _max_flow_rate: float = None
    _current_flow_rate: float = None
    _percent_of_maximum_flow_rate: float = 0

    def __init__(self, config):
        try:
            self._min_flow_rate = 0
            self._max_flow_rate = config["max_flow_rate"]
            self._current_flow_rate = 0
        except KeyError as e:
            raise KeyError("Incorrect config passed to WaterPump", e)

    def get_flow_rate(self):
        return self._current_flow_rate

    def adjust_flow_to_current_state(self):

        self._percent_of_maximum_flow_rate = self._current_flow_rate/self._max_flow_rate
        raise NotImplementedError

    def get_loggable_metrics(self):
        """
        Returns JSON of what to log.

        NOTE - Json Keys must be unique - prefix with object name to be safe
        :return: Dictionary of metric names and metric values
        """
        return {"percent_water_pump_flow_rate_used": self._percent_of_maximum_flow_rate}
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