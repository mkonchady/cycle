# calculate moments around locations of a bicycle
#
#  Point 1: Over front wheel at COM height
#  Point 2: Over rear wheel at COM height
#
#  Bicycle front wheel to the left and rear wheel to the right
#
g = 9.81    # meters per second

#*-----------------------------------------------------------------
#*-  accepts wheel base, rear crank distance, height to center of
#*-  mass from ground, mass, and brake g (as a fraction). All distances in meters
#*-  Using the moments around the com point above the front wheel
#*-----------------------------------------------------------------
def get_normal_forces_1(wheel_base, rear_crank_distance, com_height, mass, brake_g):
    mg = mass * g
    f_b = brake_g * mg # braking force

    # moment around front wheel at com height when braking
    anti_clock_wise_torque = mg * (wheel_base - rear_crank_distance)
    clock_wise_torque = f_b * com_height
    f_nr = (anti_clock_wise_torque - clock_wise_torque) / wheel_base
    f_nf = mg - f_nr

    # return both forces
    return f_nf, f_nr

#*-----------------------------------------------------------------
#*-  accepts wheel base, rear crank distance, height to center of
#*-  mass from ground, mass, and brake g (as a fraction). All distances in meters
#*-  Using the moments around the com point above the rear wheel
#*-  brake_f and brake_r are in a fraction of g
#*-----------------------------------------------------------------
def get_normal_forces_2(wheel_base, rear_crank_distance, com_height, mass, brake_g):
    mg = mass * g
    f_b = brake_g * mg # braking force

    # moment around rear wheel at com height when braking
    clock_wise_torque = mg * rear_crank_distance + f_b * com_height
    f_nf = clock_wise_torque / wheel_base
    f_nr = mg - f_nf

    # return both forces
    return f_nf, f_nr

#*---------------------------------------------------------------------------------
#*- get the normal forces using the com
#*---------------------------------------------------------------------------------
def get_normal_forces_3(wheel_base, rear_crank_distance, com_height, mass, brake_g):
    mg = mass * g
    f_b = brake_g * mg # braking force
    wt_transfer_front = (com_height / wheel_base) * f_b

    f_nr = mg * (wheel_base - rear_crank_distance) / wheel_base
    f_nf = mg * (rear_crank_distance / wheel_base)

    f_nf = f_nf + wt_transfer_front
    f_nr = f_nr - wt_transfer_front

    # return both forces
    return f_nf, f_nr

#*-----------------------------------------------------------------
#*-  accepts wheel base, rear crank distance, height to center of
#*-  mass from ground, and mass. All distances in meters
#*-  returns the brake g at which the rear wheel looses contact using
#*-  moments around point 1
#*-----------------------------------------------------------------
def get_critical_g_1(wheel_base, rear_crank_distance, com_height, mass):
    for brakes in range (0, 100):
        brake_g = brakes / 100.0     
        f_nf, f_nr = get_normal_forces_1(wheel_base, rear_crank_distance, com_height, mass, brake_g)
        if (f_nr < 0):
            return brake_g
    return 0

#*-----------------------------------------------------------------
#*-  accepts wheel base, rear crank distance, height to center of
#*-  mass from ground, and mass. All distances in meters
#*-  returns the brake g at which the rear wheel looses contact using
#*-  moments around point 2
#*-----------------------------------------------------------------
def get_critical_g_2(wheel_base, rear_crank_distance, com_height, mass):
    for brakes in range (0, 100):
        brake_g = brakes / 100.0     
        f_nf, f_nr = get_normal_forces_2(wheel_base, rear_crank_distance, com_height, mass, brake_g)
        if (f_nr < 0):
            return brake_g
    return 0

#*-----------------------------------------------------------------
#*-  accepts wheel base, rear crank distance, height to center of
#*-  mass from ground, and mass. All distances in meters
#*-  returns the brake g at which the rear wheel looses contact using
#*-  moments around com
#*-----------------------------------------------------------------
def get_critical_g_3(wheel_base, rear_crank_distance, com_height, mass):
    for brakes in range (0, 100):
        brake_g = brakes / 100.0     
        f_nf, f_nr = get_normal_forces_3(wheel_base, rear_crank_distance, com_height, mass, brake_g)
        if (f_nr < 0):
            return brake_g
    return 0

#*------------------------------------------------------------------------
#*-  accepts wheel base, rear crank distance, height to center of
#*-  mass from ground, and mass. All distances in meters
#*-  returns the max. g from rear brake alone with moments around point 2
#*------------------------------------------------------------------------
def get_max_rear_g (wheel_base, rear_crank_distance, com_height, mass, mu):
        mg = mass * g
        anti_clock_wise_torque = mg * (wheel_base - rear_crank_distance)
        clock_wise_torque = (wheel_base + mu * com_height) # * f_nr
        f_nr = anti_clock_wise_torque / clock_wise_torque
        #print (f_nr, mg, clock_wise_torque, anti_clock_wise_torque)
        return (mu * f_nr / mg)

#*------------------------------------------------------------------------
#*-  accepts wheel base, rear crank distance, height to center of
#*-  mass from ground, and mass. All distances in meters
#*-  returns the max. g from front brake alone with moments around point 1
#*------------------------------------------------------------------------
def get_max_front_g (wheel_base, rear_crank_distance, com_height, mass, mu):
        mg = mass * g
        clock_wise_torque = mg * rear_crank_distance + mu * com_height  # * f_nf
        anti_clock_wise_torque =  wheel_base  # * f_nf
        f_nf =  mg * rear_crank_distance/ (wheel_base - mu * com_height)
        #print (f_nf, mg, clock_wise_torque, anti_clock_wise_torque)
        return (mu * f_nf / mg)

