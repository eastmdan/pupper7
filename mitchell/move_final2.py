import cv2
import os
import pyapriltags
import numpy as np
import time
from movement import init, activate, trot
from move_final1 import move_robot, twist_robot, rotate_robot


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

throw_distance = 2.65 # m

# Number of coordinates to store for median filtering
num_coords = 10
coords_buffer = []


def cam_coords(camera_index=0):
    # Initialize the webcam
    print("turning cam on")
    cap = cv2.VideoCapture(camera_index)
    print("cam on")

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print(f"Error: Could not open webcam at index {camera_index}.")
        return

    # Create the detector
    detector = pyapriltags.Detector(searchpath=['apriltags'], families='tag36h11')

    coords_buffer = []

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If the frame was not captured correctly, continue to the next iteration
        if not ret:
            continue

        # Convert the frame to grayscale (AprilTags detection requires grayscale images)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags in the grayscale image
        detections = detector.detect(gray, estimate_tag_pose=True, camera_params=camera_params, tag_size=tag_size)

        # Process each detection
        for detection in detections:
            corners = detection.corners.astype(int)
            
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
            coords_buffer.append(dot_position_camera_frame[:3])

            # Keep only the last `num_coords` coordinates in the buffer
            if len(coords_buffer) > num_coords:
                coords_buffer = coords_buffer[-num_coords:]

            # Check if we have enough data points
            if len(coords_buffer) >= num_coords:
                # Calculate the average coordinates
                avg_x = np.mean([coord[0] for coord in coords_buffer])
                avg_y = np.mean([coord[1] for coord in coords_buffer])
                avg_z = np.mean([coord[2] for coord in coords_buffer])

                # Project the dot position to the image plane
                cam_x = (fx * avg_x / avg_z) + cx
                cam_y = (fy * avg_y / avg_z) + cy

                # Print or return the average coordinates
                print(f"Average coordinates: x={avg_x}, y={avg_y}, z={avg_z}, cam x={cam_x}, cam y={cam_y}")
                cap.release()
                print("cam off")
                return avg_x, avg_y, avg_z, cam_x, cam_y
   

def cam_error(cam_x,cam_y):
    # Calculate the error between the dot's coordinates and the center of the image
    error_x = cx - cam_x
    error_y = cy - cam_y

    return -error_x, error_y



def main():
    print("Main start")
    
    init()
    time.sleep(0.3)
    activate()
    time.sleep(0.3)
    trot()
    time.sleep(0.3)

    global coords_buffer
    
    stop_trot = False

    for _ in range(20):
        x,y,z,cam_x,cam_y = cam_coords(camera_index=0)

        error_x, error_y = cam_error(cam_x,cam_y)

        if z > throw_distance:
            move_robot(error_x,error_y,z,2.5)
            
        else:
            if not stop_trot:
                print('stop the trot')
                time.sleep(1)
                trot()
                stop_trot = True
                time.sleep(1)
            
            rotate_robot(error_x - 30,error_y,z,2)
            
            os.system("echo 2000000 > /sys/class/pwm/pwmchip0/pwm3/duty_cycle")
            time.sleep(0.5)
            os.system("echo 500000 > /sys/class/pwm/pwmchip0/pwm3/duty_cycle")
            
            break

        
    

if __name__ == "__main__":
    main()  # Change the index if needed