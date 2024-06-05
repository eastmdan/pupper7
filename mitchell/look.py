import cv2
import pyapriltags
import numpy as np
from statistics import median
import time
from threading import Thread, Lock
from UDPComms import Publisher
from move import move_robot
from movement import init,activate,trot,move,rotate


##### Camera parameters #####

# Set the resolution
width = 640
height = 360

fx = 600.0  # Focal length in pixels
fy = 600.0  # Focal length in pixels
cx = width/2  # Principal point x-coordinate in pixels
cy = height/2  # Principal point y-coordinate in pixels
camera_params = (fx, fy, cx, cy)

# Tag size in meters (this should match the physical size of your AprilTag)
tag_size = 0.136  # Example: 10 cm

# Distance to place the dot behind the AprilTag (6 inches = 0.1524 meters)
dot_distance = -0.14


# Number of coordinates to store for median filtering
num_coords = 1
coords_buffer = []
error_store = []
error_store_lock = Lock()

# Set the refresh rate
refresh_rate = 15
interval = 1. / refresh_rate

# Global variables for frame capture
frame = None
frame_lock = Lock()

def capture_frames(camera_index=0):
    global frame
    cap = cv2.VideoCapture(camera_index)

    # Set the resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Disable autofocus and set manual focus if needed
    #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    #cap.set(cv2.CAP_PROP_FOCUS, 0)  # Adjust this value as needed

    while True:
        ret, new_frame = cap.read()
        if ret:
            with frame_lock:
                frame = new_frame.copy()



def main(camera_index=0):
    global coords_buffer, frame
    
    init()
    time.sleep(0.5)
    activate()
    time.sleep(0.5)
    
    # Start the robot movement in a separate thread
    robot_thread = Thread(target=move_robot, args=(error_store, error_store_lock))
    robot_thread.daemon = True
    robot_thread.start()
    
    # Start frame capture in a separate thread
    capture_thread = Thread(target=capture_frames, args=(camera_index,))
    capture_thread.daemon = True
    capture_thread.start()

    # Create the detector
    detector = pyapriltags.Detector(searchpath=['apriltags'], families='tag36h11')

    while True:
        start_time = time.time()

        with frame_lock:
            current_frame = frame.copy() if frame is not None else None

        if current_frame is None:
            time.sleep(0.001)
            continue

        # Convert the frame to grayscale (AprilTags detection requires grayscale images)
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags in the grayscale image
        detections = detector.detect(gray, estimate_tag_pose=True, camera_params=camera_params, tag_size=tag_size)

        if detections:
            detection = detections[0]

            # Get the pose estimation
            pose_R = detection.pose_R
            pose_t = detection.pose_t

            # Convert the rotation matrix and translation vector to a 4x4 transformation matrix
            transformation_matrix = np.eye(4)
            transformation_matrix[:3, :3] = pose_R
            transformation_matrix[:3, 3] = pose_t[:, 0]

            # Define the position of the dot in the tag's frame (6 inches behind the tag)
            dot_position_tag_frame = np.array([0, 0, -dot_distance, 1])

            # Transform the dot position to the camera frame
            dot_position_camera_frame = np.dot(transformation_matrix, dot_position_tag_frame)

            ## Store the coordinates in the buffer
            #coords_buffer.append(dot_position_camera_frame)

            ## Keep only the last `num_coords` coordinates in the buffer
            #if len(coords_buffer) > num_coords:
            #    coords_buffer = coords_buffer[-num_coords:]

            ## Apply median filtering
            #median_x = median(coord[0] for coord in coords_buffer)
            #median_y = median(coord[1] for coord in coords_buffer)
            #median_z = median(coord[2] for coord in coords_buffer)

            dot_x = dot_position_camera_frame[0]
            dot_y = dot_position_camera_frame[1]
            dot_z = dot_position_camera_frame[2]


            # Project the dot position to the image plane
            x = (fx * dot_x / dot_z) + cx
            y = (fy * dot_y / dot_z) + cy

            # Calculate the error between the dot's coordinates and the center of the image
            error_x = cx - x
            error_y = cy - y
            
            
            with error_store_lock:
                error_store.append((error_x, error_y, dot_z))
                print(error_store[0])

            # Rotate the robot based on the error
            #move_robot(error_x, error_y, dot_z)
        
        elapsed_time = time.time() - start_time  # Calculate how long the function took
        sleep_time = interval - elapsed_time  # Calculate the remaining time to sleep

        if sleep_time > 0:
            time.sleep(sleep_time)  # Sleep for the remaining time
        else:
            print("Warning: Function execution is slower than the desired interval.")

if __name__ == "__main__":
    main(camera_index=0)  # Change the index if needed