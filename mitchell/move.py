import cv2
import pyapriltags
import numpy as np
from statistics import median
from UDPComms import Publisher
from PS4Joystick import Joystick
import time
from enum import Enum

# Camera parameters (these values should be calibrated for your specific camera)
fx = 600.0  # Focal length in pixels
fy = 600.0  # Focal length in pixels
cx = 320.0  # Principal point x-coordinate in pixels
cy = 280.0  # Principal point y-coordinate in pixels
camera_params = (fx, fy, cx, cy)

# Tag size in meters (this should match the physical size of your AprilTag)
tag_size = 0.136  # Example: 10 cm

# Distance to place the dot behind the AprilTag (6 inches = 0.1524 meters)
dot_distance = -0.14

# Number of coordinates to store for median filtering
num_coords = 5
coords_buffer = []

# UDP Publisher
drive_pub = Publisher(8830)

def rotate_robot_analog(error_x, threshold=20, max_speed=500):
    """Rotate the robot based on the x-axis error using analog input."""
    if abs(error_x) < threshold:
        # Error is within threshold, stop rotating
        drive_pub.send({'f': 0, 't': 0})
    else:
        twist = max(-1, min(1, error_x / cx))  # Normalize error to -1 to 1 range
        out = {'f': 0, 't': -max_speed * twist}
        drive_pub.send(out)
        print(out)

def main(camera_index=0):
    global coords_buffer

    # Initialize the webcam
    cap = cv2.VideoCapture(camera_index)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print(f"Error: Could not open webcam at index {camera_index}.")
        return

    # Create the detector
    detector = pyapriltags.Detector(searchpath=['apriltags'], families='tag36h11')

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

        # Draw detection results on the original frame
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
            coords_buffer.append(dot_position_camera_frame)

            # Keep only the last `num_coords` coordinates in the buffer
            if len(coords_buffer) > num_coords:
                coords_buffer = coords_buffer[-num_coords:]

            # Apply median filtering
            median_x = median(coord[0] for coord in coords_buffer)
            median_y = median(coord[1] for coord in coords_buffer)
            median_z = median(coord[2] for coord in coords_buffer)

            # Print the filtered coordinates
            print(f"X: {median_x}, Y: {median_y}, Z: {median_z}")

            # Project the dot position to the image plane
            x = (fx * median_x / median_z) + cx
            y = (fy * median_y / median_z) + cy

            # Calculate the error between the dot's x-coordinate and the center of the image
            error_x = x - cx

            # Rotate the robot based on the error
            rotate_robot_analog(error_x)

            # Draw the dot on the frame
            cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)  # Red dot

        # Display the frame with detections and dot
        cv2.imshow('AprilTags Detection', frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


main(camera_index=0)  # Change the index if needed
