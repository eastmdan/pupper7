# Make the pupper turn around with no lateral movement

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

# FOR REFRENCE
# hardware_interface.set_actuator_position(degrees_to_radians(position, axis (joint), leg_index)
# leg index(0-3) FR, FL, BR, BL
# axis(0-2) Hip, Thigh, Calf

# Concept, move each leg side in opposite directions

