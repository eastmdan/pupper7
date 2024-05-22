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

# FR, BL move first

def FRBL(): # HIP and calf at same time
    hardware_interface.set_actuator_position(degrees_to_radians(-10, 0, 0)) # FR # Hip
    hardware_interface.set_actuator_position(degrees_to_radians(10, 0, 3)) # BL
    time.sleep(0.1)
    hardware_interface.set_actuator_position(degrees_to_radians(30, 2, 0)) # Calf
    hardware_interface.set_actuator_position(degrees_to_radians(30, 2, 3))

    time.sleep(0.8)
    # reverse the motion
    hardware_interface.set_actuator_position(degrees_to_radians(0, 0, 0))
    hardware_interface.set_actuator_position(degrees_to_radians(0, 0, 3))
    time.sleep(0.1)
    hardware_interface.set_actuator_position(degrees_to_radians(45, 2, 0))
    hardware_interface.set_actuator_position(degrees_to_radians(45, 2, 3))

def FLBR(): # HIP and calf at same time
    hardware_interface.set_actuator_position(degrees_to_radians(10, 0, 1)) # FL # Hip
    hardware_interface.set_actuator_position(degrees_to_radians(-10, 0, 2)) # BR
    time.sleep(0.1)
    hardware_interface.set_actuator_position(degrees_to_radians(30, 2, 1)) # Calf
    hardware_interface.set_actuator_position(degrees_to_radians(30, 2, 2))

    time.sleep(0.8)
    # reverse the motion
    hardware_interface.set_actuator_position(degrees_to_radians(0, 0, 1))
    hardware_interface.set_actuator_position(degrees_to_radians(0, 0, 2))
    time.sleep(0.1)
    hardware_interface.set_actuator_position(degrees_to_radians(45, 2, 1))
    hardware_interface.set_actuator_position(degrees_to_radians(45, 2, 2))

def main():
    FRBL
    time.sleep(0.5)
    FLBR

if __name__ == "__main__":
    main()