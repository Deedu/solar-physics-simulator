class DataLogger:
    """
    A helper class to simplify and centralize log collection between many objects
    Currently outputs to one csv file, a timeseries of all variable values.
    """

    _output_file: str = None
    _variables_to_monitor: list = []  # list of dicts e.g.{"objectToMonitor": obj1, "objectPropertyName": "metric_name"}

    def __init__(self, config):
        try:
            self._output_file = config["data_logger_output_file"]
        except KeyError:
            raise KeyError("Incorrect config passed to DataLogger")

        # raise NotImplementedError

    def add_variable_to_log(self, objectToMonitor, objectPropertyName):
        self._variables_to_monitor.append(
            {"objectToMonitor": objectToMonitor, "objectPropertyName": objectPropertyName}
        )

    def log_current_variables(self):
        for variable_info in self._variables_to_monitor:
            object_to_monitor = variable_info["objectToMonitor"]