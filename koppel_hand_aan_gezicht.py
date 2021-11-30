from detect_open_mouth_V2 import openmond
import cv2
import time
from status_hand import hand_status
from cvzone.HandTrackingModule import HandDetector

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

main()



