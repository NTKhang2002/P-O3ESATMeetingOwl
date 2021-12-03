import time
import serial
import status_hand as sh
import cv2
from cvzone.HandTrackingModule import HandDetector
import dlib
import argparse
# import pyvirtualcam
import lip_detector
import servo_controller

class people:
    id = 0
    def __init__(self,fx,fy,t,hx,hy,hs,name):
        """
        fx, fy: face position
        t: talking status
        hx, hy: hand position
        hs: hand status
        """
        people.id += 1
        self.id = people.id
        # self.fx = [fx]
        self.fx = fx
        self.fy = fy
        self.t = t
        self.hx = hx
        self.hy = hy
        self.hs = hs
        self.active = False
        self.name = name
    def add_handdata(self,hx,hy,hs):
        self.hx = hx
        self.hy = hy
        self.hs = hs
    def add_facedata(self,fx,fy,t,name):
        # if len(self.fx) < 10:
        #     self.fx.append(fx)
        # else:
        #     self.fx.pop(0)
        #     self.fx.append(fx)
        self.fx = fx
        self.fy = fy
        self.t = t
        self.name = name
    def show_fx(self):
        # return sum(self.fx)/len(self.fx)
        return self.fx
    def show_hx(self):
        return self.hx
    def show_data(self):
        return self.id, self.fx, self.fy, self.t ,self.hx, self.hy, self.hs, self.name
    def is_talking(self):
        return self.t
    def hand_status(self):
        return self.hs
    def reset_hands(self):
        self.hx = None
        self.hy = None
        self.hs = None
    def show_name(self):
        return self.name


def set_video(camera,Width,Height):
    HEIGHT = Height
    WIDTH = Width
    cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    return cap


def min_hand(person,persons):
    hx = person[1]
    min_distance = None
    min_person = None
    for old_person in persons:
        old_fx = old_person.show_fx()
        if min_distance == None:
            min_distance = abs(hx - old_fx)
            min_person = old_person
        else:
            if abs(hx - old_fx) < min_distance:
                min_distance = abs(hx - old_fx)
                min_person = old_person
    min_person.add_handdata(person[1], person[2], person[0])

def min_face(person,persons):
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
    min_person.add_facedata(person[0], person[1], person[2], person[3])

# def choose_person(persons,person_tracked,hand_queue,hand1,hand2,handtime1,handtime2):
def choose_person(persons):
    """
    Returns x value (face) of person that is talking
    """
    for person in persons:
        if person.is_talking():
            return person.show_fx()
    # for person in persons:
    #     if person.hand_status() == 1:
    #         if person not in hand_queue:
    #             hand_queue.append(person)
    #             print("hand added")
    #             if hand1 == False:
    #                 handtime1 = time.time()
    #                 hand1 = True
    #             elif hand2 == False:
    #                 handtime2 = time.time()
    #                 hand2 = True
    #             if hand1 == hand2 == True:
    #                 if handtime2 - handtime1 < 2:
    #                     hand_queue.clear()
    #                     hand1 = False
    #                     hand2 = False
    #                     return "Error", person_tracked, hand_queue,hand1,hand2,handtime1,handtime2
    #
    # if person_tracked:
    #     person_tracked = False
    #     for person in persons:
    #         if person.is_talking():
    #             person_tracked = True
    #             person.active = True
    #             if person in hand_queue:
    #                 hand_queue.remove(person)
    #             return person.show_fx(), person_tracked, hand_queue,hand1,hand2,handtime1,handtime2
    #     if not person_tracked:
    #         if len(hand_queue) != 0:
    #             next_person = hand_queue[0]
    #             hand_queue.pop(0)
    #             person_tracked = True
    #             return next_person.show_fx(), person_tracked, hand_queue,hand1,hand2,handtime1,handtime2
    # else:
    #     for person in persons:
    #         if person.is_talking():
    #             person_tracked = True
    #             if person in hand_queue:
    #                 hand_queue.remove(person)
    #             return person.show_fx(), person_tracked, hand_queue,hand1,hand2,handtime1,handtime2
    #     if len(hand_queue) != 0:
    #             next_person = hand_queue[0]
    #             hand_queue.pop(0)
    #             person_tracked = True
    #             return next_person.show_fx(), person_tracked, hand_queue,hand1,hand2,handtime1,handtime2
    # person_tracked = False
    # return None, person_tracked, hand_queue,hand1,hand2,handtime1,handtime2



def pipeline(camera = 0,detectionCon = 0.8, maxHands = 4):
    Height = 720
    Width = int(16/9*Height)
    """
    Main pipeline: calls and implements all modules
    """
    print("Initializing...")
    """
    Initialization phase: 
        - Initializing video capture, hand detector, argument parser, face detector and shape predictor
        - Creating initial 'person' objects
    """
    # Starting video
    cap = set_video(camera,Width,Height)

    # Initializing mudles
    detector = HandDetector(detectionCon=detectionCon, maxHands=maxHands)
    detector_face = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Some variables
    person_tracked = False
    hand1 = False
    hand2 = False
    handtime1 = time.time()
    handtime2 = time.time()
    persons = list()
    hand_queue = list()

    # Startup Arduino
    x_oud = 5000
    nodeMcu = serial.Serial("COM5", 9600)  # Sartup
    straal_cm = 150
    max_aantal_pixels = Width
    helft_pixels = max_aantal_pixels / 2
    straal = (max_aantal_pixels/185)*straal_cm

    for k in range(20): # Initialization during first 20 frames
        success, img = cap.read()
        lip_detector.lipdetector(img,detector_face,predictor)
        facestatus = lip_detector.face_status()
    for person in facestatus:
        persons.append(people(person[0],person[1],person[2],None,None,None,person[3]))
    for p in range(len(persons)):
        print(persons[p].show_data())
    print("Initialization complete")
    # with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:

    while True:
        """
        Main loop: 
            - Creating and showing image
            - Updating 'person' objects with relevant data using the correct modules
            - Creating instruction for Arduino
        """
        success, img = cap.read() # initial image (clean)
        hands, img = detector.findHands(img)    # returns 'hands' and 'img', image contains visual feedback on hands
        handstatus = sh.hand_status(detector, hands)
        for person in persons:
            person.reset_hands()
        for person in handstatus:
            min_hand(person,persons)
        img = lip_detector.lipdetector(frame = img,detector = detector_face,predictor = predictor)
        facestatus = lip_detector.face_status()
        for person in facestatus:
            min_face(person,persons)

        # instruction,person_tracked,hand_queue,hand1,hand2,handtime1,handtime2 = choose_person(persons,person_tracked,hand_queue,hand1,hand2,handtime1,handtime2)
        instruction = choose_person(persons)
        if hand_queue != None:
            print(len(hand_queue))
            for person in hand_queue:   # hand queue tonen op het scherm (naam van persoon via person.name)
                print(person.show_name())
                cv2.putText(img, person.name + " (" + str(person.hx) + ", " + str(person.hy) + ")",
                          (person.hx, person.hy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)  # TEKST BOVEN HAND

        print(instruction)
        if instruction == "Error":
            print("ERROR: Make a decision!")
        if instruction != None and instruction != "Error":
            x_oud = servo_controller.move(instruction,x_oud,nodeMcu,straal,helft_pixels)
        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord('q'):
            break
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = cv2.flip(img, 1)
        # cam.send(img)
        # cam.sleep_until_next_frame()
