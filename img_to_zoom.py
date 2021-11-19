import pyvirtualcam
import numpy as np
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import argparse
import imutils
import time
import dlib
import cv2
HEIGHT = 480
WIDTH = int(16/9 * HEIGHT)

face = 0
# creating a variable with the classifiers
CLASSIFIERS = "haarcascade_frontalface_default.xml"

# Create cascade
FaceCascade = cv2.CascadeClassifier(CLASSIFIERS)
# Capture from camera, 0 because webcam
vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
vs.set(cv2.CAP_PROP_FRAME_WIDTH,  WIDTH)
vs.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
xmin, xmax, ymin, ymax = 0, WIDTH, 0, HEIGHT

def zoomboundaries(img,faces, face = 0):
    X = faces[face][0]
    Y = faces[face][1]
    W = faces[face][2]
    H = faces[face][3]

    Ry = img.shape[0]
    Rx = img.shape[1]
    V = Rx / Ry

    xfc = X + W / 2
    yfc = Y + H / 2

    ymin = max(min(int(yfc - H), int(Ry - 2 * H)), 0)
    ymax = max(min(int(yfc + H), Ry), int(2 * H))
    xmin = max(min(int(xfc - V * H), int(Rx - V * 2 * H)), 0)
    xmax = max(min(int(xfc + V * H), Rx), int(V * 2 * H))
    print(xmin,xmax,ymin,ymax)
    return xmin,xmax,ymin,ymax

def crop(img,xmin,xmax,ymin,ymax):
    imgcropped = img[ymin:ymax, xmin:xmax]
    return imgcropped

def resizer(img, Width, Height):
    imgresized = cv2.resize(img,(Width,Height))
    return imgresized

def main():
    with pyvirtualcam.Camera(width=853, height=480, fps=20) as cam:
        print(f'Using virtual camera: {cam.device}')
        while True:
            #start
            status, img = vs.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect the faces
            faces = FaceCascade.detectMultiScale(gray, scaleFactor=1.22, minNeighbors=8, minSize=(60, 60))
            #for (x, y, w, h) in faces:
            #    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if faces != () and len(faces) >= face + 1:
                (xmin, xmax, ymin, ymax) = zoomboundaries(img, faces, face)

            imgcropped = crop(img, xmin, xmax, ymin, ymax)
            imgresized = resizer(imgcropped, WIDTH, HEIGHT)

            cv2.imshow("zoomed", imgresized)
            cv2.imshow("origineel", img)
            toets = cv2.waitKey(10)
            if toets == 32:
                xmin = 0
                xmax = WIDTH
                ymin = 0
                ymax = HEIGHT

            if toets == 27:
                break
            #end
            imgresized = cv2.cvtColor(imgresized, cv2.COLOR_BGR2RGB)
            imgresized = cv2.flip(imgresized, 1)
            cam.send(imgresized)
            cam.sleep_until_next_frame()
    cv2.destroyAllWindows()
    vs.stop()
