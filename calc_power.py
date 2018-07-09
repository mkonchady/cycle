import math
import sys

# Power Calculator
# Copyright (c) 2018 Manu Konchady

# calculate head wind from bike velocity headed in 0 degree, wind velocity
# in alpha_d degrees
def get_head_wind(v_bike, v_wind, alpha_d = 0):
    alpha_r = math.radians(alpha_d)
    x = v_bike + v_wind * math.cos(alpha_r) # x component of apparent wind 
    y = v_wind * math.sin(alpha_r)          # y component of apparent wind
    v_apparent = math.sqrt(x*x + y*y)       # mag. of apparent wind
    beta = math.acos(x / v_apparent)        # angle of apparent wind 
    v_head = v_apparent * math.cos(beta)    # head wind in 0 degree direction 
    return v_head

# calculate the power from aero resistance, grade resistance, and rolling resistance
# velocities in kmph. 
def calc_power(K_A, v_bike, v_wind, alpha_d, total_res):
    v_bike = v_bike * 0.277778  # convert to m/sec
    v_wind = v_wind * 0.277778
    v_head = get_head_wind(v_bike, v_wind, alpha_d)
    print (v_head * 3.6, v_bike)
    aero_res = v_head * v_head * K_A
    power = v_bike *(aero_res + total_res) / EFFICIENCY
    return power


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
ROLL_V = 0.005
ROLLING_RES = ROLL_V * TOTAL_WT

TOTAL_RES = GRADE_RES + ROLLING_RES

# calculate K_A: aerodynamic drag factor
FRONTAL_AREA = 0.5   # m^2
C_D = 1.15
K_A = 0.5 * C_D * FRONTAL_AREA * DENSITY 

V_BIKE = 20 # bicycle velocity in kmph.
V_HEAD = 0 # head wind velocity in kmph.
V_DEG = 0   # direction (bearing of head wind)

print (calc_power(K_A, V_BIKE, V_HEAD, V_DEG, TOTAL_RES))