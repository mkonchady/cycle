import math
import sys

# Velocity Calculator from Power and Bike Parameters
# Copyright (c) 2018 Manu Konchady
#
# Tested with bikecalculator.com
#
# calculate head wind from bike velocity headed in 0 degree, wind velocity
# in alpha_d degrees
def get_head_wind(v_bike, v_wind, wind_d = 0):
    wind_r = math.radians(wind_d)
    x = v_bike + v_wind * math.cos(wind_r) # x component of apparent wind 
    y = v_wind * math.sin(wind_r)          # y component of apparent wind
    v_apparent = math.sqrt(x*x + y*y)       # mag. of apparent wind
    beta = math.acos(x / v_apparent)        # angle of apparent wind 
    v_head = v_apparent * math.cos(beta)    # head wind in 0 degree direction 
    return v_head

# calculate the bike velocity given power, A, head wind (m / sec), and sum of other resistance
def calc_velocity(frontal_area, head_wind, head_deg, other_resistance, power):
    velocity = 1000 
    MAX_ITERATIONS = 30
    TOLERANCE = 0.05
    for _ in range(1, MAX_ITERATIONS):
        #total_velocity = velocity + head_wind
        total_velocity = get_head_wind(velocity, head_wind, head_deg)
        
        if (total_velocity < 0):
            frontal_area = -frontal_area
        f = velocity * (frontal_area * total_velocity * total_velocity + other_resistance) - 0.95 * power
        fprime = frontal_area * (3.0 * velocity + head_wind) * total_velocity + other_resistance
        new_velocity = velocity - (f / fprime)
        if (abs(new_velocity - velocity) < TOLERANCE):
            return new_velocity
        velocity = new_velocity
    return 0.0

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

# set wind parameters
V_WIND = 0 # wind velocity in kmph.
V_DEG = 0   # direction (bearing of head wind)

TOLERANCE = 1.0

# Test 1:
power = 200 # watts
velocity = calc_velocity(K_A, V_WIND * 0.27778, V_DEG, GRADE_RES + ROLLING_RES, power) * 3.6
expected = 32
assert abs(math.ceil(velocity) - expected) <= TOLERANCE, "1: Expected vel: " + str(expected) 

# Test 2:
power = 100 # watts
velocity = calc_velocity(K_A, V_WIND * 0.27778, V_DEG, GRADE_RES + ROLLING_RES, power) * 3.6
expected = 24
assert abs(math.ceil(velocity) - expected) <= TOLERANCE, "2: Expected vel: " + str(expected) 

# Test 3:
V_WIND = 20 # kmph.
V_DEG = 0
velocity = calc_velocity(K_A, V_WIND * 0.27778, V_DEG, GRADE_RES + ROLLING_RES, power) * 3.6
expected = 14
assert abs(math.ceil(velocity) - expected) <= TOLERANCE, "3: Expected vel: " + str(expected) 

# Test 4:
V_WIND = 10 # kmph.
V_DEG = 0
velocity = calc_velocity(K_A, V_WIND * 0.27778, V_DEG, GRADE_RES + ROLLING_RES, power) * 3.6
expected = 18
assert abs(math.ceil(velocity) - expected) <= TOLERANCE, "3: Expected vel: " + str(expected) 

# Test 5:
ROLL_V = 0.012
ROLLING_RES = ROLL_V * TOTAL_WT
velocity = calc_velocity(K_A, V_WIND * 0.27778, V_DEG, GRADE_RES + ROLLING_RES, power) * 3.6
expected = 16
assert abs(math.ceil(velocity) - expected) <= TOLERANCE, "4: Expected vel: " + str(expected) 