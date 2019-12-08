#
# Coast Down Test for a Bicycle
# Copyright (c) 2020 Manu Konchady
#
# calculate the best c_r for a coast down time and velocity
#
# Fixed parameters
#
import sys

M = 85.0 # kgs.
g = 9.81
K_A = 0.3   # commuter 

V_INITIAL = 20.0 * 0.27778  # initial velocity m / sec.
V_FINAL = 5.0 * 0.27778     # final velocity m / sec.
V_HEAD = 5.0 * 0.27778      # head wind m. sec
DURATION = 20.0             # coast down from from v_initial to v_final in seconds

# get the time for velocity to reduce from V_INITIAL to V_FINAL 
# using the passed value of c_r
def get_time(c_r):
    v_next = V_INITIAL 
    time = 0.0
    delta_t = 0.1
    while (time < DURATION):
        v_current = v_next
        v = v_current + V_HEAD
        f_drag = -(K_A * v * v + M * g * c_r)
        delta_v = delta_t * f_drag / M
        v_next = v_current + delta_v
        time = time + delta_t
        diff_velocity = v_next - V_FINAL
        if (diff_velocity < 0.1):
            return time
    return -1

# Main section
# Try a range of values for c_r
# If none found, return a message
for i in range (15):
    c_r = i / 1000.0
    estimated_time = get_time(c_r)
    if abs(estimated_time - DURATION) < 1.0:
        print ("Best c_r = " + str(c_r))
        sys.exit()
print ("Could not find a c_r")
