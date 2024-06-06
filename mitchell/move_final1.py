import time
from UDPComms import Publisher
from movement import init,activate,trot,clear


refresh = 20 # Time to sleep inbetween individual movements
move_speed = 0.38 # scaler to change how quickly the robot performs actions



# Set the resolution
width = 640
height = 360

cx = width/2  # Principal point x-coordinate in pixels
cy = height/2  # Principal point y-coordinate in pixels


# UDP Publisher
drive_pub = Publisher(8830)


def move_robot(error_x, error_y, z_distance, duration):
    
    scaling_factor = move_speed #scaling of movement speeds

    # Calculate normalized forward and lateral movements
    lateral_error_normalized = error_x / cx  # Normalized to -1 to 1

    # Clamp the speeds within [-1, 1]
    lateral = max(-1, min(1, scaling_factor * lateral_error_normalized * 0.4))
    forward = max(-1, min(1, scaling_factor * z_distance))

    ramp_duration = 1  # Time to accelerate to full speed
    start_time = time.time()
    

    # Loop until the duration has passed
    while (time.time() - start_time) < duration:
        elapsed_time = time.time() - start_time

        # Ramp up speed
        if elapsed_time < ramp_duration:
            ly = elapsed_time / ramp_duration
            rx = elapsed_time / ramp_duration
        else:
            ly = 1
            rx = 1

        drive_pub.send({
                "L1": 0, 
                "R1": 0, 
                "x": 0, 
                "circle": 0, 
                "triangle": 0, 
                "L2": 0, 
                "R2": 0, 
                "ly": forward * ly, 
                "lx": 0, 
                "rx": lateral * rx, 
                "message_rate": refresh, 
                "ry": 0, 
                "dpady": 0, 
                "dpadx": 0
            })

        time.sleep(1/refresh)
        
    #clear()
    
    

def twist_robot(error_x, error_y, z_distance, duration):
    
    
    scaling_factor = move_speed #scaling of movement speeds

    # Calculate normalized forward and lateral movements
    lateral_error_x_normalized = error_x / cx  # Normalized to -1 to 1
    lateral_error_y_normalized = error_y / cy  # Normalized to -1 to 1

    # Clamp the speeds within [-1, 1]
    lateral = max(-1, min(1, scaling_factor * lateral_error_x_normalized))
    forward = max(-1, min(1, scaling_factor * lateral_error_y_normalized))
    

    ramp_duration = 1  # Time to accelerate to full speed
    start_time = time.time()
    
    # Loop until the duration has passed
    while (time.time() - start_time) < duration:
        elapsed_time = time.time() - start_time

        # Ramp up speed
        if elapsed_time < ramp_duration:
            ry = elapsed_time / ramp_duration
            rx = elapsed_time / ramp_duration
        else:
            ry = 1
            rx = 1

        drive_pub.send({
                "L1": 0, 
                "R1": 0, 
                "x": 0, 
                "circle": 0, 
                "triangle": 0, 
                "L2": 0, 
                "R2": 0, 
                "ly": 0, 
                "lx": 0, 
                "rx": lateral * rx, 
                "message_rate": refresh, 
                "ry": 0, 
                "dpady": 0, 
                "dpadx": 0
            })

        time.sleep(1/refresh)
        
    #clear()

        

def rotate_robot(error_x, error_y, z_distance, duration):
    
    scaling_factor = move_speed*.75 #scaling of movement speeds

    # Calculate normalized forward and lateral movements
    lateral_error_x_normalized = error_x / cx  # Normalized to -1 to 1
    lateral_error_y_normalized = error_y / cy  # Normalized to -1 to 1

    # Clamp the speeds within [-1, 1]
    lateral = max(-1, min(1, scaling_factor * lateral_error_x_normalized))
    forward = max(-1, min(1, scaling_factor * lateral_error_y_normalized))

    ramp_duration = 1  # Time to accelerate to full speed
    start_time = time.time()
    
    # Loop until the duration has passed
    while (time.time() - start_time) < duration:
        elapsed_time = time.time() - start_time

        # Ramp up speed
        if elapsed_time < ramp_duration:
            ry = elapsed_time / ramp_duration
            rx = elapsed_time / ramp_duration
        else:
            ry = 1
            rx = 1

        drive_pub.send({
                "L1": 0, 
                "R1": 0, 
                "x": 0, 
                "circle": 0, 
                "triangle": 0, 
                "L2": 0, 
                "R2": 0, 
                "ly": 0, 
                "lx": 0, 
                "rx": lateral * rx, 
                "message_rate": refresh, 
                "ry": forward * ry, 
                "dpady": 0, 
                "dpadx": 0
            })

        time.sleep(1/refresh)  
    
    #clear()