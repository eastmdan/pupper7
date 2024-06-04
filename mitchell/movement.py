from UDPComms import Publisher
import time


drive_pub = Publisher(8830)


# Define the stopping time (in seconds)
t_stop = 10  # This means the loop will run for 10 seconds

# Record the start time
start_time = time.time()


def init():
    print('init')
    drive_pub.send({"L1": 0, 
            "R1": 0, 
            "x": 0, 
            "circle": 0, 
            "triangle": 0, 
            "L2": 0, 
            "R2": 0, 
            "ly": 0, 
            "lx": 0, 
            "rx": 0, 
            "message_rate": 20, 
            "ry": 0, 
            "dpady": 0, 
            "dpadx": 0})

def activate():
    print('activate')
    drive_pub.send({"L1": 1, 
            "R1": 0, 
            "x": 0, 
            "circle": 0, 
            "triangle": 0, 
            "L2": 0, 
            "R2": 0, 
            "ly": 0, 
            "lx": 0, 
            "rx": 0, 
            "message_rate": 20, 
            "ry": 0, 
            "dpady": 0, 
            "dpadx": 0})

def trot():
    print('trot')
    drive_pub.send({"L1": 0, 
            "R1": 1, 
            "x": 0, 
            "circle": 0, 
            "triangle": 0, 
            "L2": 0, 
            "R2": 0, 
            "ly": 0, 
            "lx": 0, 
            "rx": 0, 
            "message_rate": 20, 
            "ry": 0, 
            "dpady": 0, 
            "dpadx": 0})  

def move():
    print('move')
    drive_pub.send({"L1": 0, 
            "R1": 0, 
            "x": 0, 
            "circle": 0, 
            "triangle": 0, 
            "L2": 0, 
            "R2": 0, 
            "ly": -1, 
            "lx": 0, 
            "rx": 0, 
            "message_rate": 20, 
            "ry": 0, 
            "dpady": 0, 
            "dpadx": 0}) 
    
    
def stop():
    print('stop')
    drive_pub.send({"L1": 0, 
            "R1": 1, 
            "x": 0, 
            "circle": 0, 
            "triangle": 0, 
            "L2": 0, 
            "R2": 0, 
            "ly": 0, 
            "lx": 0, 
            "rx": 0, 
            "message_rate": 20, 
            "ry": 0, 
            "dpady": 0, 
            "dpadx": 0}) 


time.sleep(1)
init()
time.sleep(1)
activate()
time.sleep(1)
trot()
time.sleep(1)

# Loop until the current time minus the start time is less than t_stop
while (time.time() - start_time) < t_stop:
    move()  # Call the move function
    time.sleep(0.5)  # Wait for 1 second before the next iteration
    
time.sleep(1)
stop()