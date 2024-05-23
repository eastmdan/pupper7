
import cv2
import pyapriltags
import math


#load the input image and convert it to greyscale

cam_image = cv2.VideoCapture(0)

expected_cross_section_250mm = 100 # size at 0.25m
expected_cross_section_1m = 50 # size at 1m 
# sizefactor = 



while True:    
    ret, img = cam_image.read()   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = pyapriltags.Detector()
    results = detector.detect(gray)
    for r in results:
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))
        ptCenter = (int(r.center[0]), int(r.center[1]))
        crossSection = (math.sqrt( ( ptB[0]-ptD[0] )**2 + ( ptB[1]-ptD[1] )**2))
        distance_meters = 40/crossSection
        #print("%.2f" % r.tag_size)
        
        cv2.line(img, ptA, ptB, (0, 255, 0), 2)
        cv2.line(img, ptB, ptC, (0, 255, 0), 2)
        cv2.line(img, ptC, ptD, (0, 255, 0), 2)
        cv2.line(img, ptD, ptA, (0, 255, 0), 2)
        
        cv2.putText(img, 'A', ptA, cv2.FONT_HERSHEY_COMPLEX, 0.5,(100,255,0),2)
        cv2.putText(img, 'B', ptB, cv2.FONT_HERSHEY_COMPLEX, 0.5,(100,255,0),2)
        cv2.putText(img, 'C', ptC, cv2.FONT_HERSHEY_COMPLEX, 0.5,(100,255,0),2)
        cv2.putText(img, 'D', ptD, cv2.FONT_HERSHEY_COMPLEX, 0.5,(100,255,0),2)
    
        cv2.circle(img, ptCenter, 2,(0,0,255), -1)
        cv2.putText(img, str(int(crossSection)), ptCenter, cv2.FONT_HERSHEY_COMPLEX, 0.5,(0,255,0),2)
        cv2.putText(img, (("%.2f" %distance_meters)+"m"), (ptCenter[0],ptCenter[1]+100), cv2.FONT_HERSHEY_COMPLEX, 0.5,(0,255,0),2)
        
    cv2.imshow("", img)     
    
    if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1)==27):
        break

cam_image.release()
cv2.destroyAllWindows()

#print(video_path)