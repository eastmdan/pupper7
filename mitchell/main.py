import cv2 as cv

cam = cv.VideoCapture(0)

while True:
    
    ret, frame = cam.read()
    if not ret:
        break

    cv.imshow('Video', frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()



pip install --no-binary opencv-python opencv-python
????