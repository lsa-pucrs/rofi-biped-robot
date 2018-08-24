#!/usr/bin/env python

import rospy
from picamera import PiCamera
from picamera.array import PiRGBArray
from sensor_msgs.msg import Image

img = Image()
#fps = String()

def capture():
    # Create publisher and initialize ros node
    pub = rospy.Publisher('/camera/image', Image, queue_size=10)
    rospy.init_node('raspicamV2', anonymous=True)
    rate = rospy.Rate(10)

    # Instatiate picamera
    camera = PiCamera()
    camera.resolution, camera.framerate = (640,480), 30
    rawCapture = PiRGBArray(camera)

    img.height = camera.resolution[1]
    img.width = camera.resolution[0]
    img.encoding = 'hsv'

    # Run this while node is active
    while not rospy.is_shutdown():
        # Get frame
        camera.capture(rawCapture, format='hsv')
        img.data = rawCapture.array
        # Publish frame
        pub.publish(img)

        rate.sleep()
