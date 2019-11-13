import math
import sys
import calc_wind

# Power Calculator
# Copyright (c) 2020 Manu Konchady
#
# Tested with bikecalculator.com
#

# calculate the power from aero resistance, grade resistance, and rolling resistance
# velocities in kmph. 
EFFICIENCY = 0.95

def calc_air_res(K_A, v_bike, v_wind, wind_d):
    v_bike = v_bike * 0.277778  # convert to m/sec
    v_wind = v_wind * 0.277778
    return K_A * calc_wind.get_head_wind2(v_bike, v_wind, wind_d, 0) 

def calc_power(total_res, v_bike):
    power = (v_bike *  0.277778 * total_res) / EFFICIENCY
    return power

def test_cases():
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
    power = math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE))
    assert abs(power - expected) <= TOLERANCE, "1: Expected " + str(power)

    # Test 2
    expected = 64
    V_BIKE = 20
    AIR_RES = calc_air_res(K_A, V_BIKE, V_WIND, V_DEG)
    power = math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE))
    assert abs(power - expected) <= TOLERANCE, "2: Expected " + str(power)

    # Test 3
    expected = 15
    V_BIKE = 10
    C_D_AREA = 0.233
    K_A = 0.5 * C_D_AREA * DENSITY 
    AIR_RES = calc_air_res(K_A, V_BIKE, V_WIND, V_DEG)
    power = math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE))
    assert abs(power - expected) <= TOLERANCE, "3: Expected " + str(power)

    # Test 4
    expected = 48
    V_BIKE = 20
    AIR_RES = calc_air_res(K_A, V_BIKE, V_WIND, V_DEG)
    power = math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE))
    assert abs(power - expected) <= TOLERANCE, "4: Expected " + str(power)

    # Test 5
    expected = 80
    ROLL_V = 0.012
    ROLLING_RES = ROLL_V * TOTAL_WT
    power = math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE))
    assert abs(power - expected) <= TOLERANCE, "5: Expected " + str(power)

    # Test 6
    expected = 99
    V_BIKE = 24.0
    ROLLING_RES = 0.005 * TOTAL_WT
    GRADE_RES = 0.0
    K_A = 0.5 * 0.388 * DENSITY
    AIR_RES = calc_air_res(K_A, V_BIKE, 0, 0)
    power = math.ceil(calc_power(GRADE_RES + ROLLING_RES + AIR_RES, V_BIKE))
    assert abs(power - expected) <= TOLERANCE, "6: Expected " + str(power)

test_cases()