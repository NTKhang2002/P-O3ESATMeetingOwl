import cv2
import time

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
