#*-------------------------------------------------------------
#*-  Calculate the stopping distance using methods
#*-------------------------------------------------------------

import math
import sys
import calc_wind
import moments
import common

# Density calculation
TEMP = 25 # centigrade
ELEVATION = 0 # meters
DENSITY = (1.293 - 0.00426 * TEMP) * math.exp(-ELEVATION / 7000.0)
G_ACCEL = 9.81

# Set Bicycle and Rider Parameters
RIDER_MASS = 70        # rider kgs.
BICYCLE_MASS = 10       # bicycle kgs.
TOTAL_WT = (RIDER_MASS + BICYCLE_MASS) * 9.81 # Newtons
TOTAL_MASS = RIDER_MASS + BICYCLE_MASS
WHEEL_MASS = 1      # one kg.

# All in meters
WHEEL_BASE = 1.01
WHEEL_RADIUS = (0.7 / 2.0)  
WHEEL_CIRCUM = 2.0 * math.pi * WHEEL_RADIUS # in meters     
REAR_CRANK_DISTANCE = 0.43
COM_HEIGHT = 1.15

BIG_NUMBER = 10000
SMALL_NEGATIVE_NUMBER = -0.00000000000000000000001
INVALID_REAR_FRAC = -1

#*-- get the maximum fraction of rear brake for a given braking g force
def get_rear_frac(G_FRAC):
    if (G_FRAC < 0 or G_FRAC > 0.56):
        return INVALID_REAR_FRAC
    return 0 # all braking force from front brake alone
    
# calculate the power from aero resistance, grade resistance, and rolling resistance
# velocities in kmph. 
def calc_air_res(K_A, v_bike, v_wind, alpha_d):
    v_bike = common.meter_per_second(v_bike)
    v_wind = common.meter_per_second(v_wind)
    return calc_wind.get_head_wind2(v_bike, v_wind, alpha_d) * K_A

def calc_power(total_res, v_bike):
    EFFICIENCY = 0.95
    return common.meter_per_second(v_bike) * total_res / EFFICIENCY

#*--------------------------------------------------
# calculate the total of all drag forces
# V_BIKE and V_WIND in kmph, grade in percent
#*--------------------------------------------------
def get_total_res(V_BIKE, V_WIND, GRADE, G_FRAC, debug, rear_frac, C_SF = 0.7):
    
    # Calculate grade resistance
    GRADE_V = GRADE / 100.0
    GRADE_RES = GRADE_V * TOTAL_WT
    COS_THETA = 1.0 - GRADE_V # approximately 
    if (debug):
        print ("Slope Resistance: " + str(GRADE_RES))

    # Calculate rolling resistance
    # Clinchers: 0.005, Tubular: 0.004, MTB: 0.012
    ROLL_V = 0.005
    ROLLING_RES = ROLL_V * TOTAL_WT
    if (debug):
        print ("Rolling resistance: " + str(ROLLING_RES))

    # calculate K_A: aerodynamic drag factor
    # C_D_Area Hoods: 0.388  Bartops: 0.445  Barends: 0.42  Drops: 0.3 Aerobar: 0.233
    FRONTAL_AREA = 0.5   # m^2
    C_D = 1.15
    C_D_AREA = C_D * FRONTAL_AREA
    C_D_AREA = 0.388
    K_A = 0.5 * C_D_AREA * DENSITY 

    # calculate air drag
    V_DEG = 0   # direction (bearing of head wind)
    AIR_RES = calc_air_res(K_A, V_BIKE, V_WIND, V_DEG)
    if (debug):
        print ("Air Drag: " + str(AIR_RES))

    # Find the max. brake force on the rear tyre from moments
    # coefficient of static friction 0.35 for wet, and 0.7 for dry
    f_nf, f_nr = moments.get_normal_forces_1(WHEEL_BASE, REAR_CRANK_DISTANCE, COM_HEIGHT, \
                TOTAL_MASS * COS_THETA, G_FRAC)
    f_rear_max = C_SF * f_nr         # max. rear wheel braking force
    f_rear_brake = G_FRAC * G_ACCEL * rear_frac * TOTAL_MASS
    if (f_rear_brake > f_rear_max): # rear brake force exceeds static friction force
        return -1

    # set the brake resistance
    BRAKE_RES = G_FRAC * TOTAL_WT  # in newtons
    if (debug):
        print ("Brake Drag: " + str(BRAKE_RES))

    return (BRAKE_RES + AIR_RES + ROLLING_RES + GRADE_RES)

#*--------------------------------------------------
# calculate stopping distance using drag forces
#*--------------------------------------------------
def dist1(V_BIKE, V_WIND, GRADE, G_FRAC, debug, rear_frac = 0.0, C_SF = 0.7):
    return calc_dist(V_BIKE, V_WIND, GRADE, G_FRAC, debug, True, rear_frac, C_SF)

def time1(V_BIKE, V_WIND, GRADE, G_FRAC, debug, rear_frac = 0.0, C_SF = 0.7):
    return calc_dist(V_BIKE, V_WIND, GRADE, G_FRAC, debug, False, rear_frac, C_SF)

