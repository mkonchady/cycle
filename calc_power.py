import math
import sys

# Power Calculator
# Copyright (c) 2018 Manu Konchady
#
# Tested with bikecalculator.com
#
# calculate head wind from bike velocity headed in 0 degree, wind velocity from wind_d degrees
def get_head_wind(v_bike, v_wind, wind_d = 0):
    wind_r = math.radians(wind_d)
    x = v_bike + v_wind * math.cos(wind_r) # x component of apparent wind 
    y = v_wind * math.sin(wind_r)          # y component of apparent wind
    v_apparent = math.sqrt(x*x + y*y)       # mag. of apparent wind
    beta = math.acos(x / v_apparent)        # angle of apparent wind 
    v_head = v_apparent * math.cos(beta)    # head wind in 0 degree direction 
    return v_head

# calculate the power from aero resistance, grade resistance, and rolling resistance
# velocities in kmph. 
def calc_air_res(K_A, v_bike, v_wind, alpha_d):
    v_bike = v_bike * 0.277778  # convert to m/sec
    v_wind = v_wind * 0.277778
    v_head = get_head_wind(v_bike, v_wind, alpha_d)
    return v_head * v_head * K_A

def calc_power(total_res, v_bike):
    return v_bike *  0.277778 * total_res / EFFICIENCY


#*--- MAIN SECTION

EFFICIENCY = 0.95

# Density calculation
TEMP = 25 # centigrade
ELEVATION = 0 # meters
DENSITY = (1.293 - 0.00426 * TEMP) * math.exp(-ELEVATION / 7000.0)

# Set Bicycle and Rider Parameters
RIDER_WT = 70 * 9.8
BICYCLE_WT = 10 * 9.8
TOTAL_WT = RIDER_WT + BICYCLE_WT # Newtons

# Calculate grade resistance
GRADE_V = 0.00
GRADE_RES = GRADE_V * TOTAL_WT

# Calculate rolling resistance
# Clinchers: 0.005, Tubular: 0.004, MTB: 0.012
ROLL_V = 0.005
ROLLING_RES = ROLL_V * TOTAL_WT

# calculate K_A: aerodynamic drag factor
# C_D_Area Hoods: 0.388  Bartops: 0.445  Barends: 0.42  Drops: 0.3 Aerobar: 0.233
FRONTAL_AREA = 0.5   # m^2
C_D = 1.15
C_D_AREA = C_D * FRONTAL_AREA
C_D_AREA = 0.388
K_A = 0.5 * C_D_AREA * DENSITY 

# calculate air drag
V_BIKE = 10 # bicycle velocity in kmph.
V_WIND = 0 # wind velocity in kmph.
V_DEG = 0   # direction (bearing of head wind)
AIR_RES = calc_air_res(K_A, V_BIKE, V_WIND, V_DEG)

TOLERANCE = 1.0

# Test 1
expected = 17
assert abs(math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE)) - expected) <= TOLERANCE, "1: Expected " + str(expected)

# Test 2
expected = 15
C_D_AREA = 0.233
K_A = 0.5 * C_D_AREA * DENSITY 
AIR_RES = calc_air_res(K_A, V_BIKE, V_WIND, V_DEG)
assert abs(math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE)) - expected) <= TOLERANCE, "2: Expected " + str(expected)

# Test 3
expected = 48
V_BIKE = 20
AIR_RES = calc_air_res(K_A, V_BIKE, V_WIND, V_DEG)
assert abs(math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE)) - expected) <= TOLERANCE, "3: Expected " + str(expected)

# Test 4
expected = 80
ROLL_V = 0.012
ROLLING_RES = ROLL_V * TOTAL_WT
assert abs(math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE)) - expected) <= TOLERANCE, "3: Expected " + str(expected)