import time
from UDPComms import Publisher
from movement import init,activate,trot


# Set the resolution
width = 640
height = 360

cx = width/2  # Principal point x-coordinate in pixels
cy = height/2  # Principal point y-coordinate in pixels


# UDP Publisher
drive_pub = Publisher(8830)


def move_robot(error_x, error_y, z_distance, duration):
    """Move the robot based on continuously updated errors until a certain distance is reached."""
    
    scaling_factor = 0.35 #scaling of movement speeds
    
    # start trotting
    trot()
    time.sleep(0.3)

    # Calculate normalized forward and lateral movements
    lateral_error_normalized = error_x / cx  # Normalized to -1 to 1

    # Clamp the speeds within [-1, 1]
    lateral = max(-1, min(1, scaling_factor * lateral_error_normalized))
    forward = max(-1, min(1, scaling_factor * z_distance))

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
                "L1": 0, 
                "R1": 0, 
                "x": 0, 
                "circle": 0, 
                "triangle": 0, 
                "L2": 0, 
                "R2": 0, 
                "ly": forward * ly, 
                "lx": lateral * lx, 
                "rx": 0, 
                "message_rate": 60, 
                "ry": 0, 
                "dpady": 0, 
                "dpadx": 0
            })

        time.sleep(0.35)  # Sleep time based on message rate 0.016
    
    # stop trotting so camera can take another measurement
    trot()


init()
time.sleep(0.5)
activate()
time.sleep(0.5)
move_robot(1,0,5,5)