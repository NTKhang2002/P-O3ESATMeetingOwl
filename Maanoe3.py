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

webcam = 0

participant_counter = 0

marge_x = 50

tijd_algemeen = time.time()


BLUE = (255, 0, 0)
GREEN = (0, 255, 0)

mond_algemeen = False




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


participant_1 = player(-1000,-1000)
participant_1.name = "participant 1"
participant_2 = player(-1000,-1000)
participant_2.name = "participant 2"
participant_3 = player(-1000,-1000)
participant_3.name = "participant 3"
participant_4 = player(-1000,-1000)
participant_4.name = "participant 4"

participant_list = [participant_1, participant_2, participant_3, participant_4]


def update(participant, x, y):
    participant.fx = x
    participant.fy = y
    participant.tijd = time.time()
    print(participant.name + ": " + str(x),str(y))
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
        print(participant.name, ": TALKING")


def localiser(participant, x):
    if (participant.fx - marge_x) <= x <= (participant.fx + marge_x):
        return True
    else:
        return False


def check(participant):
    if participant.present:

        if(tijd_algemeen - participant.tijd) > 5:
            participant.present = False
            participant.fx = -1000
            participant.fy = -1000


def assign(x, y):
    if not participant_1.present:
        update(participant_1, x, y)

    elif localiser(participant_1, x):
        update(participant_1, x, y)

    elif not participant_2.present:
        update(participant_2, x, y)

    elif localiser(participant_2, x):
        update(participant_2, x, y)

    elif not participant_3.present:
        update(participant_3, x, y)

    elif localiser(participant_3, x):
        update(participant_3, x, y)

    elif not participant_4.present:
        update(participant_4, x, y)

    elif localiser(participant_4, x):
        update(participant_4, x, y)


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
ap.add_argument("-w", "--webcam", type=int, default=webcam,
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
    #frame = imutils.resize(frame, width=640)
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

        assign(x, y)



        cv2.drawContours(frame, [mouthHull], -1, color, 1)
    # Write the frame into the file 'output.avi'
    out.write(frame)
    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    tijd_algemeen = time.time()

    for k in participant_list:
        check(k)




    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()