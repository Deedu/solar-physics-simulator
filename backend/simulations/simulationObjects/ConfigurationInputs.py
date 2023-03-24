from typing import Union, Dict
from pydantic import BaseModel


class SolarInput(BaseModel):
    length: float
    width: float
    solar_efficiency: float


class WaterPumpInput(BaseModel):
    max_flow_rate: float
    maximum_temp_difference_between_water_incoming_and_outgoing_solar: float
    minimum_temp_difference_between_water_incoming_and_outgoing_solar: float


class ConsumptionPatternOneHour(BaseModel):
    water_used: float
    average_temperature_of_water_used: float


class WaterContainerInput(BaseModel):
    water_capacity: float
    percent_of_thermal_energy_absorbed_from_pipes: float
    percent_of_thermal_energy_lost_to_waste_per_hour: float
    temperature_of_external_water_source: float
    efficiency_of_traditional_boiler: float
    minimum_average_water_temperature: float
    consumption_pattern: Dict[str, ConsumptionPatternOneHour]  # Keys are the hours, e.g. "01:00" as a key for 1am


class SimulationIncomingRequest(BaseModel):
    address: str
    optional_date_of_simulation: Union[str, None] = None
    simulation_uuid: str
    num_hours_to_simulate: int
    solar: SolarInput
    water_pump: WaterPumpInput
    water_container: WaterContainerInput
