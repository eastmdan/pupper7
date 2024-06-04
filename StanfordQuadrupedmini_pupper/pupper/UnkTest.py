#
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



# Legs can be split between drive and follow


# Single leg motion from cold rest for Driver

# Push, tilt, pull, tilt2flat, push2flat

# hardware_interface.set_actuator_position(degrees_to_radians(25), 1, 0) # Push (remember 0 extends)
# hardware_interface.set_actuator_position(degrees_to_radians(10), 0, 0) # Tilt
# hardware_interface.set_actuator_position(degrees_to_radians(60), 1, 0) # Pull
# hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 0) # Tilt2flat
# hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 0) # push2flat

# # Single leg motion for follow. It starts after the driver

# # tilt, push, tilt2flat, pull2flat

# hardware_interface.set_actuator_position(degrees_to_radians(-10), 0, 1) # tilt away to make the step
# hardware_interface.set_actuator_position(degrees_to_radians(35), 1, 1) # push out to connect to ground
# hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 1) # tilt the body back to center
# hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 1) # pull back to level

# all together now!

# Driver pushes out to move the robot, then returns to center when the follower "locks in"
hardware_interface.set_actuator_position(degrees_to_radians(25), 1, 0) # Push (remember 0 extends)
hardware_interface.set_actuator_position(degrees_to_radians(10), 0, 0) # Tilt
time.sleep(0.2)
hardware_interface.set_actuator_position(degrees_to_radians(60), 1, 0) # Pull
time.sleep(0.1)
hardware_interface.set_actuator_position(degrees_to_radians(0), 0, 0) # tilt2center
time.sleep(0.09)
hardware_interface.set_actuator_position(degrees_to_radians(45), 1, 0) # push2center
time.sleep(0.1)