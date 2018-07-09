import math
import sys

# Air Density Calculator
# Copyright (c) 2018 Manu Konchady

# return the pressure for a given altitude and temperature using the hypsometric formula
def get_pressure (alt, temp):
    kelvin = temp + 273.15
    lhs = 1.0 + (alt * 0.0065) / kelvin
    log_term = math.log(lhs, 10) / (1.0 / 5.257)
    return 1013.25 / (math.pow(10, log_term))

# get the density using teten's formula
# alt is in meters, temp in cent. and relative humidity is a percentage
def get_density(alt, temp, rh):
    kelvin = temp + 273.15
    pressure = get_pressure(alt, temp)
    if (temp >= 0):
        saturated_pressure = 0.61078 * math.exp( (17.270 * temp) / (temp + 237.3) )
    else:
        saturated_pressure = 0.61078 * math.exp( (21.875 * temp) / (temp + 265.5) )
    return (0.0034848 / kelvin) * (pressure * 100 - 0.0037960 * rh * saturated_pressure)

print (get_density(0, 25, 50))