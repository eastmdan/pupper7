#!/usr/bin/env python3

import os
import sys
import time

# This is a script that will allow you to move each indidual servo!
# With this you will be able to make custom movements.
# below is an example of how might you use this, build on it if you think it is helpful
# What you need to change is the pwm# value which matches each servo
# pwm1 = J15 connection on the board
# pwm 2 = J14...... pwm16 = J1
# ranges:  0 degree(echo 500000), 90 degree(echo 1500000), 180 degree(echo 2500000)

# 12 Leg servos, 3 per leg for each range of motion.
# Per Leg group 1 = hip, 2 = thigh, 3 = calf

# The following test was done plugging in an extra servo to J15

zero = 500000 # zero degrees has a value of 500K. Maybe find a calculator degrees to values
ninety = 1500000
one_eight = 2500000 
total_degrees = 180
mid_degrees = 90

total_pwm_change_first_half = ninety - zero
total_pwm_change_second_half = one_eight - zero


pwm_per_degree_first_half = total_pwm_change_first_half/mid_degrees
pwm_per_degree_second_half = total_pwm_change_second_half/total_degrees

# move_servo15 is just the name of the function. It does not move servo number 15
def move_servo15():
    global zero
    what_degree = 90
    # if what_degree <= 90:
    #       degree_finder = zero + (pwm_per_degree_first_half * what_degree)
    # else:
    #      degree_finder = zero + (pwm_per_degree_second_half * what_degree)

    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    degree_finder2 = int(-1*((one_eight - zero) / (180 - 0))*(what_degree) + one_eight)

    #os.system("echo " + str(degree_finder2) + " > /sys/class/pwm/pwmchip0/pwm7/duty_cycle")
    #os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm4/duty_cycle")
    time.sleep(1)
    # os.system("echo 2000000 > /sys/class/pwm/pwmchip0/pwm12/duty_cycle") # 135 degrees = 2Mil. Suspected robot range is 45 to 135
    # time.sleep(1)
    # os.system("echo 1500000 > /sys/class/pwm/pwmchip0/pwm12/duty_cycle")

    print("done")
    print(degree_finder)

def stand():
    
    time.sleep(1)
    for x in range(12):
        os.system("echo 1500000 > /sys/class/pwm/pwmchip0/pwm" + str(x+4) + "/duty_cycle")
        #time.sleep(0.2)
    time.sleep(3)


def main():
    os.system("sudo systemctl stop robot")
    stand()
    time.sleep(2)
    move_servo15()

if __name__ == "__main__":
    main()