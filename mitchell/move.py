import cv2
import pyapriltags
import numpy as np
from statistics import median
from UDPComms import Publisher
from movement import init,activate,trot
import time

# Camera parameters (these values should be calibrated for your specific camera)
fx = 600.0  # Focal length in pixels
fy = 600.0  # Focal length in pixels
cx = 640.0  # Principal point x-coordinate in pixels
cy = 360.0  # Principal point y-coordinate in pixels
camera_params = (fx, fy, cx, cy)

refresh_rate = 10.

# Tag size in meters (this should match the physical size of your AprilTag)
tag_size = 0.136  # Example: 10 cm

# Distance to place the dot behind the AprilTag (6 inches = 0.1524 meters)
dot_distance = -0.14

# Number of coordinates to store for median filtering
num_coords = 3
coords_buffer = []

# UDP Publisher
drive_pub = Publisher(8830)

def rotate_robot(error_x, error_y, threshold=20):
    """Rotate the robot based on the x-axis error."""

    twist = max(-1, min(1, error_x / cx))  # Normalize error to -1 to 1 range   

    if abs(error_x) < threshold:
        # Error is within threshold, stop rotating
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
    elif error_x > 0:
        # Rotate clockwise
        drive_pub.send({
            "L1": 0,
            "R1": 0,
            "x": 0,
            "circle": 0,
            "triangle": 0,
            "L2": 0,
            "R2": 0,
            "ly": 0,  # Left wheel forward
            "lx": 0,
            "rx": -twist,
            "message_rate": 60,
            "ry": 0,  # Right wheel backward
            "dpady": 0,
            "dpadx": 0
        })
    else:
        # Rotate counterclockwise
        drive_pub.send({
            "L1": 0,
            "R1": 0,
            "x": 0,
            "circle": 0,
            "triangle": 0,
            "L2": 0,
            "R2": 0,
            "ly": 0,  # Left wheel backward
            "lx": 0,
            "rx": twist,
            "message_rate": 60,
            "ry": 0,  # Right wheel forward
            "dpady": 0,
            "dpadx": 0
        })



def main(camera_index=0):
    global coords_buffer
    
    # Initialize the webcam
    cap = cv2.VideoCapture(camera_index)

    # Set the resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    #cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    #cap.set(cv2.CAP_PROP_FOCUS, 0) 
    #cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print(f"Error: Could not open webcam at index {camera_index}.")
        return

    # Create the detector
    detector = pyapriltags.Detector(searchpath=['apriltags'], families='tag36h11')

    interval = 1. / refresh_rate

    while True:

        start_time = time.time()

        # Capture frame-by-frame
        ret, frame = cap.read()

        # If the frame was not captured correctly, continue to the next iteration
        if not ret:
            continue

        # Convert the frame to grayscale (AprilTags detection requires grayscale images)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags in the grayscale image
        detections = detector.detect(gray, estimate_tag_pose=True, camera_params=camera_params, tag_size=tag_size)

        # Draw detection results on the original frame
        for detection in detections:
            
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

            # Store the coordinates in the buffer
            coords_buffer.append(dot_position_camera_frame)

            # Keep only the last `num_coords` coordinates in the buffer
            if len(coords_buffer) > num_coords:
                coords_buffer = coords_buffer[-num_coords:]

            # Apply median filtering
            median_x = median(coord[0] for coord in coords_buffer)
            median_y = median(coord[1] for coord in coords_buffer)
            median_z = median(coord[2] for coord in coords_buffer)

            # Print the filtered coordinates
            #print(f"X: {median_x}, Y: {median_y}, Z: {median_z}")

            # Project the dot position to the image plane
            x = (fx * median_x / median_z) + cx
            y = (fy * median_y / median_z) + cy

            # Calculate the error between the dot's coordinates and the center of the image
            error_x = cx - x
            error_y = cy - y
            print(error_x, error_y, median_z)

            # Rotate the robot based on the error
            rotate_robot(error_x, error_y)
        
        elapsed_time = time.time() - start_time  # Calculate how long the function took
        sleep_time = interval - elapsed_time  # Calculate the remaining time to sleep

        if sleep_time > 0:
            time.sleep(sleep_time)  # Sleep for the remaining time
        else:
            print("Warning: Function execution is slower than the desired interval.")

init
time.sleep(1)
activate()
time.sleep(1)

main(camera_index=0)  # Change the index if needed
