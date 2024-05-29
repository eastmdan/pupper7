import cv2 as cv
import numpy as np
from ultralytics import YOLO
from speaker import play_audio
from findDevice import findSpeakerDevice
#from findDevice import findCameraDevice



##########################################################
######################## Settings ########################
##########################################################

# Object detection settings
model_path = 'yolov8n.pt'
ids_to_track = [0]

# Camera settings
width, height = 640, 480
frames_to_skip = 5
hysteresis = 0.35 # width of center of screen to mark position as center


# Hardware Ids
cam_device_id = 0
usb_device_id = 2  



##########################################################
######################## Functions #######################
##########################################################

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

# Function to run the YOLO model and play audio if object is in the center
def analyze_frame(frame, model, frame_count):
    frame = rotate_frame(frame)
    
    if frame_count % frames_to_skip == 0:
        results = model.track(frame, persist=True)
        bboxes = results[0].boxes.xyxy
        for i, bbox in enumerate(bboxes):
            if i in ids_to_track:
                midpoint = find_midpoint(bbox)
                if midpoint:
                    if midpoint[0] > ((width / 2) * (1 + hysteresis/2)):
                        print("On right")
                    elif midpoint[0] < ((width / 2) * (1-hysteresis/2)):
                        print("On Left")
                    else:
                        print("In Center")
                        play_audio("hello", usb_device_id)

# Main function to run camera
def startObjectDetection(model):
    # Init value stores
    frame_count = 0
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



##########################################################
##################### Initialization #####################
##########################################################

# List hardware devices
findSpeakerDevice()
## findCameraDevice

# Load the YOLO model
model = YOLO(model_path)
print('YOLO model loaded')

# Open the camera
cap = cv.VideoCapture(f"/dev/video{cam_device_id}")
print("Camera Initilized")



##########################################################
######################## Main loop #######################
##########################################################

if __name__ == "__main__":
    print("Camera Started")
    startObjectDetection(model)