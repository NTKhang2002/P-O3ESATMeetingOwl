from threading import Thread
from time import sleep
import status_hand as sh
import cv2
from cvzone.HandTrackingModule import HandDetector

# use Thread to run def in background
# Example:

def main(detectionCon = 0.8, maxHands = 4):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1000)
    cap.set(4, 100)
    detector = HandDetector(detectionCon=detectionCon, maxHands=maxHands)
    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        handstatus = sh.hand_status(detector, hands)
        img = afstand(img,detector, hands)
        for i in handstatus:
            print(i)
        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord('q'):
            break
def afstand(img,detector,hands):
    if hands:
        for id in range(len(hands)):
            hand = hands[id]
            lmList = hand["lmList"]
            length, info, img = detector.findDistance(lmList[8], lmList[12], img)
            return img
    else:
        return img
if __name__ == '__main__':
    main()