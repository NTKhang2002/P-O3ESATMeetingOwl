import cv2
import time
from cvzone.HandTrackingModule import HandDetector

def hand_status(detector, hands):
    h = []
    if hands: #als er (een) hand(en) (is) zijn
        for id in range(len(hands)):
            hand = hands[id]
            cx, cy = hand["center"]  # centerpoint: cx cy
            fingers = detector.fingersUp(hand)
            if fingers == [1,1,1,1,1] or fingers == [0,1,1,1,1]: #als alle vingers van een hand (uitgezonderd duim) zijn opgestoken
                h.append(cx)
    else: #als er geen hand is
        return h
    return h

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
        print(hands)
        handstatus = hand_status(detector, hands)
        for i in handstatus:
            print(i)
        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    main()