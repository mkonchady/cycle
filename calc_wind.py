import math
import sys

# Wind Calculator
# Copyright (c) 2020 Manu Konchady
#
# calculate head wind from bike velocity headed in 0 degree, wind velocity from wind_d degrees
# wind_mag and wind_deg are the magnitude and direction of origin of the wind
# bike_mag and bike_deg are the magnitude and direction of the bicycle travel

#convert clockwise bearing (0 as N ) to counterclockwise degrees (0 as E)
def bearingToDegrees(bearing):
    return (450 - bearing) % 360

# convert counterclockwise degrees (0 as E) to clockwise bearing (0 as N )
def degreesToBearings(degrees):
    return (450 - degrees) % 360

# return the degree in the opposite direction
def flip_direction(angle):
    return (((angle + 360) - 180) % 360)

# get  the angle between two vectors in degress
def get_angle(v1_x, v1_y, v2_x, v2_y):
    angle = math.degrees(math.atan2(v2_y, v2_x) - math.atan2(v1_y, v1_x))
    return round(angle)

# get the dot product of two vectors
def get_dot_product(v1_x, v1_y, v2_x, v2_y):
    return v1_x * v2_x + v1_y * v2_y 

# get the magnitude of a vector
def get_magnitude(v_x, v_y):
    return math.sqrt(v_x * v_x + v_y * v_y)

#*---------------------------------------------------------------------------------------------
#   Calculate the relative wind velocity given bike and wind velocities.
#   v_app = v_wind - v_bike
#  Accept v_wind: wind mag, wind deg and v_bike: bike mag, and bike deg
#  degrees must be in x,y coordinate system, i.e. North 0 bearing is 90 degrees
#  1. v_wind is the velocity of wind originating at the bearing
#  2. v_bike is the velocity of bike heading in the direction of the bearing.
#
# compute v_app x and v_app_y components and the direction
# wind magnitude is from origin and therefore direction is flipped to represent a drag force
# bike magnitude is in the direction of flow and therefore direction is flipped
# positive direction is head wind and negative direction is tail wind
#*-----------------------------------------------------------------------------------------------
def get_apparent(wind_mag, wind_deg, bike_mag, bike_deg):
    wind_x = wind_mag * math.cos(math.radians(flip_direction(wind_deg)))
    bike_x = bike_mag * math.cos(math.radians(bike_deg))
    minus_bike_x = bike_mag * math.cos(math.radians(flip_direction(bike_deg)))

    wind_y = wind_mag * math.sin(math.radians(flip_direction(wind_deg)))
    bike_y = bike_mag * math.sin(math.radians(bike_deg))
    minus_bike_y = bike_mag * math.sin(math.radians(flip_direction(bike_deg)))

    apparent_y = wind_y + minus_bike_y
    apparent_x = wind_x + minus_bike_x

    angle = abs(get_angle(bike_x, bike_y, apparent_x, apparent_y))
    if (angle < 90):
        direction = -1  # tail wind
    elif  (angle == 90):
        direction = 0   # cross wind
    else:
        direction = 1   # head wind
    
    return apparent_x, apparent_y, direction

# the head wind is the apparent wind projected on the bike vector in m/s
def get_head_wind(bike_mag, wind_mag, wind_deg = 0, bike_deg = 0):
    apparent = get_apparent(wind_mag, wind_deg, bike_mag, bike_deg)
    apparent_x = apparent[0] 
    apparent_y = apparent[1]
    direction = apparent[2]

    bike_x = bike_mag * math.cos(math.radians(bike_deg))
    bike_y = bike_mag * math.sin(math.radians(bike_deg))
    
    dot_product = get_dot_product(apparent_x, apparent_y, bike_x, bike_y )
    mag = get_magnitude(bike_x, bike_y) 
    apparent_proj =  abs(dot_product / mag)

    return apparent_proj * direction

# return the head wind squared projected on the bike vector Wind factor (W_a) m^2 / s^2
def get_head_wind2(bike_mag, wind_mag, wind_deg = 0, bike_deg = 0):
    apparent = get_apparent(wind_mag, wind_deg, bike_mag, bike_deg)
    apparent_x = apparent[0]
    apparent_y = apparent[1]
    direction = apparent[2]

    bike_x = bike_mag * math.cos(math.radians(bike_deg))
    bike_y = bike_mag * math.sin(math.radians(bike_deg))
    dot_product = get_dot_product(apparent_x, apparent_y, bike_x, bike_y )
    mag = get_magnitude(bike_x, bike_y) 
    apparent_proj =  abs(dot_product / mag)
    angle = abs(get_angle(bike_x, bike_y, apparent_x, apparent_y))
    # square of projection and the angle
    apparent_proj2 = abs(apparent_proj * apparent_proj * math.cos(math.radians(angle)))
    return apparent_proj2 * direction

def test_cases():
    TOLERANCE = 0.5
    wind_mag = 8
    wind_deg = 0
    bike_mag = 6
    bike_deg = 0

    # Test 1
    head_wind = get_head_wind(bike_mag, wind_mag, wind_deg, bike_deg)
    expected = 14
    assert abs(head_wind - expected) <= TOLERANCE, "1: Expected vel: " + str(expected) + " " + str(head_wind)

    wind_deg = 180
    head_wind = get_head_wind(bike_mag, wind_mag, wind_deg, bike_deg)
    expected = -2
    assert abs(head_wind - expected) <= TOLERANCE, "2: Expected vel: " + str(expected) + " " + str(head_wind)

    wind_deg = 220
    bike_deg = 170
    head_wind = get_head_wind(bike_mag, wind_mag, wind_deg, bike_deg)
    expected = 11.14
    assert abs(head_wind - expected) <= TOLERANCE, "3: Expected vel: " + str(expected) + " " + str(head_wind)

    wind_deg = 10
    bike_deg = 190
    head_wind = get_head_wind(bike_mag, wind_mag, wind_deg, bike_deg)
    expected = -1.94
    assert abs(head_wind - expected) <= TOLERANCE, "4: Expected vel: " + str(expected) + " " + str(head_wind)
        
test_cases()
