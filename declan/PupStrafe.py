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

# INDIV ARTIFACT: Run a command that allows the pupper to move in a strafe.

# Concepts: Tilt all hips one way then slowly pitch them over

# Assume this is a move to the RIGHT

# FRH out -10
# FLH in 10
# BRH out -10
# BLH in 10. Tilts all right

# FRT in 90
# FRH 0
# FRT 45. Straighten front right

# BLT in 90
# BLH 0
# BLT 45. Straighten back left

# BRT in 90
# BRH 0
# BRT 45. Straighten back right

# FLT in 90
# FLH 0
# FLT 45. Straighten front left.

# In theory this should be everything needed


# Initial HIP TILT
def move_servo1(): # assume FRH
    global zero
    what_degree = -10 # Tilt hip
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo2(): # FLH
    global zero
    what_degree = 10
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo3(): # BRH
    global zero
    what_degree = -10
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo4(): # BLH
    global zero
    what_degree = 10
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")

# INDIV LEG MOVES

# FR stable
def move_servo5(): # FRT
    global zero
    what_degree = -90
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo6(): # FRH
    global zero
    what_degree = 0
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo7(): # FRT
    global zero
    what_degree = 0
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")

# BL Stable
def move_servo8(): # BLT
    global zero
    what_degree = -90
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo9(): # BLH
    global zero
    what_degree = 0
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo10(): # BLT
    global zero
    what_degree = 0
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")

# BR Stable
def move_servo11(): # BRT
    global zero
    what_degree = -90
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo12(): # BRH
    global zero
    what_degree = 0
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo13(): # BRT
    global zero
    what_degree = 0
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")

# FL Stable
def move_servo14(): # BRT
    global zero
    what_degree = -90
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo15(): # BRH
    global zero
    what_degree = 0
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")
def move_servo16(): # BRT
    global zero
    what_degree = 0
    degree_finder = int(((one_eight - zero) / (180 - 0))*(what_degree) + zero)
    time.sleep(0.1)
    os.system("echo " + str(degree_finder) + " > /sys/class/pwm/pwmchip0/pwm1/duty_cycle")


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

    move_servo1() # TILT
    move_servo2()
    move_servo3()
    move_servo4()

    move_servo5() # FR
    time.sleep(0.3)
    move_servo6()
    time.sleep(0.3)
    move_servo7()
    time.sleep(0.5)

    move_servo8() # BL
    time.sleep(0.3)
    move_servo9()
    time.sleep(0.3)
    move_servo10()
    time.sleep(0.5)

    move_servo11() # BR
    time.sleep(0.3)
    move_servo12()
    time.sleep(0.3)
    move_servo13()
    time.sleep(0.5)

    move_servo14() # FL
    time.sleep(0.3)
    move_servo15()
    time.sleep(0.3)
    move_servo16()
    time.sleep(0.5)

if __name__ == "__main__":
    main()