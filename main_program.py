from time import sleep
import status_hand as sh
import cv2
from cvzone.HandTrackingModule import HandDetector
import dlib
import argparse
import lip_detector

class people:
    id = 0
    def __init__(self,fx,fy,t,hx,hy,hs):
        """
        fx, fy: face position
        t: talking status
        hx, hy: hand position
        hs: hand status
        """
        people.id += 1
        self.id = people.id
        self.fx = fx
        self.fy = fy
        self.t = t
        self.hx = hx
        self.hy = hy
        self.hs = hs
    def add_handdata(self,hx,hy,hs):
        self.hx = hx
        self.hy = hy
        self.hs = hs
    def add_facedata(self,fx,fy,t):
        self.fx = fx
        self.fy = fy
        self.t = t
    def show_fx(self):
        return self.fx
    def show_hx(self):
        return self.hx
    def show_data(self):
        return self.id, self.fx, self.fy, self.t ,self.hx, self.hy, self.hs
    def is_talking(self):
        return self.t

def argsfunc():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
                    help="path to facial landmark predictor")
    ap.add_argument("-w", "--webcam", type=int, default=0,
                    help="index of webcam on system")
    args = vars(ap.parse_args())
    return args

def choose_person(persons):
    for person in persons:
        if person.is_talking():
            return person.show_fx()

def main(detectionCon = 0.8, maxHands = 4):
    print("Initializing...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1000)
    cap.set(4, 100)
    detector = HandDetector(detectionCon=detectionCon, maxHands=maxHands)
    args = argsfunc()
    detector_face = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])
    for k in range(25):
        success, img = cap.read()
        lip_detector.lipdetector(img,detector_face,predictor)
        facestatus = lip_detector.face_status()
    persons = list()
    for person in facestatus:
        persons.append(people(person[0],person[1],person[2],None,None,None))
    for p in range(len(persons)):
        print(persons[p].show_data())
    print("Initialization complete")
    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        handstatus = sh.hand_status(detector, hands)
        for person in handstatus:
            hx = person[1]
            for old_person in persons:
                old_fx = old_person.show_fx()
                if abs(hx - old_fx) < 100:
                    old_person.add_handdata(person[1], person[2],person[0])
        img = lip_detector.lipdetector(frame = img,detector = detector_face,predictor = predictor)
        facestatus = lip_detector.face_status()
        for person in facestatus:
            fx = person[0]
            for old_person in persons:
                old_fx = old_person.show_fx()
                if abs(fx - old_fx) < 100:
                    old_person.add_facedata(person[0],person[1],person[2])
        instruction = choose_person(persons)
        print(instruction)
        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord('q'):
            break
if __name__ == '__main__':
    main()


