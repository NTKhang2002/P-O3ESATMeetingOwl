import time
import status_hand as sh
import cv2
from cvzone.HandTrackingModule import HandDetector
import dlib
import argparse
import pyvirtualcam
import lip_detector
import servo_controller

hand1 = False
hand2 = False

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
        self.active = False
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
    def hand_status(self):
        return self.hs
    def reset_hands(self):
        self.hx = None
        self.hy = None
        self.hs = None
def argsfunc():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
                    help="path to facial landmark predictor")
    ap.add_argument("-w", "--webcam", type=int, default=0,
                    help="index of webcam on system")
    args = vars(ap.parse_args())
    return args

def choose_person(persons,person_tracked,hand_queue):
    """
    Returns x value (face) of person that is talking
    """
    amount_talking = 0
    for person in persons:
        if person.hand_status() == 1:
            if person not in hand_queue:
                hand_queue.append(person)
                if not person_tracked:
                    if hand1 == False:
                        handtime1 = time.time()
                        hand1 = True
                    elif hand2 == False:
                        handtime2 = time.time()
                        hand2 = True
                    if hand1 == hand2 == True:
                        if handtime2 - handtime1 < 2:
                            hand_queue.clear()
                            hand1 = False
                            hand2 = False
                            return "Error", person_tracked, hand_queue

    if person_tracked:
        person_tracked = False
        for person in persons:
            if person.is_talking():
                person_tracked = True
                person.active = True
                if person in hand_queue:
                    hand_queue.remove(person)
                return person.show_fx(), person_tracked, hand_queue
        if not person_tracked:
            if len(hand_queue) != 0:
                next_person = hand_queue[0]
                hand_queue.pop(0)
                person_tracked = True
                return next_person.show_fx(), person_tracked, hand_queue
    else:
        for person in persons:
            if person.is_talking():
                person_tracked = True
                if person in hand_queue:
                    hand_queue.remove(person)
                return person.show_fx(), person_tracked, hand_queue
        if len(hand_queue) != 0:
                next_person = hand_queue[0]
                hand_queue.pop(0)
                person_tracked = True
                return next_person.show_fx(), person_tracked, hand_queue
    person_tracked = False
    return None, person_tracked, hand_queue

def img_to_zoom(img):
    pass


def main(detectionCon = 0.8, maxHands = 4):
    """
    Main pipeline: calls and implements all modules
    """
    print("Initializing...")
    """
    Initialization phase: 
        - Initializing video capture, hand detector, argument parser, face detector and shape predictor
        - Creating initial 'person' objects
    """
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1000)
    cap.set(4, 100)
    detector = HandDetector(detectionCon=detectionCon, maxHands=maxHands)
    args = argsfunc()
    detector_face = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])
    person_tracked = False
    persons = list()
    hand_queue = list()
    for k in range(25): # Initialization during first 25 frames
        success, img = cap.read()
        img = imutils.resize(img, width=640)
        lip_detector.lipdetector(img,detector_face,predictor)
        facestatus = lip_detector.face_status()
    for person in facestatus:
        persons.append(people(person[0],person[1],person[2],None,None,None))
    for p in range(len(persons)):
        print(persons[p].show_data())
    print("Initialization complete")
    with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:
        while True:
            """
            Main loop: 
                - Creating and showing image
                - Updating 'person' objects with relevant data using the correct modules
                - Creating instruction for Arduino
            """
            success, img = cap.read() # initial image (clean)
            img = imutils.resize(img, width=640)
            hands, img = detector.findHands(img)    # returns 'hands' and 'img', image contains visual feedback on hands
            handstatus = sh.hand_status(detector, hands)
            for person in persons:
                person.reset_hands()
            for person in handstatus:
                hx = person[1]
                min_distance = None
                min_person = None
                for old_person in persons:
                    old_fx = old_person.show_fx()
                    if min_distance == None:
                        min_distance = abs(hx - old_fx)
                        min_person = old_person
                    else:
                        if abs(hx-old_fx) < min_distance:
                            min_distance = abs(hx-old_fx)
                            min_person = old_person
                min_person.add_handdata(person[1], person[2],person[0])
                    # if abs(hx - old_fx) < 100:  # New x value compared with old x value, if within predefined range -> data is updated (1)
                    #     old_person.add_handdata(person[1], person[2],person[0])
            # input: image with hand visualization, output: image with hand visualization and lip visualization (2)
            img = lip_detector.lipdetector(frame = img,detector = detector_face,predictor = predictor)
            facestatus = lip_detector.face_status()
            for person in facestatus:
                fx = person[0]
                min_distance = None
                min_person = None
                for old_person in persons:
                    old_fx = old_person.show_fx()
                    if min_distance == None:
                        min_distance = abs(fx - old_fx)
                        min_person = old_person
                    else:
                        if abs(fx - old_fx) < min_distance:
                            min_distance = abs(fx - old_fx)
                            min_person = old_person
                min_person.add_facedata(person[0], person[1], person[2])
                # for old_person in persons:
                #     old_fx = old_person.show_fx()
                #     if abs(fx - old_fx) < 100:  # (1)
                #         old_person.add_facedata(person[0],person[1],person[2])
            instruction,person_tracked,hand_queue = choose_person(persons,person_tracked,hand_queue)
            print(instruction)
            if instruction == None:
                print("ERROR: Make a decision!")
            servo_controller.move(instruction)
            cv2.imshow("image", img)
            if cv2.waitKey(1) == ord('q'):
                break
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.flip(img, 1)
            cam.send(img)
            cam.sleep_until_next_frame()
if __name__ == '__main__':
    main()


