"""
to do:
opgestoken hand(en) aan een gezicht koppelen

"""

import cv2
from hand_status import hand_status
from cvzone.HandTrackingModule import HandDetector

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def koppelen(xhanden, xgezichten):
    gekoppeld = []
    for i in range(len(xhanden)):
        min_afstand = 10000000000000000
        index = 0
        for xgezicht in xgezichten:
            afstand = abs(xhanden[i] - xgezicht)
            if afstand <= min_afstand:
                min_afstand = afstand
                juiste_gezicht = index
                index += 1
            else:
                index += 1
        ok = (xhanden[i], xgezichten[juiste_gezicht])
        gekoppeld.append(ok)
    return gekoppeld #geeft een lijst met tuples (index_xhanden, index_xgezichten)


def main(img,detector,detectionCon = 0.8, maxHands = 4):
    while True:
        hands, img = detector.findHands(img)
        handstatus = hand_status(detector, hands)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        xgezicht = []
        if len(faces) != 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                xgezicht.append(x + w)
        if len(handstatus) != 0 and len(xgezicht) != 0:
            lijst_hand_gezicht = koppelen(handstatus,xgezicht)
            return lijst_hand_gezicht
        else:
            return #print("ER ZIJN GEEN GEZICHTEN OF HANDEN")


