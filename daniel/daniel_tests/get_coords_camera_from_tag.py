import sys

sys.path.insert(1, '../lib')
import tag_finder, location, drawing
import numpy as np
import time


# ======================== Camera class==================================

def get_apriltag_coordinates(tagfinder_obj):
    tagfinder_obj.capture_Camera()
    if not tagfinder_obj.getPose():
        print("===== No tag found")
        return 0, 0, 0, round(time.time() * 1000)

    for index, (pose, result) in enumerate(zip(tagfinder_obj.Poses, tagfinder_obj.dt_results)):
        #print("Tag: family=", pose['tag_family'], " , ID=", pose['tag_id'])

        #camera from tag
        tagfinder_obj.getCamera_Pose(result)
        X, Y, Z = tagfinder_obj.camera_X, tagfinder_obj.camera_Y, tagfinder_obj.camera_Z

        #X, Y, Z = translate[0][0], translate[1][0], translate[2][0]
        #print(" ==== Translation: (", X, ",", Y, ",", Z, ")")
        radian, degree = tagfinder_obj.get_Euler(tagfinder_obj.dt_results[0].pose_R)
        print(" ==== Euler degree (Yaw,Pitch,Roll):", degree)
        print(" ==== Pose:\n", tagfinder_obj.pose)

        return X, Y, Z, round(time.time() * 1000)

        #   tagfinder_obj.get_Destination((-47,20))


# ============================================


tagfinder_obj = tag_finder.Detector(0.0535, 'test_tag_transform.json')
found_tag = False

for i in range(200):
    X_coord, Y_coord, Z_coord, system_time = get_apriltag_coordinates(tagfinder_obj)
    #print("Cycle: ", X_coord, Y_coord, Z_coord, system_time)

tagfinder_obj.release_Camera()
print("end")
