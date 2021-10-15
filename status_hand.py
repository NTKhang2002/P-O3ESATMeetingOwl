import cv2
import time

from cvzone.HandTrackingModule import HandDetector
cap = cv2.VideoCapture(0)
cap.set(3,1000)
cap.set(4,100)

detector = HandDetector(detectionCon=0.8,maxHands=4)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand1 = hands[0]
        print('hand 1')
        fingers1 = detector.fingersUp(hand1)
        if fingers1 == [0,0,0,0,0]:
            print('gesloten')
        elif fingers1 == [1,1,1,1,1] or fingers1 == [0,1,1,1,1]:
            print('ik wil praten')
        if len(hands) > 1:
            hand2 = hands[1]
            print('tweede hand')




    cv2.imshow("image", img)
    cv2.waitKey(1)