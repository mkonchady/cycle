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

# Main
TOLERANCE = 0.1

# Test 1
expected = 1.18
temp = 25 # centigrade
rh = 50 # humidity percentage
alt = 0 # altitude in meters
assert abs(get_density(alt, temp, rh) - expected) < TOLERANCE, "1: Did not match expected value of " + str(expected)

# Test 2
expected = 0.971
temp = 10 # centigrade
rh = 80 # humidity percentage
alt = 2000 # altitude in meters
assert abs(get_density(alt, temp, rh) - expected) < TOLERANCE, "2: Did not match expected value of " + str(expected)

# Test 3
expected = 1.18
temp = -10 # centigrade
rh = 50 # humidity percentage
alt = 1000 # altitude in meters
assert abs(get_density(alt, temp, rh) - expected) < TOLERANCE, "3: Did not match expected value of " + str(expected)

