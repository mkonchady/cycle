import math
import sys

# Velocity Calculator from Power and Bike Parameters
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
        #print ("f: " +  str(f) + "V: " + str(new_velocity))
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

# parameters for the air drag
FRONTAL_AREA = 0.5                          # m^2
C_D = 1.15                                  # coefficient of drag
k_a = 0.5 * C_D * FRONTAL_AREA * DENSITY  

# head wind magnitude and direction
HEAD_WIND = 0 # kmph
HEAD_WIND = HEAD_WIND * 0.277778
HEAD_DEG = 0 

# Set Bicycle and Rider Parameters to get mg
RIDER_WT = 70 * 9.8
BICYCLE_WT = 10 * 9.8
total_wt = RIDER_WT + BICYCLE_WT # Newtons

# Set grade resistance = mg theta
GRADE_V = 0.00
grade_res = GRADE_V * total_wt

# Set rolling resistance = mg s
ROLL_S = 0.005
roll_res = ROLL_S * total_wt

total_res = grade_res + roll_res

power = 100 # watts
velocity = calc_velocity(k_a, HEAD_WIND, HEAD_DEG, total_res, power) * 3.6
print (str(velocity) + " kmph.")
