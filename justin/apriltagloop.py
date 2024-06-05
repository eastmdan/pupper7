import cv2
import pyapriltags
import numpy as np
from statistics import median
from MangDang.mini_pupper.display import Display
import time


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
                cv2.destroyAllWindows()
                print("cam off")
                return avg_x, avg_y, avg_z, cam_x, cam_y


        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    

def main():
    print("Main start")

    global coords_buffer

    disp = Display()

    for x in range(3):
        x,y,z,cam_x,cam_y = cam_coords(camera_index=0)
        time.sleep(0.1)
    

if __name__ == "__main__":
    main()  # Change the index if needed