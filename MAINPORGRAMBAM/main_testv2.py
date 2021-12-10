import time
import serial
import cv2
from cvzone.HandTrackingModule import HandDetector
import dlib
import argparse
# import pyvirtualcam
import lip_detectorv2 as lip_detector
import servo_controller
import koppelen

proto = False #Testfase



class people:
    id = 0
    def __init__(self):
        """
        fx, fy: face position
        t: talking status
        hx: hand position
        """
        people.id += 1
        self.__id = people.id
        self.__present = False
        self.__fx = -1000
        self.__fy = -1000
        self.__talking = False
        self.__mouth_open = False
        self.__mouth_open_time_list = [10,0,0]   # list containing the point of time of mouth openings
        self.__mouth_open_time_index = 0         # current index in the list above
        self.__mouth_closed_time1 = 0
        self.__mouth_closed_time2 = 0
        self.__hx = None
        self.__time = time.time()
        self.__tracked = False  # person is tracked by camera
        if self.__id == 1:
            self.__name = "Ben"
        elif self.__id == 2:
            self.__name = "Barry"
        elif self.__id == 3:
            self.__name = "Hugh"
        elif self.__id == 4:
            self.__name = "Rae"
    def set_hx(self,hx):
        self.__hx = hx
    def set_facedata(self,fx,fy):
        self.__fx = fx
        self.__fy = fy

    def get_fx(self):
        return self.__fx
    def get_fy(self):
        return self.__fy
    def get_hx(self):
        return self.__hx
    def get_data(self):
        return self.__id, self.__fx, self.__fy, self.__talking ,self.__hx, self.__name
    def get_mouth_open(self):
        return self.__mouth_open
    def set_mouth_open(self,mouth_open):
        self.__mouth_open = mouth_open
    def get_mouth_open_time_list(self):
        return self.__mouth_open_time_list
    def get_mouth_open_time_diff(self):
        return self.__mouth_open_time_list[self.__mouth_open_time_index] - self.__mouth_open_time_list[self.__mouth_open_time_index - 2]
    def set_mouth_open_time_list(self):
        self.__mouth_open_time_list[self.__mouth_open_time_index] = time.time()
    def get_mouth_open_time_index(self):
        return self.__mouth_open_time_index
    def reset_mouth_open_time_index(self):
        self.__mouth_open_time_index = 0
    def update_mouth_open_time_index(self):
        self.__mouth_open_time_index += 1
    def get_mouth_closed_time1(self):
        return self.__mouth_closed_time1
    def set_mouth_closed_time1(self):
        self.__mouth_closed_time1 = time.time()
    def get_mouth_closed_time2(self):
        return self.__mouth_closed_time2
    def set_mouth_closed_time2(self):
        self.__mouth_closed_time2 = time.time()
    def get_talking(self):
        return self.__talking
    def set_talking(self,talking):
        self.__talking = talking
    def reset_hands(self):
        self.__hx = None
    def get_name(self):
        return self.__name
    def get_present(self):
        return self.__present
    def set_present(self,present):
        self.__present = present
        self.__time = time.time()
    def get_time(self):
        return self.__time
    def get_tracked(self):
        return self.__tracked
    def set_tracked(self,tracked):
        self.__tracked = tracked
    def reset(self):
        self.__present = False
        self.__fx = -1000
        self.__fy = -1000
        self.__talking = False
        self.__mouth_open = False
        self.__mouth_open_time_list = [10, 0, 0] #First item in list has to be above 10 for startup
        self.__mouth_open_time_index = 0
        self.__mouth_closed_time1 = 0
        self.__mouth_closed_time2 = 0
        self.__hx = None
        self.__time = time.time()

def set_video(camera,WIDTH,HEIGHT):
    cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_BUFFERSIZE,2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    return cap

def update_face(fx,fy,mouth_open,persons,marge_x = 150):
    for old_person in persons:
        old_fx = old_person.get_fx()
        if abs(fx - old_fx) < marge_x:
            old_person.set_facedata(fx,fy)
            old_person.set_present(True)
            determine_talking(old_person,mouth_open)
            return
    for old_person in persons:
        if not old_person.get_present():
            old_person.set_facedata(fx,fy)
            old_person.set_present(True)
            determine_talking(old_person,mouth_open)
            return

def determine_talking(person,mouth_open):

    if mouth_open:  # mouth is currently open

        if person.get_mouth_open() == False: # mouth was previously closed
            print(person.get_mouth_open())
            person.set_mouth_open(mouth_open)
            if person.get_mouth_open_time_index() == 2:
                person.reset_mouth_open_time_index()

            person.update_mouth_open_time_index()
            person.set_mouth_open_time_list()
    else:           # mouth is currently closed
        person.set_mouth_closed_time2()

        if person.get_mouth_open():     # mouth was previously open
            person.set_mouth_open(mouth_open)
            person.set_mouth_closed_time1()
    if person.get_mouth_closed_time2() -  person.get_mouth_closed_time1() > 2:  # mouth closed for longer than 2 seconds
        person.set_talking(False)
    elif person.get_mouth_open_time_diff() < 6: # mouth opened 3 different times in 4 seconds
        person.set_talking(True)


