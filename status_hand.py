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



