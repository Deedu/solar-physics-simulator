### Build Status
[![Simulation Processing Python Backend](https://github.com/Deedu/solar-physics-simulator/actions/workflows/backend-simulations-deploy-automation.yml/badge.svg)](https://github.com/Deedu/solar-physics-simulator/actions/workflows/backend-simulations-deploy-automation.yml)
# The Basic Mental Model

The idea for the system is fairly straightforward. Model a system that:
1. Collects solar energy through a solar panel
2. Puts that energy into water via heat transfer into pipes that run through the solar panels
3. Pumps that newly heated water into a water tank, where it is stored
4. Consumes some of that water over time through daily activities and continues to add energy/heat to the system from solar activity
5. Logs metrics throughout the process that monitor the system to inform later decision making (analytics)

# Potential Use Cases

* Determining if you should get a solar panel water heater system
  * Cost/Value, Payback Time
* Optimizing Location/Positioning of large scale panel placements
  * Simple reasoning would be to pick areas with highest Direct Normal Irradiation (DNI). That is probably true or close to true, but cities may care about how consistent it is - e.g. short burts of high intensity or long periods of low intensity
  * Could model one large system versus many small ones geographically spread out a bit. Maybe diversification helps.
* Optimizing consumer behavior
  * When to shower, how much to shower, etc. to minimize energy costs and reduce need for traditional energy sources
* Optimizing hardware/system design
  * How big should solar panels be relative to water tank, how powerful should the pump be, etc.

# Production Architecture

![Diagram showing the various services that produce the simulation](./architecture-graphs/solar_physics_simulator.png "Architecture Diagram")

# A Few Key Assumptions

* Tank is always kept full on an hourly basis, water removed is filled with tap/external source


# Potential Improvements

* Simulation
  * Minute by minute/continuous modelling 
  * Factoring in the lengthening/shortnening of days throughout the year
  * Use Global Horizontal Irradiance (GHI)  instead of Direct Normal Irradiation (DNI)
    * Factoring in angle of sun throughout the day (lower efficiency as you get further from 90º normal to the sun)
  * Making flow rate continous instead of fixed over a period
  * Stricter/better use of boiler, right now only kicks in after water usage but could temperature could decline overnight as well
* Metrics
  * More detailed tracking of loss/inefficiency in the system