def update_hand(fx,hx,persons,marge_x = 150):
    for old_person in persons:
        old_fx = old_person.get_fx()
        if abs(fx - old_fx) < marge_x:
            old_person.set_hx(hx)
            return

def check_presence(person,img):
    if person.get_present():
        if person.get_talking():
            cv2.putText(img, person.get_name() + " ("+ str(person.get_fx()) +", " + str(person.get_fy()) + ")" + "Talking", (person.get_fx(), person.get_fy()), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)  # TEKST BOVEN HOOFD
        else:
            cv2.putText(img, person.get_name() + " ("+ str(person.get_fx()) +", " + str(person.get_fy()) + ")", (person.get_fx(), person.get_fy()), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)  # TEKST BOVEN HOOFD

        if(time.time() - person.get_time()) > 3:
            person.reset()

def choose_person(persons,person_tracked,queue,queuetime1,queuetime2):
    """
    Returns x value (face) of person that is talking
    """
    if person_tracked:  # There was previously a person tracked
        person_tracked = False
        for person in persons:
            if person.get_tracked(): # This is the person that was previously tracked
                if person.get_talking(): # Check if that person is still talking
                    person_tracked = True
                    return "Same person talking",person_tracked,queue,queuetime1,queuetime2,person
                else:
                    person.set_tracked(False)
    if not person_tracked:
        for person in persons:
            if person.get_hx() != None and person.get_talking():    # if person is talking and has raised his hand
                if len(queue) ==  0:
                    queue.append(person)
                    queuetime1 = time.time()
                else:
                    if not person in queue:
                        queuetime2 = time.time()
                        if queuetime2 - queuetime1 < 1:  # if two persons want to talk at the same time, an error message will be shown
                            queue.clear()
                            queuetime1 = None
                            queuetime2 = None
                            return "Error",person_tracked,queue,queuetime1,queuetime2,None
        if len(queue) != 0:
            if time.time() - queuetime1 < 1: # when a second has passed, the person that wanted to talk will be tracked
                to_be_tracked = queue[0]
                queue.clear()
                queuetime1 = None
                queuetime2 = None
                to_be_tracked.set_tracked(True)
                person_tracked = True
                return to_be_tracked.get_fx(),person_tracked,queue,queuetime1,queuetime2,to_be_tracked

    return None, person_tracked, queue,queuetime1,queuetime2,None



def pipeline(camera = 0,detectionCon = 0.8, maxHands = 4,HEIGHT = 602,max_persons = 4):
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
    WIDTH = int(16/9*HEIGHT)
    cap = set_video(camera,WIDTH,HEIGHT)

    # Initializing modules
    detector = HandDetector(detectionCon=detectionCon, maxHands=maxHands)
    detector_face = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(width, height)

    # Some variables
    fps = 0
    frame_counter = 0
    person_tracked = False
    fps_time = time.time()
    queue = []
    queuetime1 = None
    queuetime2 = None
    hand_timer = time.time()
    persons = list()
    for i in range(max_persons):
        persons.append(people())

    # Startup Arduino
    x_oud = 5000

    nodeMcu = serial.Serial("COM10", 9600)  # Sartup
    straal_cm = 150



    helft_pixels = width / 2


    success, img = cap.read()

    img, facestatus = lip_detector.lipdetector(img, detector_face, predictor)
    for person in facestatus:
        fx = person[0]
        fy = person[1]
        mouth_open = person[2]
        update_face(fx, fy, mouth_open, persons)
    for p in range(len(persons)):
        print(persons[p].get_data())
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
        if time.time() - hand_timer >= 2: # hands reset every 2 seconds
            for person in persons:
                person.reset_hands()
            hand_timer = time.time()
        img,facestatus = lip_detector.lipdetector(frame = img, detector = detector_face, predictor = predictor)
        for person in facestatus:
            fx = person[0]
            fy = person[1]
            mouth_open = person[2]
            update_face(fx, fy, mouth_open, persons)
        hand_face = koppelen.main(img, detector)
        if hand_face != None:
            for person in hand_face:
                fx = person[1]
                hx = person[0]
                update_hand(fx, hx, persons)
        instruction,person_tracked,queue,queuetime1,queuetime2,tracked_person = choose_person(persons,person_tracked,queue,queuetime1,queuetime2)
        cv2.putText(img, "Tracked:", (500, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(img, "FPS:"+ str(fps) , (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        if tracked_person != None:
            cv2.putText(img, tracked_person.get_name(), (500, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        else:
            cv2.putText(img, "No one", (500, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        if instruction == "Error":
            print("ERROR: Make a decision!")
        if instruction != None and instruction != "Error":
            x_oud = servo_controller.move(instruction,x_oud,nodeMcu,width,straal_cm,helft_pixels)
        for person in persons:
            check_presence(person,img)

        frame_counter += 1
        if frame_counter == 5:
            fps = round(frame_counter/(time.time()-fps_time), 2)
            fps_time = time.time()
            frame_counter = 0


        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord('q'):
            break
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = cv2.flip(img, 1)
        # cam.send(img)
        # cam.sleep_until_next_frame()
    cap.release()
    cv2.destroyAllWindows()
pipeline(camera=0)