import math
import sys

# Altitude, Pressure and Air Density Calculators
# 

# Constants
ALT_DENSITY_POWER = 1.0 / 5.257
PRESSURE_SEA = 1013.25 # pressure in hecto pascals at sea level
LARGE_NEGATIVE = -10000000
TOLERANCE = 0.1

RD = 287.058 # Rd is the specific gas constant for dry air equal to 287.058 J/(kg·K)
RV = 461.495 # Rv is the specific gas constant for water vapor equal to 461.495 J/(kg·K)

DEW_A =17.62
DEW_B =243.12 # in centigrade

# return the altitude for a given pressure 
def get_altitude (pressure, temp):
    kelvin = temp + 273.15
    pval = math.pow((PRESSURE_SEA / pressure), ALT_DENSITY_POWER) - 1.0
    return (pval * kelvin) / 0.0065

def test_pressure():
    # Test 1
    expected = 0
    p = 1013.25
    assert abs(get_altitude(p, 25) - expected) < TOLERANCE, "1: Alt. did not match expected value of " + str(expected)
    
    # Test 2
    expected = 1045.91
    p = 900
    assert abs(get_altitude(p, 25) - expected) < TOLERANCE, "2: Alt. did not match expected value of " + str(expected)

    # Test 3
    expected = 975.8
    p = 900
    assert abs(get_altitude(p, 5) - expected) < TOLERANCE, "3: Alt. did not match expected value of " + str(expected)

    # Test 4
    expected = 2610.94
    p = 750
    assert abs(get_altitude(p, 15) - expected) < TOLERANCE, "4: Alt. did not match expected value of " + str(expected)

# return the pressure for a given altitude and temperature using the hypsometric formula
def get_pressure (alt, temp):
    kelvin = temp + 273.15
    lhs = 1.0 + (alt * 0.0065) / kelvin
    return PRESSURE_SEA /  math.pow(lhs, (1.0 / ALT_DENSITY_POWER))

# get the density using teten's formula
# alt is in meters, temp in cent. and relative humidity is a percentage
def get_density1(alt, temp, rh, pressure = LARGE_NEGATIVE):
    kelvin = temp + 273.15
    if (pressure == LARGE_NEGATIVE):
        pressure = get_pressure(alt, temp)
    
    if (temp >= 0):
        saturated_pressure = 0.61078 * math.exp( (17.270 * temp) / (temp + 237.3) )
    else:
        saturated_pressure = 0.61078 * math.exp( (21.875 * temp) / (temp + 265.5) )
    actual_pressure = rh * saturated_pressure 
    return (0.0034848 / kelvin) * (pressure * 100 - 0.0037960 * actual_pressure)


# get the dew point
# https://www.omnicalculator.com/physics/dew-point
# temp in centigrade and rh in perent
def alpha(temp, rh):
    p1 = math.log(rh / 100.0)
    p2 = (DEW_A * temp) / (DEW_B + temp)
    return p1 + p2
def get_dew_point(temp, rh):
    return (DEW_B * alpha(temp,rh)) / (DEW_A - alpha(temp,rh))
    
def test_dew_point():
    # test 1
    expected = -32.019
    temp = -5 # centigrade
    rh = 10 # humidity percentage
    assert abs(get_dew_point(temp, rh) - expected) < TOLERANCE, "1: Did not match expected value of " + str(expected)

    # test 2
    expected = -24.197
    temp = 5
    assert abs(get_dew_point(temp, rh) - expected) < TOLERANCE, "2: Did not match expected value of " + str(expected)

    # test 3
    expected = -7.50
    rh = 40
    assert abs(get_dew_point(temp, rh) - expected) < TOLERANCE, "3: Did not match expected value of " + str(expected)

    # test 4
    expected = 1.49
    temp = 15
    assert abs(get_dew_point(temp, rh) - expected) < TOLERANCE, "4: Did not match expected value of " + str(expected)

    # test 5
    expected = 11.57
    rh = 80
    assert abs(get_dew_point(temp, rh) - expected) < TOLERANCE, "4: Did not match expected value of " + str(expected)

    # test 6
    expected = 21.30
    temp = 25
    assert abs(get_dew_point(temp, rh) - expected) < TOLERANCE, "5: Did not match expected value of " + str(expected)    

# get the density 
# https://www.omnicalculator.com/physics/air-density#air-density-definition-what-is-the-density-of-air-formula
# alt is in meters, temp in cent. and relative humidity is a percentage
def get_density(alt, temp, rh, pressure = LARGE_NEGATIVE):
    kelvin = temp + 273.15

    # compute a pressure if not given
    if (pressure == LARGE_NEGATIVE):
        pressure = get_pressure(alt, temp)

    # get the dew point
    dew_point = get_dew_point(temp, rh)
    pval = (7.5 * dew_point) / (237.3 + dew_point)

    # get the saturated and actual pressure
    saturated_pressure = 6.1078 * math.pow(10, pval)
    actual_pressure = saturated_pressure * (rh / 100.0)    
    dry_pressure = (pressure - actual_pressure) * 100.0  # convert to pascals from hectopascals 
    actual_pressure = actual_pressure * 100.0

    return (dry_pressure / (RD * kelvin)) + (actual_pressure / (RV * kelvin))

def test_density():
    # Test 1
    expected = 1.048
    temp = 25 # centigrade
    rh = 50 # humidity percentage
    pressure = 900 # in mbar
    alt = 0 # altitude in meters
    assert abs(get_density(alt, temp, rh, pressure) - expected) < TOLERANCE, "1: Did not match expected value of " + str(expected)

    # Test 1a
    expected = 1.165
    pressure = 1000.0 # in mbar
    assert abs(get_density(alt, temp, rh, pressure) - expected) < TOLERANCE, "1a: Did not match expected value of " + str(expected)

    # Test 1b
    expected = 1.28
    pressure = 1100.0 # in mbar
    assert abs(get_density(alt, temp, rh, pressure) - expected) < TOLERANCE, "1b: Did not match expected value of " + str(expected)

    # Test 1c
    expected = 1.43
    temp = -5
    assert abs(get_density(alt, temp, rh, pressure) - expected) < TOLERANCE, "1c: Did not match expected value of " + str(expected)

    # Test 1d
    expected = 1.237
    temp = 35
    assert abs(get_density(alt, temp, rh, pressure) - expected) < TOLERANCE, "1c: Did not match expected value of " + str(expected)

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

# Main

#test_dew_point()
#test_pressure()
#test_density()
