import math
import sys
import calc_wind

# Velocity Calculator from Power and Bike Parameters
# Copyright (c) 2020 Manu Konchady
#
# Tested with bikecalculator.com
#

# calculate the bike velocity given power, A, head wind (m / sec), and sum of other resistance
def calc_velocity(K_A, wind_mag, wind_deg, other_resistance, power, bike_deg = 0):
    bike_mag = 1000 
    MAX_ITERATIONS = 100
    TOLERANCE = 0.05
    if (wind_mag > 28):
        TOLERANCE = 0.02 * wind_mag
    for _ in range(0, MAX_ITERATIONS):
        W_A = calc_wind.get_head_wind2(bike_mag, wind_mag, wind_deg, bike_deg)
        head_mag = calc_wind.get_head_wind(bike_mag, wind_mag, wind_deg, bike_deg)
        if (W_A < 0):
            K_A = -K_A
        f = bike_mag * (K_A * W_A + other_resistance) - 0.95 * power
        fprime = K_A * (3.0 * bike_mag + wind_mag) * head_mag + other_resistance
        new_bike_mag = bike_mag - (f / fprime)
        if (abs(new_bike_mag - bike_mag) < TOLERANCE):
            return new_bike_mag
        bike_mag = new_bike_mag
    return 0.0

#*--- MAIN SECTION
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

    # Test 2a:
    V_WIND = 10 # kmph.
    V_DEG = 0
    velocity = calc_velocity(K_A, V_WIND * 0.27778, V_DEG, GRADE_RES + ROLLING_RES, power) * 3.6
    expected = 18.6
    assert abs(math.ceil(velocity) - expected) <= TOLERANCE, "3: Expected vel: " + str(expected) 

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
    assert abs(math.ceil(velocity) - expected) <= TOLERANCE, "4: Expected vel: " + str(expected) 

    # Test 5:
    ROLL_V = 0.012
    ROLLING_RES = ROLL_V * TOTAL_WT
    velocity = calc_velocity(K_A, V_WIND * 0.27778, V_DEG, GRADE_RES + ROLLING_RES, power) * 3.6
    expected = 16
    assert abs(math.ceil(velocity) - expected) <= TOLERANCE, "5: Expected vel: " + str(expected) 

    # Test 6:
    GRADE_V = 0.07
    GRADE_RES = GRADE_V * TOTAL_WT
    velocity = calc_velocity(K_A, V_WIND * 0.27778, V_DEG, GRADE_RES + ROLLING_RES, power) * 3.6
    expected = 5
    assert abs(math.ceil(velocity) - expected) <= TOLERANCE, "6: Expected vel: " + str(expected) 

test_cases()