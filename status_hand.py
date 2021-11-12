<<<<<<< HEAD
import cv2 #(1)
from cvzone.HandTrackingModule import HandDetector
cap = cv2.VideoCapture(0)#(1)
detector = HandDetector(detectionCon=0.8,maxHands=4)

def want_to_talk(hands):
    if hands:
        nobody = True
        for hand in hands:
            # print('hand 1')
            fingers = detector.fingersUp(hand)
            if fingers == [1, 1, 1, 1]:
                print('want tot talk')
                nobody = False
        if nobody:
            print('nobody wants tot talk')
    if not hands:
        print('nobody wants tot talk')

while True: #(1)
    success, img = cap.read()#(1)
    hands, img = detector.findHands(img)
    want_to_talk(hands)
    cv2.imshow("image", img) #(1)
    cv2.waitKey(1) #(1)



=======
import cv2
import time
from cvzone.HandTrackingModule import HandDetector

def hand_status(detector, hands):
    if hands:
        for id in range(len(hands)):
            hand = hands[id]
            cx, cy = hand["center"]  # centerpoint: cx cy
            fingers = detector.fingersUp(hand)
            if fingers == [0,0,0,0,0]:
                """ HAND STATUS: -1 Closed
                                  0 Open
                                  1 Talk gesture """
                hand_status = -1
            elif fingers == [1,1,1,1,1] or fingers == [0,1,1,1,1]:
                hand_status = 1
            else:
                hand_status = 0

            result = (hand_status, cx, cy)
            yield result

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
        for i in handstatus:
            print(i)
        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    main()
>>>>>>> aae51356021ccfdcf93605fe919ae7ad6c5f0cb9
