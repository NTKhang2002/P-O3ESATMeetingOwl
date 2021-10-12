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

import time

status_mond = False     #last state of the mouth, open or closed -MN
talking = False     #Talking state -MN
open_teller = 0     #counts how many times the mouth has opened during the video, unimportant -MN

teller_timing = 0   #Counter for 'timing_open' -MN
timing_open = [0, 0, 0, 0, 0]   #List to log the 4 last times the mouth has opened -MN

timing_toe_begin = 0    #Timelog when mouth went from open to closed -MN
timing_toe_eind = 0     #Time when mouth is shut -MN




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


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
                help="path to facial landmark predictor")
ap.add_argument("-w", "--webcam", type=int, default=0,
                help="index of webcam on system")
args = vars(ap.parse_args())

# define one constants, for mouth aspect ratio to indicate open mouth
MOUTH_AR_THRESH = 0.70

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the mouth
(mStart, mEnd) = (49, 68)

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()

time.sleep(1.0)

frame_width = 640
frame_height = 360

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))
time.sleep(1.0)

# loop over frames from the video stream
while True:
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    frame = vs.read()
    frame = imutils.resize(frame, width=640)
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

        cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)



        # Draw text if mouth is open + visualize the mouth in blue
        if mar > MOUTH_AR_THRESH:

            if status_mond == False:
                status_mond = True

                if teller_timing == 4:

                    teller_timing = 0
                teller_timing += 1
                timing_open[teller_timing] = time.time()

                open_teller += 1




            cv2.putText(frame, "MOUTH OPEN", (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.putText(frame, "teller: " + str(open_teller), (30, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.putText(frame, "timing: " + str(timing_open[teller_timing]), (30, 180),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.putText(frame, "Talking: " + str(talking), (30, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            color = BLUE


        else:

            timing_toe_eind = time.time()

            if status_mond == True:
                status_mond = False
                timing_toe_begin = time.time()

            cv2.putText(frame, "MOUTH CLOSED ", (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.putText(frame,"Toe_1: " + str(timing_toe_begin),
                        (30, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.putText(frame," Toe_2: " + str(timing_toe_eind),
                        (30, 180),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.putText(frame, "Talking: " + str(talking), (30, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            color = GREEN

        toe_periode = timing_toe_eind - timing_toe_begin


        if (timing_open[teller_timing] - timing_open[teller_timing - 4]) < 2 : #Mouth has to open 4 times in less than 2 seconds to get 'talking' state -MN
            talking = True

        if toe_periode > 2:     #if mouth has been closed for longer than 2 seconds, 'talking' state will go to False -MN
            talking = False


        # Visualize the mouth in green
        cv2.drawContours(frame, [mouthHull], -1, color, 1)
    # Write the frame into the file 'output.avi'
    out.write(frame)
    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()