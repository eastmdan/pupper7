from MangDang.mini_pupper.HardwareInterface import HardwareInterface
import numpy as np
import time

def run_square():

    hardware_interface = HardwareInterface()

    #set_point = -80
    #axis = 2
    #leg_index = 2

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

    #hardware_interface.set_actuator_position(
    #    degrees_to_radians(set_point),
    #    axis,
    #    leg_index,
    #)

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

