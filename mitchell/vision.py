import cv2 as cv
import numpy as np
from ultralytics import YOLO
from speaker import play_audio


# Settings
model_path = 'yolov8n.pt'
scale = 1
frames_to_skip = 10
ids_to_track = [0]

# init value stores
frame_count = 0
last_annotated_frame = None

# Camera settings
cam_device_id = 1
width, height = 640, 480


# Audio
file = 'birds'
audio_file = f'/home/ubuntu/pupper7/mitchell/sounds/{file}.mp3'
usb_device_id = 11  # Replace with your USB sound device index




cap = cv.VideoCapture(f"/dev/video{cam_device_id}")

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

# Function to run the YOLO model and change direction based on bbox center position
def analyze_frame(frame, model, frame_count, last_annotated_frame):
    frame = rotate_frame(frame)
    
    if frame_count % frames_to_skip == 0:
        results = model.track(frame, persist=True)
        annotated_frame = results[0].plot()
        last_annotated_frame = annotated_frame

        bboxes = results[0].boxes.xyxy
        for i, bbox in enumerate(bboxes):
            if i in ids_to_track:
                midpoint = find_midpoint(bbox)
                if midpoint:
                    cv.circle(annotated_frame, midpoint, 5, (0, 255, 0), -1)
                    
                    if midpoint[0] > ((width / 2)* 1.25):
                        print("On right")
    
                    elif midpoint[0] < ((width / 2)* 0.75):
                        print("On Left")
                
                    else:
                        print("In Center")
                        play_audio("hello", usb_device_id)
                        


    elif last_annotated_frame is not None:
        annotated_frame = last_annotated_frame
    else:
        annotated_frame = frame

    resized_frame = cv.resize(annotated_frame, (width, height))

    return resized_frame, last_annotated_frame
    
    

# Main loop
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        
        annotated_frame, last_annotated_frame = analyze_frame(frame, model, frame_count, last_annotated_frame)
        
        cv.imshow('Video', annotated_frame)
        if cv.waitKey(1) & 0xFF == ord('q'):  # Press Q to exit
            break
finally:
    cv.destroyAllWindows()
    cap.release()