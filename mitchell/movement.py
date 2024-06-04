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
    print('trot')
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

def move():
    print('move')
    drive_pub.send({
        "L1": 0, 
        "R1": 0, 
        "x": 0, 
        "circle": 0, 
        "triangle": 0, 
        "L2": 0, 
        "R2": 0, 
        "ly": 1, 
        "lx": 0, 
        "rx": 0, 
        "message_rate": 60, 
        "ry": 0, 
        "dpady": 0, 
        "dpadx": 0
    }) 
     
def stop():
    print('stop')
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
    


def moveForward(duration):

    time.sleep(0.5)
    trot() # start trotting

    time.sleep(1)

    print('Moving Forward')

    start_time = time.time() # start time keep

    # Loop until duration has passed
    while (time.time() - start_time) < duration:
        drive_pub.send({
            "L1": 0, 
            "R1": 0, 
            "x": 0, 
            "circle": 0, 
            "triangle": 0, 
            "L2": 0, 
            "R2": 0, 
            "ly": 1, 
            "lx": 0, 
            "rx": 0, 
            "message_rate": 60, 
            "ry": 0, 
            "dpady": 0, 
            "dpadx": 0
        }) 
        time.sleep(0.3)

    stop() # Stop trotting


def rotate(duration):
    
    time.sleep(0.5)
    trot() # start trotting

    print('Rotate')

    start_time = time.time() # start time keep

    # Loop until duration has passed
    while (time.time() - start_time) < duration:
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
            "rx": 1, 
            "message_rate": 60, 
            "ry": 0, 
            "dpady": 0, 
            "dpadx": 0
        }) 
        time.sleep(0.3)
    
    stop() # Stop trotting



time.sleep(1)
init()
time.sleep(1)
activate()
time.sleep(1)

moveForward(5)