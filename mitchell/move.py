from UDPComms import Publisher
from PS4Joystick import Joystick

import time
from enum import Enum

drive_pub = Publisher(8830)
arm_pub = Publisher(8410)


while True:
    forward = - 15
    twist = 0

    slow = 150
    fast = 500

    max_speed = (fast+slow)/2 + 1*(fast-slow)/2

    out = {'f':(max_speed*forward),'t':-150*twist}
    drive_pub.send(out)
    print(out)
    
    time.sleep(0.1)
