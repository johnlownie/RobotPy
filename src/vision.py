#!/usr/bin/env python3

# import necessary libraries
import numpy as np
import cscore as cs
import cv2
import imutils
import json
import time
import wpilib

from cscore import CameraServer
from networktables import NetworkTables
from networktables import NetworkTablesInstance
from scipy.interpolate import interp1d

def main():
    # connect to the roborio network tables
    NetworkTables.initialize(server="127.0.0.1")
    livewindow = NetworkTablesInstance.getDefault().getTable("Shuffleboard/LiveWindow")

    # initialize some variables
    width = 480
    height = 270
    min_area = 100
    centerX = width // 2
    distance_between_targets = 11.5
    lX = lY = rX = rY = 0
 
    # set up the camera
    cameraServer = CameraServer.getInstance()
    cameraServer.enableLogging()

    camera = cameraServer.startAutomaticCapture()
    camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, width, height, 30)

    # Get a CvSink. This will capture images from the camera
    cvSink = cameraServer.getVideo()
    cvSink.setSource(camera)

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = cs.putVideo("Rectangle", width, height)
    
    # initialize frame holders to save time
    frame   = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    blurred = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    hsv     = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    mask    = np.zeros(shape=(height, width, 3), dtype=np.uint8)

    count = 0

    while True:
        time, frame = cvSink.grabFrame(frame)
        if time == 0:
            outputStream.notifyError(cvSink.getError())
            continue

        # blur frame and convert it to hsv color space
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the bounds then erode and dilate it
        mask = cv2.inRange(hsv, (113, 0, 197), (157, 10, 255))
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        # find closest contours to center on each side
        min_left = 0
        min_right = width
        left_contour = None
        right_contour = None

        # loop through contours
        for c in cnts:
            area = cv2.contourArea(c)

            # look only at contours larger than the min_area
            if area > min_area: 
                M = cv2.moments(c)
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))

                ((x, y), radius) = cv2.minEnclosingCircle(c)

                # draw a blue circle around the contour
                cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 0), 1)

                # find the contours closest to the center x-value of the frame
                if cX > centerX:
                    if cX < min_right:
                        min_right = cX
                        right_contour = c
                else:
                    if cX > min_left:
                        min_left = cX
                        left_contour = c

        # draw a yellow circle around the nearest contours
        if right_contour is not None:
            ((rX, rY), radius) = cv2.minEnclosingCircle(right_contour)
            cv2.circle(frame, (int(rX), int(rY)), int(radius), (0, 255, 255), 1)

        if left_contour is not None:
            ((lX, lY), radius) = cv2.minEnclosingCircle(left_contour)
            cv2.circle(frame, (int(lX), int(lY)), int(radius), (0, 255, 255), 1)

        # interplate the distance between the centers of the two nearest contours for 11.5 inches
        if lX > 0 and rX > 0:
            try:
                distance = interp1d([lX, rX], [0, distance_between_targets])
                distance_from_left = distance(centerX)
                offset_from_center = (distance_between_targets / 2) - distance_from_left

                direction = "left" if offset_from_center > 0 else "right" if offset_from_center < 0 else "center"
                print("The slider is {:.2f} inches {} of center".format(abs(offset_from_center), direction))

                livewindow.putNumber("Offset", offset_from_center)
            except (NameError, ValueError) as e:
                print("Error in interpolation", e)
                pass

        # draw a center line
        cv2.line(frame, (centerX, 0), (centerX, height), (255, 255, 255), 1)

        outputStream.putFrame(frame)
