import cv2
import numpy as np
from robotpy_apriltag import Detector

def detect_apriltags(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Create a detector object
    detector = Detector()
    
    # Detect tags in the frame
    detections = detector.detect(gray)
    
    return detections

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # 0 for default webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        detections = detect_apriltags(frame)
        
        # Draw AprilTag detections on the frame
        for detection in detections:
            for pt in detection.corners:
                pt = tuple(map(int, pt))
                cv2.circle(frame, pt, 5, (0, 255, 0), -1)
        
        # Show the frame with AprilTag detections
        cv2.imshow('AprilTag Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
