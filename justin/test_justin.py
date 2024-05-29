import cv2
import pyapriltags
import numpy as np

# Camera parameters (these values should be calibrated for your specific camera)
fx = 600.0  # Focal length in pixels
fy = 600.0  # Focal length in pixels
cx = 320.0  # Principal point x-coordinate in pixels
cy = 280.0  # Principal point y-coordinate in pixels
camera_params = (fx, fy, cx, cy)

# Tag size in meters (this should match the physical size of your AprilTag)
tag_size = 0.1  # Example: 10 cm

def main(camera_index=0):
    # Initialize the webcam
    cap = cv2.VideoCapture(camera_index)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print(f"Error: Could not open webcam at index {camera_index}.")
        return

    # Create the detector
    detector = pyapriltags.Detector(searchpath=['apriltags'],families='tag36h11')

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

            # Draw the detected pose axes
            if detection.pose_R is not None and detection.pose_t is not None:
                # Pose estimation returns rotation and translation vectors
                R = detection.pose_R
                t = detection.pose_t

                # Convert rotation matrix to rotation vector
                rvec, _ = cv2.Rodrigues(R)
                
                # Define the 3D point 6 inches behind the tag (convert inches to meters)
                point_behind = np.array([0, 0, -0.1524])  # 6 inches is approximately 0.1524 meters

                # Calculate the 3D coordinates of the point behind the tag in the camera coordinate system
                point_behind_camera = R @ point_behind.reshape(3, 1) + t

                # Project the 3D point onto the 2D image plane
                camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float32)
                point_behind_image, _ = cv2.projectPoints(point_behind_camera.T, rvec, t, camera_matrix, None)
                point_behind_image = tuple(point_behind_image.ravel().astype(int))

                # Draw the point on the image
                cv2.circle(frame, point_behind_image, 5, (0, 0, 255), -1)
                cv2.line(frame, (int(detection.center[0]),int(detection.center[1])), (point_behind_image), (0, 0, 255), 2)

                # Calculate XYZ coordinates of the point behind the tag
                x, y, z = point_behind_camera.ravel()

                # Calculate angle of camera from the dot (assuming dot is origin)
                angle_x = np.arctan2(x, z) * 180 / np.pi
                angle_y = np.arctan2(y, z) * 180 / np.pi

                # Print XYZ coordinates and angles
                strang = f"Point behind tag (XYZ): ({x:.2f}, {y:.2f}, {z:.2f})"
                strang2 = f"Angle of camera from the dot (degrees): (X: {angle_x:.2f}, Y: {angle_y:.2f})"
                cv2.putText(frame,strang,(20,20),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),2)
                cv2.putText(frame,strang2,(20,40),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),2)

            for i in range(4):
                cv2.line(frame, tuple(corners[i]), tuple(corners[(i + 1) % 4]), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {detection.tag_id}", tuple(corners[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with detections
        cv2.imshow('AprilTags Detection', frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(camera_index=0)  # Change the index if needed