"""
to do:
opgestoken hand(en) aan een gezicht koppelen

"""


from detect_open_mouth_V2 import openmond
import cv2
import time
from test import hand_status
from cvzone.HandTrackingModule import HandDetector

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib

BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
people = []

def mouth_aspect_ratio(mouth):
	A = dist.euclidean(mouth[12], mouth[18])
	B = dist.euclidean(mouth[13], mouth[17])
	C = dist.euclidean(mouth[14], mouth[16])

	mar = (A + B + C) / 3.0
	return mar

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
                help="path to facial landmark predictor")
ap.add_argument("-w", "--webcam", type=int, default=0,
                help="index of webcam on system")
args = vars(ap.parse_args())

# define one constants, for mouth aspect ratio to indicate open mouth
MOUTH_AR_THRESH = 8

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
mdetector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the mouth
(mStart, mEnd) = (49, 68)

# start the video stream thread
print("[INFO] starting video stream thread...")

def koppelen(xhanden, xgezichten):
    gekoppeld = []
    for i in range(len(xhanden)):
        min_afstand = 10000000000000000
        juiste_gezicht = 0
        for xgezicht in xgezichten:
            index = 0
            afstand = abs(xhanden[i] - xgezicht)
            if afstand <= min_afstand:
                min_afstand = afstand
                juiste_gezicht = index
            index += 1
        ok = (i,juiste_gezicht)
        gekoppeld.append(ok)
    return gekoppeld #geeft een lijst met tuples (index_xhanden, index_xgezichten)


def main(detectionCon = 0.8, maxHands = 4):
    # Camera preparation
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3,1000)
    cap.set(4,100)
    # Initializing HandDetector module
    detector = HandDetector(detectionCon=detectionCon, maxHands=maxHands)

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        handstatus = hand_status(detector, hands)
        img = imutils.resize(img, width=640)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale frame
        rects = mdetector(gray, 0)
        people = []
        face = []
        # loop over the face detections
        if rects:
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
                cv2.putText(img, "MAR: {:.2f}".format(mar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # Draw text if mouth is open + visualize the mouth in blue
                if mar > MOUTH_AR_THRESH:
                    cv2.putText(img, "MOUTH OPEN", (30, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    color = BLUE
                else:
                    cv2.putText(img, "MOUTH CLOSED", (30, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    color = GREEN
                # Visualize the mouth in green

                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.drawContours(img, [mouthHull], -1, color, 1)
                people.append(((shape[34][0], shape[34][1]), mar > MOUTH_AR_THRESH))
                gx = x + w
                face.append(gx)
        else:
            return face
        if len(handstatus) != 0:
            lijst_hand_gezicht = koppelen(handstatus,face)
            print(lijst_hand_gezicht)

        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord('q'):
            break

main()
