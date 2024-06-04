from UDPComms import Publisher

import time
from enum import Enum

drive_pub = Publisher(8830)
arm_pub = Publisher(8410)


MODES = Enum('MODES', 'SAFE DRIVE ARM')

mode = MODES.DRIVE

l_trigger = 100
forward = 100
twist = 100

while True:
    if mode == MODES.DRIVE:
        forward_left  = 100
        forward_right = 100
        twist = 0

        on_right = 0
        on_left = 0
        l_trigger = 0

        if on_left or on_right:
            if on_right:
                forward = forward_right
            else:
                forward = forward_left

            slow = 150
            fast = 500

            max_speed = (fast+slow)/2 + l_trigger*(fast-slow)/2

            out = {'f':(max_speed*forward),'t':-150*twist}
            drive_pub.send(out)
            print(out)
        else:
            drive_pub.send({'f':0,'t':0}