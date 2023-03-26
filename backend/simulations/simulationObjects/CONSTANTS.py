SPECIFIC_HEAT_CAPACITY_OF_WATER = 4184  # Joules to increase temp of 1kg of wayer by 1ºC.
# Simplifying assumption that 1Kg water is 1L,
# even though this varies based on purity and temp of water

BIGQUERY_TABLE_ID = "solar-phyics-simulator.simulations_dataset.simulations_hourly_metrics"
OUTPUT_METRICS_FILE_PATH = 'outputData/sampleSimulationOutput.csv'
BIGQUERY_SCHEMA = [
    {"name": "uuid", "type": "STRING"},
    {"name": "Timestamp", "type": "TIMESTAMP"},
    {"name": "DNI_Value", "type": "FLOAT"},
    {"name": "water_temp_into_solar", "type": "FLOAT"},
    {"name": "water_temp_out_of_solar", "type": "FLOAT"},
    {"name": "energy_captured_by_solar", "type": "FLOAT"},
    {"name": "solar_efficiency", "type": "FLOAT"},
    {"name": "water_flow_rate", "type": "FLOAT"},
    {"name": "percent_water_pump_flow_rate_used", "type": "FLOAT"},
    {"name": "current_average_water_temp_in_water_container", "type": "FLOAT"},
    {"name": "current_thermal_energy_in_water_container", "type": "FLOAT"},
    {"name": "average_temp_of_water_sent_out_of_water_container", "type": "FLOAT"},
    {"name": "energy_sent_out_of_water_container", "type": "FLOAT"},
    {"name": "volume_of_water_sent_out_of_water_container", "type": "FLOAT"},
    {"name": "energy_consumed_by_heater", "type": "FLOAT"},
    {"name": "energy_absorbed_from_pipes", "type": "FLOAT"}
    ,
    {"name": "int64_field_16", "type": "INTEGER"}
]
