from UDPComms import Publisher
import time


drive_pub = Publisher(8830)


def init():
    print('init')
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
        "rx": 0, 
        "message_rate": 60, 
        "ry": 0, 
        "dpady": 0, 
        "dpadx": 0
    })

def activate():
    print('activate')
    drive_pub.send({
        "L1": 1, 
        "R1": 0, 
        "x": 0, 
        "circle": 0, 
        "triangle": 0, 
        "L2": 0, 
        "R2": 0, 
        "ly": 0, 
        "lx": 0, 
        "rx": 0, 
        "message_rate": 60, 
        "ry": 0, 
        "dpady": 0, 
        "dpadx": 0
    })

def trot():
    drive_pub.send({
        "L1": 0, 
        "R1": 1, 
        "x": 0, 
        "circle": 0, 
        "triangle": 0, 
        "L2": 0, 
        "R2": 0, 
        "ly": 0, 
        "lx": 0, 
        "rx": 0, 
        "message_rate": 60, 
        "ry": 0, 
        "dpady": 0, 
        "dpadx": 0
    })  


def move(forward, lateral, duration):
    time.sleep(0.5)
    trot()  # Start trotting
    time.sleep(0.3)

    ramp_duration = 3  # time to accel to full speed
    start_time = time.time()

    # Loop until duration has passed
    while (time.time() - start_time) < duration:
        elapsed_time = time.time() - start_time
        
        # ramp up speed
        if elapsed_time < ramp_duration:
            ly = elapsed_time / ramp_duration  
            lx = elapsed_time / ramp_duration
        else:
            # set to full speed after 2 seconds
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
            "ly": forward*ly,
            "lx": lateral*lx,
            "rx": 0,
            "message_rate": 60,
            "ry": 0,
            "dpady": 0,
            "dpadx": 0
        })

        time.sleep(0.3) # 0.016 based on message rate

    time.sleep(0.3)
    trot()  # Stop trotting


def rotate(forward, lateral, duration):

    ramp_duration = 1  # time to accel to full speed
    start_time = time.time()

    # Loop until duration has passed
    while (time.time() - start_time) < duration:
        elapsed_time = time.time() - start_time
        
        # ramp up speed
        if elapsed_time < ramp_duration:
            ry = elapsed_time / ramp_duration  
            rx = elapsed_time / ramp_duration
        else:
            # set to full speed after 2 seconds
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
            "ly": 0,
            "lx": 0,
            "rx": -lateral*rx,
            "message_rate": 60,
            "ry": forward*ry,
            "dpady": 0,
            "dpadx": 0
        })

        time.sleep(0.3) # 0.016 based on message rate