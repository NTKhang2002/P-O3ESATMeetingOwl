import cv2
import time
from cvzone.HandTrackingModule import HandDetector

def hand_status(detector, hands):
    if hands:
        for id in range(len(hands)):
            hand = hands[id]
            centerPoint = hand["center"]  # centerpoint: cx cy
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

            result = (id, hand_status, centerPoint)
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
