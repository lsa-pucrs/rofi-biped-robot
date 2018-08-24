#!/usr/bin/env python

import numpy as np
import cv2
import math

import rospy
from std_msgs.msg import Float64, Int32
from sensor_msgs import Image

# img size: 640 x 480
# angles from the camera:
#   vertical   = 48.8
#   horizontal = 62.2

class blob_finder:
    # p is a tuple <diameter in cm, color (HSV)>
    def __init__(self, p):
        self.pubQUAD = rospy.Publisher('/follower/quad', Int32, queue_size=10)
        self.pubDIST = rospy.Publisher('/follower/dist', Float64, queue_size=10)

        self.image = None

        self.name = "blob finder"

        self.diameter, self.color                       = p

        self.apparent_diameter                          = None

        self.max_vertical, self.min_vertical            = 24.4, -24.4
        self.max_horizontal, self.min_horizontal        = 31.1, -31.1

    # this function will recieve a image to calculate the apparent widhth in px of the object at a distance of 10cm
    def calibrate(self, img):
        M = cv2.moments(self.processImage(img))

        self.apparent_diameter = 2 * math.sqrt(M['m00'] / math.pi)

    def processImage(self, img):
        hsv_img   = img

        min_color = self.color
        max_color = self.color

        # change max and min colors into a possible color range
        # add color range
        min_color[0] -= (15 if min_color[0] > 15 else (min_color[0] / 2))
        max_color[0] += (15 if max_color[0] < 179 - 15 else ((179 - max_b_color[0]) / 2))

        # add saturation range
        min_color[1] = 64
        max_color[1] = 255

        # add value range
        min_color[2] = 64
        max_color[2] = 255
        # =====================================================

        # make a masked image, white anything that fits in between min and max colors and black everything else
        obj_img = cv2.inRange(hsv_img, min_color, max_color)

        # now apply some morphological transformations for smoothing the image
        kernel  = np.ones((5, 5), np.uint8)

        obj_img = cv2.morphologyEx(obj_img, cv2.MORPH_OPEN, kernel)
        obj_img = cv2.morphologyEx(obj_img, cv2.MORPH_CLOSE, kernel)

        return obj_img

    # returns the distance to the object in cm
    def getDistance(self, img):
        # apparent diameter at 10 cm
        focal_length = (self.apparent_diameter * 10) / self.diameter

        M = cv2.moments(self.processImage(img))

        d = 2 * math.sqrt(M['m00'] / math.pi)

        return (self.diameter * focal_length) / self.apparent_diameter

    # this function will return 0 if it can't find anything at all in the image otherwise it will return the quadrant (6)
    #       +---+---+---+
    #       | 1 | 2 | 3 |
    #       +---+---+---+
    #       | 4 | 5 | 6 |
    #       +---+---+---+

    def getPosition(self, img):
        obj_img = self.processImage(img)

        # get the moment of the image
        M = cv2.moments(obj_img)

        if M['m00'] == 0:
            return 0
        else:
            x, y = M['m10'] / M['m00'], M['m01'] / M['m00']

            if x <= 213:
                return 1 if y >= 240 else 4
            elif x <= 426:
                return 2 if y >= 240 else 5
            else:
                return 3 if y >= 240 else 6

    def run(self, img):
        img = img.data

        dist, pos = Float64(), Int32()
        dist.data, pos.data = self.getDistance(img), self.getPosition(img)

        self.pubQUAD.publish(pos)
        self.pubDIST.publish(dist)

# ============================================================================ #

BLOB = blob_finder((10, [0, 0, 0]))

calibration_img = cv2.imread('calibration.jpg', format='hsv')
BLOB.calibrate(calibration_img)

if __name__ == '__main__':
    rospy.init_node(BLOB.name, anonymous=False)
    rospy.Subscriber('/camera/image', Image, BLOB.run)
    rospy.spin()
