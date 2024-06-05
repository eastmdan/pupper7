import cv2
import pyapriltags
import numpy as np
from statistics import median
import time
from threading import Thread, Lock
from UDPComms import Publisher
from movement import init,activate,trot,move,rotate

# Set the refresh rate
refresh_rate = 30
interval = 1. / refresh_rate

# Set the resolution
width = 640
height = 360

fx = 600.0  # Focal length in pixels
fy = 600.0  # Focal length in pixels
cx = width/2  # Principal point x-coordinate in pixels
cy = height/2  # Principal point y-coordinate in pixels
camera_params = (fx, fy, cx, cy)


throw_distance = 1. # m away form the box the robot will throw




# UDP Publisher
drive_pub = Publisher(8830)


def move_robot(error_store):
    """Move the robot based on continuously updated errors until a certain distance is reached."""

    # Movement parameters
    duration = interval
    scaling_factor = 0.5 #scaling of movement speeds
    throw_distance = 0.25  # distance for launch

    while True:
    
        error_x, error_y, z_distance = error_store
            

        # Calculate normalized forward and lateral movements
        lateral_error_normalized = error_x / cx  # Normalized to -1 to 1
        forward_error_normalized = (z_distance - throw_distance) / throw_distance  # Normalized to -1 to 1

        # Clamp the speeds within [-1, 1]
        lateral = max(-1, min(1, scaling_factor * lateral_error_normalized))
        forward = max(-1, min(1, scaling_factor * forward_error_normalized))

        if abs(z_distance - throw_distance) >= 0:  # Movement command condition

            ramp_duration = 1  # Time to accelerate to full speed
            start_time = time.time()

            # Loop until the duration has passed
            while (time.time() - start_time) < duration:
                elapsed_time = time.time() - start_time

                # Ramp up speed
                if elapsed_time < ramp_duration:
                    ly = elapsed_time / ramp_duration
                    lx = elapsed_time / ramp_duration
                else:
                    ly = 1
                    lx = 1

                drive_pub.send({
                    "ly": forward * ly,
                    "lx": lateral * lx,
                    "message_rate": 60
                })

                time.sleep(0.35)  # Sleep time based on message rate 0.016

        # Condition to exit loop (if required)
        else:   # If z-distance is within range, stop function
            break
