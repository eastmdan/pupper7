from UDPComms import Publisher

import time
from enum import Enum

drive_pub = Publisher(8830)
arm_pub = Publisher(8410)


while True:
    drive_pub.send({'f':0,'t':0})
    time.sleep(1000)
    drive_pub.send({'f':20,'t':0})