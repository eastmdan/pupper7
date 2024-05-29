# New version of strafe

from MangDang.mini_pupper.HardwareInterface import HardwareInterface
import numpy as np
import time

hardware_interface = HardwareInterface()

def degrees_to_radians(input_array):
    """Converts degrees to radians.

    Parameters
    ----------
    input_array :  Numpy array or float
        Degrees

    Returns
    -------
    Numpy array or float
        Radians
    """
    return input_array * np.pi / 180.0

# Base version

# for leg_index in range(4):
#         for axis in range(3):
#             if axis == 0:
#                 set_point = 0
#             elif axis == 1:
#                 set_point = 45
#             elif axis == 2:
#                 set_point = -45
#             hardware_interface.set_actuator_position(
#                 degrees_to_radians(set_point),
#                 axis,
#                 leg_index,
#             )
#             time.sleep(1)

# hardware_interface.set_actuator_position(degrees_to_radians(position), axis (joint), leg_index)
# leg index(0-3) FR, FL, BR, BL
# axis(0-2) Hip, Thigh, Calf

# Testing a move

# Change this to move opposite legs at the same time. Think how bipedal side movement works.


hardware_interface.set_actuator_position(degrees_to_radians(25), 1, 0) # Push (remember 0 extends)
hardware_interface.set_actuator_position(degrees_to_radians(25), 1, 3)
hardware_interface.set_actuator_position(degrees_to_radians(65), 1, 1) # Pull in reciever legs
hardware_interface.set_actuator_position(degrees_to_radians(65), 1, 2)
hardware_interface.set_actuator_position(degrees_to_radians(20), 0, 0) # Tilt
hardware_interface.set_actuator_position(degrees_to_radians(20), 0, 3)
hardware_interface.set_actuator_position(degrees_to_radians(-20), 0, 1) # Tilt reciever legs
hardware_interface.set_actuator_position(degrees_to_radians(-20), 0, 2)
time.sleep(0.19)
hardware_interface.set_actuator_position(degrees_to_radians(20), 1, 1) # Push reciever legs
hardware_interface.set_actuator_position(degrees_to_radians(20), 1, 2)
hardware_interface.set_actuator_position(degrees_to_radians(60), 1, 0) # Pull driver legs
hardware_interface.set_actuator_position(degrees_to_radians(60), 1, 3)
hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 1) # Tilt reciever legs back
hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 2)
time.sleep(0.1)
hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 0) # Tilt2flat
hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 3)
time.sleep(0.09)
hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 0) # push2flat
hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 3)

# MODIFIED FROM NANO. PAIN. This is for the other legs. (MOVE LEFT)

time.sleep(2)

hardware_interface.set_actuator_position(degrees_to_radians(25), 1, 1) # Push (remember 0 extends)
hardware_interface.set_actuator_position(degrees_to_radians(25), 1, 2)
hardware_interface.set_actuator_position(degrees_to_radians(-20), 0, 1) # Tilt
hardware_interface.set_actuator_position(degrees_to_radians(-20), 0, 2)
time.sleep(0.2)
hardware_interface.set_actuator_position(degrees_to_radians(60), 1, 1) # Pull
hardware_interface.set_actuator_position(degrees_to_radians(60), 1, 2)
time.sleep(0.1)
hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 1) # Tilt2flat
hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 2)
time.sleep(0.09)
hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 1) # push2flat
hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 2)


# # reverse the motion
# hardware_interface.set_actuator_position(degrees_to_radians(0, 0, 0))
# hardware_interface.set_actuator_position(degrees_to_radians(0, 0, 3))
# time.sleep(0.1)
# hardware_interface.set_actuator_position(degrees_to_radians(45, 1, 0))
# hardware_interface.set_actuator_position(degrees_to_radians(45, 1, 3))

# # FLBR
# hardware_interface.set_actuator_position(degrees_to_radians(10, 0, 1)) # FL # Hip
# hardware_interface.set_actuator_position(degrees_to_radians(10, 0, 2)) # BR
# time.sleep(0.1)
# hardware_interface.set_actuator_position(degrees_to_radians(30, 1, 1)) # Thigh
# hardware_interface.set_actuator_position(degrees_to_radians(30, 1, 2))

# time.sleep(0.25)
# # reverse the motion
# hardware_interface.set_actuator_position(degrees_to_radians(0, 0, 1))
# hardware_interface.set_actuator_position(degrees_to_radians(0, 0, 2))
# time.sleep(0.1)
# hardware_interface.set_actuator_position(degrees_to_radians(45, 1, 1))
# hardware_interface.set_actuator_position(degrees_to_radians(45, 1, 2))

for leg_index in range(4):
        for axis in range(3):
            if axis == 0:
                set_point = 0
            elif axis == 1:
                set_point = 45
            elif axis == 2:
                set_point = -45
            hardware_interface.set_actuator_position(
                degrees_to_radians(set_point),
                axis,
                leg_index,
            )
            time.sleep(0.4)
