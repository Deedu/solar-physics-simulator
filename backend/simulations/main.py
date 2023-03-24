from fastapi import FastAPI, Body
import os
import json
from dotenv import load_dotenv
from simulationObjects.SimulatedWorld import SimulatedWorld
from simulationObjects.ConfigurationInputs import SimulationIncomingRequest
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

load_dotenv()  # only relevant for local - P4 cleanup later

app = FastAPI()


@app.post("/createSimulation")
async def create_simulation(incoming_simulation_parameters: Annotated[SimulationIncomingRequest, Body(
    examples={
        "normal": {"summary": "A 1 week simulation",
                   "description": "**standard example** - 7 days of modelling the system with reasonable values",
                   "value": {
                       "address": "7 Station St, Toronto, Ontario",
                       "optional_date_of_simulation": "10-March-2023",
                       "simulation_uuid": "very_secure_uuid_default_example_one_week_timeframe",
                       "num_hours_to_simulate": 170,
                       "solar": {
                           "length": 4.5,
                           "width": 2,
                           "solar_efficiency": 0.15
                       },
                       "water_pump": {
                           "max_flow_rate": 20,
                           "maximum_temp_difference_between_water_incoming_and_outgoing_solar": 4,
                           "minimum_temp_difference_between_water_incoming_and_outgoing_solar": 2
                       },
                       "water_container": {
                           "water_capacity": 200,
                           "percent_of_thermal_energy_absorbed_from_pipes": 0.85,
                           "percent_of_thermal_energy_lost_to_waste_per_hour": 0.02,
                           "temperature_of_external_water_source": 7,
                           "efficiency_of_traditional_boiler": 0.75,
                           "minimum_average_water_temperature": 50,
                           "consumption_pattern": {
                               "00:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 0
                               },
                               "01:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 0
                               },
                               "02:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 0
                               },
                               "03:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 0
                               },
                               "04:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 0
                               },
                               "05:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 0
                               },
                               "06:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 0
                               },
                               "07:00": {
                                   "water_used": 55,
                                   "average_temperature_of_water_used": 38
                               },
                               "08:00": {
                                   "water_used": 10,
                                   "average_temperature_of_water_used": 50
                               },
                               "09:00": {
                                   "water_used": 10,
                                   "average_temperature_of_water_used": 50
                               },
                               "10:00": {
                                   "water_used": 20,
                                   "average_temperature_of_water_used": 30
                               },
                               "11:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 50
                               },
                               "12:00": {
                                   "water_used": 60,
                                   "average_temperature_of_water_used": 15
                               },
                               "13:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 50
                               },
                               "14:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 50
                               },
                               "15:00": {
                                   "water_used": 5,
                                   "average_temperature_of_water_used": 50
                               },
                               "16:00": {
                                   "water_used": 10,
                                   "average_temperature_of_water_used": 50
                               },
                               "18:00": {
                                   "water_used": 10,
                                   "average_temperature_of_water_used": 50
                               },
                               "19:00": {
                                   "water_used": 35,
                                   "average_temperature_of_water_used": 65
                               },
                               "20:00": {
                                   "water_used": 10,
                                   "average_temperature_of_water_used": 50
                               },
                               "21:00": {
                                   "water_used": 10,
                                   "average_temperature_of_water_used": 50
                               },
                               "22:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 50
                               },
                               "23:00": {
                                   "water_used": 0,
                                   "average_temperature_of_water_used": 50
                               }

                           }
                       }
                   }},
        "super-solar": {"summary": "A 1 week simulation - **with a gigantic solar panel**",
                        "description": "**super solar example** - 7 days of modelling the system with a huge solar panel",
                        "value": {
                            "address": "7 Station St, Toronto, Ontario",
                            "optional_date_of_simulation": "10-March-2023",
                            "simulation_uuid": "very_secure_uuid_super_solar_example",
                            "num_hours_to_simulate": 170,
                            "solar": {
                                "length": 10,
                                "width": 10,
                                "solar_efficiency": 0.15
                            },
                            "water_pump": {
                                "max_flow_rate": 45,
                                "maximum_temp_difference_between_water_incoming_and_outgoing_solar": 10,
                                "minimum_temp_difference_between_water_incoming_and_outgoing_solar": 2
                            },
                            "water_container": {
                                "water_capacity": 200,
                                "percent_of_thermal_energy_absorbed_from_pipes": 0.85,
                                "percent_of_thermal_energy_lost_to_waste_per_hour": 0.02,
                                "temperature_of_external_water_source": 7,
                                "efficiency_of_traditional_boiler": 0.75,
                                "minimum_average_water_temperature": 50,
                                "consumption_pattern": {
                                    "00:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 0
                                    },
                                    "01:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 0
                                    },
                                    "02:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 0
                                    },
                                    "03:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 0
                                    },
                                    "04:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 0
                                    },
                                    "05:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 0
                                    },
                                    "06:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 0
                                    },
                                    "07:00": {
                                        "water_used": 55,
                                        "average_temperature_of_water_used": 38
                                    },
                                    "08:00": {
                                        "water_used": 10,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "09:00": {
                                        "water_used": 10,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "10:00": {
                                        "water_used": 20,
                                        "average_temperature_of_water_used": 30
                                    },
                                    "11:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "12:00": {
                                        "water_used": 60,
                                        "average_temperature_of_water_used": 15
                                    },
                                    "13:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "14:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "15:00": {
                                        "water_used": 5,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "16:00": {
                                        "water_used": 10,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "18:00": {
                                        "water_used": 10,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "19:00": {
                                        "water_used": 35,
                                        "average_temperature_of_water_used": 65
                                    },
                                    "20:00": {
                                        "water_used": 10,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "21:00": {
                                        "water_used": 10,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "22:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 50
                                    },
                                    "23:00": {
                                        "water_used": 0,
                                        "average_temperature_of_water_used": 50
                                    }

                                }
                            }
                        }},
        "gigantic-tank": {"summary": "A 1 week simulation - **with a gigantic water tank**",
                          "description": "**super tank example** - 7 days of modelling the system with a huge water tank",
                          "value": {
                              "address": "7 Station St, Toronto, Ontario",
                              "optional_date_of_simulation": "10-March-2023",
                              "simulation_uuid": "very_secure_uuid_super_tank_example",
                              "num_hours_to_simulate": 170,
                              "solar": {
                                  "length": 4.5,
                                  "width": 2.5,
                                  "solar_efficiency": 0.15
                              },
                              "water_pump": {
                                  "max_flow_rate": 45,
                                  "maximum_temp_difference_between_water_incoming_and_outgoing_solar": 10,
                                  "minimum_temp_difference_between_water_incoming_and_outgoing_solar": 2
                              },
                              "water_container": {
                                  "water_capacity": 1200,
                                  "percent_of_thermal_energy_absorbed_from_pipes": 0.85,
                                  "percent_of_thermal_energy_lost_to_waste_per_hour": 0.02,
                                  "temperature_of_external_water_source": 7,
                                  "efficiency_of_traditional_boiler": 0.75,
                                  "minimum_average_water_temperature": 50,
                                  "consumption_pattern": {
                                      "00:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 0
                                      },
                                      "01:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 0
                                      },
                                      "02:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 0
                                      },
                                      "03:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 0
                                      },
                                      "04:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 0
                                      },
                                      "05:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 0
                                      },
                                      "06:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 0
                                      },
                                      "07:00": {
                                          "water_used": 55,
                                          "average_temperature_of_water_used": 38
                                      },
                                      "08:00": {
                                          "water_used": 10,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "09:00": {
                                          "water_used": 10,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "10:00": {
                                          "water_used": 20,
                                          "average_temperature_of_water_used": 30
                                      },
                                      "11:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "12:00": {
                                          "water_used": 60,
                                          "average_temperature_of_water_used": 15
                                      },
                                      "13:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "14:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "15:00": {
                                          "water_used": 5,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "16:00": {
                                          "water_used": 10,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "18:00": {
                                          "water_used": 10,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "19:00": {
                                          "water_used": 35,
                                          "average_temperature_of_water_used": 65
                                      },
                                      "20:00": {
                                          "water_used": 10,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "21:00": {
                                          "water_used": 10,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "22:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 50
                                      },
                                      "23:00": {
                                          "water_used": 0,
                                          "average_temperature_of_water_used": 50
                                      }

                                  }
                              }
                          }},
        "shower-hog": {
            "summary": "A 1 week simulation - with someone who loves long hot showers (no need to name names)",
            "description": "**standard example** - 7 days of modelling the system with reasonable values and a lot of hot showers",
            "value": {
                "address": "7 Station St, Toronto, Ontario",
                "optional_date_of_simulation": "10-March-2023",
                "simulation_uuid": "very_secure_uuid_default_example_one_week_timeframe",
                "num_hours_to_simulate": 170,
                "solar": {
                    "length": 4.5,
                    "width": 2,
                    "solar_efficiency": 0.15
                },
                "water_pump": {
                    "max_flow_rate": 20,
                    "maximum_temp_difference_between_water_incoming_and_outgoing_solar": 4,
                    "minimum_temp_difference_between_water_incoming_and_outgoing_solar": 2
                },
                "water_container": {
                    "water_capacity": 200,
                    "percent_of_thermal_energy_absorbed_from_pipes": 0.85,
                    "percent_of_thermal_energy_lost_to_waste_per_hour": 0.02,
                    "temperature_of_external_water_source": 7,
                    "efficiency_of_traditional_boiler": 0.75,
                    "minimum_average_water_temperature": 50,
                    "consumption_pattern": {
                        "00:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 0
                        },
                        "01:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 0
                        },
                        "02:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 0
                        },
                        "03:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 0
                        },
                        "04:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 0
                        },
                        "05:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 0
                        },
                        "06:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 0
                        },
                        "07:00": {
                            "water_used": 55,
                            "average_temperature_of_water_used": 38
                        },
                        "08:00": {
                            "water_used": 45,
                            "average_temperature_of_water_used": 50
                        },
                        "09:00": {
                            "water_used": 30,
                            "average_temperature_of_water_used": 50
                        },
                        "10:00": {
                            "water_used": 20,
                            "average_temperature_of_water_used": 30
                        },
                        "11:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 50
                        },
                        "12:00": {
                            "water_used": 60,
                            "average_temperature_of_water_used": 15
                        },
                        "13:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 50
                        },
                        "14:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 50
                        },
                        "15:00": {
                            "water_used": 5,
                            "average_temperature_of_water_used": 50
                        },
                        "16:00": {
                            "water_used": 10,
                            "average_temperature_of_water_used": 50
                        },
                        "18:00": {
                            "water_used": 85,
                            "average_temperature_of_water_used": 50
                        },
                        "19:00": {
                            "water_used": 35,
                            "average_temperature_of_water_used": 65
                        },
                        "20:00": {
                            "water_used": 30,
                            "average_temperature_of_water_used": 85
                        },
                        "21:00": {
                            "water_used": 10,
                            "average_temperature_of_water_used": 50
                        },
                        "22:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 50
                        },
                        "23:00": {
                            "water_used": 0,
                            "average_temperature_of_water_used": 50
                        }

                    }
                }
            }},
        "brightest-city-on-earth": {"summary": "A 1 week simulation - **in Yuma, AZ** - the brightest city on earth",
                                    "description": "**super sunny example** - 7 days of modelling the system with a lot of sun",
                                    "value": {
                                        "address": "One City Plaza, Yuma, AZ 85364",
                                        "optional_date_of_simulation": "10-March-2023",
                                        "simulation_uuid": "very_secure_uuid_super_sunny_city_example",
                                        "num_hours_to_simulate": 170,
                                        "solar": {
                                            "length": 10,
                                            "width": 10,
                                            "solar_efficiency": 0.15
                                        },
                                        "water_pump": {
                                            "max_flow_rate": 45,
                                            "maximum_temp_difference_between_water_incoming_and_outgoing_solar": 10,
                                            "minimum_temp_difference_between_water_incoming_and_outgoing_solar": 2
                                        },
                                        "water_container": {
                                            "water_capacity": 200,
                                            "percent_of_thermal_energy_absorbed_from_pipes": 0.85,
                                            "percent_of_thermal_energy_lost_to_waste_per_hour": 0.02,
                                            "temperature_of_external_water_source": 7,
                                            "efficiency_of_traditional_boiler": 0.75,
                                            "minimum_average_water_temperature": 50,
                                            "consumption_pattern": {
                                                "00:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 0
                                                },
                                                "01:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 0
                                                },
                                                "02:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 0
                                                },
                                                "03:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 0
                                                },
                                                "04:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 0
                                                },
                                                "05:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 0
                                                },
                                                "06:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 0
                                                },
                                                "07:00": {
                                                    "water_used": 55,
                                                    "average_temperature_of_water_used": 38
                                                },
                                                "08:00": {
                                                    "water_used": 10,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "09:00": {
                                                    "water_used": 10,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "10:00": {
                                                    "water_used": 20,
                                                    "average_temperature_of_water_used": 30
                                                },
                                                "11:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "12:00": {
                                                    "water_used": 60,
                                                    "average_temperature_of_water_used": 15
                                                },
                                                "13:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "14:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "15:00": {
                                                    "water_used": 5,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "16:00": {
                                                    "water_used": 10,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "18:00": {
                                                    "water_used": 10,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "19:00": {
                                                    "water_used": 35,
                                                    "average_temperature_of_water_used": 65
                                                },
                                                "20:00": {
                                                    "water_used": 10,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "21:00": {
                                                    "water_used": 10,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "22:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 50
                                                },
                                                "23:00": {
                                                    "water_used": 0,
                                                    "average_temperature_of_water_used": 50
                                                }

                                            }
                                        }
                                    }},
        "one-month-model": {"summary": "A 1 month simulation - standard/default values",
                            "description": "**standard example 1 month** - 1 month of modelling the system with reasonable values",
                            "value": {
                                "address": "7 Station St, Toronto, Ontario",
                                "optional_date_of_simulation": "10-March-2023",
                                "simulation_uuid": "very_secure_uuid_default_example_one_month_timeframe",
                                "num_hours_to_simulate": 700,
                                "solar": {
                                    "length": 4.5,
                                    "width": 2,
                                    "solar_efficiency": 0.15
                                },
                                "water_pump": {
                                    "max_flow_rate": 20,
                                    "maximum_temp_difference_between_water_incoming_and_outgoing_solar": 4,
                                    "minimum_temp_difference_between_water_incoming_and_outgoing_solar": 2
                                },
                                "water_container": {
                                    "water_capacity": 200,
                                    "percent_of_thermal_energy_absorbed_from_pipes": 0.85,
                                    "percent_of_thermal_energy_lost_to_waste_per_hour": 0.02,
                                    "temperature_of_external_water_source": 7,
                                    "efficiency_of_traditional_boiler": 0.75,
                                    "minimum_average_water_temperature": 50,
                                    "consumption_pattern": {
                                        "00:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 0
                                        },
                                        "01:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 0
                                        },
                                        "02:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 0
                                        },
                                        "03:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 0
                                        },
                                        "04:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 0
                                        },
                                        "05:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 0
                                        },
                                        "06:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 0
                                        },
                                        "07:00": {
                                            "water_used": 55,
                                            "average_temperature_of_water_used": 38
                                        },
                                        "08:00": {
                                            "water_used": 10,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "09:00": {
                                            "water_used": 10,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "10:00": {
                                            "water_used": 20,
                                            "average_temperature_of_water_used": 30
                                        },
                                        "11:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "12:00": {
                                            "water_used": 60,
                                            "average_temperature_of_water_used": 15
                                        },
                                        "13:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "14:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "15:00": {
                                            "water_used": 5,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "16:00": {
                                            "water_used": 10,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "18:00": {
                                            "water_used": 10,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "19:00": {
                                            "water_used": 35,
                                            "average_temperature_of_water_used": 65
                                        },
                                        "20:00": {
                                            "water_used": 10,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "21:00": {
                                            "water_used": 10,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "22:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 50
                                        },
                                        "23:00": {
                                            "water_used": 0,
                                            "average_temperature_of_water_used": 50
                                        }

                                    }
                                }
                            }},
        "one-year-model": {"summary": "A 1 year simulation - standard/default values",
                           "description": "**standard example 1 year** - 1 year of modelling the system with reasonable values",
                           "value": {
                               "address": "7 Station St, Toronto, Ontario",
                               "optional_date_of_simulation": "10-March-2023",
                               "simulation_uuid": "very_secure_uuid_default_example_one_year_timeframe",
                               "num_hours_to_simulate": 9000,
                               "solar": {
                                   "length": 4.5,
                                   "width": 2,
                                   "solar_efficiency": 0.15
                               },
                               "water_pump": {
                                   "max_flow_rate": 20,
                                   "maximum_temp_difference_between_water_incoming_and_outgoing_solar": 4,
                                   "minimum_temp_difference_between_water_incoming_and_outgoing_solar": 2
                               },
                               "water_container": {
                                   "water_capacity": 200,
                                   "percent_of_thermal_energy_absorbed_from_pipes": 0.85,
                                   "percent_of_thermal_energy_lost_to_waste_per_hour": 0.02,
                                   "temperature_of_external_water_source": 7,
                                   "efficiency_of_traditional_boiler": 0.75,
                                   "minimum_average_water_temperature": 50,
                                   "consumption_pattern": {
                                       "00:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 0
                                       },
                                       "01:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 0
                                       },
                                       "02:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 0
                                       },
                                       "03:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 0
                                       },
                                       "04:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 0
                                       },
                                       "05:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 0
                                       },
                                       "06:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 0
                                       },
                                       "07:00": {
                                           "water_used": 55,
                                           "average_temperature_of_water_used": 38
                                       },
                                       "08:00": {
                                           "water_used": 10,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "09:00": {
                                           "water_used": 10,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "10:00": {
                                           "water_used": 20,
                                           "average_temperature_of_water_used": 30
                                       },
                                       "11:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "12:00": {
                                           "water_used": 60,
                                           "average_temperature_of_water_used": 15
                                       },
                                       "13:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "14:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "15:00": {
                                           "water_used": 5,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "16:00": {
                                           "water_used": 10,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "18:00": {
                                           "water_used": 10,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "19:00": {
                                           "water_used": 35,
                                           "average_temperature_of_water_used": 65
                                       },
                                       "20:00": {
                                           "water_used": 10,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "21:00": {
                                           "water_used": 10,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "22:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 50
                                       },
                                       "23:00": {
                                           "water_used": 0,
                                           "average_temperature_of_water_used": 50
                                       }

                                   }
                               }
                           }}

    })]):
    # TODO - Implement marshmallow or similar for schema enforcement and sanitization
    print("Simulation Starting - Received Input Below")
    # print(incoming_simulation_parameters)

    try:
        new_world = SimulatedWorld(incoming_simulation_parameters)
        new_world.run_entire_simulation()
    except KeyError as e:
        print(f'Request failed with exception {str(e)}')
        JSONResponse(status_code=400,
                     content={"exception": str(e), "message": "Input Parameters incorrectly sent"})

    except Exception as e:
        print(f'Request failed with exception {str(e)}')
        return JSONResponse(status_code=500, content={"exception": str(e),
                                                      "message": "Simulation encoutered the following critical exception that stopped successful simulation run"})
    return "Simulation Successful", 200
