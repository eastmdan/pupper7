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

# hardware_interface.set_actuator_position(degrees_to_radians(position, axis (joint), leg_index)
# leg index(0-3) FR, FL, BR, BL
# axis(0-2) Hip, Thigh, Calf

# Testing a move
move = 20

for x in range(5):
    time.sleep(0.5)
# full tilt
    hardware_interface.set_actuator_position(degrees_to_radians(15), 0, 0) # FR 0. Servo deg swapped on side
    hardware_interface.set_actuator_position(degrees_to_radians(15), 0, 1) # FL 1
    hardware_interface.set_actuator_position(degrees_to_radians(15), 0, 2) # BR 2
    hardware_interface.set_actuator_position(degrees_to_radians(15), 0, 3) # BL 3
    time.sleep(0.1)

# FR set
    hardware_interface.set_actuator_position(degrees_to_radians(55), 1, 0) # tuck in
    time.sleep(0.09)
    hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 0) # tilt back
    hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 0) # plant leg


# BL set
    hardware_interface.set_actuator_position(degrees_to_radians(90), 1, 3) # tuck in
    time.sleep(0.1)
    hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 3) # tilt back
    hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 3) # plant leg

    time.sleep(0.1)

# BR set
    hardware_interface.set_actuator_position(degrees_to_radians(90), 1, 2) # tuck in
    time.sleep(0.1)
    hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 2) # tilt back
    hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 2) # plant leg


# FL set
    hardware_interface.set_actuator_position(degrees_to_radians(90), 1, 1) # tuck in
    time.sleep(0.1)
    hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 1) # tilt back
    hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 1) # plant leg


# Reset legs
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
            time.sleep(0.25)
