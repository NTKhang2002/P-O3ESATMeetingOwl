from time import sleep
import status_hand as sh
import cv2
from cvzone.HandTrackingModule import HandDetector
import face_test
import detect_open_mouth_test
import dlib
import argparse


class people:
    def __init__(self,fx,fy,t,hx,hy,hs):
        """
        fx, fy: face position
        t: talking status
        hx, hy: hand position
        hs: hand status
        """
        self.fx = fx
        self.fy = fy
        self.t = t
        self.hx = hx
        self.hy = hy
        self.hs = hs
    def add_data(self,fx,fy,t,hx,hy,hs):
        self.fx = fx
        self.fy = fy
        self.t = t
        self.hx = hx
        self.hy = hy
        self.hs = hs
    def x_position_face(self):
        return self.fx

def argsfunc():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
                    help="path to facial landmark predictor")
    ap.add_argument("-w", "--webcam", type=int, default=0,
                    help="index of webcam on system")
    args = vars(ap.parse_args())
    return args

def main(detectionCon = 0.8, maxHands = 4):
    print("Initializing")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1000)
    cap.set(4, 100)
    detector = HandDetector(detectionCon=detectionCon, maxHands=maxHands)
    args = argsfunc()
    detector_face = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])
    for k in range(100)
    success, img = cap.read()
    hands, img = detector.findHands(img)
    handstatus = sh.hand_status(detector, hands)
    for i in handstatus:
        print(i)
    sleep(100)
    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        handstatus = sh.hand_status(detector, hands)
        img = detect_open_mouth_test.main(img,detector_face,predictor)
        for i in handstatus:
            print(i)
        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    main()