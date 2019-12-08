# 
# Spoke length Calculator
# Copyright (c) 2020 Manu Konchady
#
# Tested with http://www.sapim.be/spoke-calculator
#
# All parameters in mm.

import math

total_hub_length = 120
non_gear_side_hub_length = 16
gear_side_hub_length = 30
non_gear_side_hub_diameter = 16
gear_side_hub_diameter = 16
internal_rim_diameter = 622
rim_thickness = 5
num_spokes = 32
non_gear_side_crossings = 0
gear_side_crossings = 0

non_gear_length = (total_hub_length / 2) - non_gear_side_hub_length;
non_gear_temp = (    math.pow(internal_rim_diameter / 2, 2) + 
                            math.pow(non_gear_side_hub_diameter / 2, 2) +
							math.pow(non_gear_length, 2) ) - \
							(internal_rim_diameter * (non_gear_side_hub_diameter / 2) * 
                            (math.cos(math.radians( ( 720 * non_gear_side_crossings) / num_spokes))))
spoke_length = round(math.sqrt(non_gear_temp)) + rim_thickness
print ("Non-gear side length: " + str(spoke_length))


gear = (total_hub_length / 2) - gear_side_hub_length;
gear_temp = (    math.pow(internal_rim_diameter / 2, 2) + 
                            math.pow(gear_side_hub_diameter / 2, 2) +
							math.pow(gear, 2) ) - \
							(internal_rim_diameter * (gear_side_hub_diameter / 2) * 
                            (math.cos(math.radians( ( 720 * gear_side_crossings) / num_spokes))))
spoke_length = round(math.sqrt(gear_temp)) + rim_thickness
print ("Gear side length: " + str(spoke_length))
