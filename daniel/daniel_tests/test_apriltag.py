import sys

sys.path.insert(1, '../lib')
import tag_finder, location, drawing
import numpy as np

iterations = 1000

for i in range(iterations):
    find_apriltag = tag_finder.Detector(0.0535, 'test_tag_transform.json')
    print(find_apriltag)