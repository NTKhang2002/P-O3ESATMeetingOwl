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

participant_counter = 0
marge_x = 50
tijd_algemeen = time.time()
mond_algemeen = False

BLUE = (255, 0, 0)
GREEN = (0, 255, 0)


class player:
    def __init__(self, fx, fy):
        self.fx = fx
        self.fy = fy
        self.talking = False
        self.present = False
        self.tijd = 0
        self.mouth = False
        self.closed_1 = 0
        self.closed_2 = 1
        self.teller_open = 0
        self.open = [10, 0, 0, 0, 0]
    def return_tuple(self):
        return (self.fx,self.fy,self.talking)
    def reset(self):
        self.fx = -1000
        self.fy = -1000
        self.talking = False
        self.present = False
        self.mouth = False
        self.teller_open = 0
        self.open = [10, 0, 0, 0, 0]

participant_1 = player(-1000,-1000)
participant_1.name = "participant 1"
participant_2 = player(-1000,-1000)
participant_2.name = "participant 2"
participant_3 = player(-1000,-1000)
participant_3.name = "participant 3"
participant_4 = player(-1000,-1000)
participant_4.name = "participant 4"
participant_list = [participant_1, participant_2, participant_3, participant_4]

def update(participant, x, y,mond_algemeen):
    participant.fx = x
    participant.fy = y
    participant.tijd = time.time()
    participant.present = True
    if mond_algemeen:
        if not participant.mouth:
            participant.mouth = True
            if participant.teller_open == 4:
                participant.teller_open = 0
            participant.teller_open += 1
            participant.open[participant.teller_open] = time.time()
    else:
        participant.closed_2 = time.time()
        if participant.mouth:
            participant.mouth = False
            participant.closed_1 = time.time()
    if (participant.closed_2 - participant.closed_1) > 3:
        participant.talking = False
    elif (participant.open[participant.teller_open] - participant.open[participant.teller_open - 4]) < 2:
        participant.talking = True

def localiser(participant, x):
    if (participant.fx - marge_x) <= x <= (participant.fx + marge_x):
        return True
    else:
        return False

def check(participant,tijd_algemeen):
    if participant.present:
        if(tijd_algemeen - participant.tijd) > 5:
            participant.reset()


def assign(x, y,mond_algemeen):
    for participant in participant_list:
        if not participant.present:
            update(participant,x,y,mond_algemeen)
            break
        elif localiser(participant,x):
            update(participant,x,y,mond_algemeen)
            break

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

def lipdetector(frame, detector,predictor, MOUTH_AR_THRESH = 0.70, mStart = 49, mEnd = 68):
    # loop over frames from the video stream
    while True:
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
                cv2.putText(frame, "MOUTH OPEN", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                color = BLUE
                mond_algemeen = True
            else:
                cv2.putText(frame, "MOUTH CLOSED", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                color = GREEN
                mond_algemeen = False
            # Visualize the mouth in green
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)      #Square over face
            assign(x, y,mond_algemeen)
            cv2.drawContours(frame, [mouthHull], -1, color, 1)
        tijd_algemeen = time.time()
        for k in participant_list:
            check(k, tijd_algemeen)
        return frame

def face_status():
    for participant in participant_list:
        yield participant.return_tuple()