def calc_dist(V_BIKE, V_WIND, GRADE, G_FRAC, debug, return_dist, rear_frac, C_SF):
    if (rear_frac == INVALID_REAR_FRAC):
        rear_frac = get_rear_frac(G_FRAC)
    TOTAL_RES = get_total_res(V_BIKE, V_WIND, GRADE, G_FRAC, debug, rear_frac, C_SF)
    DELTA_TIME = 0.05 # seconds
    total_time = 0
    velocity = V_BIKE
    iter = 0
    stopping_dist = 0
    while (velocity > 1):
        # calculate the drag force, new acceleration, new velocity, and cumulative stopping distance
        TOTAL_RES = get_total_res(velocity, V_WIND, GRADE, G_FRAC, debug, rear_frac, C_SF)
        if (TOTAL_RES < 0):
            return -1
        accel = TOTAL_RES / TOTAL_MASS
        new_velocity = velocity - common.kmph(accel) * DELTA_TIME  # convert accel from m/s to kmph
        stopping_dist = stopping_dist + common.meter_per_second(DELTA_TIME * new_velocity)
        velocity = new_velocity
        iter = iter + 1
        total_time += DELTA_TIME
        if (iter > 10000):
           return -1
    if (return_dist):
        return stopping_dist
    return total_time

#*-----------------------------------------------------------------------------------------------------
#*-- return stopping distance from formula in pg 246 of Bicycling Science
#*-- velocity in kmph. and c_a, c_r in fractions are coefficients of adhesion and rolling resistance
#*-----------------------------------------------------------------------------------------------------
def dist2(velocity, c_a, c_r):
    numer = common.meter_per_second(velocity) * common.meter_per_second(velocity)
    denom = 20 * (c_a + c_r)
    return numer / denom

#*-------------------------------------------------------------------------------------------------
# In the book "A Policy on Geometric Design of Highways and Streets", AASHTO gives the formula for 
# calculating the stopping distance. This formula is commonly used in road design for establishing 
# the minimum stopping sight distance required on a given road.
#
# The AASHTO formula is as follows:
#
# s = (0.278 * t * v) + v² / (254 * (f + G))
#
# where:
#
#    s is the stopping distance, measured in meters;
#
#    t is the perception-reaction time in seconds;
#
#    v is the speed of the car in km/h;
#
#    G is the grade (slope) of the road, expressed as a decimal. 
#      It is positive for an uphill grade and negative for a road going downhill;
#
#    f is the coefficient of friction between the tires and the road. 
#      It is typically assumed to be equal to 0.7 on a dry road and in the range from 0.3 to 0.4 on a wet road.
#*--------------------------------------------------------------------------------------------------------------
def dist3(t, v, g, f):
    grade = g / 100.0
    return (0.278 * t * v) + (v * v) / (254 * (f + grade))

#*--------------------------------------------------
# calculate stopping distance using kinetic energy
# V_BIKE and V_WIND in kmph., GRADE in percent, and g_frac as a fraction of g
#*--------------------------------------------------
def dist4(V_BIKE, V_WIND, GRADE, G_FRAC, debug, C_SF):
    total_s = 0
    DELTA_V = 0.05              # m/sec
    v_i = common.meter_per_second(V_BIKE)  # convert from kmph to m/sec.
    delta_e = get_delta_ke(v_i, v_i - DELTA_V)
    drag_forces = get_total_res(common.kmph(v_i), V_WIND, GRADE, G_FRAC, debug, get_rear_frac(G_FRAC), C_SF)
    delta_s = delta_e / drag_forces
    while (v_i > 1.0):      # repeat till velocity is 1 m/s
        v_f = v_i - DELTA_V
        v_a = (v_f + v_i) / 2.0     # average velocity
        delta_t = delta_s / (v_a)   # time interval
        drag_forces = get_total_res(common.kmph(v_f), V_WIND, GRADE, G_FRAC, debug, get_rear_frac(G_FRAC), C_SF)
        if (drag_forces < 0):
            return -1
        delta_ke = get_delta_ke(v_i, v_f) 
        # calculate delta pe using delta s, positive when gradient is uphill and negative for downhill
        delta_pe = TOTAL_MASS * G_ACCEL * (GRADE / 100.0) * v_a * delta_t
        #delta_pe = TOTAL_MASS * G_ACCEL * (GRADE / 100.0) * delta_s

        # calculate the drag forces as F * d_s = d_e, delta_ke will be negative when slowing down
        # d_e is the total energy lost 
        delta_e = delta_ke - delta_pe        
        delta_s = delta_e / drag_forces
        total_s = total_s + delta_s
        v_i = v_f
        if (debug):
            print ("TE: " + common.nice_s(delta_e)  + " KE: "          + common.nice_s(delta_ke) + \
                   " PE: " + common.nice_s(delta_pe) + " Drag Forces: " + common.nice_s(drag_forces) + \
                   " DS: " + common.nice_s(delta_s) + " DT: " + common.nice_s(delta_t))
       
    return total_s

#*-------------------------------------------------
#*-  return change in ke + re
#*-------------------------------------------------
def get_delta_ke(v_i, v_f):
     delta_ke = 0.5 * TOTAL_MASS * (v_i * v_i - v_f * v_f) 
     w_f = 2.0 * math.pi * (v_f / WHEEL_CIRCUM) # calculate delta re using w in radians
     w_i = 2.0 * math.pi * (v_i / WHEEL_CIRCUM)
     delta_re = 0.5 * WHEEL_MASS * WHEEL_RADIUS * WHEEL_RADIUS * (w_i * w_i - w_f * w_f)
     return (delta_ke + delta_re)

