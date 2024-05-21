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

# hardware_interface.set_actuator_position(position (in rads?), axis, leg_index)


# Testing a move

# full tilt
hardware_interface.set_actuator_position(degrees_to_radians(-10), 0, 0) # FR 0. Servo deg swapped on side
hardware_interface.set_actuator_position(degrees_to_radians(10), 0, 1) # FL 1
hardware_interface.set_actuator_position(degrees_to_radians(-10), 0, 2) # BR 2
hardware_interface.set_actuator_position(degrees_to_radians(10), 0, 3) # BL 3


