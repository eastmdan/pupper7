import cv2 as cv
import numpy as np
from ultralytics import YOLO
from speaker import play_audio

# Settings
model_path = 'yolov8n.pt'
frames_to_skip = 10
ids_to_track = [0]

# Init value stores
frame_count = 0

# Camera settings
cam_device_id = 0
width, height = 640, 480

# Audio
file = 'hello'
usb_device_id = 1  # Replace with your USB sound device index

# Load the YOLO model
model = YOLO(model_path)
print('YOLO model loaded')

# Function to find the center of bounding boxes
def find_midpoint(bbox):
    x_min = int(bbox[0])
    y_min = int(bbox[1])
    x_max = int(bbox[2])
    y_max = int(bbox[3])

    x_pos = (x_max - x_min) / 2 + x_min
    y_pos = (y_max - y_min) / 2 + y_min

    center_pos = (int(x_pos), int(y_pos))
    print(center_pos)
    return center_pos

# Rotate frame clockwise
def rotate_frame(frame):
    return cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)

# Function to run the YOLO model and play audio if a person is in the center
def analyze_frame(frame, model, frame_count):
    frame = rotate_frame(frame)
    
    if frame_count % frames_to_skip == 0:
        results = model.track(frame, persist=True)
        bboxes = results[0].boxes.xyxy
        for i, bbox in enumerate(bboxes):
            if i in ids_to_track:
                midpoint = find_midpoint(bbox)
                if midpoint:
                    if midpoint[0] > ((width / 2) * 1.25):
                        print("On right")
                    elif midpoint[0] < ((width / 2) * 0.75):
                        print("On Left")
                    else:
                        print("In Center")
                        play_audio("hello", usb_device_id)

# Open the camera
cap = cv.VideoCapture(f"/dev/video{cam_device_id}")

# Main loop
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        
        analyze_frame(frame, model, frame_count)
        
        if cv.waitKey(1) & 0xFF == ord('q'):  # Press Q to exit
            break
finally:
    cap.release()
