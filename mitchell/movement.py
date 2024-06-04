from UDPComms import Publisher

import time
from enum import Enum

drive_pub = Publisher(8830)
arm_pub = Publisher(8410)


MODES = Enum('MODES', 'SAFE DRIVE ARM')

mode = MODES.DRIVE


while True:
    if mode == MODES.DRIVE:
        slow = 150
        fast = 500

        max_speed = (fast+slow)/2 + 1*(fast-slow)/2

        out = {'f':(max_speed*forward),'t':-150*twist}
        drive_pub.send(out)
            
        drive_pub.send({'f':0,'t':0})
        time.sleep(1000)
        drive_pub.send({'f':20,'t':0})
        time.sleep(1000)