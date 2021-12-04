# USAGE
# python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav

# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2


BLUE = (255, 0, 0)
GREEN = (0, 255, 0)

def mouth_aspect_ratio(mouth):
    # compute the euclidean distances between the two sets of
    # vertical mouth landmarks (x, y)-coordinates
    A = dist.euclidean(mouth[2], mouth[10])  # 51, 59
    B = dist.euclidean(mouth[4], mouth[8])  # 53, 57

    # compute the euclidean distance between the horizontal
    # mouth landmark (x, y)-coordinates
    C = dist.euclidean(mouth[0], mouth[6])  # 49, 55

    # compute the mouth aspect ratio
    mar = (A + B) / (2.0 * C)

    # return the mouth aspect ratio
    return mar

def lipdetector(frame, detector,predictor,MOUTH_AR_THRESH = 0.70, mStart = 49, mEnd = 68):
    # loop over frames from the video stream
    while True:
        faces = []
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale frame
        rects = detector(gray, 0)
        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            # extract the mouth coordinates, then use the
            # coordinates to compute the mouth aspect ratio
            mouth = shape[mStart:mEnd]
            mouthMAR = mouth_aspect_ratio(mouth)
            mar = mouthMAR
            # compute the convex hull for the mouth, then
            # visualize the mouth
            mouthHull = cv2.convexHull(mouth)
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # Draw text if mouth is open + visualize the mouth in blue
            if mar > MOUTH_AR_THRESH:

                color = BLUE
                mond_algemeen = True
            else:
                color = GREEN
                mond_algemeen = False
            # Visualize the mouth in green
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)      #Square over face
            cv2.drawContours(frame, [mouthHull], -1, color, 1)
            faces.append([x+w,y+h,mond_algemeen])
        return frame, faces



